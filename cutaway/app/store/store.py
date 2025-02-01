import typing

from app.admin.accessor import AdminAccessor
from app.projects.accessor import ProjectAccessor
from app.store.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, application):
        self.database = Database(application)

        self.project = ProjectAccessor(application)
        self.admin = AdminAccessor(application)


def setup_store(application: "Application"):
    application.store = Store(application)
