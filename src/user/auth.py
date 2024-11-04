from datetime import datetime, timedelta

from  passlib.hash import bcrypt
from fastapi.exceptions import HTTPException
from fastapi import Request
from sqlalchemy import update

from src.config import settings
from src.database import async_session_maker
from src.user.dao import UserDAO
from jose import jwt

from src.user.models import Users

def get_password_hash(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

async def verify_mail(code: int  , mail :  str  ):
    current = await UserDAO.read(gmail=mail)



    if not current or current['code'] == 1 :
        raise HTTPException(status_code=401 , detail='user already veryfied or never exists')
    if current['code'] != code:
        raise HTTPException(status_code=405, detail='Wrong code')
    try:

        async with async_session_maker() as session:

            query = update(Users).where(Users.gmail == mail).values(code=1)
            res = await session.execute(query)
            await session.commit()
            return res.mappings()
    except():
        return {'Error': 'Cannot update data into table'}

async def change_password(code: int  , mail :  str , new_password  ):
    current = await UserDAO.read(gmail=mail)

    #if not current or current['code'] == 1:
    #    raise HTTPException(status_code=401, detail='user already veryfied or never exists')
    if current['code'] != code:
        raise HTTPException(status_code=405, detail='Wrong code')
    try:

        password = get_password_hash(new_password)
        async with async_session_maker() as session:

            query = update(Users).where(Users.gmail == mail).values( code=1 , password=password)
            res = await session.execute(query)
            await session.commit()
            return res.mappings()
    except():
        return {'Error': 'Cannot update data into table'}



async def authenticate_user(username : str , password : str):

    current = await UserDAO.find_one_or_none(username=username)
    if not current or not verify_password(password , current.password) :
        raise HTTPException(status_code=404)
    return current

def create_access_token(data : dict) -> str:

    to_copy = data.copy()
    expire_data = datetime.utcnow() + timedelta(1440)
    to_copy.update({"exp": expire_data})

    jwtt = jwt.encode(
        to_copy , settings.SECRET_KEY , settings.ALGORITHM
    )
    return jwtt

async def get_current_user(request: Request):

    token = request.cookies.get('booking_access_token')
    if  token is None:  raise HTTPException(status_code= 404, detail={'отсутствует токен'}) from None

    try:
        decoded_token = jwt.decode(
            token , settings.SECRET_KEY , settings.ALGORITHM
        )
    except:
        raise HTTPException(status_code=403 , detail={'инвалидный токен'})

    user_id = decoded_token.get('sub')
    if not  user_id: raise HTTPException(status_code=401  , detail={'отсутствует  такой пользователь'} )

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user: raise HTTPException(status_code=403 ,  detail={'инвалидный пользователь'} )
    return user
