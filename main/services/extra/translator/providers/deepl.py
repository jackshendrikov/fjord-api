from main.const.common import Language
from main.core.config import get_app_settings
from main.services.extra.errors import TranslationError
from main.services.extra.translator.providers import BaseTranslationProvider

settings = get_app_settings()


class DeeplProvider(BaseTranslationProvider):
    """
    @DeeplProvider: This is an integration with DeepL Translator API.
    Website: https://www.deepl.com
    Documentation: https://www.deepl.com/docs-api
    """

    base_url = "https://api-free.deepl.com/v2/translate"
    base_pro_url = "https://api.deepl.com/v2/translate"

    async def _translate(
        self, text: str, source: str, target: str, proxy: str | None
    ) -> str:
        params = {"target_lang": target, "text": text}
        if settings.deepl_auth_key:
            self.base_url = self.base_pro_url
            params["auth_key"] = settings.deepl_auth_key

        if source != Language.AUTO:
            params["source_lang"] = source

        data: dict = await self._make_request(url=self.base_url, params=params)  # type: ignore

        if "error" in data:
            raise TranslationError(data["error"]["message"])

        return data["translations"][0]["text"]
