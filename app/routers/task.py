from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def all_tasks():
    pass


@router.get("/{task_id}")
async def task_by_id(task_id: int):
    pass


@router.post("/create")
async def create_task():
    pass

@router.put("/{task_id}")
async def update_task(task_id: int):
    pass


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    pass