from datetime import datetime

from sqlalchemy import Column, DateTime

from app.infra.db.database import Base


class TimeStampModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
