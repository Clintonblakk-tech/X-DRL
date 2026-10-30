"""Run the historical 60-run GA/DQN benchmark without overwriting prior results.

Requires Hanoi.inp, Net3.inp and C-Town.inp in benchmarks/; see README.md.
This is a full experiment (3 networks x 10 seeds x 2 methods), not a smoke test.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from config import NETWORKS, SEEDS, GA_PARAMS, HISTORICAL_BENCHMARK_DQN_WEIGHTS


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", help="New output directory; default is a UTC timestamped folder under results/benchmark_runs/.")
    args = parser.parse_args()

    # Preflight every input before importing engines or creating output files.
    paths = {name: Path(info["file"]).resolve() for name, info in NETWORKS.items()}
    missing = [f"{name}: {path}" for name, path in paths.items() if not path.is_file()]
    if missing:
        raise SystemExit(
            "Benchmark input files are missing. No experiment was started:\n  "
            + "\n  ".join(missing)
            + "\nSee benchmarks/README.md for source and local placement instructions."
        )

    # Import compute engines only after all network files have passed preflight.
    from ga_engine import run_ga
    from dqn_engine_real import run_dqn

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(args.output_dir).expanduser().resolve() if args.output_dir else REPO_ROOT / "results" / "benchmark_runs" / stamp
    if out.exists():
        raise SystemExit(f"Refusing to reuse existing output directory: {out}")
    out.mkdir(parents=True, exist_ok=False)

    manifest = {
        "protocol": "historical 60-run GA/DQN benchmark",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "networks": {name: {"file": p.name, "sha256": sha256(p), "sensor_budget": NETWORKS[name]["budget"]}
                     for name, p in paths.items()},
        "seeds": SEEDS,
        "dqn_episodes": 1000,
        "dqn_reward_weights": HISTORICAL_BENCHMARK_DQN_WEIGHTS,
        "ga_parameters": GA_PARAMS,
        "output_directory": str(out),
    }
    (out / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    rows = []
    for name, path in paths.items():
        info = NETWORKS[name]
        for seed in SEEDS:
            ga_best, ga_final, ga_time, ga_nodes = run_ga(
                name, str(path), info["budget"], seed, ga_params=GA_PARAMS
            )
            dq_best, dq_final, dq_time, dq_nodes = run_dqn(
                name, str(path), info["budget"], seed, episodes=1000,
                coverage_weight=HISTORICAL_BENCHMARK_DQN_WEIGHTS["coverage_weight"],
                centrality_weight=HISTORICAL_BENCHMARK_DQN_WEIGHTS["centrality_weight"],
                replay_buffer=True, target_network=True,
                output_dir=str(out / "dqn_artifacts"),
            )
            rows.extend([
                [name, "GA", seed, ga_best, ga_final, ga_time, json.dumps(ga_nodes)],
                [name, "DQN", seed, dq_best, dq_final, dq_time, json.dumps(dq_nodes)],
            ])

    df = pd.DataFrame(rows, columns=[
        "Network", "Method", "Seed", "BestReward", "FinalReward", "Runtime", "SensorNodes"
    ])
    df.to_csv(out / "final_benchmark_results_1000.csv", index=False)
    summary = (df.groupby(["Network", "Method"])
               .agg(MeanBestReward=("BestReward", "mean"),
                    StdBestReward=("BestReward", "std"),
                    MeanRuntime=("Runtime", "mean")).reset_index())
    summary.to_csv(out / "final_benchmark_summary_1000.csv", index=False)
    print(f"Completed {len(df)} method-runs. Results: {out}")


if __name__ == "__main__":
    main()
