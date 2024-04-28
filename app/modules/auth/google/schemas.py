from pydantic import BaseModel
from typing import Optional


class GoogleUser(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: Optional[str] = None
    picture: str
    locale: Optional[str] = None
    access_token: str

    class Config:
        from_attributes = True
