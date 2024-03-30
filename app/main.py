from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import declarative_base

from app.infra.config import origins
from app.infra.db.database import engine
from app.router.routes import main_router

load_dotenv()

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(main_router)

# Create the database tables if they don't exist
Base = declarative_base()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
