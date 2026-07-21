import csv
from decimal import Decimal
from datetime import date
from pathlib import Path

from finflow.models import Transaction

def parse_transaction(row: dict[str, str]) -> Transaction:
    return Transaction(
        transaction_id=row["transaction_id"].strip(),
        transaction_date=date.fromisoformat(row["transaction_date"].strip()),
        description=row["description"].strip(),
        amount=Decimal(row["amount"].strip()),
        currency=row["currency"].strip().upper(),
        account_id=row["account_id"].strip()     
    )

def read_transactions(file_path: Path) -> list[Transaction]:
    transactions:list[Transaction] = []

    with file_path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            transactions.append(parse_transaction(row))

    return transactions

