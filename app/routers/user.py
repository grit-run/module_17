from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import User, Task
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateUser, UpdateUser

from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/create")
async def create_user(new_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(new_user.username)
    user_data = new_user.dict()
    user_data['slug'] = slug
    try:
        db.execute(insert(User).values(**user_data))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': "Successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}")
async def update_user(user_id: int, user_to_update: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user=db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.execute(update(User).where(User.id == user_id).values(**user_to_update.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': "Successful"}


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': "User ans its tasks deletion successful"}
