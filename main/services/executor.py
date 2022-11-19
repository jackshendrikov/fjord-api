import asyncio

import pandas as pd

from main.const.common import ASYNC_TRANSLATION_TEXTS, READ_CSV_CHUNK_SIZE, Language
from main.const.translator import DEFAULT_PROVIDER, Provider, TextHashMap
from main.core.config import get_app_settings
from main.core.exceptions import PoolEmptyException
from main.core.logging import logger
from main.db.models.postgres import Translation
from main.db.repositories.proxies import ProxyPoolRepository
from main.schemas.tasks import TranslationRunPayload
from main.services.common.proxy import ProxyPoolService
from main.services.extra.errors import TranslationError, TranslationRequestError
from main.services.extra.proxynator.main import Proxynator
from main.services.extra.translator.main import Translator
from main.utils.common import chunks, get_text_hash

settings = get_app_settings()


class TranslationTaskExecutor:

    # Repositories
    _proxies_repository: ProxyPoolRepository = ProxyPoolRepository()

    # Services
    _proxy_service: ProxyPoolService = ProxyPoolService()

    # Extra Services
    _translator: Translator = Translator()
    _proxynator: Proxynator = Proxynator()

    async def execute(self, payload: TranslationRunPayload) -> None:
        for chunk in pd.read_csv(
            payload.link,
            usecols=payload.columns_to_translate,
            chunksize=READ_CSV_CHUNK_SIZE,
        ):
            for column in payload.columns_to_translate:
                try:
                    texts = await self._get_texts_to_translate(
                        texts=chunk[column].unique()
                    )
                    await self._process_translation_texts(texts=texts, payload=payload)
                except TranslationError as e:
                    if payload.provider != DEFAULT_PROVIDER:
                        payload.provider = DEFAULT_PROVIDER  # type: ignore
                        texts = await self._get_texts_to_translate(
                            texts=chunk[column].unique()
                        )
                        await self._process_translation_texts(
                            texts=texts, payload=payload
                        )
                    else:
                        raise e
                logger.info(f"Successfully translated {len(chunk)} texts..")

    async def _process_translation_texts(
        self, texts: list[TextHashMap], payload: TranslationRunPayload
    ) -> None:
        for texts_pack in chunks(texts, size=ASYNC_TRANSLATION_TEXTS):
            logger.info(f"Going to translate pack of {len(texts_pack)} texts..")
            await self._get_translation(
                provider=payload.provider,
                source=payload.source_language,
                target=payload.target_language,
                texts=texts_pack,
            )

    async def _get_translation(
        self,
        provider: Provider,
        source: Language,
        target: Language,
        texts: list[TextHashMap],
    ) -> None:
        # TODO: Think about keep session for stable proxy more than on 1 async batch

        try:
            proxy = await self._proxy_service.get_random_proxy()
        except PoolEmptyException:
            await self._proxynator.find_proxies()
            return await self._get_translation(
                provider=provider, source=source, target=target, texts=texts
            )

        try:
            translated_items = await self._translator.translate_multiple(
                provider=provider,
                source=source,
                target=target,
                texts=texts,
                proxy=proxy,
            )

            translations = [
                Translation(
                    original=item.original,
                    translated=item.translation,
                    provider=provider,
                    source=source,
                    target=target,
                    text_hash=item.hash,
                )
                for item in translated_items
            ]
            logger.info(f"Successfully translated {len(translations)} texts!")
            await Translation.insert(*translations)
        except TranslationRequestError:
            logger.info("Invalid proxy, going to replace it.")
            await self._proxies_repository.decrease_score(proxy=proxy)
            return await self._get_translation(
                provider=provider, source=source, target=target, texts=texts
            )

    async def _get_texts_to_translate(self, texts: set[str]) -> list[TextHashMap]:
        texts_to_translate = [
            TextHashMap(original=text, hash=get_text_hash(text=text)) for text in texts
        ]
        return await self._filter_texts(items=texts_to_translate)

    async def _filter_texts(self, items: list[TextHashMap]) -> list[TextHashMap]:
        tasks = [asyncio.create_task(self._is_item_exist(item=item)) for item in items]
        texts = await asyncio.gather(*tasks)
        return [text for text in texts if text is not None]

    @staticmethod
    async def _is_item_exist(item: TextHashMap) -> TextHashMap | None:
        if not await Translation.exists().where(Translation.text_hash == item.hash):
            return item
