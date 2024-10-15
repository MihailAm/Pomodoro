from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import String, Integer, ForeignKey

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    pomodoro_count: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("Categories.id"), nullable=False)


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
