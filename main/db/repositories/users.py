from main.core.config import get_app_settings
from main.db.repositories.base import BaseMongoRepository
from main.schemas.auth import UserInDB

settings = get_app_settings()


class BaseUsersRepository(BaseMongoRepository):
    """
    Base repository to manipulate with the users.
    """

    async def insert_user(self, user: UserInDB) -> None:
        """Insert registered user to collection."""

        await self.connection.insert_one(document=user.dict())

    async def find_user_by_username(self, username: str) -> UserInDB | None:
        """
        Find user using `username` field.
        Return db user if user found, otherwise return None.
        """

        query = {"username": username}
        user = await self.connection.find_one(filter=query)
        return UserInDB(**user) if user else None


class UsersRepository(BaseUsersRepository):
    """
    Base repository to manipulate with the users.
    """

    db = settings.mongo_db
    collection = settings.mongo_users_collection
