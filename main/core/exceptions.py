from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from main.utils.tasks import form_error_message


class BaseInternalException(Exception):
    """
    Base error class for inherit all internal errors.
    """

    def __init__(
        self, message: str, status_code: int, errors: list[str] | None = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors


class TaskNotFoundException(BaseInternalException):
    """
    Exception raised when `task_id` field from JSON body not found.
    """


class InvalidSheetException(BaseInternalException):
    """
    Exception raised when the link in payload is inaccessible or does not contain needed columns.
    """


class BadLanguagesChoiceException(BaseInternalException):
    """
    Exception raised when source and target language is identical.
    """


class ProviderUnavailableException(BaseInternalException):
    """
    Exception raised when specific provider unavailable for some reason.
    """


class UnsupportedLanguageException(BaseInternalException):
    """
    Exception raised when provider can`t process selected language.
    """


class PoolEmptyException(BaseInternalException):
    """
    Exception raised when proxy pool is empty.
    """


def add_internal_exception_handler(app: FastAPI) -> None:
    """
    Handle all internal exceptions.
    """

    @app.exception_handler(BaseInternalException)
    async def _exception_handler(
        _: Request, exc: BaseInternalException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "type": type(exc).__name__,
                "message": exc.message,
                "errors": exc.errors or [],
            },
        )


def add_request_exception_handler(app: FastAPI) -> None:
    """
    Handle request validation errors exceptions.
    """

    @app.exception_handler(RequestValidationError)
    async def _exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "status": 422,
                "type": "RequestValidationError",
                "message": "Schema validation error",
                "errors": form_error_message(errors=exc.errors()),
            },
        )


def add_http_exception_handler(app: FastAPI) -> None:
    """
    Handle http exceptions.
    """

    @app.exception_handler(HTTPException)
    async def _exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "type": "HTTPException",
                "message": exc.detail,
                "errors": [],
            },
        )


def add_exception_handlers(app: FastAPI) -> None:
    """
    Set all exception handlers to app object.
    """
    add_internal_exception_handler(app=app)
    add_request_exception_handler(app=app)
    add_http_exception_handler(app=app)
