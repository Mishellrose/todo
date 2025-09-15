from sqlalchemy import Column ,String,Integer,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class Todo(Base):
    __tablename__ = "todolist"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, index=True, nullable=False)
    completed=Column(Boolean, default=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner=relationship("User")


class User(Base):
    __tablename__ ="users"
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
