from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from simple_budget_tracker.tracker import BudgetTracker, Transaction, default_storage


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track simple income and expenses.")
    parser.add_argument(
        "--storage",
        type=Path,
        default=default_storage(),
        help="Path to the JSON storage file.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a transaction.")
    add_parser.add_argument("description", help="Short description of the transaction.")
    add_parser.add_argument("amount", type=float, help="Positive for income, negative for expenses.")
    add_parser.add_argument("category", help="Category, e.g. groceries, rent, salary.")
    add_parser.add_argument(
        "--date",
        dest="posted_on",
        default=date.today().isoformat(),
        help="ISO date for the transaction (YYYY-MM-DD).",
    )

    subparsers.add_parser("list", help="List all transactions.")
    subparsers.add_parser("summary", help="Show totals by category.")
    subparsers.add_parser("balance", help="Show current balance.")

    return parser


def run_cli(args: list[str] | None = None) -> int:
    parser = _build_parser()
    namespace = parser.parse_args(args)

    tracker = BudgetTracker(namespace.storage)
    tracker.load()

    if namespace.command == "add":
        transaction = Transaction(
            description=namespace.description,
            amount=namespace.amount,
            category=namespace.category,
            posted_on=date.fromisoformat(namespace.posted_on),
        )
        tracker.add(transaction)
        tracker.save()
        print("Added transaction.")
        return 0

    if namespace.command == "list":
        for transaction in tracker.list_transactions():
            print(
                f"{transaction.posted_on} | {transaction.category:<12} "
                f"{transaction.amount:>8.2f} | {transaction.description}"
            )
        return 0

    if namespace.command == "summary":
        summary = tracker.summary_by_category()
        for category, total in sorted(summary.items()):
            print(f"{category:<12} {total:>8.2f}")
        return 0

    if namespace.command == "balance":
        print(f"Balance: {tracker.balance():.2f}")
        return 0

    parser.error("Unknown command")
    return 1
