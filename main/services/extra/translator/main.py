from main.const.translator import Provider
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
        provider = self._get_provider_class(provider=item.provider)
        autodetect = isinstance(provider, (GoogleTranslateProvider, DeeplProvider))
        return await provider.get_translation(
            text=item.text,
            source=item.source_language.value,
            target=item.target_language.value,
            autodetect=autodetect,
        )

    async def detect_language(self, item: DetectionIn) -> str:
        provider = self._get_provider_class(provider=item.provider)
        return await provider.detect(text=item.text)

    @staticmethod
    def _get_provider_class(provider: Provider) -> BaseTranslationProvider:
        """
        Return specific provider class.
        """
        provider_to_class_map: dict[str, type[BaseTranslationProvider]] = {
            Provider.GOOGLE_TRANSLATE: GoogleTranslateProvider,
            Provider.LIBRE_TRANSLATE: LibreTranslateProvider,
            Provider.DEEPL: DeeplProvider,
            Provider.MYMEMORY: MyMemoryProvider,
        }
        return provider_to_class_map[provider]()
