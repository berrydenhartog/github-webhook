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


@pytest.mark.parametrize(
    "client",
    [
        {
            "EVENT_TYPE_FILTERS": '{"ALLOW": ["delete"]}',
        }
    ],
    indirect=True,
)
def test_post_with_filter_event_type_allow(client: TestClient) -> None:
    body = {"sender": {"login": "123"}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}

    response1 = client.request("POST", "/", json=body, headers={"x-github-event": "delete"})
    response2 = client.request("POST", "/", json=body, headers={"x-github-event": "delete2"})
    response3 = client.request("POST", "/", json=body, headers={"x-github-event": "delete3"})
    response4 = client.request("POST", "/", json=body, headers={"x-github-event": "delete4"})
    assert response1.status_code == 204
    assert response2.status_code == 200
    assert response2.json() == {"status": "filtered"}
    assert response3.status_code == 200
    assert response3.json() == {"status": "filtered"}
    assert response4.status_code == 200
    assert response4.json() == {"status": "filtered"}


@pytest.mark.parametrize(
    "client",
    [
        {
            "EVENT_TYPE_FILTERS": '{"DENY": ["delete"]}',
        }
    ],
    indirect=True,
)
def test_post_with_filter_event_type_deny(client: TestClient) -> None:
    body = {"sender": {"login": "123"}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}

    response1 = client.request("POST", "/", json=body, headers={"x-github-event": "delete"})
    response2 = client.request("POST", "/", json=body, headers={"x-github-event": "delete2"})
    response3 = client.request("POST", "/", json=body, headers={"x-github-event": "delete3"})
    response4 = client.request("POST", "/", json=body, headers={"x-github-event": "delete4"})
    assert response1.status_code == 200
    assert response1.json() == {"status": "filtered"}
    assert response2.status_code == 204
    assert response3.status_code == 204
    assert response4.status_code == 204
