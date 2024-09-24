import pytest
from app.exporter.mattermost import MattermostWebhookModel
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

TEST_URL: str = "https://httpbin.org/post"


@pytest.mark.parametrize("client", [{"EXPORTER_IDS": "mattermost", "MATTERMOST_URL": TEST_URL}], indirect=True)
def test_mattermostclient_with_projects_v2_event(client: TestClient, mocker: MockerFixture) -> None:
    # given
    body = {"sender": {"login": "asdfgsdf"}, "action": "delete", "projects_v2": {"title": "test"}}
    headers = {"x-github-event": "projects_v2"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"message": "Success"}
    mock_response.status_code = 204
    patch = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    patch.assert_called_once()


@pytest.mark.parametrize("client", [{"EXPORTER_IDS": "mattermost", "MATTERMOST_URL": TEST_URL}], indirect=True)
def test_mattermostexporter_with_projects_v2_even_failed(
    client: TestClient, mocker: MockerFixture, caplog: pytest.LogCaptureFixture
) -> None:
    # given
    body = {"sender": {"login": "asdfgsdf"}, "action": "delete", "projects_v2": {"title": "test"}}
    headers = {"x-github-event": "projects_v2"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"message": "Success"}
    mock_response.status_code = 500
    patch = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    patch.assert_called_once()
    assert "Failed to send message to Mattermost" in caplog.text


@pytest.mark.parametrize(
    "client",
    [{"EXPORTER_IDS": "mattermost", "MATTERMOST_URL": TEST_URL, "MATTERMOST_DEFAULT_CHANNEL": "test"}],
    indirect=True,
)
def test_mattermostexporter_defaultchannel(client: TestClient, mocker: MockerFixture) -> None:
    # given
    body = {"sender": {"login": "asdfgsdf"}, "action": "delete", "projects_v2": {"title": "test"}}
    headers = {"x-github-event": "projects_v2"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"message": "Success"}
    mock_response.status_code = 204
    patch = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    model = MattermostWebhookModel(text="asdfgsdf delete project_v2 test", channel="test")
    patch.assert_called_once()
    patch.assert_called_with(TEST_URL, json=model.model_dump())


@pytest.mark.parametrize(
    "client",
    [
        {
            "EXPORTER_IDS": "mattermost",
            "MATTERMOST_URL": TEST_URL,
            "MATTERMOST_DEFAULT_CHANNEL": "test",
            "MATTERMOST_EVENT_CHANNEL_MAPPING": '{"projects_v2":"test3"}',
        }
    ],
    indirect=True,
)
def test_mattermostexporter_eventchannelmapping(client: TestClient, mocker: MockerFixture) -> None:
    # given
    body = {"sender": {"login": "asdfgsdf"}, "action": "delete", "projects_v2": {"title": "test"}}
    headers = {"x-github-event": "projects_v2"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"message": "Success"}
    mock_response.status_code = 204
    patch = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    model = MattermostWebhookModel(text="asdfgsdf delete project_v2 test", channel="test3")
    patch.assert_called_once()
    patch.assert_called_with(TEST_URL, json=model.model_dump())


@pytest.mark.parametrize(
    "client",
    [
        {
            "EXPORTER_IDS": "mattermost",
            "MATTERMOST_URL": TEST_URL,
            "MATTERMOST_DEFAULT_CHANNEL": "test",
            "MATTERMOST_EVENT_CHANNEL_MAPPING": '{"NONEXISTING":"test3"}',
        }
    ],
    indirect=True,
)
@pytest.mark.xfail(raises=Exception)
def test_mattermostexporter_eventchannelmapping_wrong(client: TestClient, mocker: MockerFixture) -> None:
    # given
    body = {"name": "Foo", "description": "Some description", "price": 5.5}
    headers = {"x-github-event": "projects_v2"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"message": "Success"}
    mock_response.status_code = 204
    patch = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    model = MattermostWebhookModel(text=" ", channel="test3")
    patch.assert_called_once()
    patch.assert_called_with(TEST_URL, json=model.model_dump())
