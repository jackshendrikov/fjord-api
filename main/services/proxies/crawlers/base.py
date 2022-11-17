import asyncio
from collections.abc import Iterator

import aiohttp
import urllib3

from main.const.common import DEFAULT_HEADERS
from main.const.proxies import PROXY_CHECK_TIMEOUT, PROXY_CHECK_URL
from main.core.config import get_app_settings
from main.core.logging import logger
from main.schemas.proxies import Proxy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings = get_app_settings()


class BaseCrawler:
    urls: list[str] = []

    async def crawl(self) -> list[list[Proxy]]:
        """
        Proxy crawl method.
        """
        tasks = [
            asyncio.create_task(self._handle_proxies(url=url)) for url in self.urls
        ]
        return await asyncio.gather(*tasks)

    async def _handle_proxies(self, url: str) -> list[Proxy]:
        html = await self._make_request(url=url)
        proxies = self.parse(html=html)
        return await self._process_proxies(proxies)

    def parse(self, html: str) -> Iterator[Proxy]:
        raise NotImplementedError

    @staticmethod
    async def _make_request(
        url: str, headers: dict = DEFAULT_HEADERS, timeout: int = PROXY_CHECK_TIMEOUT
    ) -> str:
        """
        Make request to specific endpoint.

        :param url: Specific URL.
        :param timeout: Timeout for the Request.
        :param verify: security certificate check in Request.
        :param headers: Specific headers for the Request.
        :return: Text response.
        """
        async with aiohttp.ClientSession(headers=headers) as session:
            logger.info(f"Make `GET` request to: {url}")
            async with session.get(url, timeout=timeout) as r:
                r.encoding = "utf-8"
                return await r.text()

    async def _process_proxies(self, proxy_list: Iterator[Proxy]) -> list[Proxy]:
        async with aiohttp.ClientSession() as session:
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
        try:
            async with session.get(
                PROXY_CHECK_URL, proxy=proxy.http_string, timeout=PROXY_CHECK_TIMEOUT
            ) as _:
                if settings.log_proxies:
                    logger.info(f"Good proxy: {proxy.string}")
                return proxy
        except Exception as e:
            logger.info(e)
            if settings.log_proxies:
                logger.info(f"Bad proxy: {proxy.string}")
            return None
