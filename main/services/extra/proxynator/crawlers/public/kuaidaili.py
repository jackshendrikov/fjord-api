from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.core.config import get_app_settings
from main.schemas.proxies import Proxy
from main.services.extra.proxynator.crawlers import BaseCrawler

settings = get_app_settings()
base_url = "https://www.kuaidaili.com/free/{type}/{page}/"


class KuaidailiCrawler(BaseCrawler):
    """
    Kuaidaili crawler.
    Website: https://www.kuaidaili.com/
    """

    urls = [
        base_url.format(type=proxy_type, page=page)
        for proxy_type in ("intr", "inha")
        for page in range(1, settings.proxy_service_max_page + 1)
    ]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc("table tr").items():
            host = item.find('td[data-title="IP"]').text()
            port = item.find('td[data-title="PORT"]').text()
            if host and port:
                yield Proxy(host=host, port=port)
