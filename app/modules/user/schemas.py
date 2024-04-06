from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    first_name: str
    last_name: str
    cpf: str


class User(UserBase):
    id: int
    is_active: bool
    first_name: str
    last_name: str
    cpf: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    cpf: Optional[str] = None

    class Config:
        from_attributes = True
