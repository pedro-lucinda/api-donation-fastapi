from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infra.db.shared.models import TimeStampModel


class Cause(TimeStampModel):
    __tablename__ = "causes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_links = Column(JSON, default=[])
    payment_link = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    donations = relationship("Donation", back_populates="cause")
    institute_id = Column(Integer, ForeignKey('institute.id'))
    institute = relationship("Institute", back_populates="causes")
