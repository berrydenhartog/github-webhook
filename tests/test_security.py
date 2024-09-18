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
