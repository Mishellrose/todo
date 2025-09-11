from typing import Optional,List

from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db
from .schemas import CreateTodo,UpdateTodo
from pydantic import BaseModel


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='todolist',
            user='postgres',
            password='youbitch',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
     print("Error connecting to the database")
     print("Error:", error)
    time.sleep(2)





@app.get("/todo")
def read_todos(db:Session=Depends(get_db)):
    todos=db.query(models.Todo).all()
    return {"data":todos}
    

@app.post("/todo")
def create_todo(todo:CreateTodo ,db: Session = Depends(get_db)):

    new_todo=models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit() 
    db.refresh(new_todo)
    return {"message": "Todo created", "todo": new_todo}




@app.delete("/todo/{id}")
def delete_todo(id: int,db: Session = Depends(get_db)):
    todos=db.query(models.Todo).filter(models.Todo.id==id)
    if todos.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id: {id} does not exist")
    todos.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/todo/{id}")
def update_todo(id: int, todo: UpdateTodo,db: Session = Depends(get_db)):
    todo_query=db.query(models.Todo).filter(models.Todo.id==id)
    todos=todo_query.first()
    if todos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id: {id} does not exist")
    todo_query.update(todo.dict(), synchronize_session=False)
    db.commit()
    return {"message": todo_query.first()}


