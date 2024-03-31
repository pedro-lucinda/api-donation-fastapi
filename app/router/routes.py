"""
This module sets up the main router for the FastAPI application, aggregating
routes from different modules.

By including specific routers like `user_router`, the main router consolidates
all the routes defined in these routers, allowing them to be registered with the
FastAPI application in a centralized manner.

Attributes
----------
main_router : APIRouter
    The main router instance that aggregates routes from various modules.
"""

from fastapi import APIRouter

from app.modules.user.routes import user_router

main_router = APIRouter()

# Include your routers
main_router.include_router(user_router)
