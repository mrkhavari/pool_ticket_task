from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.modules.task.schemas.delete import TaskDeleteOutputSchema
from app.modules.auth.models.user import User
from app.db.session import get_session
from app.modules.auth.helpers.get_current_user import get_current_user
from app.modules.task.helpers.remove_task import remove_task

router = APIRouter()


@router.delete("/{task_id}", response_model=TaskDeleteOutputSchema)
async def delete_task(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
    task_id: Annotated[str, Path()],
) -> TaskDeleteOutputSchema:
    return await remove_task(
        db=db,
        task_id=task_id,
    )
