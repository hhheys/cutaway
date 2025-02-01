import os
import typing

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.projects.models import Project
from app.web.utils import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class ProjectAccessor(BaseAccessor):
    async def create_project(
            self,
            title: str,
            description: str,
            image_filename: str,
            link: str = None,
            github_link:str = None,
            order:int = 0,
            *args
    ) -> Project | None:

        description = None if description == "" else description
        link = None if link == "" else link
        github_link = None if github_link == "" else github_link

        async_session = async_sessionmaker(
            self.app.store.database.engine, expire_on_commit=True, class_=AsyncSession
        )
        pr = Project(title=title, description=description, link=link, github_link=github_link, order=order,
                     image_filename=image_filename)
        async with async_session() as session:
            try:
                data = await session.execute(select(Project).where(Project.order == order))
                if data:
                    await session.execute(update(Project).where(Project.order >= order).values(
                    order=Project.order + 1
                ))
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
            data = res.scalars().all()
            return sorted(data, key=lambda p: p.order)

    async def delete_project(self, pr_id: int):
        async_session = async_sessionmaker(
            self.app.store.database.engine, expire_on_commit=True, class_=AsyncSession
        )
        async with async_session() as session:
            try:
                result = await session.execute(select(Project).where(Project.id == pr_id))
                pr = result.scalars().first()
                if pr is not None:
                    try:
                        os.remove(f"static/img/cards/{pr.image_filename}")
                    except FileNotFoundError:
                        pass
                    await session.delete(pr)
                    await session.execute(update(Project).where(Project.order >= pr.order).values(
                        order=Project.order - 1
                    ))
                await session.commit()
            except IntegrityError:
                print("err")