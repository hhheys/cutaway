import os
from pathlib import Path

import aiohttp_jinja2
from aiohttp.web_response import json_response

from app.web.app import View
from aiohttp.web_exceptions import HTTPConflict, HTTPFound, HTTPNotFound

from app.web.utils import auth_required, validate_session


class ProjectList(View):
    @aiohttp_jinja2.template('projects.html')
    async def get(self):
        return {"projects": await self.request.app.store.project.get_projects(), "is_admin": await validate_session(self.request)}

class ProjectDelete(View):
    @auth_required
    async def delete(self):
        query = self.request.query
        pr_id = query.get('id')
        if pr_id is not None:
            await self.request.app.store.project.delete_project(int(pr_id))
            return json_response({})
        raise HTTPNotFound


class ProjectAdd(View):
    # {
    #     "title"
    #     "description"
    #     "image"
    #     "links":[
    #         "github":
    #     ]
    # }
    @auth_required
    @aiohttp_jinja2.template('project_add.html')
    async def get(self):
        return {}

    @auth_required
    async def post(self):
        data = await self.request.post()

        title = data['title']

        file = data["picture"].file
        filename = data["picture"].filename

        file_extension = str(Path(filename).suffix).lower()

        if not os.path.exists("static/img/cards"):
            os.mkdir("static/img/cards")

        with open(os.path.join("static/img/cards", f"{title}{file_extension}"), 'wb+') as f:
            f.write(file.read())

        res = await self.request.app.store.project.create_project(*data.values())

        if not res:
            raise HTTPConflict

        raise HTTPFound('/projects')
