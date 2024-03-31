from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import declarative_base

from app.config.env_variables import ALLOWED_ORIGINS, validate_env_variables
from app.infra.db.database import engine
from app.infra.logger.config import logger
from app.infra.logger.middleware import LoggerMiddleware
from app.router.routes import main_router

# Load environment variables and validate them
load_dotenv()
validate_env_variables()

# Initialize the FastAPI application
app = FastAPI()
logger.info("Starting API...")

# Add CORS middleware to allow cross-origin requests from the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main router to add API routes to the application
app.include_router(main_router)

# Add custom LoggerMiddleware to log HTTP requests and responses
app.add_middleware(LoggerMiddleware)

# Declare the base class for the SQLAlchemy models
Base = declarative_base()


@app.on_event("startup")
def startup_event():
    """
    This function creates all database tables defined in SQLAlchemy models
    if they don't already exist, using the engine bound to our SQLAlchemy Base.
    """
    Base.metadata.create_all(bind=engine)
