from main.const.tasks import TaskState
from main.schemas.tasks import TranslationDocumentPayload, TranslationTask
from main.utils.tasks import generate_task_id


class TranslationTasksService:
    """Translation Task Service."""

    def create_task(self, payload: TranslationDocumentPayload) -> TranslationTask:
        """
        Main function for registration translation tasks.
        """
        task = TranslationTask(
            run_id=generate_task_id(), payload=payload, state=TaskState.queued
        )
        return task
