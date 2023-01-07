from fastapi import APIRouter, Depends, Query

from main.const.common import Language
from main.const.translator import Provider
from main.core.config import get_app_settings
from main.core.dependencies import basic_security
from main.schemas.common import Response
from main.schemas.translation import (
    DetectionIn,
    DetectionOut,
    TranslationIn,
    TranslationOut,
)
from main.services.common.translation import TranslationService

settings = get_app_settings()
router = APIRouter(dependencies=[Depends(basic_security)])


@router.get("/translate", response_model=Response[TranslationOut])
async def get_translation(
    text: str = Query(..., max_length=5000, description="Text you want to translate"),
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
    service: TranslationService = Depends(),
) -> Response:
    """Get single translation."""

    payload = TranslationIn(**locals())
    data = await service.get_translation(payload=payload)
    return Response(data=data, message="Successfully received the translation")


@router.get("/detect", response_model=Response[DetectionOut])
async def get_source_language(
    text: str = Query(
        ..., max_length=5000, description="Text language of which you want to detect"
    ),
    provider: Provider = Query(
        default=Provider.GOOGLE_TRANSLATE,
        description="Detection provider you want to use",
    ),
    service: TranslationService = Depends(),
) -> Response:
    """Get language of input text."""

    payload = DetectionIn(**locals())
    data = await service.get_source_language(payload=payload)
    return Response(
        data=data,
        message="The language of the input text has been successfully determined",
    )
