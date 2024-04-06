from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.database import get_db

from .repository import DonationRepository


def get_donation_repository(db: Session = Depends(get_db)) -> DonationRepository:
    """
    Dependency that provides a DonationRepository instance.

    This function is used with FastAPI's dependency injection system to get a DonationRepository
    instance initialized with a database session.

    Parameters
    ----------
    db : Session
        The SQLAlchemy session dependency injected by FastAPI, used to perform
        database operations.

    Returns
    -------
    DonationRepository
        An instance of DonationRepository initialized with the given database session.
    """
    return DonationRepository(db)
