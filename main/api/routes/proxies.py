from fastapi import APIRouter, Depends

from main.core.dependencies import basic_security
from main.schemas.common import Response
from main.schemas.proxies import ProxiesList, Proxy, ProxyNumber
from main.services.common.proxy import ProxyPoolService

router = APIRouter(dependencies=[Depends(basic_security)])


@router.get("", response_model=Response[ProxiesList])
async def get_all_proxies(service: ProxyPoolService = Depends()) -> Response:
    """Get all available valid proxies."""

    proxies = await service.get_all_proxies()
    return Response(data=proxies, message="Proxies retrieved successfully")


@router.get("/random", response_model=Response[Proxy])
async def get_proxy(service: ProxyPoolService = Depends()) -> Response:
    """Get random proxy."""

    proxy = await service.get_random_proxy()
    return Response(data=proxy, message="Proxy retrieved successfully")


@router.get("/count/", response_model=Response[ProxyNumber])
async def get_proxies_num(service: ProxyPoolService = Depends()) -> Response:
    """Get number of valid proxies."""

    proxy_num = await service.get_proxies_num()
    return Response(data=proxy_num, message="Proxies number retrieved successfully")
