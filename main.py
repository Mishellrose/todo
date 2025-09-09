

from fastapi import Body, FastAPI

from app.models import TodoList

app = FastAPI()

@app.get("/todos")
def read_todos():
    return {"todos": [{"id": 1, "task": "Task 1", "completed": False},
                      {"id": 2, "task": "Task 2", "completed": False},
                      {"id": 3, "task": "Task 3", "completed": False}]}


@app.post("/todos")
def create_todo(todo: TodoList):

    return {"message": "Todo created", "todo": todo}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoList):
    print(todo)
    return {"message": f"Todo {todo_id} updated", "todo": todo}



@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    print(f"Todo {todo_id} deleted")
    return {"message": f"Todo {todo_id} deleted"}

