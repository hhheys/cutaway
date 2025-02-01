from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, MappedColumn

from app.projects.models import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"

    id: Mapped[int] = MappedColumn(
        Integer(), primary_key=True, autoincrement=True
    )

    login: Mapped[str] = MappedColumn(String)
    password: Mapped[str] = MappedColumn(String)
