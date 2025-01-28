import typing

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.projects.accessor import BaseAccessor
if typing.TYPE_CHECKING:
    from app.web.app import Application


class Database(BaseAccessor):
    engine: AsyncEngine = None

    app: "Application" = None

    def __init__(self, app: "Application"):
        super().__init__(app)
        self.engine = create_async_engine(
            url=self.app.config.db_url
        )