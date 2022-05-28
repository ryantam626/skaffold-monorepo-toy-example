from fastapi import APIRouter

from fastapi_api.api.api_v1.endpoints import hello

api_router = APIRouter()
api_router.include_router(hello.router, tags=["hello"])
