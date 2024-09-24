import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, Response

from .config import get_settings
from .constants import DEFAULT_EVENT_FORMATS
from .enricher import enricher_factory
from .eventhandlers import (
    DEFAULT_EVENT_HANDLERS,
    handle_enrich_event,
    handle_filter_event,
    handle_filter_event_type,
    handle_format_event,
    handle_unknown_event,
)
from .exporter import exporter_factory
from .log import setup_logging
from .middleware.security import SecurityMiddleware
from .security import verify_signature

VERSION = "dev"


def create_app() -> FastAPI:
    settings = get_settings()  # type: ignore[reportCallIssue]

    setup_logging(settings.LOGGING_LEVEL)
    logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        app.state.secret_token = settings.WEBHOOK_SECRET
        app.state.exporters = exporter_factory(settings.EXPORTER_IDS)
        app.state.enrichers = enricher_factory(settings.ENRICHER_IDS)
        app.state.event_header = settings.EVENT_HEADER
        app.state.event_formats = DEFAULT_EVENT_FORMATS | settings.EVENT_FORMATS
        app.state.event_filters = settings.EVENT_FILTERS
        app.state.event_type_filters = settings.EVENT_TYPE_FILTERS

        if not app.state.secret_token:
            logger.warning("Webhook secret disabled. This is unsafe!")

        logger.info(f"Version:       {VERSION}")
        logger.info(f"Debug:         {settings.DEBUG}")
        logger.info(f"Logging level: {settings.LOGGING_LEVEL}")
        logger.info(f"Enricher IDs:    {settings.ENRICHER_IDS}")
        logger.info(f"Exporter IDs:    {settings.EXPORTER_IDS}")
        logger.info(f"Event header:  {settings.EVENT_HEADER}")
        logger.info(f"Event Filter Allow :  {len(settings.EVENT_FILTERS.get('ALLOW', []))}")
        logger.info(f"Event Filter Deny :  {len(settings.EVENT_FILTERS.get('DENY', []))}")
        logger.info(f"Event Filter Type Allow :  {len(settings.EVENT_TYPE_FILTERS.get('ALLOW', []))}")
        logger.info(f"Event Filter Type Deny :  {len(settings.EVENT_TYPE_FILTERS.get('DENY', []))}")
        yield
        logger.info("Closing app")

    app = FastAPI(lifespan=lifespan, openapi_url=None, debug=settings.DEBUG)

    app.add_middleware(SecurityMiddleware)

    @app.post("/", status_code=status.HTTP_204_NO_CONTENT)
    @verify_signature
    async def webhook(request: Request) -> Response:  # type: ignore
        event_type = request.headers.get(app.state.event_header, "unknown")
        content_type = request.headers.get("content-type")

        logger.debug(f"Received event-type: {event_type}")
        logger.debug(f"Received content-type: {content_type}")

        if content_type != "application/json":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid content-type")

        json_data: dict[str, Any] = await request.json()

        logger.debug(f"request data: {json_data}")

        filter_type = await handle_filter_event_type(event_type, app.state.event_type_filters)
        if filter_type:
            logger.debug(f"Event type {event_type} filtered out")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "filtered"})

        filter = await handle_filter_event(event_type, app.state.event_filters, json_data)
        if filter:
            logger.debug(f"Event {event_type} filtered out")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "filtered"})

        json_data = await handle_enrich_event(event_type, app.state.enrichers, json_data)

        msg = await handle_format_event(event_type, app.state.event_formats, json_data)

        handler = DEFAULT_EVENT_HANDLERS.get(event_type, handle_unknown_event)
        await handler(event_type, app.state.exporters, msg)

    @app.get("/health", status_code=status.HTTP_200_OK)
    async def health() -> Response:  # type: ignore
        return JSONResponse(content={"status": "ok"})

    return app


app = create_app()
