"""Module for custom database errors."""


class ClientDoesNotExist(Exception):
    """
    Raised when getting not registered client.
    """


class ClientConnectionError(Exception):
    """
    Raised when getting not registered client.
    """


class RepositoryDoesNotInit(Exception):
    """
    Raised when database not provided to repository.
    """
