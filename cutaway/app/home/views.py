from urllib import response

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_response import json_response
from jinja2 import Template

from app.web.app import View


class HomePage(View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {
            'telegram_link':self.request.app.config.links.telegram,
            'github_link': self.request.app.config.links.github,
            'email': self.request.app.config.links.email,
        }