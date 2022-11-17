from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.schemas.proxies import Proxy
from main.services.proxies.crawlers import BaseCrawler


class IPAddressCrawler(BaseCrawler):
    """
    IPAddress crawler.
    Website: https://www.ipaddress.com/proxy-list/
    """

    urls = ["https://www.ipaddress.com/proxy-list/"]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc(".proxylist tbody tr").items():
            ip_port: str = item.find("td:nth-child(1)").text()
            host, port = ip_port.split(":")
            if host and port:
                yield Proxy(host=host, port=port)
