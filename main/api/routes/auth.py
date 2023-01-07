from fastapi import APIRouter, Depends

from main.core.dependencies import get_current_user
from main.schemas.auth import UserInDB, UserLogin, UserToken
from main.schemas.common import Response
from main.services.extra.auth import BasicAuthService

router = APIRouter()
service = BasicAuthService()


@router.get("", response_model=Response[UserInDB])
async def get_user(user: UserInDB = Depends(get_current_user)) -> Response:
    """Get current user by provided credentials."""

    return Response(data=user)


@router.post("/login", response_model=Response[UserToken])
async def login_user(
    user: UserLogin, auth_service: BasicAuthService = Depends()
) -> Response:
    """Process user login."""

    token = await auth_service.login_user(user=user)
    return Response(data=token, message="The user authenticated successfully")
