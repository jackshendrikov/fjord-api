from fastapi import APIRouter

from main.api.routes import status

router = APIRouter()

router.include_router(router=status.router, tags=["Status"], prefix="/status")
