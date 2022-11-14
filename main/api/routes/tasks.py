from fastapi import APIRouter, Depends

from main.core.config import get_app_settings
from main.schemas.common import Response
from main.schemas.tasks import TranslationDocumentPayload, TranslationTask
from main.services.tasks import TranslationTasksService

settings = get_app_settings()
router = APIRouter()


@router.post("", response_model=Response[TranslationTask])
def set_task(
    payload: TranslationDocumentPayload, service: TranslationTasksService = Depends()
) -> Response:
    """Run translation task."""
    task = service.create_task(payload=payload)
    return Response(data=task)
