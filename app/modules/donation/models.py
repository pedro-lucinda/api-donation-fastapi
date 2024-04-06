from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.infra.db.shared.models import TimeStampModel


class Donation(TimeStampModel):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    is_paid = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    user = relationship("User", back_populates="donations")

    cause_id = Column(Integer, ForeignKey('causes.id'))
    cause = relationship("Cause", back_populates="donations")
