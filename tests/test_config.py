import pytest

from finflow.config import load_settings


def test_load_settings_returns_defaults_when_environment_is_empty(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv("FINFLOW_NBP_BASE_URL", raising=False)
    monkeypatch.delenv("FINFLOW_API_TIMEOUT", raising=False)

    settings = load_settings()

    assert settings.nbp_base_url == "https://api.nbp.pl/api/"
    assert settings.api_timeout == 5.0


def test_load_settings_uses_environment_values(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FINFLOW_NBP_BASE_URL", "https://example.com/api/")
    monkeypatch.setenv("FINFLOW_API_TIMEOUT", "2.5")

    settings = load_settings()

    assert settings.nbp_base_url == "https://example.com/api/"
    assert settings.api_timeout == 2.5


def test_load_settings_rejects_non_numeric_timeout(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FINFLOW_API_TIMEOUT", "not-a-number")

    with pytest.raises(ValueError, match="FINFLOW_API_TIMEOUT must be a number"):
        load_settings()


@pytest.mark.parametrize("invalid_timeout", ["0", "-1", "inf", "nan"])
def test_load_settings_rejects_invalid_numeric_timeout(
    monkeypatch: pytest.MonkeyPatch,
    invalid_timeout: str,
):
    monkeypatch.setenv("FINFLOW_API_TIMEOUT", invalid_timeout)

    with pytest.raises(
        ValueError,
        match="FINFLOW_API_TIMEOUT must be a finite number greater than zero",
    ):
        load_settings()
