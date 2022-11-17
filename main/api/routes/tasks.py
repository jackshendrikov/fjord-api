from fastapi import APIRouter, Depends

from main.core.config import get_app_settings
from main.schemas.common import Response
from main.schemas.tasks import (
    TranslationRunPayload,
    TranslationTask,
    TranslationTasksList,
    TranslationTaskStatus,
)
from main.services.tasks import TranslationTasksService

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
    payload: TranslationRunPayload, service: TranslationTasksService = Depends()
) -> Response:
    """Run translation task."""
    task = service.create_task(payload=payload)
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
