from dataclasses import dataclass

from fastapi_utils.enums import StrEnum

from main.const.common import Language

DEFAULT_TIMEOUT = 3
GOOGLE_TTS_RPC = "MkEWBc"


class Provider(StrEnum):
    """
    Stores available translation providers.
    """

    GOOGLE_TRANSLATE = "Google Translate"
    DEEPL = "Deepl"
    LIBRE_TRANSLATE = "LibreTranslate"
    MYMEMORY = "MyMemory"


@dataclass
class TextHashMap:
    original: str
    hash: str


@dataclass
class TranslationMap(TextHashMap):
    translation: str


DEFAULT_PROVIDER = Provider.GOOGLE_TRANSLATE
UNSUPPORTED_LANGUAGES = {Provider.LIBRE_TRANSLATE: [Language.NO, Language.UA]}
