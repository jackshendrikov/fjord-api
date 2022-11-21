from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.core.config import get_app_settings
from main.schemas.proxies import Proxy
from main.services.extra.proxynator.crawlers import BaseCrawler

settings = get_app_settings()
base_url = "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{page}"


class ProxyListPlusCrawler(BaseCrawler):
    """
    ProxyListPlus crawler.
    Website: https://list.proxylistplus.com
    """

    urls = [
        base_url.format(page=page)
        for page in range(1, settings.proxy_service_max_page + 1)
    ]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc("table").eq(2).find("tr[@class='cells']").items():
            host = item.find("td").eq(1).text()
            port = item.find("td").eq(2).text()
            if host and port:
                yield Proxy(host=host, port=port)
