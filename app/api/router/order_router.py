from fastapi import APIRouter


router = APIRouter(tags=['Orders'],
                   prefix="/api/orders")

@router.get('/')
async def root():
    return {"msg": "hello"}