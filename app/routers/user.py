from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users():
    pass


@router.get("/{user_id}")
async def user_by_id(user_id: int):
    pass


@router.post("/create")
async def create_user():
    pass


@router.put("/{user_id}")
async def update_user(user_id: int):
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    pass
