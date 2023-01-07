from functools import lru_cache

from main.core.settings.app import AppSettings
from main.core.settings.base import AppEnvTypes, BaseAppSettings
from main.core.settings.development import DevAppSettings
from main.core.settings.production import ProdAppSettings
from main.core.settings.test import TestAppSettings

AppEnvType = TestAppSettings | DevAppSettings | ProdAppSettings

environments: dict[str, type[AppEnvType]] = {  # type: ignore
    AppEnvTypes.test: TestAppSettings,
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    """Return application config."""

    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()  # type: ignore
