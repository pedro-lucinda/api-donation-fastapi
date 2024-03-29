from app.infra.db.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Define the User model
class User(Base):
    __tablename__ = "users"  # The table in the database

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Define the relationship to the Item model
    items = relationship("Item", back_populates="owner")

# Define the Item model
class Item(Base):
    __tablename__ = "items"  # The table in the database

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Define the relationship to the User model
    owner = relationship("User", back_populates="items")
