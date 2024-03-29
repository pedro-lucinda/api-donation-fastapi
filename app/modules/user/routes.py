from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from . import repository, schemas
from app.infra.db.database import get_db

user_router = APIRouter()

@user_router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return repository.create_user(db=db, user=user)


@user_router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = repository.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return repository.create_user_item(db=db, item=item, user_id=user_id)


@user_router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = repository.get_items(db, skip=skip, limit=limit)
    return items


@user_router.delete("/users/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    repository.delete_user(db, user_id)
    return {"message": "User deleted successfully"}


@user_router.put("/users/{user_id}")
def update_user_by_id(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return repository.update_user(db, user_id, user)