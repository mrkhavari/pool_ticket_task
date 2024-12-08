from sqlalchemy import Column, String

from app.db.base_class import Base
from app.core.constant_variables import UUID_LENGTH, STRING_LENGTH_32, STRING_LENGTH_60

TABLE_NAME = "users"


class User(Base):
    __tablename__ = TABLE_NAME

    id = Column(String(UUID_LENGTH), primary_key=True, index=True)
    username = Column(String(STRING_LENGTH_32), nullable=False, unique=True, index=True)
    password = Column(String(STRING_LENGTH_60), nullable=False)
