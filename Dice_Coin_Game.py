import random
from datetime import datetime
from typing import Optional


def get_int(prompt: str, min_value: int = 1, max_value: Optional[int] = None) -> int:
    """Safely get an integer from the user within a valid range."""
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Please enter a positive whole number.")
            continue

        value = int(raw)
        if value < min_value:
            print(f"Please enter a number >= {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a number <= {max_value}.")
            continue
        return value


def get_yes_no(prompt: str) -> bool:
    """Return True for yes, False for no."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please type y/n.")


def text_histogram(counts: dict, total: int, bar_width: int = 30) -> str:
    """Make a simple text histogram."""
    lines = []
    max_count = max(counts.values()) if counts else 1
    for key in counts:
        count = counts[key]
        # scale bar length relative to max_count
        bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0
        bar = "#" * bar_len
        pct = (count / total) * 100 if total > 0 else 0
        lines.append(f"{str(key):>5}: {count:>7} ({pct:6.2f}%) | {bar}")
    return "\n".join(lines)


def simulate_coin_flips(trials: int) -> dict:
    """Simulate coin flips and return counts."""
    counts = {"Heads": 0, "Tails": 0}
    for _ in range(trials):
        flip = random.choice(["Heads", "Tails"])
        counts[flip] += 1
    return counts


def simulate_dice_rolls(trials: int, sides: int = 6) -> dict:
    """Simulate dice rolls and return counts."""
    counts = {i: 0 for i in range(1, sides + 1)}
    for _ in range(trials):
        roll = random.randint(1, sides)
        counts[roll] += 1
    return counts


def format_results(title: str, counts: dict, trials: int) -> str:
    """Format results nicely for printing/saving."""
    lines = [f"\n=== {title} ===", f"Trials: {trials}"]
    lines.append(text_histogram(counts, trials))
    return "\n".join(lines)


def save_to_file(content: str, filename: str = "results.txt") -> None:
    """Append results to a file with a timestamp."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n\n--- {stamp} ---\n")
        f.write(content)
    print(f"\nSaved to {filename} ✅")


def main() -> None:
    print("Coin & Dice Simulator")
    print("---------------------")

    while True:
        print("\nMenu:")
        print("1) Coin flips")
        print("2) Dice rolls")
        print("3) Both")
        print("4) Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "4":
            print("Goodbye!")
            break

        if choice not in ("1", "2", "3"):
            print("Please choose 1, 2, 3, or 4.")
            continue

        trials = get_int("How many trials? (e.g., 1000): ", min_value=1)

        results_output = []

        if choice in ("1", "3"):
            coin_counts = simulate_coin_flips(trials)
            results_output.append(format_results("Coin Flip Results", coin_counts, trials))

        if choice in ("2", "3"):
            sides = get_int("How many sides on the die? (6 for normal dice): ", min_value=2, max_value=100)
            dice_counts = simulate_dice_rolls(trials, sides=sides)
            results_output.append(format_results(f"Dice Roll Results ({sides}-sided)", dice_counts, trials))

        final_text = "\n".join(results_output)
        print(final_text)

        if get_yes_no("\nSave these results to results.txt? (y/n): "):
            save_to_file(final_text)

        if not get_yes_no("\nRun another simulation? (y/n): "):
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()