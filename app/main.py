from fastapi import FastAPI

from app.modules.auth.main import router as auth_router
from app.modules.task.main import router as task_router


def get_application() -> FastAPI():
    application = FastAPI()
    application.include_router(auth_router)
    application.include_router(task_router)
    return application


app = get_application
