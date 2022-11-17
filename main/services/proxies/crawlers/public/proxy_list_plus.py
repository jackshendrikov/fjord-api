from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.const.proxies import PROXY_SERVICE_MAX_PAGE
from main.schemas.proxies import Proxy
from main.services.proxies.crawlers import BaseCrawler

base_url = "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{page}/"


class ProxyListPlusCrawler(BaseCrawler):
    """
    ProxyListPlus crawler.
    Website: https://list.proxylistplus.com
    """

    urls = [base_url.format(page=page) for page in range(1, PROXY_SERVICE_MAX_PAGE + 1)]

    def parse(self, html: str) -> Iterator[Proxy]:
        doc = pq(html)
        for item in doc("table").eq(2).find("tr[@class='cells']").items():
            host = item.find("td").eq(1).text()
            port = item.find("td").eq(2).text()
            if host and port:
                yield Proxy(host=host, port=port)
