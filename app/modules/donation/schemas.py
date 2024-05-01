from typing import Optional

from pydantic import BaseModel


class CreateDonation(BaseModel):
    cause_id: int


class UpdateDonation(BaseModel):
    is_paid: bool


class Donation(BaseModel):
    id: int
    is_paid: bool
    user_id: int
    cause_id: int

    class Config:
        from_attributes = True
