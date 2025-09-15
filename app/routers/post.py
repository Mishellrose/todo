from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session


from .. import models, schemas,oauth2
from ..database import get_db
from typing import List


router = APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=list[schemas.Post])
def read_todos(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    todos=db.query(models.Todo).all()
    return todos

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_todo(todo:schemas.PostCreate ,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 
    print(current_user.id)
    new_todo=models.Todo( owner_id=current_user.id,**todo.dict())
    db.add(new_todo)
    db.commit() 
    db.refresh(new_todo)
    return new_todo


@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT * FROM posts WHERE id=%s """,str(id),)
    #get_new_post=cursor.fetchone()

    post=db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return post





@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    todos_query=db.query(models.Todo).filter(models.Todo.id==id)
    todos=todos_query.first()
    if todos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id: {id} does not exist")
    if todos.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    todos_query.delete(synchronize_session=False)
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