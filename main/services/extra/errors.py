"""Module for custom translation errors."""

from asyncio.exceptions import TimeoutError
from collections.abc import Callable
from typing import Any

from aiohttp import ClientError
from aiohttp.web import HTTPError


class TranslationError(Exception):
    """
    An exception occurs when an unexpected error occurred during the translation process.
    """


class TranslationRequestError(Exception):
    """
    Exception raised when error hen the error is related to a request for a translation.
    """


CLIENT_EXCEPTIONS = (HTTPError, ClientError, TimeoutError, AttributeError)


def async_session_handler(func: Callable) -> Callable:
    """
    Decorator that handles possible errors during the translation process.
    """

    async def wrapper(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
        try:
            return await func(self, *args, **kwargs)
        except CLIENT_EXCEPTIONS as e:
            await self.close()
            raise TranslationRequestError(e)
        except Exception as e:
            await self.close()
            raise TranslationError(e)

    return wrapper
