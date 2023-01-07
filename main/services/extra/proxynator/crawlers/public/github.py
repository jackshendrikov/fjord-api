from collections.abc import Iterator

from pyquery import PyQuery as pq

from main.schemas.proxies import Proxy
from main.services.extra.proxynator.crawlers import BaseCrawler
from main.utils.proxies import is_valid_proxy_signature


class RawProxyCrawler(BaseCrawler):
    """
    GitHub + raw resources' crawler.
    """

    urls = [
        "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    ]

    def parse(self, html: str) -> Iterator[Proxy]:
        if not len(html):
            return
        doc = pq(html)
        for item in doc.text().split():
            if is_valid_proxy_signature(item):
                host, port = item.split(":")
                yield Proxy(host=host, port=port)
