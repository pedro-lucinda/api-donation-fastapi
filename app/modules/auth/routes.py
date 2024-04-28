from fastapi import APIRouter, Depends, HTTPException, status
from requests.exceptions import RequestException
from jose.exceptions import JWTError
from pydantic import ValidationError

from app.infra.logger.config import logger
from app.modules.user.dependencies import get_user_repository
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate
from .dependecies import get_google_oauth
from .google.google_oauth import GoogleOAuth

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.get("/google/login")
def login_google(google_oauth: GoogleOAuth = Depends(get_google_oauth)):
    """
    Initiates a login request using Google OAuth. Redirects user to Google's login page.

    Args:
        google_oauth (GoogleOAuth): The GoogleOAuth dependency to handle OAuth operations.

    Returns:
        A URL to initiate OAuth login via Google.
    """
    return google_oauth.login_google()


@auth_router.get("/google/callback")
def auth_google(
    code: str,
    google_oauth: GoogleOAuth = Depends(get_google_oauth),
    user_repository: UserRepository = Depends(get_user_repository),
):
    try:
        user_info = google_oauth.auth_google(code)
        if not user_info.email:
            raise HTTPException(status_code=400, detail="Email not provided in Google data")

        db_user = user_repository.get_user_by_email(email=user_info.email)
        if db_user:
            return {
                "user": db_user,
                "access_token": user_info.access_token,
            }

        user_obj = {
            "email": user_info.email,
            "first_name": user_info.given_name,
            "last_name": user_info.family_name or "",
            "picture": user_info.picture or "",
            "locale": user_info.locale or "",
        }
        created_user = user_repository.create_user(user=UserCreate(**user_obj))
        return {
            "user": created_user,
            "access_token": user_info.access_token,
        }
    except ValidationError as ve:
        logger.error("Validation error for GoogleUser: %s", ve)
        raise HTTPException(status_code=400, detail=f"Invalid user data: {ve.errors()}") from ve
    except RequestException as e:
        logger.error("Network-related error during Google authentication: %s", e)
        raise HTTPException(status_code=503, detail="Service unavailable") from e
    except Exception as e:
        logger.error("Unexpected error in auth_google:  %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@auth_router.get("/google/token")
def get_token(token: str, google_oauth: GoogleOAuth = Depends(get_google_oauth)):
    """
    Decodes the provided JWT token to extract the user's information stored within.

    Args:
        token (str): The JWT token to decode.
        google_oauth (GoogleOAuth): The GoogleOAuth dependency to handle OAuth operations.

    Returns:
        The decoded information from the JWT token.
    """
    try:
        return google_oauth.get_token(token)
    except JWTError as e:
        logger.error("Error decoding token: %s, token = %s", e, token)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        ) from e
    except ValueError as e:
        logger.error("Value error with token: %s, token = %s", e, token)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        ) from e
