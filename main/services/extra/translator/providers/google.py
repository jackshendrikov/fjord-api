import json
from urllib.parse import quote

from main.const.common import Language
from main.const.translator import GOOGLE_TTS_RPC
from main.services.extra.translator.providers import BaseTranslationProvider


class GoogleTranslateProvider(BaseTranslationProvider):
    """
    @GoogleTranslateProvider: This is an integration with Google Translate.
    Website: https://translate.google.com/
    """

    base_url = "https://translate.google.com"

    def __init__(self) -> None:
        super().__init__()
        self.full_url = f"{self.base_url}/_/TranslateWebserverUi/data/batchexecute"
        self.headers.update(
            {
                "Referer": self.base_url,
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            }
        )

    async def detect(self, text: str, proxy: str | None = None) -> str:  # type: ignore
        freq = self._package_rpc(text)
        r: str = await self._make_request(  # type: ignore
            url=self.full_url,
            data=freq,
            headers=self.headers,
            proxy=proxy,
            return_json=False,
        )
        for line in r.splitlines():
            if GOOGLE_TTS_RPC in line:
                response = list(json.loads(line))
                response = list(json.loads(response[0][2]))
                return response[0][2]

    async def _translate(  # type: ignore
        self, text: str, source: str, target: str, proxy: str | None
    ) -> str:
        if source == Language.AUTO:
            source = "auto"

        freq = self._package_rpc(text=text, source=source, target=target)
        r: str = await self._make_request(  # type: ignore
            url=self.full_url,
            data=freq,
            headers=self.headers,
            proxy=proxy,
            return_json=False,
        )

        for line in r.splitlines():
            if GOOGLE_TTS_RPC in line:
                response = list(json.loads(line))
                response = list(json.loads(response[0][2]))
                response = response[1][0]

                if len(response) == 1:
                    if len(response[0]) > 5:
                        sentences = response[0][5]
                    else:  # only URL
                        sentences = response[0][0]
                        return sentences

                    translate_text = ""
                    for sentence in sentences:
                        sentence = sentence[0]
                        translate_text += sentence.strip() + " "
                    return translate_text

                elif len(response) == 2:
                    sentences = [i[0] for i in response]
                    return " ".join(sentences)

    @staticmethod
    def _package_rpc(text: str, source: str = "auto", target: str = "auto") -> str:
        parameter = [[text.strip(), source, target, True], [1]]
        escaped_parameter = json.dumps(parameter, separators=(",", ":"))
        rpc = [[[GOOGLE_TTS_RPC, escaped_parameter, None, "generic"]]]
        spaced_rpc = json.dumps(rpc, separators=(",", ":"))
        freq = f"f.req={quote(spaced_rpc)}&"
        return freq
