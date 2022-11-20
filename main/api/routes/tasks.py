from urllib.parse import parse_qs

import pandas as pd
from fastapi import APIRouter, Depends, Query
from pydantic import HttpUrl
from starlette.responses import StreamingResponse

from main.const.common import GOOGLE_SHEET_HOST, GOOGLE_SPREADSHEET_ID_LEN, Language
from main.const.translator import Provider
from main.core.config import get_app_settings
from main.core.exceptions import InvalidSheetException
from main.schemas.common import Response
from main.schemas.tasks import (
    TranslationRunPayload,
    TranslationTask,
    TranslationTasksList,
    TranslationTaskStatus,
)
from main.services.tasks import TranslationTasksService
from main.utils.tasks import gen_export_sheet_url

settings = get_app_settings()
router = APIRouter()


@router.get("", response_model=Response[TranslationTasksList])
def get_all_task(
    limit: int = settings.default_pagination_limit,
    offset: int = 0,
    service: TranslationTasksService = Depends(),
) -> Response:
    """Retrieve all translation tasks."""
    tasks = service.get_all_tasks(limit=limit, offset=offset)
    return Response(data=tasks)


@router.post("", response_model=Response[TranslationTask])
def set_task(
    link: HttpUrl = Query(
        description="Ordinary Google Sheet URL, should contain `gid` param in path"
    ),
    columns_to_translate: list[str] = Query(
        default=["text", "title"],
        min_length=1,
        description="Columns to translate from Google Sheet",
    ),
    source_language: Language = Query(
        default=Language.AUTO, description="Language of the text being translated"
    ),
    target_language: Language = Query(
        default=Language.EN, description="Language you want to translate"
    ),
    provider: Provider = Query(
        default=Provider.GOOGLE_TRANSLATE,
        description="Translation provider you want to use",
    ),
    service: TranslationTasksService = Depends(),
) -> Response:
    """Run translation task."""
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
    link = gen_export_sheet_url(spreadsheet_id=spreadsheet_id, sheet_id=sheet_id)

    columns_to_translate = set(columns_to_translate)
    if not columns_to_translate.issubset(set(pd.read_csv(link, nrows=0))):
        raise InvalidSheetException(
            f"The spreadsheet is missing 1 or more columns from: {columns_to_translate}.",
            status_code=400,
        )

    task = service.create_task(
        payload=TranslationRunPayload(
            source_language=source_language,
            target_language=target_language,
            provider=provider,
            link=link,
            columns_to_translate=columns_to_translate,
        )
    )
    return Response(data=task)


@router.get("/{task_id}", response_model=Response[TranslationTask])
def get_task(task_id: str, service: TranslationTasksService = Depends()) -> Response:
    """Retrieve translation task by `task_id`."""
    task = service.get_task(task_id=task_id)
    return Response(data=task)


@router.delete("/{task_id}", response_model=Response[TranslationTask])
def delete_task(task_id: str, service: TranslationTasksService = Depends()) -> Response:
    """Soft delete translation task by `task_id`."""
    task = service.delete_task(task_id=task_id)
    return Response(data=task)


@router.get("/{task_id}/status", response_model=Response[TranslationTaskStatus])
def get_task_status(
    task_id: str, service: TranslationTasksService = Depends()
) -> Response:
    """Retrieve translation task status by `task_id`."""
    task = service.get_task_status(task_id=task_id)
    return Response(data=task)


@router.get("/{task_id}/download")
async def get_translation_csv(
    task_id: str, service: TranslationTasksService = Depends()
) -> StreamingResponse:
    """Generate and Download CSV with translations by link from task with `task_id`."""

    stream = await service.get_translation_csv(task_id=task_id)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response
