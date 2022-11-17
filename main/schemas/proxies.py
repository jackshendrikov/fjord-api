from pydantic.main import BaseModel


class Proxy(BaseModel):
    host: str
    port: int

    @property
    def string(self) -> str:
        """
        String representation of proxy.
        """
        return f"{self.host}:{self.port}"

    @property
    def http_string(self) -> str:
        """
        String representation of proxy.
        """
        return f"http://{self.host}:{self.port}"


class ProxiesList(BaseModel):
    proxies: list[Proxy]


class ProxyNumber(BaseModel):
    count: int
