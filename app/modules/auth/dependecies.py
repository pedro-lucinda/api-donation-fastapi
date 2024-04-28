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
