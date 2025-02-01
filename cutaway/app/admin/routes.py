import typing

from app.admin.views import Auth

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(application: "Application"):
    application.router.add_route("GET", "/admin", Auth)
    application.router.add_route("POST", "/admin", Auth)
