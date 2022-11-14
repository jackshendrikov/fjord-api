from fastapi import APIRouter

from main.api.routes import status, tasks

router = APIRouter()

router.include_router(router=status.router, tags=["Status"], prefix="/status")
router.include_router(router=tasks.router, tags=["Translation tasks"], prefix="/tasks")
