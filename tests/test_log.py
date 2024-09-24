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


@pytest.mark.parametrize("client", [{"LOGGING_LEVEL": "DEBUG"}], indirect=True)
def test_logging_level_debug(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    # given
    body = {"sender": {"login": "asdfgsdf"}, "action": "delete", "projects_v2": {"title": "test"}}
    headers = {"x-github-event": "projects_v2"}

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    assert len(caplog.records) == 8
    assert caplog.records[0].name == "app.security"
    assert caplog.records[1].name == "app.security"
    assert caplog.records[2].name == "app.main"
    assert caplog.records[3].name == "app.main"
    assert caplog.records[4].name == "app.main"
    assert caplog.records[5].name == "app.eventhandlers"
    assert caplog.records[6].name == "app.eventhandlers"
    assert caplog.records[7].name == "app.exporter.dummy"
