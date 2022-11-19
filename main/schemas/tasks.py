from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from main.const.common import TaskState
from main.schemas.common import TranslationBaseModel


class PaginationMeta(BaseModel):
    total_tasks: int
    limit: int
    offset: int


class TranslationRunPayload(TranslationBaseModel):
    link: HttpUrl
    columns_to_translate: list[str]


class TranslationTask(BaseModel):
    task_id: str
    payload: TranslationRunPayload
    state: TaskState
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None


class TranslationTasksList(BaseModel):
    tasks: list[TranslationTask]
    meta: PaginationMeta


class TranslationTaskStatus(BaseModel):
    task_id: str
    status: str
