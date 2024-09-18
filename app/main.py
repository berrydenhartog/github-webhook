import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from .clients import client_factory
from .config import get_settings
from .github import DEFAULT_EVENT_HANDLERS, handle_unknown_event
from .log import setup_logging
from .security import verify_signature

VERSION = "dev"


def create_app() -> FastAPI:
    settings = get_settings()  # type: ignore[reportCallIssue]

    setup_logging(settings.LOGGING_LEVEL)
    logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        logger.info(f"Application {VERSION} starting")
        logger.info(f"Debug mode: {settings.DEBUG}")
        logger.info(f"Logging level: {settings.LOGGING_LEVEL}")
        logger.info(f"Client id: {settings.CLIENT_ID}")
        yield
        logger.info(f"Application {VERSION} closing")

    app = FastAPI(lifespan=lifespan, openapi_url=None, debug=settings.DEBUG)
    app.state.secret_token = settings.GITHUB_WEBHOOK_SECRET
    app.state.client = client_factory(settings.CLIENT_ID, str(settings.CLIENT_URL))

    @app.post("/", status_code=status.HTTP_204_NO_CONTENT)
    @verify_signature
    async def github_webhook(request: Request) -> JSONResponse:  # type: ignore
        github_event = request.headers.get("x-github-event", "unknown")
        content_type = request.headers.get("content-type")

        logger.debug(f"Received event {github_event}")
        logger.debug(f"Received contenttype {content_type}")

        if content_type != "application/json":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid content type")

        json_data = await request.json()

        logger.debug(f"request data: {json_data}")

        handler = DEFAULT_EVENT_HANDLERS.get(github_event, handle_unknown_event)
        await handler(github_event, app.state.client, json_data)

    @app.get("/health")
    async def health_check() -> JSONResponse:  # type: ignore
        return JSONResponse(
            content={"status": "ok"},
        )

    return app


app = create_app()
