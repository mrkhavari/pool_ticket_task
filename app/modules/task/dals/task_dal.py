from typing import Optional
import uuid

from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Insert, Update

from app.db.crud_base import CRUDBase
from app.modules.task.models.task import Task
from app.modules.task.schemas.create import TaskCreateInputSchema
from app.modules.task.schemas.get import TaskGetInputSchema
from app.modules.task.schemas.update import TaskUpdateInputSchema


class TaskDAL(CRUDBase[Task]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, model=Task)

    async def get_by_title(
        self,
        title: str,
    ) -> Optional[Task]:
        select_clause: Select = select(self.model).where(
            self.model.title == title,
        )
        task: Optional[Task] = await self.get_by_clause(
            clause=select_clause,
        )
        return task

    async def create(
        self,
        obj_in: TaskCreateInputSchema,
        autocommit: bool = True,
    ) -> Task:
        task_attributes: Task = Task(
            id=str(uuid.uuid4()),
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
        )
        new_task: Task = await super().create(
            obj_in=task_attributes,
            autocommit=autocommit,
        )
        return new_task

    async def filter_by_user_query(
        self,
        obj_in: TaskGetInputSchema,
    ) -> list[Task]:
        conditions = []
        if obj_in.status:
            conditions.append(self.model.status == obj_in.status)

        if obj_in.created_at:
            initial_time = datetime.fromtimestamp(obj_in.created_at)
            conditions.append(self.model.created_at >= initial_time)

        select_clause: Select = select(self.model)

        if conditions:
            select_clause = select_clause.where(*conditions)

        select_clause = select_clause.order_by(self.model.created_at.desc())

        tasks: list[Task] = await self.filter_by_clause(
            clause=select_clause,
            skip=obj_in.skip,
            limit=obj_in.limit,
        )

        return tasks

    async def update_task(
        self,
        task_id: str,
        obj_in: TaskUpdateInputSchema,
        autocommit: bool = True,
    ) -> int:
        update_clause: Update = (
            update(self.model)
            .where(self.model.id == task_id)
            .values(obj_in.dict(exclude_unset=True))
        )
        return await self.update_by_clause(
            clause=update_clause,
            autocommit=autocommit,
        )
