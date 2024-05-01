from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session

from app.infra.db.database import get_db
from app.modules.user.repository import UserRepository
from app.infra.logger.config import logger

from .google.google_oauth import GoogleOAuth


def get_google_oauth() -> GoogleOAuth:
    """
    Dependency that provides a GoogleOAuth instance.

    This function is used with FastAPI's dependency injection system to get a GoogleOAuth

    Returns
    -------
    GoogleOAuth
        An instance of GoogleOAuth.
    """
    return GoogleOAuth()


def get_current_user(token: str = Header(None), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Decode the token to get user details
    user_details = GoogleOAuth().get_token(token)
    if not token:
        logger.error("No token provided")
        raise HTTPException(status_code=401, detail="Unauthorized")

    if token.startswith("Bearer "):
        token = token[7:]
        logger.debug("Token after removing Bearer: %s", token)

    if not user_details:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = user_details.get('email')
    if not email:
        raise HTTPException(status_code=401, detail="Token does not include email")

    # Fetch user from database
    user_repo = UserRepository(db)
    usr = user_repo.get_user_by_email(email)
    if not usr:
        raise HTTPException(status_code=404, detail="usr not found")

    return usr
