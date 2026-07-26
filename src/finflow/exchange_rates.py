from datetime import date
from decimal import Decimal
from typing import Any

from finflow.models import Currency, ExchangeRate


def parse_nbp_exchange_rate(payload: dict[str, Any]) -> ExchangeRate:
    rate_data = payload["rates"][0]

    base_currency = Currency(payload["code"])
    quote_currency = Currency.PLN
    rate = Decimal(str(rate_data["mid"]))
    effective_date = date.fromisoformat(rate_data["effectiveDate"])

    return ExchangeRate(
        base_currency=base_currency,
        quote_currency=quote_currency,
        rate=rate,
        effective_date=effective_date,
    )
