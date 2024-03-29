from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

# Import the engine from your database configuration module
from app.infra.db.database import engine

# Import your aggregated models
from app.infra.db.models import *

# Import routers from your modules
from app.modules.user.routes import user_router

# Create the FastAPI application instance
app = FastAPI()

# Include your routers
app.include_router(user_router)

# Create the database tables if they don't exist
Base = declarative_base()

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
