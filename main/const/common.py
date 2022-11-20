from fastapi_utils.enums import StrEnum


class Region(StrEnum):
    """
    Stores
    """


class Language(StrEnum):
    """
    Stores the languages into which we can translate textю
    """

    AUTO = "autodetect"
    EN = "en"
    JP = "ja"
    IT = "it"
    GE = "de"
    NO = "no"
    UA = "uk"


class TaskState(StrEnum):
    """
    Global tasks states.
    """

    queued = "QUEUED"
    consumed = "CONSUMED"
    ready = "READY"
    error = "ERROR"
    deleted = "DELETED"


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/47.0.2526.106 Safari/537.36"
}

GOOGLE_SHEET_HOST = "docs.google.com"
GOOGLE_SPREADSHEET_ID_LEN = 44

READ_CSV_CHUNK_SIZE = 10000
ASYNC_TRANSLATION_TEXTS = 20
