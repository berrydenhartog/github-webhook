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
