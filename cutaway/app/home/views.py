import aiohttp_jinja2

from app.web.app import View


class HomePage(View):
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        return {
            "telegram_link": self.request.app.config.links.telegram,
            "github_link": self.request.app.config.links.github,
            "email": self.request.app.config.links.email,
        }
