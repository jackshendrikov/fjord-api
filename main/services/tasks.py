import asyncio
from io import StringIO

import pandas as pd

from main.const.common import TaskState
from main.db.models.postgres import Translation
from main.db.repositories.tasks import TranslationTasksRepository
from main.schemas.tasks import (
    TranslationRunPayload,
    TranslationTask,
    TranslationTasksList,
    TranslationTaskStatus,
)
from main.utils.common import get_text_hash
from main.utils.tasks import generate_task_id


class TranslationTasksService:
    """Translation Task Service."""

    _tasks_repository: TranslationTasksRepository = TranslationTasksRepository()

    def create_task(self, payload: TranslationRunPayload) -> TranslationTask:
        """
        Create translation task.

        :param payload: payload of the task.
        :return: Translation task.
        """

        task = TranslationTask(
            task_id=generate_task_id(), payload=payload, state=TaskState.queued
        )
        self._tasks_repository.insert_translation_task(task=task)

        return task

    def get_all_tasks(self, limit: int, offset: int) -> TranslationTasksList:
        """
        Return all translation tasks with specific `offset`.

        :param limit: Total task per one page.
        :param offset: Number of task to skip.
        :return: Object with tasks list and current pagination metadata.
        """

        total, tasks = self._tasks_repository.find_all_tasks(limit=limit, offset=offset)
        return TranslationTasksList(
            tasks=tasks, meta={"total_tasks": total, "limit": limit, "offset": offset}
        )

    def get_task(self, task_id: str) -> TranslationTask:
        """
        Return translation task by `task_id` field or raise an exception if not found.

        :param task_id: ID of the task.
        :return: Translation task.
        """

        return self._tasks_repository.find_task_by_task_id(task_id=task_id)

    def delete_task(self, task_id: str) -> TranslationTask:
        """
        Return translation task by `task_id` field or raise an exception if not found.

        :param task_id: ID of the task.
        :return: Translation task.
        """

        self._tasks_repository.update_task_field(
            task_id=task_id, state=TaskState.deleted
        )

        return self._tasks_repository.find_task_by_task_id(task_id=task_id)

    def get_task_status(self, task_id: str) -> TranslationTaskStatus:
        """
        Return translation task status by `task_id` field or raise an exception if not found.

        :param task_id: ID of the task.
        :return: Task Status for Translation task.
        """

        task = self._tasks_repository.find_task_by_task_id(task_id=task_id)
        return TranslationTaskStatus(task_id=task_id, status=task.state)

    async def get_translation_csv(self, task_id: str) -> StringIO:
        """
        Generate CSV with translations (the original CSV is taken from the link in the payload).

        :param task_id: ID of the task.

        :return: streaming response.
        """
        task = self._tasks_repository.find_task_by_task_id(task_id=task_id)

        df = pd.read_csv(task.payload.link)
        stream = StringIO()

        for column in task.payload.columns_to_translate:
            df[f"{column}_translated"] = await asyncio.gather(
                *(self._get_translation(v) for v in df[column])
            )

        df.to_csv(stream, index=False)

        return stream

    @staticmethod
    async def _get_translation(text: str) -> str | None:
        """Map translation with original text hash"""

        text_hash = get_text_hash(text=text)
        item = await Translation.objects().get(Translation.text_hash == text_hash)
        if item:
            return item.translated
