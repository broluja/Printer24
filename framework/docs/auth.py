from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import Depends, Response, Request
from fastapi.responses import ORJSONResponse
from fastapi.openapi.utils import get_openapi

from framework.docs.metadata import OpenAPIMetadata
from framework.middleware.authentication import BasicAuth, SuperAdmin


class Documentation:

    def __init__(self, app):
        self.user = None
        self.load(app)

    def show_auth_dialog(self) -> Response:
        return Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)

    def load(self, app):
        @app.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html(request: Request):
            return get_swagger_ui_html(openapi_url="/openapi.json", title="Docs")

        @app.get("/openapi.json", include_in_schema=False, dependencies=[Depends(SuperAdmin)])
        async def get_open_api_endpoint():
            return ORJSONResponse(get_openapi(
                title="PRINTER24 API",
                version="1.0.0",
                routes=app.routes,
                description=OpenAPIMetadata.description,
                tags=OpenAPIMetadata.tags_metadata
            ))

        @app.get("/docs/login", include_in_schema=False)
        async def docs_auth(auth: BasicAuth = Depends(BasicAuth(auto_error=False))):
            if not auth:
                response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
                return response

    def validate(self, token):
        pass
