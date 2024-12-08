from fastapi import APIRouter

from app.modules.auth.routes.create import router as create_router
from app.modules.auth.routes.login import router as login_router


AUTH_PREFIX = "/auth"

router = APIRouter(prefix=AUTH_PREFIX, tags=["Authentication"])

router.include_router(create_router)
router.include_router(login_router)
