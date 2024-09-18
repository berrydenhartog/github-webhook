import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("client", [{"LOGGING_LEVEL": "None"}], indirect=True)
@pytest.mark.xfail
def test_logging_level(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    # given
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2"}

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
