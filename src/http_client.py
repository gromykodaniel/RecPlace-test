
from aiohttp import ClientSession
from src.config import settings


class HTTPclient:


    def __init__(self , api_key:str ):

        self._session = ClientSession(

            base_url = 'https://kinopoiskapiunofficial.tech/' ,
            headers={
                'X-API-KEY': api_key ,
                'Content-Type': 'application/json',
            }

        )

class cryptoHTTPclient(HTTPclient):

    async def search_movies(self , query):
        #ИЛИ МОЖНО ЧЕРЕЗ params ПЕРЕДАТЬ
        async with self._session.get(f'/api/v2.1/films/search-by-keyword?keyword={query}&page=2') as responce:

            result = await responce.json()
            return result


    async def get_details_from_id(self , id_of_movie: int ):
        async with self._session.get(f'/api/v2.2/films/{str(id_of_movie)}' ) as responce:
            result = await responce.json(content_type=None)

            return result



api_helper = cryptoHTTPclient(api_key=settings.API_KEY)