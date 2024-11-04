from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.movies.models import Favorites
from sqlalchemy import delete, insert, select

class FavoritesDAO(BaseDAO):
    model = Favorites

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.kinopoisk_id).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()