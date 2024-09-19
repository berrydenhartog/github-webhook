import pytest
from app.config import Settings
from app.exceptions import MyappValidationException


def test_settings():
    settings = Settings(WEBHOOK_SECRET="dummysecret")  # noqa: S106

    assert not settings.DEBUG
    assert settings.LOGGING_LEVEL == "INFO"
    assert settings.CLIENT_IDS == ["dummy"]
    assert settings.WEBHOOK_SECRET == "dummysecret"  # noqa: S105


def test_settings_logging_level_error():
    logging_level = "DEBUGGGGG"

    with pytest.raises(MyappValidationException):
        _settings = Settings(LOGGING_LEVEL=logging_level)


def test_settings_clientid():
    settings = Settings(CLIENT_IDS="mattermost")

    assert settings.CLIENT_IDS == "mattermost"


def test_settings_clientids():
    settings = Settings(CLIENT_IDS=["mattermost", "dummy"])

    assert settings.CLIENT_IDS == ["mattermost", "dummy"]


def test_settings_event_formats():
    settings = Settings(EVENT_FORMATS={"push": "pushed {ref} in {repository[full_name]}"})
    assert settings.EVENT_FORMATS == {"push": "pushed {ref} in {repository[full_name]}"}


def test_settings_event_filters():
    settings = Settings(EVENT_FILTERS={"ALLOW": [{"FILTER": ".", "VALUE": "value"}]})
    assert settings.EVENT_FILTERS == {"ALLOW": [{"FILTER": ".", "VALUE": "value"}]}

    settings = Settings(EVENT_FILTERS={"DENY": [{"FILTER": ".myobj[]", "VALUE": 5}]})
    assert settings.EVENT_FILTERS == {"DENY": [{"FILTER": ".myobj[]", "VALUE": 5}]}


def test_settings_event_filters_allow_wrong():
    with pytest.raises(MyappValidationException):
        Settings(EVENT_FILTERS={"ALLOW": [{"FILTER": "wrong", "VALUE": "value"}]})


def test_settings_event_filters_deny_wrong():
    with pytest.raises(MyappValidationException):
        Settings(EVENT_FILTERS={"DENY": [{"FILTER": "wrong", "VALUE": "value"}]})
