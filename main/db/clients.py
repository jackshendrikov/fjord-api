from abc import ABC, abstractmethod
from enum import Enum

from aioredis import ConnectionError, Redis, from_url
from motor.motor_asyncio import AsyncIOMotorClient

from main.core.config import get_app_settings
from main.core.logging import logger
from main.db.errors import ClientConnectionError, ClientDoesNotExist


class Client(Enum):
    """
    Enum for storing available clients.
    """

    redis = "redis"
    mongo = "mongo"


class AbstractClient(ABC):
    """
    Abstract class for clients.
    """

    @abstractmethod
    def connect(self) -> Redis | AsyncIOMotorClient:
        """Return client object."""

        raise NotImplementedError()


class RedisClient(AbstractClient):
    """Provide client for Redis."""

    settings = get_app_settings()

    def connect(self) -> Redis:
        """
        Make connection to Redis and return client.
        """

        return self._get_client(
            host=self.settings.redis_host,
            port=self.settings.redis_port,
            password=self.settings.redis_password,
        )

    @staticmethod
    def _get_client(host: str, port: int, password: str | None) -> Redis:
        """
        Return Redis client based on init arguments.
        """

        try:
            client = from_url(
                url=f"redis://{host}:{port}",
                password=password,
                db=0,
                decode_responses=True,
            )
        except ConnectionError:
            raise ClientConnectionError(f"Cannot connect to Redis server: {host}.")

        logger.debug(f"Successfully connected to Redis server: {host}")

        return client


class MongoDBClient(AbstractClient):
    """Provide client for MongoDB."""

    settings = get_app_settings()

    def connect(self) -> AsyncIOMotorClient:
        """
        Make connection to MongoDB and return client.
        """

        return self._get_client(
            host=self.settings.mongo_host,
            username=self.settings.mongo_user,
            password=self.settings.mongo_password,
        )

    @staticmethod
    def _get_client(
        host: str, username: str | None, password: str | None
    ) -> AsyncIOMotorClient:
        """
        Return MongoDB client based on init arguments.
        """

        database_url = (
            f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
        )
        client = AsyncIOMotorClient(database_url, uuidRepresentation="standard")
        logger.debug(f"Successfully connected to Mongo server: {host}")

        return client


class ClientFacade:
    """
    Client facade for getting already initialized client.
    """

    def __init__(self) -> None:
        self._clients: dict[Client, type[AbstractClient]] = {}

    def register_client(self, name: Client, client: type[AbstractClient]) -> None:
        """Register client in state."""

        self._clients[name] = client

    def get_client(self, name: Client) -> AbstractClient:
        """Return registered client."""

        if not self._clients.get(name):
            raise ClientDoesNotExist()
        return self._clients[name]()


client_facade = ClientFacade()
client_facade.register_client(name=Client.redis, client=RedisClient)
client_facade.register_client(name=Client.mongo, client=MongoDBClient)
