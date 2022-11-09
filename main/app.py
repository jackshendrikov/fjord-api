from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from main.api.background import register_background_tasks
from main.api.router import router as api_router
from main.core.config import get_app_settings
from main.core.exceptions import add_exception_handlers


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

    if settings.app_env != "test":
        from main.core.integrations import setup_sentry

        setup_sentry()

    return application


app = create_app()

add_exception_handlers(app=app)
register_background_tasks(app=app)
