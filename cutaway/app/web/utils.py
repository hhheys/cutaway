import typing
from functools import wraps

from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp_session import get_session
from jinja2 import Environment, PackageLoader, select_autoescape
from sqlalchemy.orm import DeclarativeBase

if typing.TYPE_CHECKING:
    from app.web.app import Application

class BaseAccessor:
    def __init__(self, app, *args, **kwargs):
        self.app: "Application" = app

class BaseModel(DeclarativeBase):
    pass

def setup_environment(application:"Application"):
    env = Environment(
        loader=PackageLoader("app"),
        autoescape=select_autoescape()
    )
    application.jinja_env = env

def auth_required(func):
    @wraps(func)
    async def inner(cls, *args, **kwargs):
        session = await get_session(cls.request)
        data = session.get("manager")
        if data:
            cls.request.userdata = data
            return await func(cls, *args, **kwargs)
        raise HTTPUnauthorized

    return inner