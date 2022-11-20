from main.schemas.translation import (
    DetectionIn,
    DetectionOut,
    TranslationIn,
    TranslationOut,
)
from main.services.extra.translator.main import Translator


class TranslationService:
    """Translation Service."""

    _translator = Translator()

    async def get_translation(self, payload: TranslationIn) -> TranslationOut:
        """Get translation of single text."""

        translation = await self._translator.translate(item=payload)
        return TranslationOut(translation=translation)

    async def get_source_language(self, payload: DetectionIn) -> DetectionOut:
        """Detect language of input text."""

        language = await self._translator.detect_language(item=payload)
        return DetectionOut(language=language)
