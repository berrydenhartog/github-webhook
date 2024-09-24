from fastapi.testclient import TestClient


def test_middleware_security(client: TestClient) -> None:
    response = client.get(
        "/health",
    )
    assert response.headers["Strict-Transport-Security"] == "max-age=63072000"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["Content-Security-Policy"] == "default-src 'none'; frame-ancestors 'none'"
    assert response.headers["Referrer-Policy"] == "no-referrer"
