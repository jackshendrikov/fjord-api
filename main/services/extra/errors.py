"""Module for custom translation errors."""

from asyncio.exceptions import TimeoutError
from collections.abc import Callable
from typing import Any

from aiohttp import ClientError, ClientSession
from aiohttp.web import HTTPError


class TranslationError(Exception):
    """
    An exception occurs when an unexpected error occurred during the translation process.
    """


class TranslationRequestError(Exception):
    """
    Exception raised when error hen the error is related to a request for a translation.
    """


CLIENT_EXCEPTIONS = (HTTPError, ClientError, TimeoutError)


def async_session_handler(session: ClientSession) -> Callable:
    """
    Decorator that handles possible errors during the translation process.
    """

    def decorator(func: Callable) -> Callable:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except CLIENT_EXCEPTIONS as e:
                await session.close()
                raise TranslationRequestError(e)
            except Exception as e:
                await session.close()
                raise TranslationError(e)

        return wrapper

    return decorator
