from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class SuccessModel(BaseModel):
    success: bool | None = True


ResponseData = TypeVar("ResponseData")


class Response(GenericModel, Generic[ResponseData]):
    success: bool = True
    data: ResponseData | None = None
    message: str | None = None
    errors: list | None = None

    def dict(self, *args, **kwargs) -> dict[str, Any]:  # type: ignore
        """Exclude `null` values from the response."""
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)
