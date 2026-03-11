from policies import Play
import matplotlib.pyplot as plt
import numpy as np

N = 100000

# --- Strategy 1: Stand >= 17 ---
wins1 = losses1 = ties1 = 0

for _ in range(N):
    game = Play()
    result = game.playStandGE17()

    if result == "Tie":
        ties1 += 1
    elif result is True:
        wins1 += 1
    else:
        losses1 += 1

# --- Strategy 2: Stand hard 17, hit soft 17 ---
wins2 = losses2 = ties2 = 0

for _ in range(N):
    game = Play()
    result = game.playStandGE17AndHard()

    if result == "Tie":
        ties2 += 1
    elif result is True:
        wins2 += 1
    else:
        losses2 += 1

# --- Strategy 3: Always stand ---
wins3 = losses3 = ties3 = 0

for _ in range(N):
    game = Play()
    result = game.playAlwaysStand()

    if result == "Tie":
        ties3 += 1
    elif result is True:
        wins3 += 1
    else:
        losses3 += 1

# --- Convert to percentages ---
labels = ["Wins", "Losses", "Ties"]

percent1 = [
    wins1/N * 100,
    losses1/N * 100,
    ties1/N * 100
]

percent2 = [
    wins2/N * 100,
    losses2/N * 100,
    ties2/N * 100
]

percent3 = [
    wins3/N * 100,
    losses3/N * 100,
    ties3/N * 100
]

# --- Plot ---
x = np.arange(len(labels))
width = 0.25

plt.bar(x - width, percent1, width, label="Stand >=17")
plt.bar(x, percent2, width, label="Stand Hard17 Hit Soft17")
plt.bar(x + width, percent3, width, label="Always Stand")

plt.xticks(x, labels)
plt.ylabel("Percentage (%)")
plt.title("Blackjack Strategy Comparison")
plt.legend()

plt.show()