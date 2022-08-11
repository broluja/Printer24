import uvicorn
import traceback
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware

from framework.exceptions.exceptions import ServerException
from framework.responses.response import ClientResponse
from framework.routing.routes import Routes
from framework.docs.auth import Documentation
from config import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger('documents-api')

app = FastAPI(debug=DEBUG, default_response_class=ClientResponse, docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key="!secret")

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(middleware_class=TrustedHostMiddleware, allowed_hosts=["*"])

security = HTTPBasic()
Documentation(app)
Routes(app)


@app.exception_handler(ServerException)
async def client_exception_handler(request: Request, exc: ServerException):
    return ORJSONResponse(
        status_code=exc.status_code if exc.status_code in [401, 400] else 200,
        content={
            "message": exc.message,
            "status_code": exc.status_code,
            "success": exc.success,
            "data": exc.data,
            "pagination": None
        }
    )


@app.middleware("http")
async def middleware(request: Request, call_next):
    try:
        start_time = datetime.now()
        response = await call_next(request)
        if DEBUG:
            ms = str(round((datetime.now() - start_time).total_seconds() * 1000, 1))
            response.headers["X-Process-Time"] = f"{ms}ms"
        return response
    except Exception as e:
        print(e)
        log = f">>> TIMESTAMP    : {datetime.now()}\n" \
              f">>> API          : API-DOCUMENTS" \
              f">>> PATH         : {str(request.scope.get('path'))}\n" \
              f">>> PATH PARAMS  : {str(request.scope.get('path_params'))}\n" \
              f">>> QUERY STRING : {str(request.scope.get('query_string'))}\n" \
              f">>> ENDPOINT     : {str(request.scope.get('endpoint').__name__)}\n" \
              f"{traceback.format_exc()}"
        if DEBUG:
            print(log)
        else:
            logger.error(log)
        return ORJSONResponse(
            status_code=400,
            content={"message": "An unknown error occurred", "status_code": 400, "success": False, "data": None}
        )


if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        workers=WORKERS,
        timeout_keep_alive=TIMEOUT_KEEP_ALIVE
    )
