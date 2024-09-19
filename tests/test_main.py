import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get(
        "/health",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


def test_nonexistent(client: TestClient):
    response = client.get("/nonexistent")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Not Found"}


def test_post_with_delete_event(client: TestClient) -> None:
    body = {"sender": {"login": "123"}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    headers = {"x-github-event": "delete"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204


def test_post_with_delete_event_wrong(client: TestClient) -> None:
    body = {"ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    headers = {"x-github-event": "delete"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing data for event delete: 'sender'"}


def test_post_with_wrong_content_type(client: TestClient) -> None:
    response = client.request("POST", "/", content="asad")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid content-type"}


def test_post_with_unknown_body(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "unknown"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204
    assert "Unknown event unknown: {'name': 'Foo', 'description': 'Some description', 'price': 5.5}" in caplog.text


def test_post_with_wrong_contenttype(client: TestClient) -> None:
    body = b"hello"
    response = client.request("POST", "/", content=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid content-type"}
