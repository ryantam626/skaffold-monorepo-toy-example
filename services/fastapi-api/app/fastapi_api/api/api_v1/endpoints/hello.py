from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def hi():
    return {"message": "Hello World"}
