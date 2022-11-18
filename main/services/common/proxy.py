from main.core.config import get_app_settings
from main.core.exceptions import PoolEmptyException
from main.db.repositories.proxies import ProxyPoolRepository
from main.schemas.proxies import ProxiesList, Proxy, ProxyNumber

settings = get_app_settings()


class ProxyPoolService:
    """
    Proxy pool service.
    """

    _proxies_repository: ProxyPoolRepository = ProxyPoolRepository()

    async def get_all_proxies(self) -> ProxiesList:
        """Return all proxies."""
        return await self._proxies_repository.get_all_proxy()

    async def get_random_proxy(self) -> Proxy:
        """Return random proxy."""

        proxy = await self._proxies_repository.get_random_proxy()
        if not proxy:
            raise PoolEmptyException(
                "Cannot find valid proxy, proxy pool is empty!", status_code=404
            )
        return proxy

    async def get_proxies_num(self) -> ProxyNumber:
        """Return number of valid proxies."""

        return await self._proxies_repository.count_proxies()
