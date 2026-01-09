import random
from datetime import datetime
from typing import Optional, Dict, Any, List


# ----------------------------
# Input helpers
# ----------------------------
def get_int(prompt: str, min_value: int = 1, max_value: Optional[int] = None) -> int:
    """Safely get an integer from the user within a valid range.
    Accepts commas/spaces. Allows negatives only if min_value < 0.
    """
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number (e.g., 2500).")
            continue

        if value < min_value:
            print(f"Please enter a number >= {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a number <= {max_value}.")
            continue
        return value


def get_choice(prompt: str, valid: List[str]) -> str:
    """Get a menu choice from a list of valid strings."""
    valid_set = set(valid)
    while True:
        ans = input(prompt).strip()
        if ans in valid_set:
            return ans
        print(f"Please choose one of: {', '.join(valid)}")


def get_yes_no(prompt: str) -> bool:
    """Return True for yes, False for no."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please type y/n.")


# ----------------------------
# Simulation + reporting
# ----------------------------
def text_histogram(counts: Dict[Any, int], total: int, bar_width: int = 30) -> str:
    """Make a simple text histogram with percentages."""
    if not counts:
        return "(no data)"

    max_count = max(counts.values()) or 1

    # Order nicely: numeric keys sorted, otherwise keep insertion order
    try:
        keys = sorted(counts)  # works if keys are all comparable (e.g., ints)
    except TypeError:
        keys = list(counts.keys())

    lines = []
    for key in keys:
        count = counts[key]
        bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0
        bar = "#" * bar_len
        pct = (count / total) * 100 if total > 0 else 0
        lines.append(f"{str(key):>6}: {count:>8} ({pct:6.2f}%) | {bar}")
    return "\n".join(lines)


def coin_counts(trials: int) -> Dict[str, int]:
    counts = {"Heads": 0, "Tails": 0}
    for _ in range(trials):
        counts[random.choice(("Heads", "Tails"))] += 1
    return counts


def dice_counts(trials: int, sides: int) -> Dict[int, int]:
    counts = {i: 0 for i in range(1, sides + 1)}
    for _ in range(trials):
        counts[random.randint(1, sides)] += 1
    return counts


def summary_stats(counts: Dict[Any, int], total: int) -> str:
    """Simple stats: most common outcome(s), min/max count, and 'spread'."""
    if not counts or total <= 0:
        return "Stats: (no data)"

    values = list(counts.values())
    max_count = max(values)
    min_count = min(values)

    modes = [k for k, v in counts.items() if v == max_count]
    mode_str = ", ".join(map(str, modes))

    # A simple spread metric: max - min
    spread = max_count - min_count

    return (
        "Stats:\n"
        f"  Most common: {mode_str} ({max_count}, {(max_count/total)*100:.2f}%)\n"
        f"  Least common count: {min_count}\n"
        f"  Spread (max-min): {spread}\n"
    )


def expected_report(counts: Dict[Any, int], expected_each: float, total: int, top_n: int = 3) -> str:
    """Show differences from expected (good for demonstrating 'randomness')."""
    # Sort by absolute difference from expected (largest first)
    diffs = []
    for k, v in counts.items():
        diffs.append((abs(v - expected_each), k, v - expected_each, v))
    diffs.sort(reverse=True)

    lines = [
        f"Expected per outcome ≈ {expected_each:.2f}",
        f"Top {min(top_n, len(diffs))} biggest deviations from expected:",
    ]
    for i, (_, k, delta, v) in enumerate(diffs[:top_n], start=1):
        lines.append(f"  {i}. {k}: actual {v}, diff {delta:+.2f} ({(v/total)*100:.2f}%)")
    return "\n".join(lines) + "\n"


def format_block(title: str, counts: Dict[Any, int], trials: int, bar_width: int) -> str:
    lines = [f"\n=== {title} ===", f"Trials: {trials}", ""]
    lines.append(text_histogram(counts, trials, bar_width=bar_width))
    lines.append("")
    lines.append(summary_stats(counts, trials))
    return "\n".join(lines)


def save_to_file(content: str, filename: str = "results.txt") -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n\n--- {stamp} ---\n")
        f.write(content)
    print(f"\nSaved to {filename} ✅")


# ----------------------------
# Main program
# ----------------------------
def main() -> None:
    print("Coin & Dice Simulator (Upgraded)")
    print("--------------------------------")

    # Optional reproducible randomness
    if get_yes_no("Set a random seed for repeatable results? (y/n): "):
        seed = get_int("Enter seed (any whole number): ", min_value=-10**18, max_value=10**18)
        random.seed(seed)
        print(f"Seed set to {seed}.\n")

    while True:
        print("\nMenu:")
        print("1) Coin flips")
        print("2) Dice rolls")
        print("3) Both")
        print("4) Exit")

        choice = get_choice("Choose an option (1-4): ", ["1", "2", "3", "4"])
        if choice == "4":
            print("Goodbye!")
            return

        trials = get_int("How many trials? (e.g., 1000): ", min_value=1, max_value=10_000_000)
        bar_width = get_int("Histogram width (10-80): ", min_value=10, max_value=80)

        output_parts: List[str] = []

        if choice in ("1", "3"):
            c = coin_counts(trials)
            block = format_block("Coin Flip Results", c, trials, bar_width)
            # Expected analysis
            block += "\n" + expected_report(c, expected_each=trials / 2, total=trials, top_n=2)
            output_parts.append(block)

        if choice in ("2", "3"):
            sides = get_int("How many sides on the die? (2-100): ", min_value=2, max_value=100)
            d = dice_counts(trials, sides)
            block = format_block(f"Dice Roll Results ({sides}-sided)", d, trials, bar_width)
            # Expected analysis
            block += "\n" + expected_report(d, expected_each=trials / sides, total=trials, top_n=min(3, sides))
            output_parts.append(block)

        final_text = "\n".join(output_parts)
        print(final_text)

        if get_yes_no("Save these results to results.txt? (y/n): "):
            save_to_file(final_text)

        if not get_yes_no("Run another simulation? (y/n): "):
            print("Goodbye!")
            return


if __name__ == "__main__":
    main()
