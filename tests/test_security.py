import pytest
from fastapi.testclient import TestClient


def test_security_validhash(client: TestClient) -> None:
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204


def test_security_invalidhash(client: TestClient) -> None:
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2", "x-hub-signature-256": "wronghash"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Request signatures didn't match!"}


def test_security_nosecret(client: TestClient) -> None:
    client.app.state.secret_token = None  # type: ignore
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2", "x-hub-signature-256": "wronghash"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204


@pytest.mark.parametrize("client", [{"WEBHOOK_SECRET": ""}], indirect=True)
def test_security_nosecret_env(client: TestClient) -> None:
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204


def test_security_nohash(client: TestClient) -> None:
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2", "x-hub-signature-256": ""}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "x-hub-signature-256 header is missing!"}
