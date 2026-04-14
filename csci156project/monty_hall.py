import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DOORS = [3, 6, 9, 20, 100]
ITER_GRID = [10, 30, 100, 300, 1_000, 3_000, 10_000, 30_000, 100_000]

def exact_probs(n: int):
    """Return the exact win probabilities where classic 
    is the informed host opening one goat door and banana
    is the host accidentally opening one random unchosen door."""
    stick_classic = 1/n
    switch_classic = (n-1)/(n*(n-2))
    stick_banana = 1/n
    switch_banana = 1/n
    return{
        "classic_stick": stick_classic,
        "classic_switch": switch_classic,
        "banana_stick": stick_banana,
        "banana_switch": switch_banana
    }

def simulate_classic(n: int, trials: int, rng: np.random.Generator):
    """Monty Carlo for an informed host Monty Hall with N doors.
    The host opens exactly one goat door among the unchose doors.
    The player either sticks or randomly switches to one of the remaining closed doors."""
    car = rng.integers(0, n, size=trials)
    pick = rng.integers(0, n, size=trials)
    stick_win = (pick == car)
    #If the initial choice is wrong the car is among the n-2 closed alternatives
    #left after the host reveals one goat door.
    switch_win = (pick != car) & (rng.integers(0, n-2, size=trials) == 0)
    return float(stick_win.mean()), float(switch_win.mean())

def simulate_banana(n: int, trials: int, rng: np.random.Generator):
    """Monte Carlo for an accidental opening variant.
    A random unchosen door is opend. If it reveals the car, the game is lost
    immediately. Otherwise the player either sticks or randomly swithces to one of the
    remaining closed doors."""
    car = rng.integers(0, n, size=trials)
    pick = rng.integers(0, n, size=trials)
    stick_win = (pick == car)
    #When the intial pick is wrong a random unchosen door reveals the car
    #with probability 1/(n-1).
    opened_car = (pick != car) & (rng.integers(0, n-1, size=trials) == 0)
    #If the opened door is not the car and the original pick is wrong
    #then the cr is one of the remaining n-2 closed alternatives.
    switch_win = (~opened_car) & (pick != car) & (rng.integers(0, n-2, size=trials) == 0)
    return float(stick_win.mean()), float(switch_win.mean())

def convergence_table(rng: np.random.Generator, reps: int = 400):
    rows = []
    for variant in ["classic", "banana"]:
        for n in DOORS:
            probs = exact_probs(n)
            for policy_key, p in [
                ("Stick", probs[f"{variant}_stick"]),
                ("Random Switch", probs[f"{variant}_switch"])
            ]:
                for T in ITER_GRID:
                    counts = rng.binomial(T, p, size=reps)
                    estimates = counts / T
                    rows.append({
                        "variant": variant,
                        "doors": n,
                        "policy": policy_key,
                        "iterations": T,
                        "exact_p": p,
                        "mae": float(np.mean(np.abs(estimates - p))),
                        "rmse": float(np.sqrt(np.mean((estimates - p)**2))),
                        "q10": float(np.quantile(estimates, 0.1)),
                        "q50": float(np.quantile(estimates, 0.5)),
                        "q90": float(np.quantile(estimates, 0.9)),
                    }
                    )
    return pd.DataFrame(rows)

def final_estimates(rng: np.random.Generator, trials: int):
    rows = []
    for n in DOORS:
        sc_stick, sc_switch = simulate_classic(n, trials, rng)
        sb_stick, sb_switch = simulate_banana(n, trials, rng)
        exact = exact_probs(n)
        rows.append({
            "doors": n,
            "classic_stick_est": sc_stick,
            "classic_stick_exact": exact["classic_stick"],
            "classic_switch_est": sc_switch,
            "classic_switch_exact": exact["classic_switch"],
            "banana_stick_est": sb_stick,
            "banana_stick_exact": exact["banana_stick"],
            "banana_switch_est": sb_switch,
            "banana_switch_exact": exact["banana_switch"],
        })
    return pd.DataFrame(rows)

def make_plots(out_dir: Path, summary_df: pd.DataFrame, conv_df: pd.DataFrame):
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    x = summary_df["doors"]
    plt.figure(figsize=(8, 4.8))
    plt.plot(x, summary_df["classic_stick_exact"], marker="o", label="Stick(exact)")
    plt.plot(x, summary_df["classic_switch_exact"], marker="o", label="Random switch(exact)")
    plt.xscale("log")
    plt.xlabel("Number of doors(log scale)")
    plt.ylabel("Winning probability")
    plt.title("Classic informed host variant")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "classic_probabilities.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8, 4.8))
    plt.plot(x, summary_df["banana_stick_exact"], marker="o", label="Stick(exact)")
    plt.plot(x, summary_df["banana_switch_exact"], marker="o", label="Random switch(exact)")
    plt.xscale("log")
    plt.xlabel("Number of doors(log scale)")
    plt.ylabel("Winning probability")
    plt.title("Banana peel accidental opening variant")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "banana_probabilities.png", dpi=220)
    plt.close()

    for variant in ["classic", "banana"]:
        plt.figure(figsize=(8.6, 5.2))
        for policy in ["Stick", "Random Switch"]:
            for n in DOORS:
                sub = conv_df[
                    (conv_df["variant"] == variant) &
                    (conv_df["policy"] == policy) &
                    (conv_df["doors"] == n)
                ]
                plt.plot(
                    sub["iterations"],
                    sub["mae"],
                    marker="o",
                    linewidth=1.5,
                    label=f"{policy} N={n}"
                )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Number of iterations(log scale)")
        plt.ylabel("Mean absolute error over 400 replications")
        plt.title(f"Convergence of Monte Carlo estimates for {variant.capitalize()} variant")
        plt.grid(True, alpha=0.25)
        plt.legend(ncol=2, fontsize=8)
        plt.tight_layout()
        plt.savefig(fig_dir / f"{variant}_convergence_mae.png", dpi=220)
        plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trails", type=int, default=500_000, help="Trials per door count for final estimates")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="monty_hall_output")
    args = parser.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    summary_df = final_estimates(rng, trials=args.trails)
    conv_df = convergence_table(rng, reps=400)
    summary_df.to_csv(out_dir / "simulation_summary.csv", index=False)
    conv_df.to_csv(out_dir / "convergence_summary.csv", index=False)
    make_plots(out_dir, summary_df, conv_df)
    print(f"The results have been saved to {out_dir.resolve()}")

if __name__ == "__main__":
    main()