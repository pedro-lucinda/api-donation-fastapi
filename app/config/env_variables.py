"""
This script manages the loading and validation of environment variables needed
for the application.

It uses the python-dotenv package to load variables from a .env file into the
environment, and then validates that essential variables are present, raising an
error if any are missing.
"""

import os

from dotenv import load_dotenv

load_dotenv()


# Function to validate environment variables.
def validate_env_variables():
    """
    Validates that all required environment variables are set.

    This function checks for the presence of essential environment variables and
    raises an exception if any are missing, to ensure that the application
    configuration is complete before proceeding with the application startup.

    Raises
    ------
    ValueError
        If any of the required environment variables are not set.
    """

    required_env_vars = [
        "LOGGER_TOKEN",
        "DATABASE_URL",
        "ALLOWED_ORIGINS",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "GOOGLE_REDIRECT_URI",
    ]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")


# Load environment variables from .env file
LOGGER_TOKEN = os.getenv("LOGGER_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://myuser:mypass@localhost:5432/mydatabase"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")

# AUTH
# GOOGLE OAUTH
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
