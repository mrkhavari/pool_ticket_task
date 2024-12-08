from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.sql.functions import func

from app.modules.task.schemas.task_status import TaskStatus
from app.db.base_class import Base
from app.core.constant_variables import UUID_LENGTH, STRING_LENGTH_32, STRING_LENGTH_60


TABLE_NAME = "tasks"


class Task(Base):
    __tablename__ = TABLE_NAME

    id = Column(String(UUID_LENGTH), primary_key=True, index=True)
    title = Column(String(STRING_LENGTH_32), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
