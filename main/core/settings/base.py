from pydantic import BaseSettings


class AppEnvTypes:
    """
    Available application environments.
    """

    prod = "prod"
    dev = "dev"
    test = "test"


class ProjectEnv:
    """
    Available project environments.
    """

    production = "production"
    staging = "staging"
    testing = "testing"


class BaseAppSettings(BaseSettings):
    """
    Base application setting class.
    """

    current_env: str

    app_env: str = AppEnvTypes.prod

    # How many tasks can be processed in parallel.
    max_concurrent_tasks: int

    # Scheduler background task interval.
    scheduler_task_interval: int

    # Flag enable/disable background tasks on startup.
    run_background_tasks: bool

    # Graylog setup.
    graylog_host: str | None
    graylog_input_port: int | None = 0

    # Sentry setup.
    sentry_dsn: str | None

    class Config:
        env_file = ".env"
