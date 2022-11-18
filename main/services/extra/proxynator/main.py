import asyncio

from main.core.logging import logger
from main.db.repositories.proxies import ProxyPoolRepository
from main.schemas.proxies import Proxy
from main.services.extra.proxynator.crawlers import __all__ as crawler_cls


class Proxynator:

    _proxies_repository: ProxyPoolRepository = ProxyPoolRepository()
    _crawlers = [cls() for cls in crawler_cls]

    async def find_proxies(self) -> None:
        """Start fetching new fresh proxies and add them to Redis."""

        proxies_to_add = await self._find_fresh_proxies()
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
