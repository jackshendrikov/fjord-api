from typing import Any, Generic, TypeVar

from pydantic import BaseModel, root_validator
from pydantic.generics import GenericModel

from main.const.common import Language
from main.const.translator import UNSUPPORTED_LANGUAGES, Provider
from main.core.config import get_app_settings
from main.core.exceptions import (
    BadLanguagesChoiceException,
    ProviderUnavailableException,
    UnsupportedLanguageException,
)

settings = get_app_settings()


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


class TranslationBaseModel(BaseModel):
    source_language: Language
    target_language: Language
    provider: Provider

    @root_validator(pre=False, skip_on_failure=True)
    def validate_model(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values["source_language"] == values["target_language"]:
            raise BadLanguagesChoiceException(
                "Source and target languages are identical!", status_code=400
            )

        if values["provider"] == Provider.DEEPL and not settings.deepl_auth_key:
            raise ProviderUnavailableException(
                "DeepL provider currently unavailable! We need paid auth key..",
                status_code=400,
            )

        langs = (values["source_language"], values["target_language"])
        unsupported_langs = UNSUPPORTED_LANGUAGES.get(values["provider"], [])
        if any(x in unsupported_langs for x in langs):
            raise UnsupportedLanguageException(
                "Selected provider cannot process selected language.", status_code=400
            )

        return values
