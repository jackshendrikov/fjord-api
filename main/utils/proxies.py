from main.schemas.proxies import Proxy


def is_valid_proxy_signature(data: str) -> bool:
    """
    Check string if it is in valid proxy format.
    """

    if ":" in data:
        ip, port = data.split(":")
        return is_ip_valid(ip=ip) and is_port_valid(port=port)
    return is_ip_valid(ip=data)


def is_ip_valid(ip: str) -> bool:
    """
    Check string if it is in valid IP format.
    """

    a = ip.split(".")
    if len(a) != 4:
        return False

    for x in a:
        if not x.isdigit():
            return False

        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def is_port_valid(port: str) -> bool:
    """
    Check if proxy port is valid number.
    """

    return port.isdigit()


def convert_proxy(data: str) -> Proxy:
    """
    Convert str repr to valid proxy.
    """

    host, port = data.split(":")
    return Proxy.construct(host=host, port=int(port))
