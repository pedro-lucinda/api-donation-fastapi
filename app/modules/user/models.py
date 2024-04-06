from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infra.db.shared.models import TimeStampModel


class UserBase(TimeStampModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class User(UserBase):
    __tablename__ = "users"

    cpf = Column(String(length=11), unique=True, index=True)
    donations = relationship("Donation", back_populates="user")

    institute_id = Column(Integer, ForeignKey('institute.id'), nullable=True)
    institute = relationship("Institute", back_populates="admins")
