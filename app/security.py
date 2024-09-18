import hashlib
import hmac
import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def verify_signature(
    func: Callable[[Request], Awaitable[JSONResponse]],
) -> Callable[[Request], Awaitable[JSONResponse]]:
    async def wrapper(request: Request) -> JSONResponse:
        payload_body = await request.body()
        secret_token = request.app.state.secret_token
        signature_header = request.headers.get("x-hub-signature-256")

        if not signature_header:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="x-hub-signature-256 header is missing!")

        hash_object = hmac.new(secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
        expected_signature = "sha256=" + hash_object.hexdigest()

        logger.debug(f"Expected signature: {expected_signature}")
        logger.debug(f"Received signature: {signature_header}")

        if not hmac.compare_digest(expected_signature, signature_header):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request signatures didn't match!")

        return await func(request)

    return wrapper
