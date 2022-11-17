from main.core.config import get_app_settings
from main.services.translator.providers import BaseTranslationProvider

settings = get_app_settings()


class LibreTranslateProvider(BaseTranslationProvider):
    """
    @LibreTranslateProvider: This is an integration with LibreTranslate translation API.
    Website: https://libretranslate.com/
    Documentation: https://libretranslate.com/docs/
    """

    base_url = "https://translate.argosopentech.com"

    def detect(self, text: str) -> str:
        """Detect the language of a single text.

        :param text: Text to detect
        :return: The detected language code.
        """
        url = f"{self.base_url}/detect"
        params = {"q": text}
        if settings.libre_api_key:
            params["api_key"] = settings.libre_api_key

        data = self._make_request(url=url, params=params)
        return data[0]["language"]

    def _translate(self, text: str, source: str, target: str) -> str:
        """Translate specific string.

        :param text: The text to translate.
        :param source: The source language code (ISO 639).
        :param target: The target language code (ISO 639).
        :return: The translated text.
        """
        url = f"{self.base_url}/translate"
        params = {"q": text, "source": source, "target": target}
        if settings.libre_api_key:
            params["api_key"] = settings.libre_api_key

        data = self._make_request(url=url, params=params)
        return data["translatedText"]
