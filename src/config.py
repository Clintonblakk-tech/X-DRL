"""Central configuration for the X-DRL release candidate."""
from pathlib import Path

RELEASE_ROOT = Path(__file__).resolve().parent.parent
NETWORK_DIR = RELEASE_ROOT / "benchmarks"

NETWORKS = {
    "Hanoi": {"file": str(NETWORK_DIR / "Hanoi.inp"), "budget": 3},
    "Net3": {"file": str(NETWORK_DIR / "Net3.inp"), "budget": 5},
    "C-Town": {"file": str(NETWORK_DIR / "C-Town.inp"), "budget": 10},
}

SEEDS = list(range(1, 11))

# Preserve the effective historical GA settings verified from the engine.
GA_PARAMS = {
    "population": 100,
    "generations": 1000,
    "mutation": 0.10,
    "crossover": 0.80,
    "tournament": 5,
}

# Defaults for the 0.70/0.30 budget-sensitivity protocol.
DQN_PARAMS = {
    "episodes": 1000,
    "batch_size": 64,
    "buffer_size": 50000,
    "gamma": 0.99,
    "learning_rate": 0.0005,
    "target_update": 100,
    "epsilon_start": 1.0,
    "epsilon_end": 0.01,
    "epsilon_decay": 0.995,
    "coverage_weight": 0.70,
    "centrality_weight": 0.30,
}

# The historical 60-row benchmark explicitly used coverage-only reward.
HISTORICAL_BENCHMARK_DQN_WEIGHTS = {
    "coverage_weight": 1.0,
    "centrality_weight": 0.0,
}

COVERAGE_RADIUS = 2
