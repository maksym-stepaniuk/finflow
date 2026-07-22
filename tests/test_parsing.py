from finflow.models import Transaction
from datetime import date
from decimal import Decimal
from finflow.parsing import parse_transaction
from finflow.parsing import read_transactions

def test_parse_transaction_converts_csv_row_to_transaction():
    row = {
        "transaction_id": "txn-001",
        "transaction_date": "2026-06-01",
        "description": "    SPOTIFY",
        "amount": "-23.99",
        "currency": "pln   ",
        "account_id": "checking-pln"
    }

    transaction = parse_transaction(row)

    assert transaction == Transaction(
        transaction_id="txn-001",
        transaction_date=date(2026, 6, 1),
        description="SPOTIFY",
        amount=Decimal("-23.99"),
        currency="PLN",
        account_id="checking-pln"
    )

def test_read_transactions_reads_csv_file(tmp_path):
    csv_file = tmp_path / "examples.csv"
    csv_file.write_text(
        "transaction_id,transaction_date,description,amount,currency,account_id\n"
        "txn-202606-005,2026-06-04,SPOTIFY,-23.99,PLN,checking-pln\n",
        encoding="utf-8"
    )

    transactions = read_transactions(csv_file)

    assert len(transactions) == 1
    assert transactions[0].amount == Decimal("-23.99")
    assert transactions[0].currency == "PLN"
