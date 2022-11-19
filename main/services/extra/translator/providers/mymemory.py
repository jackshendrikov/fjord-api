from main.core.config import get_app_settings
from main.services.extra.errors import TranslationError
from main.services.extra.translator.providers import BaseTranslationProvider

settings = get_app_settings()


class MyMemoryProvider(BaseTranslationProvider):
    """
    @MyMemoryProvider: This is an integration with Translated MyMemory API.
    Follow Information's:
      Website: https://mymemory.translated.net/
      Documentation: https://mymemory.translated.net/doc/spec.php
    """

    base_url = "http://api.mymemory.translated.net/get"
    chars_limit = 500

    async def _translate(
        self, text: str, source: str, target: str, proxy: str | None
    ) -> str:
        params = {"q": text, "langpair": f"{source}|{target}"}
        if settings.mymemory_email:
            params["de"] = settings.mymemory_email

        data: dict = await self._make_request(url=self.base_url, params=params)  # type: ignore

        translation = data["responseData"]["translatedText"]
        if data["responseStatus"] != 200:
            raise TranslationError(translation)

        if translation:
            return translation

        matches = data["matches"]
        next_best_match = next(match for match in matches)
        return next_best_match["translation"]
