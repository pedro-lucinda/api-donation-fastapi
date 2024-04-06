from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.database import get_db

from .repository import CauseRepository


def get_cause_repository(db: Session = Depends(get_db)) -> CauseRepository:
    """
    Dependency that provides a CauseRepository instance.

    This function is used with FastAPI's dependency injection system to get a CauseRepository
    instance initialized with a database session.

    Parameters
    ----------
    db : Session
        The SQLAlchemy session dependency injected by FastAPI, used to perform
        database operations.

    Returns
    -------
    CauseRepository
        An instance of CauseRepository initialized with the given database session.
    """
    return CauseRepository(db)
