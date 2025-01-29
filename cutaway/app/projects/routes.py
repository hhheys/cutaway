import typing

from app.projects.views import ProjectList, ProjectAdd

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(application: "Application") -> None:
    application.router.add_route("GET", "/projects", ProjectList)

    application.router.add_route("POST", "/api/projects/add", ProjectAdd)
    application.router.add_route("GET", "/api/projects/add", ProjectAdd)