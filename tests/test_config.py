import pytest
from app.config import Settings
from app.exceptions import MyappValidationException


def test_settings():
    settings = Settings()

    assert not settings.DEBUG
    assert settings.LOGGING_LEVEL == "INFO"
    assert settings.CLIENT_ID == "dummy"
    assert settings.GITHUB_WEBHOOK_SECRET is None
    assert settings.CLIENT_URL is None


def test_settings_logging_level_error():
    logging_level = "DEBUGGGGG"

    with pytest.raises(MyappValidationException):
        _settings = Settings(LOGGING_LEVEL=logging_level)
