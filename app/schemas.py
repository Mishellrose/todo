from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateTodo(BaseModel):
    title: str
    completed: bool = False

class UpdateTodo(BaseModel):
    title: Optional[str]
    completed: Optional[bool]