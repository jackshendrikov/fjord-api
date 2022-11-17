from fastapi import APIRouter

from main.api.routes import proxies, status, tasks, translation

router = APIRouter()

router.include_router(router=status.router, tags=["Status"], prefix="/status")
router.include_router(router=tasks.router, tags=["Translation Tasks"], prefix="/tasks")
router.include_router(
    router=translation.router, tags=["Translation Utils"], prefix="/utils"
)
router.include_router(router=proxies.router, tags=["Proxy Utils"], prefix="/proxies")