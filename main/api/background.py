from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from main.core.config import get_app_settings
from main.core.logging import logger
from main.services.scheduler import TranslationTaskScheduler

settings = get_app_settings()


def register_background_tasks(app: FastAPI) -> None:
    """
    Register tasks before initialize application.
    """
    if not settings.run_background_tasks:
        return

    if settings.scheduler_task_interval:
        scheduler_task_interval = settings.scheduler_task_interval

        @app.on_event("startup")
        @repeat_every(seconds=scheduler_task_interval, logger=logger)
        async def check_tasks() -> None:
            logger.info("Start Jarl tasks process...")
            scheduler = TranslationTaskScheduler()
            await scheduler.run_translation_process()
            logger.info("Nothing to process. Sleeping..")
