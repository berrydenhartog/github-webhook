from app.clients.dummy import DummyClient
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


def test_dummyclient_with_projects_v2_event(client: TestClient, mocker: MockerFixture) -> None:
    # given
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2"}

    # when
    spy = mocker.spy(DummyClient, "handle_event")
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    spy.assert_called_once()
