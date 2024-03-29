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
        """Get all available proxies."""

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
        """Get amount of proxies."""

        proxy_num = await self.connection.zcard(name=settings.redis_key)
        return ProxyNumber(count=proxy_num)

    async def set_score(self, proxy: Proxy, set_max: bool = False) -> int:
        """Set proxy to init or max score."""

        if await self._is_proxy_exists(proxy=proxy):
            score = settings.proxy_score_max if set_max else settings.proxy_score_init
            logger.info(f"{proxy.string} is valid, set to {score}.")
            return await self.connection.zadd(
                name=settings.redis_key, mapping={proxy.string: score}
            )
        return await self._add_proxy(proxy=proxy)

    async def decrease_score(self, proxy: Proxy) -> None:
        """
        Decrease score of proxy, if smaller than PROXY_SCORE_MIN, delete it.
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
        """

        logger.info(f"{proxy.string} is valid, add it to Redis.")
        return await self.connection.zadd(
            name=settings.redis_key, mapping={proxy.string: score}
        )

    async def _is_proxy_exists(self, proxy: Proxy) -> bool:
        """Check if proxy exists."""

        return (
            await self.connection.zscore(name=settings.redis_key, value=proxy.string)
            is not None
        )
