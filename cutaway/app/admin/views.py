import hashlib

import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPConflict, HTTPFound
from aiohttp.web_response import json_response
from aiohttp_session import get_session, new_session

from app.web.app import View


class Auth(View):
    @aiohttp_jinja2.template('auth.html')
    async def get(self):
        return

    async def post(self):
        data = await self.request.post()
        login = data['login']
        password = data['password']
        data = await self.request.app.store.admin.validate_admin(login, password)
        if data:
            session = await new_session(request=self.request)
            session["manager"] = "asd"
            raise HTTPFound('/')
        else:
            raise HTTPConflict
        # return json_response({'login': login, 'password': password, 'valid': True if await self.request.app.store.admin.validate_admin(login, password) else False})
        # session = await new_session(request=self.request)
        # session["manager"] = "asd"