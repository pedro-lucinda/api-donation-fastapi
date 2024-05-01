from typing import List, Optional

from pydantic import BaseModel, EmailStr
from app.modules.user.schemas import User


class CreateInstitute(BaseModel):
    """
    Schema representing the data required to create a new institute.
    """

    name: str
    email: EmailStr
    cnpj: str
    is_active: bool


class UpdateInstitute(BaseModel):
    """
    Schema representing the data required to update an institute.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cnpj: Optional[str] = None
    is_active: Optional[bool] = None


class AddAdmin(BaseModel):
    """
    Schema representing the data required to add an admin to an institute.
    """

    user_id: int
    institute_id: int


class InstituteSchema(BaseModel):
    """Schema representing the data of an institute."""

    id: int
    name: str
    email: str
    cnpj: str
    is_active: bool
    admins: List[User]

    class Config:
        from_attributes = True


class AdminsList(BaseModel):
    """Schema representing a list of admins."""

    admins: List[User]

    class Config:
        from_attributes = True
