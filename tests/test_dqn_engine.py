import sys
import types
import unittest
import tempfile
from unittest.mock import patch
import networkx as nx
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

if "wntr" not in sys.modules:
    wntr_stub = types.ModuleType("wntr")
    wntr_stub.network = types.SimpleNamespace()
    sys.modules["wntr"] = wntr_stub

import config
from dqn_engine_real import DQN, ReplayBuffer, mask_invalid_actions, run_dqn


class TestDQNRegression(unittest.TestCase):
    def test_dqn_parameters_are_centralised(self):
        for key in ("episodes", "batch_size", "buffer_size", "gamma",
                    "learning_rate", "target_update"):
            self.assertIn(key, config.DQN_PARAMS)

    def test_action_mask_hides_previously_selected_nodes(self):
        q = torch.tensor([[0.1, 0.9, 0.3], [0.8, 0.2, 0.5]])
        states = torch.tensor([[1., 0., 1.], [0., 1., 0.]])
        masked = mask_invalid_actions(q, states)
        self.assertEqual(int(masked[0].argmax()), 1)
        self.assertEqual(int(masked[1].argmax()), 0)
        self.assertAlmostEqual(float(q[0, 0]), 0.1)

    def test_all_selected_actions_are_masked(self):
        q = torch.tensor([[1., 2.]])
        states = torch.tensor([[1., 1.]])
        self.assertTrue(torch.all(mask_invalid_actions(q, states) < -1e8))

    def test_model_output_dimension(self):
        model = DQN(7, 7)
        self.assertEqual(tuple(model(torch.zeros(2, 7)).shape), (2, 7))

    def test_replay_buffer_copies_state_arrays(self):
        state = np.array([0., 1.], dtype=np.float32)
        memory = ReplayBuffer(4)
        memory.push(state, 0, 1., state, False)
        state[0] = 1.
        sampled = memory.buffer[0]
        self.assertEqual(float(sampled[0][0]), 0.0)

    def test_historical_protocol_is_explicit(self):
        self.assertEqual(config.HISTORICAL_BENCHMARK_DQN_WEIGHTS,
                         {"coverage_weight": 1.0, "centrality_weight": 0.0})

    def test_short_run_saves_best_episode_artifacts(self):
        graph = nx.path_graph(["J1", "J2", "J3", "J4"])
        fake_wn = types.SimpleNamespace(to_graph=lambda: graph)
        fake_network = types.SimpleNamespace(WaterNetworkModel=lambda path: fake_wn)
        with tempfile.TemporaryDirectory() as td, patch("dqn_engine_real.wntr.network", fake_network):
            result = run_dqn(
                "Tiny", "unused.inp", 2, 7, episodes=2,
                dqn_params={"batch_size": 64, "buffer_size": 100,
                            "target_update": 1, "coverage_weight": 0.7,
                            "centrality_weight": 0.3},
                output_dir=td,
            )
            self.assertEqual(len(result), 4)
            self.assertEqual(len(result[3]), 2)
            self.assertEqual(len(set(result[3])), 2)
            self.assertTrue((Path(td) / "best_dqn_Tiny_seed_7.pth").is_file())
            self.assertTrue((Path(td) / "dqn_eval_states_Tiny_seed_7.npz").is_file())
            self.assertTrue((Path(td) / "dqn_run_Tiny_seed_7.json").is_file())


if __name__ == "__main__":
    unittest.main()
