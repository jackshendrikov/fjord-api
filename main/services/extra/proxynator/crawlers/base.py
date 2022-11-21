import asyncio
from collections.abc import Iterator

import aiohttp
import urllib3

from main.const.common import DEFAULT_HEADERS
from main.const.proxies import PROXY_CHECK_TIMEOUT, PROXY_CHECK_URL
from main.core.config import get_app_settings
from main.core.logging import logger
from main.schemas.proxies import Proxy
from main.services.extra.errors import CLIENT_EXCEPTIONS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings = get_app_settings()


class BaseCrawler:
    urls: list[str] = []

    async def crawl(self) -> list[list[Proxy]]:
        """Async proxy crawl method."""

        tasks = [
            asyncio.create_task(self._handle_proxies(url=url)) for url in self.urls
        ]
        return await asyncio.gather(*tasks)

    async def _handle_proxies(self, url: str) -> list[Proxy]:
        """General method to process all proxies"""

        html = await self._make_request(url=url)
        proxies = self.parse(html=html)
        return await self._process_proxies(proxies)

    def parse(self, html: str) -> Iterator[Proxy]:
        """Method to parse proxy from specific provider"""

        raise NotImplementedError

    @staticmethod
    async def _make_request(
        url: str, headers: dict = DEFAULT_HEADERS, timeout: int = PROXY_CHECK_TIMEOUT
    ) -> str:
        """
        Make request to specific endpoint.

        :param url: specific URL.
        :param headers: request headers.
        :param timeout: request timeout value.

        :return: text response.
        """

        # TODO: Remove connector
        connector = aiohttp.TCPConnector(limit=100)
        async with aiohttp.ClientSession(
            headers=headers, connector=connector
        ) as session:
            logger.info(f"Make `GET` request to: {url}")
            async with session.get(url, timeout=timeout) as r:
                r.encoding = "utf-8"
                return await r.text()

    async def _process_proxies(self, proxy_list: Iterator[Proxy]) -> list[Proxy]:
        """Run async tasks to validate proxies and return filtered result"""

        connector = aiohttp.TCPConnector(limit=100)
        async with aiohttp.ClientSession(connector=connector) as session:
            good_proxies = [
                asyncio.create_task(self._check_proxy(session, proxy))
                for proxy in proxy_list
            ]
            proxies = await asyncio.gather(*good_proxies)
            return [proxy for proxy in proxies if proxy is not None]

    @staticmethod
    async def _check_proxy(
        session: aiohttp.ClientSession, proxy: Proxy
    ) -> Proxy | None:
        """Check if proxy is valid (response returns the same address as the proxy)"""

        try:
            async with session.get(
                PROXY_CHECK_URL, proxy=proxy.http_string, timeout=PROXY_CHECK_TIMEOUT
            ) as _:
                if settings.log_proxies:
                    logger.info(f"Good proxy: {proxy.string}")
                return proxy
        except CLIENT_EXCEPTIONS:
            if settings.log_proxies:
                logger.info(f"Bad proxy: {proxy.string}")
            return None
