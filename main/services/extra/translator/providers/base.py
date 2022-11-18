import json
from abc import ABCMeta, abstractmethod

import aiohttp
import urllib3

from main.const.common import DEFAULT_HEADERS, Language
from main.const.translator import DEFAULT_TIMEOUT
from main.core.config import get_app_settings
from main.core.logging import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings = get_app_settings()


class BaseTranslationProvider(metaclass=ABCMeta):
    base_url = ""

    timeout = DEFAULT_TIMEOUT
    headers = DEFAULT_HEADERS

    # TODO: Add 5000 char limit

    async def get_translation(
        self,
        text: str,
        source: str,
        target: str,
        autodetect: bool,
        proxy: str | None = None,
    ) -> str:
        """
        Get translation of a single text.

        :param text: The text to translate.
        :param source: The source language code (ISO 639).
        :param target: The target language code (ISO 639).
        :param autodetect: Indicates whether the provider has its own language detection or whether a third-party service is needed.
        :param proxy: proxy for request.
        :return: Translated text.
        """
        if not autodetect and source == Language.AUTO:
            source = await self.detect(text, proxy=proxy)
        translated_text = await self._translate(
            text=text, source=source, target=target, proxy=proxy
        )
        return translated_text.strip()

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
        """Translate specific string.

        :param text: The text to translate.
        :param source: The source language code (ISO 639).
        :param target: The target language code (ISO 639).
        :param proxy: Specific proxy for the request.

        :return: The translated text.
        """
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
        """
        Make request to specific endpoint.

        :param url: Specific URL.
        :param params: Dictionary in the query string for the request.
        :param data: Specific data for the request.
        :param headers: Specific headers for the request.
        :param proxy: Specific proxy for the request.
        :return: Deserialized JSON response.
        """
        if headers is None:
            headers = self.headers

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(headers=headers) as session:
            logger.info(f"Make `POST` request to: {url}")
            async with session.post(
                url=url,
                params=params,
                data=data,
                headers=headers,
                verify_ssl=False,
                timeout=timeout,
                proxy=proxy,
            ) as r:
                response = await r.text()
                r.raise_for_status()

                if return_json:
                    return json.loads(response)
                return response
