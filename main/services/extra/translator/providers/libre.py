from main.core.config import get_app_settings
from main.services.extra.translator.providers import BaseTranslationProvider

settings = get_app_settings()


class LibreTranslateProvider(BaseTranslationProvider):
    """
    @LibreTranslateProvider: This is an integration with LibreTranslate translation API.
    Website: https://libretranslate.com/
    Documentation: https://libretranslate.com/docs/
    """

    base_url = "https://translate.argosopentech.com"

    async def detect(self, text: str, proxy: str | None = None) -> str:
        url = f"{self.base_url}/detect"
        params = {"q": text}
        if settings.libre_api_key:
            params["api_key"] = settings.libre_api_key

        data: dict = await self._make_request(url=url, params=params)  # type: ignore
        return data[0]["language"]

    async def _translate(
        self, text: str, source: str, target: str, proxy: str | None
    ) -> str:
        url = f"{self.base_url}/translate"
        params = {"q": text, "source": source, "target": target}
        if settings.libre_api_key:
            params["api_key"] = settings.libre_api_key

        data: dict = await self._make_request(url=url, params=params)  # type: ignore
        return data["translatedText"]
