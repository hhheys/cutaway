import aiohttp_jinja2
import jinja2
from aiohttp.web import Application as AiohttpApplication
from aiohttp.web import Request as AiohttpRequest
from aiohttp.web import View as AiohttpView
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from jinja2 import Environment

from app.store.store import Store, setup_store
from app.web.config import Config, setup_config
from app.web.routes import register_urls


class Application(AiohttpApplication):
    db = None
    store: Store = None
    config: Config = None
    jinja_env: Environment = None

class Request(AiohttpRequest):
    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request


app = Application()

def setup_app():
    register_urls(app)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('./templates'))
    setup_config(app)
    setup_store(app)
    setup(app,
          EncryptedCookieStorage(b'Thirty  two  length  bytes  key.'))
    return app