from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from app.infra.db.database import engine
from app.infra.db.models import *
from app.modules.user.routes import user_router

load_dotenv()

# Create the FastAPI app
app = FastAPI()

# Include your routers
app.include_router(user_router)

# Create the database tables if they don't exist
Base = declarative_base()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
