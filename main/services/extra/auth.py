from fastapi.security import HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from main.core.config import get_app_settings
from main.core.exceptions import (
    InvalidUserCredentialsException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from main.core.logging import logger
from main.core.security import get_basic_auth_token, get_password_hash, verify_password
from main.db.repositories.users import UsersRepository
from main.schemas.auth import UserInCreate, UserInDB, UserLogin, UserToken

settings = get_app_settings()


class BasicAuthService:
    """Basic Auth service."""

    _users_repo: UsersRepository = UsersRepository()

    async def get_user(self, credentials: HTTPBasicCredentials) -> UserInDB | None:
        """
        Retrieve current user info by login credentials.
        """

        logger.info(f"Getting user: {credentials.username}")
        return await self._users_repo.find_user_by_username(
            username=credentials.username
        )

    async def login_user(self, user: UserLogin) -> UserToken:
        """
        Validate user login request with email and password.
        """

        logger.info(f"Try to login user: {user.username}")
        await self.authenticate(username=user.username, password=user.password)
        return UserToken(
            token=get_basic_auth_token(username=user.username, password=user.password)
        )

    async def register_user(self, user_create: UserInCreate) -> UserInDB:
        """
        Register user in application.
        This method is using for CLI command.
        """

        logger.info(f"Try to find user: {user_create.username}")
        db_user = await self._users_repo.find_user_by_username(
            username=user_create.username
        )
        if db_user:
            raise UserAlreadyExistException(
                message=f"User with username: `{user_create.username}` already exists",
                status_code=HTTP_401_UNAUTHORIZED,
            )
        logger.info(f"Creating user: {user_create.username}")
        user = await self._insert_user(user=user_create)
        return user

    async def authenticate(self, username: str, password: str) -> UserInDB:
        """Authenticate user."""

        logger.info(f"Try to authenticate user: {username}")
        user = await self._users_repo.find_user_by_username(username=username)
        if not user:
            raise UserNotFoundException(
                message=f"User with username: `{username}` not found",
                status_code=HTTP_401_UNAUTHORIZED,
            )
        if not verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            raise InvalidUserCredentialsException(
                message="Invalid credentials", status_code=HTTP_401_UNAUTHORIZED
            )
        return user

    async def _insert_user(self, user: UserInCreate) -> UserInDB:
        """
        Hash user password and insert user info to database.
        """

        hashed_password = get_password_hash(password=user.password)
        db_user = UserInDB(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            disabled=False,
        )
        await self._users_repo.insert_user(user=db_user)
        return db_user
