from main.const.common import TaskState
from main.core.config import get_app_settings
from main.core.logging import logger
from main.db.repositories.proxies import ProxyPoolRepository
from main.db.repositories.tasks import TranslationTasksRepository
from main.schemas.tasks import TranslationTask

# from main.services.runner import TranslationTaskExecutor

settings = get_app_settings()


class TranslationTaskScheduler:
    """
    Manager class that control all translation task activity.
    """

    # Repositories
    _tasks_repository: TranslationTasksRepository = TranslationTasksRepository()
    _proxies_repository: ProxyPoolRepository = ProxyPoolRepository()

    # Runner/Checker
    # _runner: TranslationTaskExecutor = TranslationTaskExecutor()

    @property
    def queued_tasks(self) -> list[TranslationTask]:
        """
        Return list of currently queued tasks.
        """
        return self._tasks_repository.get_tasks_with_state(state=TaskState.queued)

    @property
    def active_tasks(self) -> list[TranslationTask]:
        """
        Return list of currently consumed tasks.
        """
        return self._tasks_repository.get_tasks_with_state(state=TaskState.consumed)

    @property
    def free_slots(self) -> int:
        """Return amount of free slots."""
        return settings.max_concurrent_tasks - len(self.active_tasks)

    def run_translation_process(self) -> None:
        """General method for running translation task."""
        queued_tasks = self.queued_tasks
        if not queued_tasks:
            logger.info("Queued translation tasks not found.")
            return

        free_slots = self.free_slots
        logger.info(f"Number of free translation slots: {free_slots}.")

        while free_slots > 0:
            task = queued_tasks.pop()
            logger.info(f"Starting to work with `{task.task_id}` task.")

            self._tasks_repository.update_task_field(
                task_id=task.task_id, state=TaskState.consumed
            )
            logger.info(
                f"Task state updated to {TaskState.consumed} for task: {task.task_id}"
            )

            # self._runner.execute(task=task)

            free_slots -= 1
