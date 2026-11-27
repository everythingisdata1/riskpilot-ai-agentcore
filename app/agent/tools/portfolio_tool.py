import csv
import json
from pathlib import Path

from strands import tool

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "loan_portfolio.csv"

print("*" * 40)
print(f"CSV exists: {DATA_FILE}")


# Load data
def load_portfolio_data() -> list:
    print("Loading data file")
    with open(DATA_FILE, mode='r', encoding="utf-8") as data:
        records = list(csv.DictReader(data))
    print("*" * 40)
    return records


@tool
def get_portfolio_data() -> str:
    """ Retrieve all banking loan portfolio exposure, probability of default and loss given  default..."""
    records = load_portfolio_data()
    return json.dumps(records)
