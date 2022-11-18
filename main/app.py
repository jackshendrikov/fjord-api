from fastapi import FastAPI
from piccolo_admin import create_admin
from starlette.middleware.cors import CORSMiddleware

from main.api.background import register_background_tasks
from main.api.router import router as api_router
from main.apps.piccolo_app import APP_CONFIG
from main.core.config import get_app_settings
from main.core.exceptions import add_exception_handlers
from main.db.connections import handle_database_connections


def create_app() -> FastAPI:
    """
    Application factory, used to create application.
    """
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api/v1")

    admin = create_admin(tables=APP_CONFIG.table_classes, site_name="V API")
    application.mount(path="/admin/", app=admin)

    if settings.app_env != "test":
        from main.core.integrations import setup_sentry

        setup_sentry()

    return application


app = create_app()

add_exception_handlers(app=app)
handle_database_connections(app=app)
register_background_tasks(app=app)
