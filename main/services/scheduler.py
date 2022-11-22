from main.const.common import TaskState
from main.core.config import get_app_settings
from main.core.logging import logger
from main.db.repositories.tasks import TranslationTasksRepository
from main.schemas.notifier import NotifierError
from main.schemas.tasks import TranslationTask
from main.services.executor import TranslationTaskExecutor
from main.services.extra.errors import TranslationError
from main.services.extra.notifier import NotificationService

settings = get_app_settings()


class TranslationTaskScheduler:
    """
    Manager class that control all translation task activity.
    """

    # Repositories
    _tasks_repository: TranslationTasksRepository = TranslationTasksRepository()

    # Notifier
    _notifier: NotificationService = NotificationService()

    # Executor
    _executor: TranslationTaskExecutor = TranslationTaskExecutor()

    @property
    async def queued_tasks(self) -> list[TranslationTask]:
        """Return list of currently queued tasks."""

        return await self._tasks_repository.get_tasks_with_state(state=TaskState.queued)

    @property
    async def active_tasks(self) -> list[TranslationTask]:
        """Return list of currently consumed tasks."""

        return await self._tasks_repository.get_tasks_with_state(
            state=TaskState.consumed
        )

    @property
    async def free_slots(self) -> int:
        """Return amount of free slots."""

        return settings.max_concurrent_tasks - len(await self.active_tasks)

    async def run_translation_process(self) -> None:
        """General method for executing translation task."""

        queued_tasks = await self.queued_tasks
        if not queued_tasks:
            logger.info("Queued translation tasks not found.")
            return

        free_slots = await self.free_slots
        logger.info(f"Number of free translation slots: {free_slots}.")

        while free_slots > 0:
            task = queued_tasks.pop()
            logger.info(f"Starting to work with `{task.task_id}` task.")

            # await self._tasks_repository.update_task_field(
            #     task_id=task.task_id, state=TaskState.consumed
            # )
            logger.info(
                f"Task state updated to {TaskState.consumed} for task: {task.task_id}"
            )

            try:
                await self._executor.execute(payload=task.payload)
            except TranslationError as exc:
                self._notifier.send_notification(
                    error=NotifierError(task_id=task.task_id, error_msg=str(exc))
                )
                # await self._tasks_repository.update_task_field(
                #     task_id=task.task_id, state=TaskState.error
                # )
                return

            await self._tasks_repository.update_task_field(
                task_id=task.task_id, state=TaskState.ready
            )
            free_slots -= 1
