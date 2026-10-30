import sys
import types
import unittest
import networkx as nx
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

# WNTR is only needed when constructing a real network; stub import for unit tests.
if "wntr" not in sys.modules:
    wntr_stub = types.ModuleType("wntr")
    wntr_stub.network = types.SimpleNamespace()
    sys.modules["wntr"] = wntr_stub

import config
import ga_engine
from unittest.mock import patch
import types


class TestGAConfigurationAndRepair(unittest.TestCase):
    def test_historical_effective_ga_parameters_are_centralised(self):
        self.assertEqual(config.GA_PARAMS, {
            "population": 100, "generations": 1000, "mutation": 0.10,
            "crossover": 0.80, "tournament": 5,
        })

    def test_engine_has_no_duplicate_parameter_constants(self):
        for name in ("POPULATION_SIZE", "GENERATIONS", "MUTATION_RATE",
                     "CROSSOVER_RATE", "TOURNAMENT_SIZE"):
            self.assertFalse(hasattr(ga_engine, name))

    def test_repair_enforces_exact_unique_budget(self):
        repaired = ga_engine._repair_chromosome(
            ["a", "a", "b"], ["a", "b", "c", "d"], 3
        )
        self.assertEqual(len(repaired), 3)
        self.assertEqual(len(set(repaired)), 3)
        self.assertTrue(set(repaired).issubset({"a", "b", "c", "d"}))

    def test_repair_rejects_impossible_budget(self):
        with self.assertRaises(ValueError):
            ga_engine._repair_chromosome(["a"], ["a", "b"], 3)

    def test_mutation_preserves_budget_and_uniqueness(self):
        child = ga_engine._mutate(["a", "b", "c"], ["a", "b", "c", "d"], 1.0)
        self.assertEqual(len(child), 3)
        self.assertEqual(len(set(child)), 3)

    def test_small_ga_smoke_returns_four_consistent_values(self):
        graph = nx.path_graph(["a", "b", "c", "d", "e"])
        fake_wn = types.SimpleNamespace(to_graph=lambda: graph)
        fake_network = types.SimpleNamespace(WaterNetworkModel=lambda path: fake_wn)
        with patch("ga_engine.wntr.network", fake_network):
            result = ga_engine.run_ga(
                "Tiny", "unused.inp", 2, 3,
                ga_params={"population": 4, "generations": 2,
                           "mutation": 0.1, "crossover": 0.8,
                           "tournament": 2},
            )
        self.assertEqual(len(result), 4)
        self.assertEqual(len(result[3]), 2)
        self.assertEqual(len(set(result[3]), 2))


if __name__ == "__main__":
    unittest.main()
