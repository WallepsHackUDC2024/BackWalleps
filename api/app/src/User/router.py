from typing import List, Union
from fastapi import Depends, Response, APIRouter
from sqlalchemy.orm import Session

from database import get_db

import src.User.service as user_service

from src.User.model import User as ModelUser

from src.User.schema import UserGet as UserGetSchema
from src.User.schema import UserGetAll as UserGetAllSchema
from src.User.schema import UserCreate as UserCreateSchema
from src.User.schema import UserUpdate as UserUpdateSchema



router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/signup")
def signup(payload: UserCreateSchema,
                 db: Session = Depends(get_db)):
    new_user = user_service.add_user(payload, db)

    # return new_user

    return {
        "success": True,
        "user_id": new_user.id
    }


@router.get("/all", response_model=List[UserGetSchema])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all(db)


@router.get("/{userId}", response_model=Union[UserGetSchema, UserGetAllSchema])
def get_user(userId: int,
                     db: Session = Depends(get_db)):
    return user_service.get_user(userId, db)


@router.put("/{userId}")
def update_user(userId: int,
                        payload: UserUpdateSchema,
                        db: Session = Depends(get_db)):
    user, updated = user_service.update_user(
        userId, payload, db)
    return {"success": True, "updated_id": user.id, "updated": updated}


@router.delete("/{userId}")
def delete_user(userId: int,
                        db: Session = Depends(get_db)):
    user = user_service.remove_user(userId, db)
    return {"success": True, "deleted_id": user.id}
    # return user


@router.get("/scheduler/{userId}")
def get_scheduler(userId: int,
                         db: Session = Depends(get_db)):
    return user_service.get_scheduler(userId, db)