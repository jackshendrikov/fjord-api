# import pandas as pd
#
# from main.const.common import READ_CSV_CHUNK_SIZE
# from main.core.config import get_app_settings
# from main.core.logging import logger
# from main.schemas.proxies import Proxy
# from main.services.common.proxy import ProxyPoolService
# from main.services.extra.proxynator.main import Proxynator
# from main.services.extra.translator.main import Translator
# from main.schemas.tasks import TranslationTask
#
# settings = get_app_settings()
#
#
# class TranslationTaskExecutor:
#
#     # Services
#     _proxy_service: ProxyPoolService = ProxyPoolService()
#
#     # Extra Services
#     _translator: Translator = Translator()
#     _proxynator: Proxynator = Proxynator()
#
#     def execute(self, task: TranslationTask) -> None:
#         for chunk in pd.read_csv(
#             task.payload.link,
#             usecols=task.payload.columns_to_translate,
#             chunksize=READ_CSV_CHUNK_SIZE,
#         ):
#             for column in task.payload.columns_to_translate:
#                 texts_to_translate = chunk[column].tolist()
#
#         pass
#
#     async def _process_translation_texts(self, texts_to_translate: list[str]):
#         for text in texts_to_translate:
#             proxy = await self._proxy_service.get_random_proxy()
#             self._get_translation(text=text, proxy=proxy)
#         pass
#
#     def _get_translation(self, text: str, proxy: Proxy) -> str:
#         pass
