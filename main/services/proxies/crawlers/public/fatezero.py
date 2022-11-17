import json
from collections.abc import Iterator

from main.schemas.proxies import Proxy
from main.services.proxies.crawlers import BaseCrawler


class FateZeroCrawler(BaseCrawler):
    """
    FateZero crawler.
    Website: http://proxylist.fatezero.org/proxy.list
    """

    urls = ["http://proxylist.fatezero.org/proxy.list"]

    def parse(self, html: str) -> Iterator[Proxy]:
        hosts_ports = html.split("\n")
        for addr in hosts_ports:
            if addr:
                ip_address = json.loads(addr)
                host = ip_address["host"]
                port = ip_address["port"]
                yield Proxy(host=host, port=port)
