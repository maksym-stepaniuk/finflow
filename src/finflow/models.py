from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    transaction_date: date
    description: str
    amount: Decimal
    currency: str
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
