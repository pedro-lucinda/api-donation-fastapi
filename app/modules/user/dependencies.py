from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.database import get_db

from .repository import UserRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Dependency that provides a UserRepository instance.

    This function is used with FastAPI's dependency injection system to get a UserRepository
    instance initialized with a database session.

    Parameters
    ----------
    db : Session
        The SQLAlchemy session dependency injected by FastAPI, used to perform
        database operations.

    Returns
    -------
    UserRepository
        An instance of UserRepository initialized with the given database session.
    """
    return UserRepository(db)
