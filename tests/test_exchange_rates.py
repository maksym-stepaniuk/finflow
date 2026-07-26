from datetime import date
from decimal import Decimal

from finflow.exchange_rates import parse_nbp_exchange_rate
from finflow.models import Currency, ExchangeRate


def test_parse_nbp_exchange_rate_normalizes_response():
    payload = {
        "table": "A",
        "currency": "euro",
        "code": "EUR",
        "rates": [
            {
                "no": "142/A/NBP/2026",
                "effectiveDate": "2026-07-24",
                "mid": 4.2507,
            }
        ],
    }

    result = parse_nbp_exchange_rate(payload)

    assert result == ExchangeRate(
        base_currency=Currency.EUR,
        quote_currency=Currency.PLN,
        rate=Decimal("4.2507"),
        effective_date=date(2026, 7, 24),
    )
