from fastapi import APIRouter

from app.modules.user.routes import user_router

main_router = APIRouter()

# Include your routers
main_router.include_router(user_router)
