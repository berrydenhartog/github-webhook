import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        response.headers["Strict-Transport-Security"] = "max-age=63072000"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["Referrer-Policy"] = "no-referrer"

        return response
