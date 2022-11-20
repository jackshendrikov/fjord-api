"""Module for project 3rd parties services."""

import graypy
import sentry_sdk

from main.core.config import get_app_settings

settings = get_app_settings()


def setup_sentry() -> None:
    """Setup error logging to Sentry."""

    if settings.sentry_dsn:
        sentry_sdk.init(settings.sentry_dsn, traces_sample_rate=1.0)


def setup_graylog() -> graypy.GELFUDPHandler | None:
    """Initialize Graylog handler."""

    if settings.graylog_host and settings.graylog_input_port:
        handler = graypy.GELFUDPHandler(
            host=settings.graylog_host, port=settings.graylog_input_port
        )
        return handler
