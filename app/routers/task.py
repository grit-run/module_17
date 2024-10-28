from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Task, User
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask

from slugify import slugify

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/create")
async def create_task(new_task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    slug = slugify(new_task.title)
    new_task = Task(
        title=new_task.title,
        content=new_task.content,
        priority=new_task.priority,
        completed=False,
        user_id=user_id,
        slug=slug
    )
    db.add(new_task)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
async def update_task(task_id: int, updated_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(User.id == task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")

    db.execute(update(Task).where(Task.id == task_id).values(**updated_task.dict()))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful"}


@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion successful"}


@router.get("/{user_id}/tasks")
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found for this user")
    return tasks
