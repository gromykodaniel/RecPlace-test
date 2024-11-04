import json

from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from src.database import async_session_maker
from src.http_client import api_helper
from src.movies.dao import FavoritesDAO
from src.movies.schemas import SMovieRequest, SMovieRequestDetails
from src.user.auth import get_password_hash, authenticate_user, create_access_token, get_current_user, verify_mail, \
    change_password
from src.user.dao import UserDAO
from fastapi import BackgroundTasks, FastAPI , HTTPException

from src.user.models import Users
from src.user.schemas import SUserAuth
router_movies = APIRouter(
    prefix='/movies' ,
    tags=["Логика работы с фильмами"],
)


@router_movies.post("/search/{kinopoisk_id}", status_code=200)
async def get_movies(response: Response, data:SMovieRequest):


    return await api_helper.search_movies(data.movie)

@router_movies.post("/{kinopoisk_id}",status_code=200)
async def get_details(response: Response, id:int , current_user = Depends(get_current_user) ):


    res =  await api_helper.get_details_from_id(id)
    if not res: raise HTTPException(status_code=404, detail={'Error': 'not found any movie with this Id. Please cheak another Id!'})
    print(current_user)
    return res


@router_movies.post('/favorites/',status_code=200)
async def add_to_favorite(response: Response, id : int  , current_user = Depends(get_current_user)  ):
    if_exist = await FavoritesDAO.find_one_or_none(kinopoisk_id = id , user_id = current_user['id'])
    if if_exist :raise HTTPException(status_code=404, detail={'Error': 'Already at favorites'})
    return await FavoritesDAO.add( kinopoisk_id = id , user_id = int(current_user['id']) )

@router_movies.delete('/favorites/{kinopoisk_id}',status_code=200)
async def delete_from_favorite(response: Response, id : int  , current_user = Depends(get_current_user)  ):

    return await FavoritesDAO.delete( kinopoisk_id = id , user_id = int(current_user['id']) )

@router_movies.get('/favorites/{kinopoisk_id}',status_code=200)
async def select_all_from_favorites(response: Response , current_user = Depends(get_current_user)  ):


    cur_movies = await FavoritesDAO.find_all( user_id = int(current_user['id']) )
    if not cur_movies:  raise HTTPException(status_code=404, detail={'Error': 'Nobody at favorites'})

    cur_detail_info = {}

    for i in cur_movies :

        cur : SMovieRequestDetails = i
        current_detail = await get_details( response,   id=cur)
        print(current_detail)
        if current_detail:
            cur_detail_info[i] = current_detail['nameRu']



    return cur_detail_info
