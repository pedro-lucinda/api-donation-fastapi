from fastapi import APIRouter, Depends, HTTPException

from app.infra.logger.config import logger
from app.modules.auth.dependecies import get_current_user
from . import schemas
from .dependencies import get_user_repository
from .repository import UserRepository

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/", response_model=list[schemas.User])
def list_users(
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
    try:
        users = user_repository.get_users(skip=skip, limit=limit)
        logger.info("Users fetched successfully")
        return users
    except Exception as e:
        logger.error("Error fetching users")
        raise HTTPException(status_code=500, detail=str(e)) from e


@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, user_repository: UserRepository = Depends(get_user_repository)):
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
    try:
        user = user_repository.get_user_by_id(user_id=user_id)
        if not user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.error("Error fetching user %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@user_router.put("/{user_id}")
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
    try:
        updated_user = user_repository.update_user(user_id=user_id, user_update=user)
        logger.info("User updated successfully %s", updated_user.id)
        return updated_user
    except Exception as e:
        logger.error("Error updating user %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@user_router.get("/data/me", response_model=schemas.User)
def read_current_user(user: schemas.User = Depends(get_current_user)):
    """
    Retrieve the current user.

    Parameters
    ----------
    user : schemas.User
        The current user.

    Returns
    -------
    schemas.User
        The current user object.
    """
    return user
