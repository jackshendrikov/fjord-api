import asyncio

from main.core.config import get_app_settings
from main.core.exceptions import PoolEmptyException
from main.core.logging import logger
from main.db.repositories.proxies import ProxyPoolRepository
from main.schemas.proxies import ProxiesList, Proxy, ProxyNumber
from main.services.proxies.crawlers import __all__ as crawler_cls

settings = get_app_settings()


class ProxyPoolService:
    """
    Proxy pool service.
    """

    _proxies_repository = ProxyPoolRepository()
    _crawlers = [cls() for cls in crawler_cls]

    async def get_all_proxies(self) -> ProxiesList:
        """
        Return all proxies.
        """
        return await self._proxies_repository.get_all_proxy()

    async def get_random_proxy(self) -> Proxy:
        """
        Return random proxy.
        """
        proxy = await self._proxies_repository.get_random_proxy()
        if not proxy:
            raise PoolEmptyException(
                "Cannot find valid proxy, proxy pool is empty!", status_code=404
            )
        return proxy

    async def get_proxies_num(self) -> ProxyNumber:
        """
        Return number of valid proxies.
        """
        return await self._proxies_repository.count_proxies()

    async def find_proxies(self) -> None:
        """
        Start fetching new fresh proxies and add them to Redis.
        """
        proxies_to_add = asyncio.get_event_loop().run_until_complete(
            self._find_fresh_proxies()
        )
        proxies_to_add = [
            self._proxies_repository.set_max_score(proxy=proxy)
            for proxy_packs in proxies_to_add
            for proxy_pack in proxy_packs
            for proxy in proxy_pack
        ]
        logger.info(f"Found {len(proxies_to_add)} fresh proxies.")
        await asyncio.wait(proxies_to_add)

    async def _find_fresh_proxies(self) -> list[list[list[Proxy]]]:
        """
        Start async proxies scraping for all crawlers and its corresponding URLS.
        """
        crawler_tasks = [
            asyncio.create_task(crawler.crawl()) for crawler in self._crawlers
        ]
        results = await asyncio.gather(*crawler_tasks)
        return results
