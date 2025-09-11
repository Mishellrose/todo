from sqlalchemy import Column ,String,Integer,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Todo(Base):
    __tablename__ = "todolist"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, index=True, nullable=False)
    completed=Column(Boolean, default=False)
