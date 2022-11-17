from random import choice

from main.core.config import get_app_settings
from main.core.logging import logger
from main.db.repositories.base import BaseRedisRepository
from main.schemas.proxies import ProxiesList, Proxy, ProxyNumber
from main.utils.proxies import convert_proxy

settings = get_app_settings()


class ProxyPoolRepository(BaseRedisRepository):
    """
    Repository to manipulate with proxies in Redis.
    """

    async def get_all_proxy(self) -> ProxiesList:
        """
        Get all proxies.

        :return: list of proxies.
        """
        proxies = await self.connection.zrangebyscore(
            name=settings.redis_key,
            min=settings.proxy_score_min,
            max=settings.proxy_score_max,
        )
        return ProxiesList(proxies=[convert_proxy(data=proxy) for proxy in proxies])

    async def get_random_proxy(self) -> Proxy | None:
        """
        Get random proxy.

        Firstly try to get proxy with max score.
            -> If not exists, try to get proxy by rank.
            -> If not exists, raise error.

        :return: proxy, like 8.8.8.8:8.
        """
        # try to get proxy with max score
        proxies = await self.connection.zrangebyscore(
            name=settings.redis_key,
            min=settings.proxy_score_max,
            max=settings.proxy_score_max,
        )
        if proxies:
            return convert_proxy(data=choice(proxies))

        # else get proxy by rank
        proxies = await self.connection.zrevrange(
            name=settings.redis_key,
            start=settings.proxy_score_min,
            end=settings.proxy_score_max,
        )
        if proxies:
            return convert_proxy(data=choice(proxies))

        return None

    async def count_proxies(self) -> ProxyNumber:
        """
        Get count of proxies.

        :return: count, int.
        """
        proxy_num = await self.connection.zcard(name=settings.redis_key)
        return ProxyNumber(count=proxy_num)

    async def set_max_score(self, proxy: Proxy) -> int:
        """
        Set proxy to max score.

        :param proxy: proxy.
        :return: new score.
        """
        if await self._is_proxy_exists(proxy=proxy):
            logger.info(f"{proxy.string} is valid, set to {settings.proxy_score_max}.")
            return await self.connection.zadd(
                name=settings.redis_key,
                mapping={proxy.string: settings.proxy_score_max},
            )
        return await self._add_proxy(proxy=proxy)

    async def decrease_score(self, proxy: Proxy) -> None:
        """
        Decrease score of proxy, if small than PROXY_SCORE_MIN, delete it.

        :param proxy: proxy.
        :return: new score.
        """
        if await self._is_proxy_exists(proxy=proxy):
            await self.connection.zincrby(
                name=settings.redis_key, amount=-1, value=proxy.string
            )
            score = await self.connection.zscore(
                name=settings.redis_key, value=proxy.string
            )

            logger.info(f"{proxy.string} score decrease 1, current {score}.")
            if score <= settings.proxy_score_min:
                logger.info(f"{proxy.string} current score {score}, remove.")
                await self.connection.zrem(settings.redis_key, proxy.string)

    async def _add_proxy(
        self, proxy: Proxy, score: int = settings.proxy_score_init
    ) -> int:
        """
        Add proxy and set it to init score.

        :param proxy: proxy, ip:port, like 8.8.8.8:88.
        :param score: int score.
        :return: result.
        """
        logger.info(f"{proxy.string} is valid, add it to Redis.")
        return await self.connection.zadd(
            name=settings.redis_key, mapping={proxy.string: score}
        )

    async def _is_proxy_exists(self, proxy: Proxy) -> bool:
        """
        Check if proxy exists.

        :param proxy: proxy.
        :return: if exists, bool.
        """
        return (
            await self.connection.zscore(name=settings.redis_key, value=proxy.string)
            is not None
        )
