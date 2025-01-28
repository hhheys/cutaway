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
        db_config = self.app.config.database
        self.engine = create_async_engine(
            url=f"postgresql+asyncpg://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
        )