from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.database import get_db

from .repository import InstituteRepository


def get_institute_repository(db: Session = Depends(get_db)) -> InstituteRepository:
    """
    Dependency that provides a InstituteRepository instance.

    This function is used with FastAPI's dependency injection system to get a InstituteRepository
    instance initialized with a database session.

    Parameters
    ----------
    db : Session
        The SQLAlchemy session dependency injected by FastAPI, used to perform
        database operations.

    Returns
    -------
    InstituteRepository
        An instance of InstituteRepository initialized with the given database session.
    """
    return InstituteRepository(db)
