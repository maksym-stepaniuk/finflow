from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class Currency(StrEnum):
    PLN = "PLN"
    EUR = "EUR"


@dataclass(frozen=True)
class ExchangeRate:
    base_currency: Currency
    quote_currency: Currency
    rate: Decimal
    effective_date: date


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    transaction_date: date
    description: str
    amount: Decimal
    currency: Currency
    account_id: str


@dataclass(frozen=True)
class RejectedRow:
    reason: str
    row_number: int
    row: dict[str, str]


@dataclass(frozen=True)
class ImportResult:
    transactions: list[Transaction]
    errors: list[RejectedRow]
