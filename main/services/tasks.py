from main.const.common import TaskState
from main.db.repositories.tasks import TranslationTasksRepository
from main.schemas.tasks import (
    TranslationRunPayload,
    TranslationTask,
    TranslationTasksList,
    TranslationTaskStatus,
)
from main.utils.tasks import generate_task_id


class TranslationTasksService:
    """Translation Task Service."""

    _tasks_repository: TranslationTasksRepository = TranslationTasksRepository()

    def create_task(self, payload: TranslationRunPayload) -> TranslationTask:
        """
        Create document translation task.
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
        Return translation task by `task_id` field.
        Or raise an exception if not found.
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
        return TranslationTaskStatus(task_id=task_id, state=task.state)
