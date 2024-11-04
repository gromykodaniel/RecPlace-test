import json

from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from src.database import async_session_maker
from src.user.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    verify_mail,
    change_password,
)
from src.user.dao import UserDAO
from fastapi import BackgroundTasks, FastAPI, HTTPException

from src.user.models import Users
from src.user.schemas import SUserAuth

router_auth = APIRouter(
    tags=["Аутентификация и авторизация"],
)


@router_auth.post("/register", status_code=200)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=409, detail={"Error": "UserAlreadyExistsException"}
        )
    hashed_password = get_password_hash(user_data.password)
    a = await UserDAO.add(username=user_data.username, password=hashed_password)
    return a


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.get("/profile")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
