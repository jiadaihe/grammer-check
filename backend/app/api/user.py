from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"user_id": 1, "username": "user1"}, {"user_id": 2, "username": "user2"}]
