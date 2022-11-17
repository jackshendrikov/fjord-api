from requests import exceptions

from main.schemas.translation import (
    DetectionIn,
    DetectionOut,
    TranslationIn,
    TranslationOut,
)
from main.services.translator.translate import Translator


class TranslationService:
    """Translation Service."""

    _translator = Translator()

    RETRY_EXCEPTION = (
        exceptions.ConnectionError,
        exceptions.RequestException,
        exceptions.HTTPError,
        exceptions.Timeout,
        exceptions.ConnectTimeout,
        exceptions.ReadTimeout,
    )

    def get_translation(self, payload: TranslationIn) -> TranslationOut:
        """
        Regular translation text.
        """
        translation = self._translator.translate(item=payload)
        return TranslationOut(translation=translation)

    def get_source_language(self, payload: DetectionIn) -> DetectionOut:
        """
        Detect language of input text.
        """
        language = self._translator.detect_language(item=payload)
        return DetectionOut(language=language)
