from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infra.db.shared.models import TimeStampModel


class InstituteBase(TimeStampModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    cnpj = Column(String(length=14), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)


class Institute(InstituteBase):
    __tablename__ = "institute"

    causes = relationship("Cause", back_populates="institute")
    admins = relationship("User", back_populates="institute")
