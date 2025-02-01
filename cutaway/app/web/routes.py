import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def register_urls(application: "Application"):
    import app.admin.routes
    import app.home.routes
    import app.projects.routes

    app.home.routes.setup_routes(application)
    app.projects.routes.setup_routes(application)
    app.admin.routes.setup_routes(application)

    application.router.add_static("/static/", path="static")
