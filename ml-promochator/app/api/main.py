from fastapi import APIRouter

from app.api.routes import recommend, utils

api_router = APIRouter()
api_router.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])