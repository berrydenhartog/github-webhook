import pytest
from fastapi.testclient import TestClient


def test_post_with_json_body(client: TestClient) -> None:
    body = {"sender": {"login": "123"}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    headers = {"x-github-event": "delete"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204


def test_post_with_json_body_wrong(client: TestClient) -> None:
    body = {"ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    headers = {"x-github-event": "delete"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing data for event delete: 'sender'"}


def test_post_with_nonjson_body(client: TestClient) -> None:
    response = client.request("POST", "/", data=None)
    assert response.status_code == 403
    assert response.json() == {"detail": "x-hub-signature-256 header is missing!"}


def test_post_with_unkonwn_body(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "unknown"}
    response = client.request("POST", "/", json=body, headers=headers)
    assert response.status_code == 204
    assert "Unknown event" in caplog.text


def test_post_with_wrong_contenttype(client: TestClient) -> None:
    body = b"hello"
    response = client.request("POST", "/", content=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid content type"}
