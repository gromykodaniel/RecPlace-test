from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="user"
    )

    def __str__(self):
        return f"Пользователь {self.username}"


# Users.favorites = relationship("Favorites", back_populates="user", cascade="all, delete-orphan")
