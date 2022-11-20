import asyncio
import json
from abc import ABCMeta, abstractmethod
from textwrap import wrap

import urllib3
from aiohttp import ClientSession, ClientTimeout

from main.const.common import DEFAULT_HEADERS, Language
from main.const.translator import DEFAULT_TIMEOUT, TranslationMap
from main.core.config import get_app_settings
from main.services.extra.errors import async_session_handler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings = get_app_settings()


class BaseTranslationProvider(metaclass=ABCMeta):
    base_url = ""
    chars_limit = 5000

    __session = ClientSession()

    timeout = DEFAULT_TIMEOUT
    headers = DEFAULT_HEADERS

    @property
    def _session(self) -> ClientSession:
        if self.__session.closed:
            self.__session = ClientSession()
        return self.__session

    @async_session_handler(session=__session)
    async def get_translation(
        self,
        text: str,
        source: str,
        target: str,
        autodetect: bool,
        proxy: str | None = None,
        text_hash: str | None = None,
    ) -> str | TranslationMap:
        """
        Get translation of a single text.

        :param text: The text to translate.
        :param source: The source language code (ISO 639).
        :param target: The target language code (ISO 639).
        :param autodetect: Indicates whether the provider has its own language detection
                           or whether a third-party service is needed.
        :param proxy: proxy for request.
        :param text_hash: if present, then we need to return translation with original text + hash.

        :return: Translated text.
        """

        text_list = wrap(text, self.chars_limit, replace_whitespace=False)

        if not autodetect and source == Language.AUTO:
            source = await self.detect(text_list[0], proxy=proxy)

        translations_tasks = [
            asyncio.create_task(
                self._translate(
                    text=wrapped_text, source=source, target=target, proxy=proxy
                )
            )
            for wrapped_text in text_list
        ]
        translations = await asyncio.gather(*translations_tasks)
        translated_text = " ".join(translations).strip()

        if text_hash:
            return TranslationMap(
                original=text, translation=translated_text, hash=text_hash
            )
        return translated_text

    async def detect(self, text: str, proxy: str | None = None) -> str:
        """
        Detect the language of a single text.

        :param text: Text to detect.
        :param proxy: Specific proxy for the request.

        :return: The detected language code.
        """
        url = "https://ws.detectlanguage.com/0.2/detect"
        params = {"q": text}

        headers = self.headers
        headers["Authorization"] = f"Bearer {settings.detect_language_api_key}"

        data: dict = await self._make_request(  # type: ignore
            url=url, params=params, headers=headers, proxy=proxy
        )

        return data["data"]["detections"][0]["language"]

    @abstractmethod
    async def _translate(
        self, text: str, source: str, target: str, proxy: str | None
    ) -> str:
        """A method for obtaining a text translation"""

        raise NotImplementedError("Translation getter not implemented!")

    async def _make_request(
        self,
        url: str,
        params: dict | None = None,
        data: str | None = None,
        headers: dict | None = None,
        proxy: str | None = None,
        return_json: bool = True,
    ) -> dict | str:
        """Make request to specific endpoint."""

        if headers is None:
            headers = self.headers

        timeout = ClientTimeout(total=self.timeout)
        s = self._session.post(
            url=url,
            params=params,
            data=data,
            headers=headers,
            verify_ssl=False,
            timeout=timeout,
            proxy=proxy,
        )
        async with s as r:
            response = await r.text()
        r.raise_for_status()

        if return_json:
            return json.loads(response)
        return response

    async def close(self) -> None:
        await self.__session.close()

    def __del__(self) -> None:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.create_task(self.__session.close())
