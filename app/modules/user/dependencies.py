from fastapi import Depends
from sqlalchemy.orm import Session
from app.infra.db.database import get_db
from .repository import UserRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
