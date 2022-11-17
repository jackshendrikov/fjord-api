from pydantic import BaseModel

from main.const.translator import Provider
from main.schemas.common import TranslationBaseModel


class TranslationIn(TranslationBaseModel):
    text: str


class DetectionIn(BaseModel):
    text: str
    provider: Provider


class TranslationOut(BaseModel):
    translation: str


class DetectionOut(BaseModel):
    language: str
