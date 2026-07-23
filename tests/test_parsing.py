from datetime import date
from decimal import Decimal

import pytest

from finflow.exceptions import TransactionParseError
from finflow.models import Transaction
from finflow.parsing import parse_transaction, read_transactions


@pytest.fixture
def transaction_row() -> dict[str, str]:
    return {
        "transaction_id": "txn-001",
        "transaction_date": "2026-06-01",
        "description": "    SPOTIFY",
        "amount": "-23.99",
        "currency": "pln   ",
        "account_id": "checking-pln",
    }


def test_parse_transaction_converts_csv_row_to_transaction(
    transaction_row: dict[str, str],
):
    transaction = parse_transaction(transaction_row)

    assert transaction == Transaction(
        transaction_id="txn-001",
        transaction_date=date(2026, 6, 1),
        description="SPOTIFY",
        amount=Decimal("-23.99"),
        currency="PLN",
        account_id="checking-pln",
    )


def test_read_transactions_reads_csv_file(tmp_path):
    csv_file = tmp_path / "examples.csv"
    csv_file.write_text(
        "transaction_id,transaction_date,description,amount,currency,account_id\n"
        "txn-202606-005,2026-06-04,SPOTIFY,-23.99,PLN,checking-pln\n",
        encoding="utf-8",
    )

    result = read_transactions(csv_file)

    assert len(result.transactions) == 1
    assert result.errors == []
    assert result.transactions[0].amount == Decimal("-23.99")
    assert result.transactions[0].currency == "PLN"


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_message"),
    [
        ("amount", "not-a-number", "Invalid amount"),
        ("transaction_date", "2026-99-99", "Invalid transaction date"),
    ],
)
def test_parse_transaction_raises_custom_error_for_invalid_value(
    field: str,
    invalid_value: str,
    expected_message: str,
    transaction_row: dict[str, str],
):
    transaction_row[field] = invalid_value

    with pytest.raises(TransactionParseError, match=expected_message):
        parse_transaction(transaction_row)


def test_read_transactions_reports_invalid_rows(tmp_path):
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "transaction_id,transaction_date,description,amount,currency,account_id\n"
        "txn-001,2026-06-04,SPOTIFY,-23.99,PLN,checking-pln\n"
        "txn-002,2026-07-04,invalid,not-a-number,PLN,checking-pln\n",
        encoding="utf-8",
    )

    result = read_transactions(csv_file)

    assert len(result.transactions) == 1
    assert len(result.errors) == 1

    rejected_row = result.errors[0]

    assert rejected_row.reason == "Invalid amount: 'not-a-number'"
    assert rejected_row.row_number == 3
    assert rejected_row.row["transaction_id"] == "txn-002"
