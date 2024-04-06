from typing import List, Optional

from pydantic import BaseModel


class CauseBase(BaseModel):
    title: str
    description: str = None
    payment_link: str
    image_links: list[str] = []


class CreateCause(CauseBase):
    institute_id: int
    user_id: int


class UpdateCause(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    payment_link: Optional[str] = None
    image_links: Optional[list[str]] = None


class CauseSchema(CauseBase):
    id: int
    institute_id: int
    is_active: bool

    class Config:
        from_attributes = True


class CausesList(BaseModel):
    causes: List[CauseSchema]

    class Config:
        from_attributes = True
