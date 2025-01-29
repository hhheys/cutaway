import typing

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.projects.models import Project
from app.web.utils import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class ProjectAccessor(BaseAccessor):
    async def create_project(self, title: str, description: str, link: str = None, github_link:str = None, *args) -> Project | None:
        if description == "":
            description = None
        if link == "":
            link = None
        if github_link == "":
            github_link = None


        pr = Project(title=title, description=description, link=link, github_link=github_link)
        async_session = async_sessionmaker(
            self.app.store.database.engine, expire_on_commit=True, class_=AsyncSession
        )
        async with async_session() as session:
            try:
                await session.merge(pr)
                await session.flush()
            except IntegrityError:
                await session.rollback()
                return None
            else:
                session.expunge_all()
                await session.commit()
                return pr
    async def get_projects(self):
        async_session = async_sessionmaker(
            self.app.store.database.engine, expire_on_commit=True, class_=AsyncSession
        )
        async_session.configure(bind=self.app.store.database.engine)
        async with async_session() as session:
            res = await session.execute(
                select(Project)
            )
            return res.scalars().all()
