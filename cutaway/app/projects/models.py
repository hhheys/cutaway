from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.web.utils import BaseModel


class Project(BaseModel):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String(), nullable=True)
    link: Mapped[str] = mapped_column(String(), nullable=True)
    github_link: Mapped[str] = mapped_column(String(), nullable=True)

