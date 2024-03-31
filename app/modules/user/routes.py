from fastapi import APIRouter, Depends, HTTPException

from app.infra.logger.config import logger

from . import schemas
from .dependencies import get_user_repository
from .repository import UserRepository

user_router = APIRouter()


@user_router.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    """
    Create a new user with the given user data.

    Parameters
    ----------
    user : schemas.UserCreate
        The user data for creating a new user.
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    schemas.User
        The created user object.

    Raises
    ------
    HTTPException
        If the email is already registered.
    """
    db_user = user_repository.get_user_by_email(email=user.email)
    if db_user:
        logger.error("Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repository.create_user(user=user)


@user_router.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    user_repository: UserRepository = Depends(get_user_repository),
):
    """
    Retrieve a list of users, with pagination.

    Parameters
    ----------
    skip : int, optional
        The number of items to skip (default is 0).
    limit : int, optional
        The maximum number of items to return (default is 100).
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    list[schemas.User]
        A list of user objects.
    """
    users = user_repository.get_users(skip=skip, limit=limit)
    return users


@user_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, user_repository: UserRepository = Depends(get_user_repository)
):
    """
    Retrieve a user by their user ID.

    Parameters
    ----------
    user_id : int
        The ID of the user to retrieve.
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    schemas.User
        The requested user object.

    Raises
    ------
    HTTPException
        If no user with the given ID was found.
    """
    db_user = user_repository.get_user(user_id=user_id)
    if db_user is None:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    """
    Create a new item for a specified user.

    Parameters
    ----------
    user_id : int
        The ID of the user for whom to create the item.
    item : schemas.ItemCreate
        The item data for creating a new item.
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    schemas.Item
        The created item object.
    """
    return user_repository.create_user_item(item=item, user_id=user_id)


@user_router.get("/items/", response_model=list[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    user_repository: UserRepository = Depends(get_user_repository),
):
    """
    Retrieve a list of items, with pagination.

    Parameters
    ----------
    skip : int, optional
        The number of items to skip (default is 0).
    limit : int, optional
        The maximum number of items to return (default is 100).
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    list[schemas.Item]
        A list of item objects.
    """
    items = user_repository.get_items(skip=skip, limit=limit)
    return items


@user_router.delete("/users/{user_id}")
def delete_user_by_id(
    user_id: int, user_repository: UserRepository = Depends(get_user_repository)
):
    """
    Delete a user by their user ID.

    Parameters
    ----------
    user_id : int
        The ID of the user to be deleted.
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    dict
        A message indicating successful deletion.
    """
    user_repository.delete_user(user_id)
    return {"message": "User deleted successfully"}


@user_router.put("/users/{user_id}")
def update_user_by_id(
    user_id: int,
    user: schemas.UserUpdate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    """
    Update a user by their user ID.

    Parameters
    ----------
    user_id : int
        The ID of the user to update.
    user : schemas.UserUpdate
        The updated user data.
    user_repository : UserRepository
        The user repository dependency.

    Returns
    -------
    schemas.User
        The updated user object.
    """
    return user_repository.update_user(user_id, user)
