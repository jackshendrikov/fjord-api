import re
from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.schemas.proxies import Proxy
from main.services.proxies.crawlers import BaseCrawler


class ProxyNovaCrawler(BaseCrawler):
    """
    ProxyNova crawler.
    Website: https://www.proxynova.com/proxy-server-list/
    """

    urls = ["https://www.proxynova.com/proxy-server-list/"]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc("#tbl_proxy_list > tbody:nth-child(2) > tr").items():
            host_element = item.find("td:nth-child(1) > abbr > script").text()
            port = item.find("td:nth-child(2)").text()

            if not host_element or not port:
                continue

            groups = re.findall(r"document\.write\((.+?)\)", host_element)

            if not groups or len(groups) != 1:
                continue

            host = re.sub(r'["+ ]', "", groups[0])

            if host and port:
                yield Proxy(host=host, port=port)
