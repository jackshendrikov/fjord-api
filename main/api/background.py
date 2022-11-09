from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from main.core.config import get_app_settings
from main.core.logging import logger

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
        def check_tasks() -> None:
            logger.info("Start V tasks process...")
            logger.info("Nothing to process. Sleeping..")
