import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from finflow.exceptions import TransactionParseError
from finflow.models import ImportResult, RejectedRow, Transaction


def parse_transaction(row: dict[str, str]) -> Transaction:
    raw_amount = row["amount"].strip()
    raw_date = row["transaction_date"].strip()

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
        transaction_id=row["transaction_id"].strip(),
        transaction_date=transaction_date,
        description=row["description"].strip(),
        amount=amount,
        currency=row["currency"].strip().upper(),
        account_id=row["account_id"].strip(),
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
                errors.append(
                    RejectedRow(
                        reason=str(error),
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
