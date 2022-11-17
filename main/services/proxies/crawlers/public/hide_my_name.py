from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.core.config import get_app_settings
from main.schemas.proxies import Proxy
from main.services.proxies.crawlers import BaseCrawler

settings = get_app_settings()
base_url = "https://hidemy.name/en/proxy-list/?type=hs&start={start}/"


class HideMyNameCrawler(BaseCrawler):
    """
    HideMyName crawler.
    Website:https://hidemy.name/en/proxy-list/
    """

    urls = [
        base_url.format(start=start)
        for start in range(0, settings.proxy_service_max_page * 64, 64)
    ]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc("tbody tr").items():
            host = item.find("td").eq(0).text()
            port = item.find("td").eq(1).text()
            if host and port:
                yield Proxy(host=host, port=port)
