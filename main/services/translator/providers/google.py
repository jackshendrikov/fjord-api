import json
from typing import Any
from urllib.parse import quote

from main.const.common import Language
from main.const.translator import DEFAULT_TIMEOUT, GOOGLE_TTS_RPC
from main.services.translator.providers import BaseTranslationProvider


class GoogleTranslateProvider(BaseTranslationProvider):
    """
    @GoogleTranslateProvider: This is an integration with Google Translate.
    Website: https://translate.google.com/
    """

    base_url = "https://translate.google.com"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.full_url = f"{self.base_url}/_/TranslateWebserverUi/data/batchexecute"

        self.timeout = DEFAULT_TIMEOUT
        self.headers.update(
            {
                "Referer": self.base_url,
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            }
        )

    def detect(self, text: str) -> str:
        freq = self._package_rpc(text)
        response = self._make_advanced_request(
            url=self.full_url, method="POST", data=freq, timeout=self.timeout
        )
        for line in response.iter_lines(chunk_size=1024):
            decoded_line = line.decode("utf-8")
            if GOOGLE_TTS_RPC in decoded_line:
                response = list(json.loads(decoded_line))
                response = list(json.loads(response[0][2]))
                return response[0][2]

    def _translate(self, text: str, source: str, target: str) -> str:
        if source == Language.AUTO:
            source = "auto"

        freq = self._package_rpc(text=text, source=source, target=target)
        response = self._make_advanced_request(
            url=self.full_url, method="POST", data=freq, timeout=self.timeout
        )

        for line in response.iter_lines(chunk_size=1024):
            decoded_line = line.decode("utf-8")
            if GOOGLE_TTS_RPC in decoded_line:
                response = list(json.loads(decoded_line))
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
