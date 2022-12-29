import os

import jinja2
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import HTMLResponse

ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(__file__), "templates")
    )
)


class HomeEndpoint(HTTPEndpoint):
    """Home Page of Fjord API"""

    async def get(self, request: Request) -> HTMLResponse:
        """Return HTML template"""

        template = ENVIRONMENT.get_template("index.html.jinja")
        content = template.render(title="Fjord API", app_url=request.url)
        return HTMLResponse(content)
