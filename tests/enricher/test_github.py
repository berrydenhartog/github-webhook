import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


@pytest.mark.parametrize("client", [{"ENRICHER_IDS": "github", "GITHUB_TOKEN": "fake"}], indirect=True)
def test_githubenricher(client: TestClient, mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
    body = {
        "sender": {"login": "asdfgsdf"},
        "action": "delete",
        "projects_v2_item": {
            "content_type": "DRAFT_ISSUE",
            "node_id": "sdfdsf",
            "content_node_id": "sdfdsf",
            "project_node_id": "1234",
        },
    }
    headers = {"x-github-event": "projects_v2_item"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "data": {"node": {"content": {"title": "asdfasdf"}, "project": {"title": "@berrydenhartog test project"}}}
    }
    mock_response.status_code = 200
    patch = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    # when
    response = client.request("POST", "/", json=body, headers=headers)

    # then
    assert response.status_code == 204
    assert patch.call_count == 1
    assert (
        caplog.records[-1].message
        == "Dummy exporter received - projects_v2_item: asdfgsdf delete DRAFT_ISSUE sdfdsf from 1234"
    )
