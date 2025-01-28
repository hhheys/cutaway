import os
import typing
from dataclasses import dataclass
from multiprocessing.spawn import set_executable

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class LinkConfig:
    telegram: str = None
    github: str = None
    email: str = None

@dataclass
class DatabaseConfig:
    user: str = None
    password: str = None
    host: str = None
    port: int = None
    database: str = None


@dataclass
class Config:
    links: LinkConfig = None
    database: DatabaseConfig = None

def setup_config(application: "Application"):
    with open("config.yaml", "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    username = os.environ.get('DB_USER')
    secret = os.environ.get('DB_SECRET')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    database = os.environ.get('DB_NAME')


    a = {"user":username, "password":secret, "host":host, "port":port, "database":database}

    application.config = Config(
        links = LinkConfig(**raw_config["links"]),
        database = DatabaseConfig(**a)
    )
