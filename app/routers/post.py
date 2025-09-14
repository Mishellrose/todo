from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas
from ..database import get_db
from typing import List


router = APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=List[schemas.Post])
def read_todos(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    todos=db.query(models.Todo).all()
    return {"data":todos}
    

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_todo(todo:schemas.PostCreate ,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 
    print(current_user.id)
    new_todo=models.Todo(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit() 
    db.refresh(new_todo)
    return {"message": "Todo created", "todo": new_todo}




@router.delete("/{id}")
def delete_todo(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    todos=db.query(models.Todo).filter(models.Todo.id==id)
    if todos.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id: {id} does not exist")
    if todos.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    todos.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_todo(id: int, todo: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    todo_query=db.query(models.Todo).filter(models.Todo.id==id)
    todos=todo_query.first()
    if todos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id: {id} does not exist")
    if todos.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    todo_query.update(todo.dict(), synchronize_session=False)
    db.commit()
    return {"message": todo_query.first()}