import os
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Settings:
    nbp_base_url: str
    api_timeout: float


def load_settings() -> Settings:
    nbp_base_url = os.getenv("FINFLOW_NBP_BASE_URL", "https://api.nbp.pl/api/")
    raw_timeout = os.getenv("FINFLOW_API_TIMEOUT", "5.0")

    try:
        api_timeout = float(raw_timeout)
    except ValueError as error:
        raise ValueError("FINFLOW_API_TIMEOUT must be a number") from error

    if not isfinite(api_timeout) or api_timeout <= 0:
        raise ValueError(
            "FINFLOW_API_TIMEOUT must be a finite number greater than zero"
        )

    return Settings(
        nbp_base_url=nbp_base_url,
        api_timeout=api_timeout,
    )
