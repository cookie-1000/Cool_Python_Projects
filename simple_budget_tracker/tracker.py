from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Transaction:
    description: str
    amount: float
    category: str
    posted_on: date

    @staticmethod
    def from_dict(payload: dict[str, str]) -> "Transaction":
        return Transaction(
            description=payload["description"],
            amount=float(payload["amount"]),
            category=payload["category"],
            posted_on=date.fromisoformat(payload["posted_on"]),
        )

    def to_dict(self) -> dict[str, str]:
        data = asdict(self)
        data["posted_on"] = self.posted_on.isoformat()
        return data


class BudgetTracker:
    def __init__(self, storage_path: Path) -> None:
        self._storage_path = storage_path
        self._transactions: list[Transaction] = []

    def load(self) -> None:
        if not self._storage_path.exists():
            self._transactions = []
            return
        payload = json.loads(self._storage_path.read_text())
        self._transactions = [Transaction.from_dict(item) for item in payload]

    def save(self) -> None:
        payload = [transaction.to_dict() for transaction in self._transactions]
        self._storage_path.write_text(json.dumps(payload, indent=2))

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def list_transactions(self) -> Iterable[Transaction]:
        return list(self._transactions)

    def summary_by_category(self) -> dict[str, float]:
        summary: dict[str, float] = {}
        for transaction in self._transactions:
            summary[transaction.category] = summary.get(transaction.category, 0.0) + transaction.amount
        return summary

    def balance(self) -> float:
        return sum(transaction.amount for transaction in self._transactions)


def default_storage() -> Path:
    return Path.home() / ".budget_tracker.json"
