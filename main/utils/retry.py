from collections.abc import Callable
from time import sleep
from typing import Any

from main.core.logging import logger


def retry(times: int, delay: int, exceptions: tuple) -> Callable:
    """
    Retry decorator in case of exception from `exceptions`.
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown.
    :param times: The number of times to repeat the wrapped function/method.
    :param delay: The time of sleep between repeating.
    :param exceptions: Lists of exceptions that trigger a retry attempt.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 1
            while attempt <= times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    logger.exception(
                        f"Exception thrown when attempting to run {func}, "
                        f"attempt {attempt}/{times}"
                    )
                    sleep(delay)
                    attempt += 1
            return func(*args, **kwargs)

        return wrapper

    return decorator
