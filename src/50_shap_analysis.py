"""Explain one action-value output using states actually visited by a trained DQN.

Example:
  python src/50_shap_analysis.py --states results/dqn_eval_states_Hanoi_seed_1.npz \
      --checkpoint results/best_dqn_Hanoi_seed_1.pth --action-index 12 --output-dir results/shap
"""
import argparse
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, action_dim),
        )

    def forward(self, x):
        return self.network(x)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--states", required=True, help="NPZ exported by run_dqn.")
    parser.add_argument("--checkpoint", required=True, help="Matching DQN checkpoint.")
    parser.add_argument("--action-index", type=int, required=True,
                        help="Q-value output index to explain.")
    parser.add_argument("--background-size", type=int, default=20)
    parser.add_argument("--output-dir", default="results/shap")
    args = parser.parse_args()

    import shap
    import matplotlib.pyplot as plt

    data = np.load(args.states, allow_pickle=False)
    states = np.asarray(data["states"], dtype=np.float32)
    node_names = data["node_names"].astype(str)
    if states.ndim != 2 or states.shape[0] < 2:
        raise ValueError("At least two genuine evaluation states are required.")
    state_dim = states.shape[1]
    if len(node_names) != state_dim:
        raise ValueError("Node-name metadata does not match state dimension.")
    if not 0 <= args.action_index < state_dim:
        raise ValueError("action-index is outside the DQN output dimension.")

    model = DQN(state_dim, state_dim)
    state_dict = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()

    # Background and explained samples are both drawn from genuine episode states.
    n_background = min(max(1, args.background_size), len(states) - 1)
    background = torch.as_tensor(states[:n_background], dtype=torch.float32)
    explained = torch.as_tensor(states[n_background:] if len(states) > n_background
                                else states, dtype=torch.float32)
    action_index = args.action_index

    def selected_q(x):
        return model(x)[:, action_index:action_index + 1]

    explainer = shap.DeepExplainer(selected_q, background)
    values = explainer.shap_values(explained)
    values = values[0] if isinstance(values, list) else values
    values = np.asarray(values)
    if values.ndim == 3 and values.shape[-1] == 1:
        values = values[..., 0]
    if values.ndim != 2:
        raise RuntimeError(f"Unexpected SHAP output shape: {values.shape}")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / f"shap_action_{action_index}.npz",
                        shap_values=values,
                        states=explained.numpy(),
                        feature_names=node_names,
                        action_index=np.asarray(action_index))
    names = [f"{i}:{name}" for i, name in enumerate(node_names)]
    plt.figure()
    shap.summary_plot(values, explained.numpy(), feature_names=names, show=False)
    plt.tight_layout()
    plt.savefig(out / f"shap_beeswarm_action_{action_index}.png", dpi=300,
                bbox_inches="tight")
    plt.close()
    plt.figure()
    shap.summary_plot(values, explained.numpy(), feature_names=names,
                      plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(out / f"shap_bar_action_{action_index}.png", dpi=300,
                bbox_inches="tight")
    plt.close()
    print(f"Explained Q-value for action {action_index}; {len(explained)} genuine states.")
    print(f"Saved SHAP outputs to {out.resolve()}")


if __name__ == "__main__":
    main()
