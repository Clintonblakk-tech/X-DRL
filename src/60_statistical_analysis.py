"""Statistical analysis of common, independently evaluated GA/DQN metrics.

Input schema: Network, Method, Seed, Metric, Value.
This script deliberately does not compare raw GA fitness with DQN cumulative reward.
"""
import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon


REQUIRED = {"Network", "Method", "Seed", "Metric", "Value"}


def analyse(path, metric):
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Evaluation file is missing columns: {sorted(missing)}")
    df = df[df["Metric"] == metric].copy()
    if df.empty:
        raise ValueError(f"No rows found for common metric {metric!r}.")
    df["Value"] = pd.to_numeric(df["Value"], errors="raise")
    if df["Value"].isna().any():
        raise ValueError("Metric values contain missing observations.")
    if not set(df["Method"].unique()).issubset({"GA", "DQN"}):
        raise ValueError("Method must be GA or DQN.")
    output = []
    for network, group in df.groupby("Network"):
        ga_raw = group[group.Method == "GA"].set_index("Seed")["Value"]
        dqn_raw = group[group.Method == "DQN"].set_index("Seed")["Value"]
        if ga_raw.index.has_duplicates or dqn_raw.index.has_duplicates:
            raise ValueError(f"{network}: duplicate seed observations.")
        if len(ga_raw) < 2 or len(dqn_raw) < 2:
            raise ValueError(f"{network}: at least two observations per method are required.")
        common_seeds = sorted(set(ga_raw.index).intersection(dqn_raw.index))
        if len(common_seeds) >= 2:
            ga, dqn = ga_raw.loc[common_seeds], dqn_raw.loc[common_seeds]
            differences = ga.to_numpy() - dqn.to_numpy()
            if (differences == 0).all():
                statistic, p_value = 0.0, 1.0
            else:
                statistic, p_value = wilcoxon(ga, dqn, alternative="two-sided")
            test = "Wilcoxon signed-rank (matched common seeds)"
            n_used = len(common_seeds)
        else:
            if len(set(ga_raw.index).intersection(dqn_raw.index)) != 0:
                raise ValueError(
                    f"{network}: fewer than two matched seeds; cannot safely pair samples."
                )
            statistic, p_value = mannwhitneyu(
                ga_raw.to_numpy(), dqn_raw.to_numpy(), alternative="two-sided"
            )
            test = "Mann-Whitney U (non-overlapping seed sets)"
            n_used = min(len(ga_raw), len(dqn_raw))
        output.append({
            "Network": network, "Metric": metric, "N_matched": n_used,
            "GA_mean": ga.mean(), "GA_sd": ga.std(ddof=1),
            "DQN_mean": dqn.mean(), "DQN_sd": dqn.std(ddof=1),
            "Test": test, "Statistic": statistic, "P_value": p_value,
        })
    return pd.DataFrame(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="evaluation_metrics.csv")
    parser.add_argument("--metric", required=True,
                        help="Common metric, e.g. coverage_fraction or detection_rate.")
    parser.add_argument("--output", default="statistical_summary.csv")
    args = parser.parse_args()
    result = analyse(args.input, args.metric)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
