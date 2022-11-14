from fastapi_utils.enums import StrEnum


class AvailableLanguages(StrEnum):
    """
    Stores the languages into which we can translate text
    """

    EN = "EN"
    JP = "JA"
    IT = "IT"
    GE = "GE"
    UA = "UK"


class TaskState(StrEnum):
    """
    Global tasks states.
    """

    queued = "QUEUED"
    consumed = "CONSUMED"
    ready = "READY"
    error = "ERROR"


GOOGLE_SHEET_HOST = "docs.google.com"
GOOGLE_SPREADSHEET_ID_LEN = 44
