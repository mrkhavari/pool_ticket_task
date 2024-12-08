from typing import TypeVar, Generic, Type, Optional, Tuple, Any

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.expression import select, delete
from sqlalchemy.sql.dml import Update
from sqlalchemy.engine.result import ChunkedIteratorResult
from pydantic import BaseModel

from app.db.base_class import Base

TupleFirstType = TypeVar("TupleFirstType")
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

DB_ERROR_CODE_FOR_INSERT_DUPLICATE_DATA = 1062


def tuple_first_item(tuple_item: Tuple[TupleFirstType, Any]) -> TupleFirstType:
    return tuple_item[0]


class CRUDBase(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def get(
        self,
        obj_id: Any,
    ) -> Optional[ModelType]:
        try:
            db_obj: Optional[Tuple[ModelType, Any]] = (
                await self.db.execute(
                    select(self.model).where(self.model.id == obj_id),
                )
            ).first()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if db_obj is not None:
            return db_obj[0]
        return None

    async def create(
        self,
        *,
        obj_in: CreateSchemaType,
        autocommit: bool = True,
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj: ModelType = self.model(**obj_in_data)
        self.db.add(db_obj)
        if autocommit:
            try:
                await self.db.commit()
                await self.db.refresh(db_obj)
            except Exception as exc:
                if (
                    isinstance(exc, IntegrityError)
                    and exc.orig.args[0] == DB_ERROR_CODE_FOR_INSERT_DUPLICATE_DATA
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                    )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return db_obj

    async def get_by_clause(
        self,
        clause: Select,
    ) -> Optional[ModelType]:
        try:
            obj_iter: ChunkedIteratorResult[Tuple[ModelType, Any]] = (
                await self.db.execute(
                    clause.limit(2).offset(0),
                )
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        obj_list: list[ModelType] = list(
            map(tuple_first_item, obj_iter),
        )

        if len(obj_list) != 1:
            return None
        return obj_list[0]

    async def remove(
        self,
        *,
        obj_id: str,
        autocommit: bool = True,
    ) -> int:
        try:
            remove_result = await self.db.execute(
                delete(self.model).where(self.model.id == obj_id),
            )
            if autocommit:
                await self.db.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        count: int = remove_result.rowcount
        return count

    async def filter_by_clause(
        self,
        clause: Select,
        skip: int = 0,
        limit: int = 5,
    ) -> list[ModelType]:
        try:
            list_obj: ChunkedIteratorResult[Tuple[ModelType, Any]] = (
                await self.db.execute(
                    clause.limit(limit).offset(skip),
                )
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return list(
            map(tuple_first_item, list_obj),
        )

    async def update_by_clause(
        self,
        clause: Update,
        autocommit: bool = True,
    ) -> int:
        new_object = await self.db.execute(clause)
        if autocommit:
            try:
                await self.db.commit()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        count: int = new_object.rowcount
        return count
