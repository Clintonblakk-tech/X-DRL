import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd

MODULE = Path(__file__).resolve().parents[1] / "src" / "60_statistical_analysis.py"
spec = importlib.util.spec_from_file_location("stat_analysis", MODULE)
stat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stat)


class TestStatisticalAnalysis(unittest.TestCase):
    def test_rejects_raw_reward_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "raw.csv"
            pd.DataFrame({"Network": ["Hanoi"], "Method": ["GA"],
                          "Seed": [1], "BestReward": [4]}).to_csv(p, index=False)
            with self.assertRaises(ValueError):
                stat.analyse(p, "coverage_fraction")

    def test_uses_common_metric_and_matched_seeds(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "metrics.csv"
            pd.DataFrame([
                ["Hanoi", "GA", 1, "coverage_fraction", .7],
                ["Hanoi", "GA", 2, "coverage_fraction", .8],
                ["Hanoi", "DQN", 1, "coverage_fraction", .8],
                ["Hanoi", "DQN", 2, "coverage_fraction", .9],
            ], columns=["Network", "Method", "Seed", "Metric", "Value"]).to_csv(p, index=False)
            result = stat.analyse(p, "coverage_fraction")
            self.assertEqual(result.loc[0, "Test"], "Wilcoxon signed-rank (matched common seeds)")
            self.assertEqual(int(result.loc[0, "N_matched"]), 2)


if __name__ == "__main__":
    unittest.main()
