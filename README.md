# FinFlow

FinFlow is a Python project for importing and validating financial
transactions from CSV files.

## The problem

Financial data is often exported as CSV, but a single malformed row should not
stop the entire import. FinFlow converts valid rows into typed transaction
objects while collecting rejected rows with clear error messages and their
original line numbers.

The project uses `Decimal` for monetary values to avoid the precision issues of
binary floating-point arithmetic.

## Current features

- Read transaction data from CSV files
- Normalize whitespace and currency codes
- Parse ISO-formatted transaction dates
- Store monetary values as `Decimal`
- Validate required fields, dates, amounts, and supported currencies
- Continue importing after an invalid row
- Report successful transactions and rejected rows separately
- Log rejected row numbers and error reasons
- Cover parsing and import behavior with pytest

FinFlow currently supports `PLN` and `EUR`.

## Stack

- Python 3.12+
- Python standard library: `csv`, `dataclasses`, `decimal`, `logging`, and
  `pathlib`
- pytest
- Ruff
- Git and GitHub

## Project structure

```text
finflow/
├── examples/
│   └── sample_transactions.csv
├── src/
│   └── finflow/
│       ├── __init__.py
│       ├── exceptions.py
│       ├── models.py
│       └── parsing.py
├── tests/
│   └── test_parsing.py
├── pyproject.toml
└── README.md
```

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/maksym-stepaniuk/finflow.git
cd finflow
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## CSV format

FinFlow expects a CSV file with the following columns:

| Column | Description | Example |
| --- | --- | --- |
| `transaction_id` | Unique transaction identifier | `txn-202606-001` |
| `transaction_date` | Transaction date in ISO `YYYY-MM-DD` format | `2026-06-01` |
| `description` | Transaction description | `SALARY ACME SOFTWARE` |
| `amount` | Decimal amount; expenses can be negative | `-23.99` |
| `currency` | Currency code; currently `PLN` or `EUR` | `PLN` |
| `account_id` | Identifier of the related account | `checking-pln` |

All columns are required. Leading and trailing whitespace is removed from field
values, and currency codes are normalized to uppercase.

## Usage

```python
from pathlib import Path

from finflow.parsing import read_transactions

result = read_transactions(Path("examples/sample_transactions.csv"))

print(f"Imported: {len(result.transactions)}")
print(f"Rejected: {len(result.errors)}")

for rejected_row in result.errors:
    print(
        f"Row {rejected_row.row_number}: "
        f"{rejected_row.reason}"
    )
```

Running this example with `examples/sample_transactions.csv` produces:

```text
Imported: 22
Rejected: 0
```

`read_transactions` returns an `ImportResult` containing:

- `transactions`: successfully parsed `Transaction` objects
- `errors`: rejected `RejectedRow` objects with the row number, reason, and
  original data

## Development

Run the test suite:

```bash
python -m pytest -q
```

Check code quality:

```bash
python -m ruff check .
python -m ruff format --check .
```

## Status

The CSV import and validation layer is implemented. FinFlow is under active
development and does not yet provide a command-line interface.

## Known limitations

- Only `PLN` and `EUR` currencies are currently supported.
- Transaction dates must use the ISO `YYYY-MM-DD` format.
- Imported transactions are not yet stored in a database.
- The project does not yet provide a CLI or an HTTP API.

## Roadmap

- Integrate an external exchange-rate API.
- Add a CLI command for importing transaction files.
- Store transactions in PostgreSQL.
- Expose transaction data through a REST API.
