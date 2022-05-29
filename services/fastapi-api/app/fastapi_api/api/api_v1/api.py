from fastapi import APIRouter

from fastapi_api.api.api_v1.endpoints import todos

api_router = APIRouter()
api_router.include_router(todos.router, tags=["TODO"], prefix="/todos")
