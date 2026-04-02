from policies import Policies
import matplotlib.pyplot as plt
import numpy as np

# --- Config ---
N = 1000000

# --- Strategies: (method_name, label) ---
strategies = [
    ("playStandGE17", "Stand >=17"),
    ("playStandGE17AndHard", "Stand H17 Hit S17"),
    ("playAlwaysStand", "Always Stand"),
    ("stand16DealerUnder10", "Stand 16 Dealer <= 10"),
    ("stand17DealerUnder9", "Stand 17 Dealer <= 9"),
    ("playBasicStrategy", "Basic Strategy"),
]

# --- Deck types ---
deck_types = [
    (False, "Infinite Deck"),
    (True, "Single Deck"),
]

# --- Simulate both deck types ---
all_results = {}

for singleDeck, deck_label in deck_types:
    results = {}

    for method_name, label in strategies:
        wins = losses = ties = 0

        for _ in range(N):
            game = Policies(singleDeck)
            result = getattr(game, method_name)()

            if result == "Tie":
                ties += 1
            elif result is True:
                wins += 1
            else:
                losses += 1

        results[label] = [wins / N * 100, losses / N * 100, ties / N * 100]

    all_results[deck_label] = results

    # --- Print rankings (by loss %, lowest first = best) ---
    ranked = sorted(results.items(), key=lambda x: x[1][1])
    print(f"\n{'='*60}")
    print(f"  {deck_label}")
    print(f"{'='*60}")
    print(f"{'Strategy':<30} {'Loss %':>8} {'Win %':>8} {'Tie %':>8}")
    print("-" * 56)
    for label, (w, l, t) in ranked:
        print(f"{label:<30} {l:>7.2f}% {w:>7.2f}% {t:>7.2f}%")

# --- Plot: 2 rows (one per deck type), 2 columns (grouped bar + ranked bar) ---
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for row, (deck_label, results) in enumerate(all_results.items()):
    ranked = sorted(results.items(), key=lambda x: x[1][1])

    # Left: grouped bar chart
    ax1 = axes[row][0]
    labels = ["Wins", "Losses", "Ties"]
    x = np.arange(len(labels))
    num_strategies = len(strategies)
    width = 0.8 / num_strategies

    for i, (_, strategy_label) in enumerate(strategies):
        offset = (i - num_strategies / 2 + 0.5) * width
        ax1.bar(x + offset, results[strategy_label], width, label=strategy_label)

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_ylabel("Percentage (%)")
    ax1.set_title(f"{deck_label} — Strategy Comparison")
    ax1.legend(fontsize=8)

    # Right: horizontal bar chart ranked by loss %
    ax2 = axes[row][1]
    ranked_labels = [label for label, _ in ranked]
    ranked_losses = [vals[1] for _, vals in ranked]
    colors = plt.cm.RdYlGn(np.linspace(0.8, 0.3, len(ranked)))

    bars = ax2.barh(ranked_labels, ranked_losses, color=colors)
    ax2.set_xlabel("Loss %")
    ax2.set_title(f"{deck_label} — Strategies Ranked by Loss % (Best to Worst)")
    ax2.invert_yaxis()

    for bar, val in zip(bars, ranked_losses):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                 f"{val:.2f}%", va="center", fontsize=9)

plt.tight_layout()
plt.show()
