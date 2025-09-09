from pydantic import BaseModel



class TodoList(BaseModel):
    id: int
    task: str
    completed: bool = False

