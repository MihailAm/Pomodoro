from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)
    google_access_token: Mapped[Optional[str]] = mapped_column(nullable=True)
    yandex_access_token: Mapped[Optional[str]] = mapped_column(nullable=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
