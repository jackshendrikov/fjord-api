from datetime import datetime
from typing import Any
from urllib.parse import parse_qs

import pandas as pd
from pydantic import BaseModel, Field, HttpUrl, root_validator

from main.const.tasks import (
    GOOGLE_SHEET_HOST,
    GOOGLE_SPREADSHEET_ID_LEN,
    AvailableLanguages,
    TaskState,
)
from main.core.exceptions import InvalidSheetException
from main.utils.tasks import gen_export_sheet_url


class TranslationDocumentPayload(BaseModel):
    link: HttpUrl
    target_language: AvailableLanguages = Field(default=AvailableLanguages.EN)
    columns_to_translate: list[str] = Field(default=["text", "title"])

    @root_validator
    def is_valid_sheet(cls, values: dict[str, Any]) -> dict[str, Any]:
        link: HttpUrl = values["link"]

        if link.host != GOOGLE_SHEET_HOST:
            raise InvalidSheetException(
                f"Host `{link.host}` is invalid. Should be `{GOOGLE_SHEET_HOST}`.",
                status_code=400,
            )

        try:
            spreadsheet_id = link.path.split("/")[-2]
        except (IndexError, AttributeError):
            raise InvalidSheetException(
                "Cannot find spreadsheet ID in your link!", status_code=400
            )

        if len(spreadsheet_id) != GOOGLE_SPREADSHEET_ID_LEN:
            raise InvalidSheetException(
                f"Invalid spreadsheet ID: `{spreadsheet_id}`. Must be {GOOGLE_SPREADSHEET_ID_LEN} chars long.",
                status_code=400,
            )

        sheet_id = parse_qs(link.fragment).get("gid")
        if not sheet_id or not sheet_id[0].isdigit():
            raise InvalidSheetException(
                "The sheet ID is missing or has an invalid format.", status_code=400
            )

        sheet_id = int(sheet_id[0])
        link: str = gen_export_sheet_url(
            spreadsheet_id=spreadsheet_id, sheet_id=sheet_id
        )

        columns_to_translate = set(values["columns_to_translate"])
        if not columns_to_translate.issubset(set(pd.read_csv(link, nrows=0))):
            raise InvalidSheetException(
                f"The spreadsheet is missing 1 or more columns from: {columns_to_translate}.",
                status_code=400,
            )

        return values


class TranslationRegular(BaseModel):
    text: str
    target_lang: AvailableLanguages = Field(default=AvailableLanguages.EN)


class TranslationTask(BaseModel):
    run_id: str
    payload: TranslationDocumentPayload
    state: TaskState
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
