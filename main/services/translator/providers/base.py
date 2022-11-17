import json
from abc import ABCMeta, abstractmethod

import urllib3
from requests import Request, Response, Session

from main.const.common import DEFAULT_HEADERS, Language
from main.core.config import get_app_settings
from main.core.logging import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings = get_app_settings()


class BaseTranslationProvider(metaclass=ABCMeta):
    base_url = ""
    session = None
    headers = DEFAULT_HEADERS

    def get_translation(
        self, text: str, source: str, target: str, autodetect: bool
    ) -> str:
        """
        Get translation of a single text.

        :param text: The text to translate.
        :param source: The source language code (ISO 639).
        :param target: The target language code (ISO 639).
        :param autodetect: Indicates whether the provider has its own language detection or whether a third-party service is needed.
        :return: Translated text.
        """
        # TODO : Add retry for request error, catch Translation Error outside or here but move retry other place
        # Here replace proxy
        if not autodetect and source == Language.AUTO:
            source = self.detect(text)
        return self._translate(text=text, source=source, target=target).strip()

    def detect(self, text: str) -> str:
        """
        Detect the language of a single text.

        :param text: Text to detect.
        :return: The detected language code.
        """
        url = "https://ws.detectlanguage.com/0.2/detect"
        params = {"q": text}

        headers = self.headers
        headers["Authorization"] = f"Bearer {settings.detect_language_api_key}"

        data = self._make_request(url=url, params=params, headers=headers)

        return data["data"]["detections"][0]["language"]

    @abstractmethod
    def _translate(self, text: str, source: str, target: str) -> str:
        """Translate specific string.

        :param text: The text to translate.
        :param source: The source language code (ISO 639).
        :param target: The target language code (ISO 639).
        :return: The translated text.
        """
        raise NotImplementedError("Translation getter not implemented!")

    def _make_request(
        self,
        url: str,
        params: dict | None = None,
        data: str | None = None,
        headers: dict | None = None,
    ) -> dict:
        """
        Make request to specific endpoint.

        :param url: Specific URL.
        :param params: Dictionary in the query string for the Request.
        :param data: Specific data for the Request.
        :param headers: Specific headers for the Request.
        :return: Deserialized JSON response.
        """
        if headers is None:
            headers = self.headers

        if self.session is None:
            self.session = Session()

        logger.info(f"Make `POST` request to: {url}")
        response = self.session.post(url, params=params, data=data, headers=headers)
        response.raise_for_status()
        return json.loads(response.text)

    def _make_advanced_request(
        self,
        url: str,
        method: str,
        data: str,
        timeout: int,
        headers: dict | None = None,
        proxy: dict | None = None,
    ) -> Response:
        """
        Make advanced request to specific endpoint.

        :param url: Specific URL.
        :param method: Method for Request object: ``GET``, ``POST``.
        :param data: Specific data for the Request.
        :param timeout: Response timeout.
        :param headers: Specific headers for the Request.
        :param proxy: Specific proxy for the Request.
        :return: Response object.
        """
        if headers is None:
            headers = self.headers

        if self.session is None:
            self.session = Session()

        logger.info(f"Make `{method}` prepare request to: {url}")

        req = Request(method="POST", url=url, data=data, headers=headers)
        prepped = req.prepare()

        self.session.proxies = proxy
        response = self.session.send(request=prepped, verify=False, timeout=timeout)
        response.raise_for_status()
        return response
