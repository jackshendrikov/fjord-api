from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from redis.asyncio import Redis

from main.db.clients import Client, client_facade
from main.db.errors import RepositoryDoesNotInit


class BaseRedisRepository:
    """Base Redis repository."""

    def __init__(self) -> None:
        self._is_connected: bool = False
        self._conn: Redis | None = None

    @property
    def connection(self) -> Redis:
        """
        Provide connection to Redis.
        """

        if not self._is_connected:
            self._is_connected = True
            client: Redis = client_facade.get_client(name=Client.redis).connect()
            self._conn = client
        return self._conn


class BaseMongoRepository:
    """Base MongoDB repository."""

    db: str
    collection: str

    def __init__(self) -> None:
        self._is_connected: bool = False
        self._conn: AsyncIOMotorCollection | None = None
        self._check_init_params()

    @property
    def connection(self) -> AsyncIOMotorCollection:
        """
        Provide connection to MongoDB.
        """

        if not self._is_connected:
            self._is_connected = True
            client: AsyncIOMotorClient = client_facade.get_client(
                name=Client.mongo
            ).connect()
            self._conn = client[self.db][self.collection]
        return self._conn

    def _check_init_params(self) -> None:
        """
        Raise an error if repository attributes didn't set.
        """

        if not self.db or not self.collection:
            raise RepositoryDoesNotInit()
