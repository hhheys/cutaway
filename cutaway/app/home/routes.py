import typing

from app.home.views import HomePage

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(application: "Application") -> None:
    application.router.add_route("GET", "/", HomePage)