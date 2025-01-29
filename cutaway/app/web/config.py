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
class Config:
    links: LinkConfig = None
    db_url: str = None

def setup_config(application: "Application"):
    with open("config.yaml", "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    application.config = Config(
        links = LinkConfig(**raw_config["links"]),
        db_url = os.environ.get('DATABASE_URL'),
    )
