import inspect
import pkgutil

# load classes subclass of BaseCrawler
from main.services.extra.proxynator.crawlers.base import BaseCrawler

classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):  # type: ignore
    module = loader.find_module(name).load_module(name)  # type: ignore
    for title, value in inspect.getmembers(module):
        globals()[title] = value
        if (
            inspect.isclass(value)
            and issubclass(value, BaseCrawler)
            and value is not BaseCrawler
            and not getattr(value, "ignore", False)
        ):
            classes.append(value)
__all__ = __ALL__ = classes
