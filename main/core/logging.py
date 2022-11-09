"""
Module configuration custom logger.
"""
import logging

from main.core.config import get_app_settings

DISABLE_LOGGERS: list[str] = []
DEFAULT_LOGGER_NAME = "v-api"

LOG_MESSAGE_FORMAT = "[%(name)s] [%(asctime)s] %(message)s"

settings = get_app_settings()


class ProjectLogger:
    """
    Custom project logger.
    """

    def __init__(self, name: str):
        self.name = name
        self._logger: logging.Logger | None = None

    def __call__(self) -> logging.Logger:
        return self.logger

    @property
    def logger(self) -> logging.Logger:
        """
        Return initialized logger object.
        """
        if not self._logger:
            self._logger = self.create_logger()
        return self._logger

    def create_logger(self) -> logging.Logger:
        """
        Return configured logger.
        """
        logging.basicConfig(format=LOG_MESSAGE_FORMAT)

        project_logger = logging.getLogger(name=self.name)
        project_logger.setLevel(level=logging.INFO)

        self._disable_loggers()
        self._setup_graylog(project_logger=project_logger)

        return project_logger

    def _disable_loggers(self) -> None:
        """
        Disable 3rd parties loggers.
        """
        for logger_name in DISABLE_LOGGERS:
            self._disable_logger(name=logger_name)

    @staticmethod
    def _disable_logger(name: str) -> None:
        """
        Set `CRITICAL` log level to disable logs from specific logger.
        """
        logging.getLogger(name=name).setLevel(logging.CRITICAL)

    @staticmethod
    def _setup_graylog(project_logger: logging.Logger) -> None:
        """
        Initialize Graylog handler.
        """
        if settings.app_env != "test":
            from main.core.integrations import setup_graylog

            graylog_handler = setup_graylog()

            if graylog_handler:
                project_logger.addHandler(graylog_handler)
            else:
                project_logger.warning("Graylog host and port not provided")


def _create_logger() -> logging.Logger:
    """
    Initialize logger for project.
    """
    return ProjectLogger(name=DEFAULT_LOGGER_NAME)()


logger = _create_logger()
