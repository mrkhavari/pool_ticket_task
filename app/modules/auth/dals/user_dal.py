import uuid
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.selectable import Select

from app.db.crud_base import CRUDBase
from app.modules.auth.models.user import User
from app.modules.auth.schemas.create import UserCreateInputSchema
from app.modules.auth.helpers.get_hash_password import get_password_hash


class UserDAL(CRUDBase[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, model=User)

    async def get_by_username(
        self,
        username: str,
    ) -> Optional[User]:
        select_clause: Select = select(self.model).where(
            self.model.username == username,
        )
        user: Optional[User] = await self.get_by_clause(
            clause=select_clause,
        )
        return user

    async def create(
        self,
        obj_in: UserCreateInputSchema,
        autocommit: bool = True,
    ) -> User:
        user_attributes: User = User(
            id=str(uuid.uuid4()),
            username=obj_in.username,
            password=get_password_hash(obj_in.password),
        )
        new_user: User = await super().create(
            obj_in=user_attributes,
            autocommit=autocommit,
        )
        return new_user
