from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from main.schemas.auth import UserInDB
from main.services.extra.auth import BasicAuthService

basic_security = HTTPBasic()


async def get_current_user(
    user_service: BasicAuthService = Depends(),
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> UserInDB:
    """Return current user."""

    user = await user_service.authenticate(
        username=credentials.username, password=credentials.password
    )
    return user
