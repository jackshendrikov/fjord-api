from fastapi_utils.enums import StrEnum

from main.const.common import Language

DEFAULT_TIMEOUT = 5
GOOGLE_TTS_RPC = "MkEWBc"


class Provider(StrEnum):
    """
    Stores available translation providers.
    """

    GOOGLE_TRANSLATE = "Google Translate"
    DEEPL = "Deepl"
    LIBRE_TRANSLATE = "LibreTranslate"
    MYMEMORY = "MyMemory"


DEFAULT_PROVIDER = Provider.GOOGLE_TRANSLATE
UNSUPPORTED_LANGUAGES = {Provider.LIBRE_TRANSLATE: [Language.UA]}
