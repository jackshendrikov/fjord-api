from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.schemas.proxies import Proxy
from main.services.extra.proxynator.crawlers import BaseCrawler


class FreePoxyListCrawler(BaseCrawler):
    """
    FreePoxyList crawler.
    Website: https://free-proxy-list.net/
    """

    urls = [
        "https://free-proxy-list.net/",
        "https://www.sslproxies.org/",
        "http://www.us-proxy.org/",
    ]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc("section#list table tr").items():
            host = item.find("td").eq(0).text()
            port = item.find("td").eq(1).text()
            if host and port:
                yield Proxy(host=host, port=port)
