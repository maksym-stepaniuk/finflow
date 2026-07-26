import csv
import logging
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from finflow.exceptions import TransactionParseError
from finflow.models import Currency, ImportResult, RejectedRow, Transaction

logger = logging.getLogger(__name__)


def _validate_required_field(row: dict[str, str], field: str) -> str:
    value = row.get(field)

    if value is None or not value.strip():
        raise TransactionParseError(f"Missing required field: {field}")

    return value.strip()


def parse_transaction(row: dict[str, str]) -> Transaction:
    transaction_id = _validate_required_field(row, "transaction_id")
    raw_date = _validate_required_field(row, "transaction_date")
    description = _validate_required_field(row, "description")
    raw_amount = _validate_required_field(row, "amount")
    raw_currency = _validate_required_field(row, "currency").upper()
    account_id = _validate_required_field(row, "account_id")

    try:
        currency = Currency(raw_currency)
    except ValueError as error:
        raise TransactionParseError(
            f"Unsupported currency: {raw_currency!r}"
        ) from error

    try:
        amount = Decimal(raw_amount)
    except InvalidOperation as error:
        raise TransactionParseError(f"Invalid amount: {raw_amount!r}") from error

    try:
        transaction_date = date.fromisoformat(raw_date)
    except ValueError as error:
        raise TransactionParseError(
            f"Invalid transaction date: {raw_date!r}"
        ) from error

    return Transaction(
        transaction_id=transaction_id,
        transaction_date=transaction_date,
        description=description,
        amount=amount,
        currency=currency,
        account_id=account_id,
    )


def read_transactions(file_path: Path) -> ImportResult:
    transactions: list[Transaction] = []
    errors: list[RejectedRow] = []

    with file_path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                transaction = parse_transaction(row)
            except TransactionParseError as error:
                reason = str(error)

                logger.warning(
                    "Rejected CSV row %d: %s",
                    row_number,
                    reason,
                )

                errors.append(
                    RejectedRow(
                        reason=reason,
                        row_number=row_number,
                        row=row,
                    )
                )
            else:
                transactions.append(transaction)

    return ImportResult(
        transactions=transactions,
        errors=errors,
    )
