from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.database import Base
from sqlalchemy import ForeignKey
from src.user.models import Users


class Favorites(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    kinopoisk_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[Users] = relationship("Users", back_populates="favorites")
