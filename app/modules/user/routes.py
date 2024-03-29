from fastapi import APIRouter, Depends, HTTPException

from . import schemas
from .dependencies import get_user_repository
from .repository import UserRepository

user_router = APIRouter()


@user_router.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    db_user = user_repository.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repository.create_user(user=user)


@user_router.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    user_repository: UserRepository = Depends(get_user_repository),
):
    users = user_repository.get_users(skip=skip, limit=limit)
    return users


@user_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, user_repository: UserRepository = Depends(get_user_repository)
):
    db_user = user_repository.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    return user_repository.create_user_item(item=item, user_id=user_id)


@user_router.get("/items/", response_model=list[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    user_repository: UserRepository = Depends(get_user_repository),
):
    items = user_repository.get_items(skip=skip, limit=limit)
    return items


@user_router.delete("/users/{user_id}")
def delete_user_by_id(
    user_id: int, user_repository: UserRepository = Depends(get_user_repository)
):
    user_repository.delete_user(user_id)
    return {"message": "User deleted successfully"}


@user_router.put("/users/{user_id}")
def update_user_by_id(
    user_id: int,
    user: schemas.UserUpdate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    return user_repository.update_user(user_id, user)
