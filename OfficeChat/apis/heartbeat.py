from fastapi import APIRouter,Depends

router = APIRouter()


@router.get("/beat")
async def beat():
    return True
