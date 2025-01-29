from pathlib import Path

from aiohttp.web import run_app
from dotenv import load_dotenv

from app.web.app import setup_app

if __name__ == "__main__":
    load_dotenv()

    run_app(setup_app())