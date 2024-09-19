import pytest
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


@pytest.mark.parametrize(
    "client",
    [{"EVENT_FILTERS": '{"DENY": [{"FILTER": ".sender.login", "VALUE": 123}]}'}],
    indirect=True,
)
def test_dummyclient_post_with_delete_event_filterred(client: TestClient, mocker: MockerFixture) -> None:
    body = {"sender": {"login": 123}, "ref_type": "test", "ref": "test1", "repository": {"full_name": "123123"}}
    headers = {"x-github-event": "delete"}

    spy = mocker.spy(DummyClient, "handle_event")
    response = client.request("POST", "/", json=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"status": "filtered"}
    assert spy.call_count == 0
