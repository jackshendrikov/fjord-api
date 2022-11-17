from main.const.common import TaskState
from main.schemas.tasks import TranslationRunPayload, TranslationTask
from main.utils.tasks import generate_task_id


class TranslationTasksService:
    """Translation Task Service."""

    def create_task(self, payload: TranslationRunPayload) -> TranslationTask:
        """
        Create document translation task.
        """
        task = TranslationTask(
            run_id=generate_task_id(), payload=payload, state=TaskState.queued
        )
        return task
