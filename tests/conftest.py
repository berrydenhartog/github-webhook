from collections.abc import Generator

import pytest
from app.main import create_app
from fastapi.testclient import TestClient

from .CustomTestClient import CustomTestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> Generator[TestClient, None, None]:
    secret_token = "dummysecret"  # noqa: S105
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", secret_token)

    if hasattr(request, "param"):
        for key, value in request.param.items():
            monkeypatch.setenv(key, value)

    app = create_app()

    # tofo: add custom test client to handle special headers
    with CustomTestClient(app, secret_token, raise_server_exceptions=True) as c:  # type: ignore
        c.timeout = 2
        yield c
