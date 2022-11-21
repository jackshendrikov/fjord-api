import asyncio

from main.const.common import Language
from main.const.translator import Provider, TextHashMap, TranslationMap
from main.schemas.proxies import Proxy
from main.schemas.translation import DetectionIn, TranslationIn
from main.services.extra.translator.providers import (
    BaseTranslationProvider,
    DeeplProvider,
    GoogleTranslateProvider,
    LibreTranslateProvider,
    MyMemoryProvider,
)


class Translator:
    async def translate(self, item: TranslationIn) -> str:
        """Get the translation of input text"""

        provider = self._get_provider_class(provider=item.provider)
        translation = await provider.get_translation(
            text=item.text,
            source=item.source_language.value,
            target=item.target_language.value,
            autodetect=self._has_autodetect(provider=item.provider),
        )
        await provider.close()
        return translation

    async def detect_language(self, item: DetectionIn) -> str:
        """Get the language definition based on the input text"""

        provider = self._get_provider_class(provider=item.provider)
        detection = await provider.detect(text=item.text)
        await provider.close()
        return detection

    async def translate_multiple(
        self,
        provider: Provider,
        source: Language,
        target: Language,
        proxy: Proxy,
        texts: list[TextHashMap],
    ) -> list[TranslationMap]:
        """Get translation of multiple texts"""

        # TODO: Seems like session does not close, but why?

        trans_provider = self._get_provider_class(provider=provider)

        translations_tasks = [
            trans_provider.get_translation(
                text=text.original,
                source=source.value,
                target=target.value,
                autodetect=self._has_autodetect(provider=provider),
                proxy=proxy.http_string,
                text_hash=text.hash,
            )
            for text in texts
        ]

        translations = await asyncio.gather(*translations_tasks)
        await trans_provider.close()
        return translations

    @staticmethod
    def _has_autodetect(provider: Provider) -> bool:
        """Check if the provider has automatic language detection"""

        return isinstance(provider, (GoogleTranslateProvider, DeeplProvider))

    @staticmethod
    def _get_provider_class(provider: Provider) -> BaseTranslationProvider:
        """Return specific provider class."""

        provider_to_class_map: dict[str, type[BaseTranslationProvider]] = {
            Provider.GOOGLE_TRANSLATE: GoogleTranslateProvider,
            Provider.LIBRE_TRANSLATE: LibreTranslateProvider,
            Provider.DEEPL: DeeplProvider,
            Provider.MYMEMORY: MyMemoryProvider,
        }
        return provider_to_class_map[provider]()
