from fastapi import APIRouter

from app.modules.task.routes.get import router as get_router
from app.modules.task.routes.create import router as create_router
from app.modules.task.routes.update import router as update_router
from app.modules.task.routes.delete import router as delete_router

TASK_PREFIX = "/tasks"

router = APIRouter(prefix=TASK_PREFIX, tags=["Tasks"])

router.include_router(create_router)
router.include_router(get_router)
router.include_router(update_router)
router.include_router(delete_router)
