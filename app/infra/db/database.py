from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.env_variables import DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a local session factory, bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the declarative base class for the models to inherit from
Base = declarative_base()


# Dependency for database sessions
def get_db():
    """
    Generator that creates and provides a database session for a single request,
    then closes the session after the request is finished.

    Yields
    ------
    Session
        An instance of the database session.

    This function is intended to be used as a dependency with FastAPI's
    dependency injection system. It allows each request to have its own database
    session that is closed when the request is completed, ensuring that
    resources are properly freed.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
