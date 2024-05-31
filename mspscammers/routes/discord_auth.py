import aiofiles
from typing import Dict
from blacksheep import Application, Request
from blacksheep.server.responses import html, redirect
from urllib.parse import quote_plus

class TemplateCache:
    """
    A simple template cache for reading HTML templates asynchronously.
    """

    _cache: Dict[str, str]

    def __init__(self):
        """
        Initializes the TemplateCache.
        """
        self._cache = {}

    async def read_template(self, file_name: str) -> str:
        """
        Reads an HTML template from the file system asynchronously,
        caching it for subsequent reads.

        Args:
            file_name (str): The name of the HTML template file.

        Returns:
            str: The content of the HTML template.
        """
        if file_name not in self._cache:
            async with aiofiles.open(f"./templates/{file_name}", "r", encoding="utf-8") as file:
                self._cache[file_name] = await file.read()
        return self._cache[file_name]


def register_discord_routes(app: Application) -> None:
    """
    Registers Discord routes with the given BlackSheep Application.

    Args:
        app (Application): The BlackSheep Application instance.
    """
    app.router.add_get("/discord/connect", connect)
    app.router.add_get("/discord/app/login", login)

cache = TemplateCache()

async def connect(request: Request) -> html:
    """
    Handles requests to the /discord/connect route by rendering the discordlogin.html template.

    Args:
        request (Request): The HTTP request.

    Returns:
        html: The rendered HTML response.
    """
    return html(await cache.read_template(file_name="discordlogin.html"))

async def login(request: Request) -> redirect:
    CLIENT_ID = "1200476142554062941"
    REDIRECT_URI = "https://msp-scammers.fr/discord/callback"
    SCOPE = "identify"
    RESPONSE_TYPE = "code"
    
    authorization_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={quote_plus(REDIRECT_URI)}"
        f"&response_type={RESPONSE_TYPE}"
        f"&scope={SCOPE}"
    )

    return redirect(authorization_url)
