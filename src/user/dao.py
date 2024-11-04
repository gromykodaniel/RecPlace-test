from src.dao.base import BaseDAO
from src.user.models import Users


class UserDAO(BaseDAO):
    model = Users