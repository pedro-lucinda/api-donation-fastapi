from fastapi.security import OAuth2PasswordBearer
import requests
from app.config.env_variables import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from .schemas import GoogleUser


class GoogleOAuth:
    """
    Handles OAuth2 operations for Google authentication.
    """

    def __init__(self):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.client_id = GOOGLE_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.redirect_uri = GOOGLE_REDIRECT_URI
        self.login_url = (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&scope=openid%20profile%20email&access_type=offline"
        )
        self.token_url = "https://accounts.google.com/o/oauth2/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        self.user_token = "https://www.googleapis.com/oauth2/v3/tokeninfo"

    def login_google(self) -> dict:
        """
        Generates a URL to initiate Google OAuth2 login process.

        Returns:
            dict: A dictionary containing the URL to redirect the user for Google login.
        """
        return {"url": self.login_url}

    def auth_google(self, code: str) -> GoogleUser:
        """
        Handles the authentication of the user with Google using the code received from Google
        after user consent.

        Args:
            code (str): The authorization code received from Google.

        Returns:
            dict: A dictionary containing user information after successful authentication.
        """
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.token_url, data=data, timeout=100)
        access_token = response.json().get("access_token")
        return self.get_user_info(access_token)

    def get_user_info(self, access_token: str) -> dict:
        """
        Retrieves user information from Google using the access token.

        Args:
            access_token (str): Access token provided by Google.

        Returns:
            dict: A dictionary containing the user's information.
        """
        response = requests.get(
            self.user_info_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=100
        )
        info = response.json()
        data = {**info, "access_token": access_token}
        return GoogleUser(**data)

    def get_token(self, token: str) -> dict:
        """
        Decodes a JWT token using the application's secret.
        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token.
        """

        response = requests.get(
            self.user_info_url, headers={"Authorization": f"Bearer {token}"}, timeout=100
        )
        info = response.json()
        return info
