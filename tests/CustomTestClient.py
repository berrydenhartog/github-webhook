import hashlib
import hmac
from json import dumps as jsondump
from typing import Any

import httpx
from fastapi.testclient import TestClient
from starlette.testclient import _RequestData  # type: ignore
from starlette.types import ASGIApp


class CustomTestClient(TestClient):
    def __init__(self, app: ASGIApp, secret_token: str, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        super().__init__(app, *args, **kwargs)  # type: ignore
        self.secret_token = secret_token

    def request(  # type: ignore[override]
        self,
        method: str,
        url: httpx._types.URLTypes,  # type: ignore
        *,
        content: httpx._types.RequestContent | None = None,  # type: ignore
        data: _RequestData | None = None,
        files: httpx._types.RequestFiles | None = None,  # type: ignore
        json: Any = None,  # noqa: ANN401
        params: httpx._types.QueryParamTypes | None = None,  # type: ignore
        headers: dict[str, str] | None = None,  # type: ignore
        cookies: httpx._types.CookieTypes | None = None,  # type: ignore
        auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,  # type: ignore
        follow_redirects: bool | None = None,
        allow_redirects: bool | None = None,
        timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,  # type: ignore
        extensions: dict[str, Any] | None = None,
    ) -> httpx.Response:
        # Extract the payload body from the request

        if json is not None:
            payload_body = jsondump(json).encode("utf-8")

            # Calculate the hash
            hash_object = hmac.new(self.secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
            expected_signature = "sha256=" + hash_object.hexdigest()

            # Add the hash to the headers
            if headers is None:
                headers = {}

            if "x-hub-signature-256" not in headers:
                headers.update({"x-hub-signature-256": expected_signature})
        if data is not None or content is not None:
            payload_body = data if data is not None else content

            if isinstance(payload_body, bytes):
                # Calculate the hash
                hash_object = hmac.new(self.secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
                expected_signature = "sha256=" + hash_object.hexdigest()

                # Add the hash to the headers
                if headers is None:
                    headers = {}

                if "x-hub-signature-256" not in headers:
                    headers.update({"x-hub-signature-256": expected_signature})

        return super().request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            allow_redirects=allow_redirects,
            timeout=timeout,
            extensions=extensions,
        )  # type: ignore
