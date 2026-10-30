"""DQN engine with configuration injection and auditable best-episode artifacts."""
import copy
import json
import random
import time
from collections import deque
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import wntr

from config import DQN_PARAMS, COVERAGE_RADIUS


class SensorPlacementEnvironment:
    def __init__(self, network_file, sensor_budget, coverage_radius=COVERAGE_RADIUS,
                 coverage_weight=0.70, centrality_weight=0.30):
        self.sensor_budget = int(sensor_budget)
        self.coverage_radius = int(coverage_radius)
        self.coverage_weight = float(coverage_weight)
        self.centrality_weight = float(centrality_weight)
        self.wn = wntr.network.WaterNetworkModel(network_file)
        self.G = self.wn.to_graph()
        self.nodes = list(self.G.nodes())
        if not self.nodes:
            raise ValueError("Network graph contains no nodes.")
        if not 1 <= self.sensor_budget <= len(self.nodes):
            raise ValueError("sensor_budget must be between 1 and graph node count.")
        self.node_to_idx = {node: i for i, node in enumerate(self.nodes)}
        self.degree = nx.degree_centrality(self.G)
        self.reset()

    def reset(self):
        self.selected_nodes = []
        return self.get_state()

    def get_state(self):
        state = np.zeros(len(self.nodes), dtype=np.float32)
        for node in self.selected_nodes:
            state[self.node_to_idx[node]] = 1.0
        return state

    def compute_coverage(self):
        covered = set()
        for sensor in self.selected_nodes:
            covered.update(nx.single_source_shortest_path_length(
                self.G, sensor, cutoff=self.coverage_radius
            ).keys())
        return len(covered)

    def step(self, action):
        if not 0 <= int(action) < len(self.nodes):
            raise ValueError("Action index is outside the action space.")
        chosen = self.nodes[int(action)]
        if chosen in self.selected_nodes:
            return self.get_state(), -1.0, True
        self.selected_nodes.append(chosen)
        coverage_score = self.compute_coverage() / len(self.nodes)
        centrality_score = float(np.mean([self.degree[n] for n in self.selected_nodes]))
        reward = self.coverage_weight * coverage_score + self.centrality_weight * centrality_score
        return self.get_state(), float(reward), len(self.selected_nodes) >= self.sensor_budget


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


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=int(capacity))

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((np.array(state, copy=True), int(action), float(reward),
                            np.array(next_state, copy=True), bool(done)))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.asarray(states), np.asarray(actions), np.asarray(rewards),
                np.asarray(next_states), np.asarray(dones))

    def __len__(self):
        return len(self.buffer)


def mask_invalid_actions(q_values, next_states, invalid_value=-1e9):
    """Mask already-selected actions row-wise; input tensors are not modified."""
    masked = q_values.clone()
    invalid = next_states.bool()
    return masked.masked_fill(invalid, invalid_value)


def run_dqn(network_name, network_file, sensor_budget, seed, episodes=None,
            coverage_weight=None, centrality_weight=None, replay_buffer=True,
            target_network=True, dqn_params=None, output_dir="results"):
    params = dict(DQN_PARAMS)
    if dqn_params:
        params.update(dqn_params)
    episodes = int(params["episodes"] if episodes is None else episodes)
    batch_size = int(params["batch_size"])
    buffer_size = int(params["buffer_size"])
    gamma = float(params["gamma"])
    learning_rate = float(params["learning_rate"])
    target_update = int(params["target_update"])
    epsilon = float(params["epsilon_start"])
    epsilon_end = float(params["epsilon_end"])
    epsilon_decay = float(params["epsilon_decay"])
    coverage_weight = float(params["coverage_weight"] if coverage_weight is None else coverage_weight)
    centrality_weight = float(params["centrality_weight"] if centrality_weight is None else centrality_weight)
    if episodes < 1 or batch_size < 1 or buffer_size < 1 or target_update < 1:
        raise ValueError("episodes, batch_size, buffer_size and target_update must be positive.")
    if not 0 <= epsilon_end <= epsilon <= 1 or not 0 < epsilon_decay <= 1:
        raise ValueError("Invalid epsilon schedule.")
    if not np.isclose(coverage_weight + centrality_weight, 1.0):
        raise ValueError("coverage_weight and centrality_weight must sum to 1.")

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    start = time.time()
    env = SensorPlacementEnvironment(network_file, sensor_budget,
                                     coverage_weight=coverage_weight,
                                     centrality_weight=centrality_weight)
    state_dim = action_dim = len(env.nodes)
    online_net = DQN(state_dim, action_dim)
    target_net = copy.deepcopy(online_net)
    optimizer = optim.Adam(online_net.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    memory = ReplayBuffer(buffer_size)
    best_reward = -float("inf")
    best_sensors = None
    best_model_state = None
    best_episode_states = None
    reward_history = []

    for episode in range(episodes):
        state = env.reset()
        done = False
        episode_reward = 0.0
        episode_states = []
        while not done:
            episode_states.append(state.copy())
            valid = np.flatnonzero(state == 0)
            if len(valid) == 0:
                raise RuntimeError("No valid actions remain before episode termination.")
            if random.random() < epsilon:
                action = int(random.choice(valid.tolist()))
            else:
                with torch.no_grad():
                    q = online_net(torch.as_tensor(state, dtype=torch.float32).unsqueeze(0))[0]
                    q = q.clone()
                    q[torch.as_tensor(state == 1)] = -1e9
                    action = int(torch.argmax(q).item())

            next_state, reward, done = env.step(action)
            memory.push(state, action, reward, next_state, done)
            state = next_state
            episode_reward += reward

            if replay_buffer and len(memory) >= batch_size:
                states, actions, rewards, next_states, dones = memory.sample(batch_size)
                states_t = torch.as_tensor(states, dtype=torch.float32)
                actions_t = torch.as_tensor(actions, dtype=torch.long)
                rewards_t = torch.as_tensor(rewards, dtype=torch.float32)
                next_states_t = torch.as_tensor(next_states, dtype=torch.float32)
                dones_t = torch.as_tensor(dones, dtype=torch.float32)
                current_q = online_net(states_t).gather(1, actions_t.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    target_source = target_net if target_network else online_net
                    next_q_all = target_source(next_states_t)
                    next_q_all = mask_invalid_actions(next_q_all, next_states_t)
                    next_q = next_q_all.max(dim=1).values
                    target_q = rewards_t + gamma * next_q * (1.0 - dones_t)
                loss = loss_fn(current_q, target_q)
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(online_net.parameters(), 10.0)
                optimizer.step()

        reward_history.append(float(episode_reward))
        if episode_reward > best_reward:
            best_reward = float(episode_reward)
            best_sensors = env.selected_nodes.copy()
            best_model_state = {k: v.detach().cpu().clone()
                                for k, v in online_net.state_dict().items()}
            best_episode_states = np.asarray(episode_states, dtype=np.float32)
        epsilon = max(epsilon_end, epsilon * epsilon_decay)
        if target_network and (episode + 1) % target_update == 0:
            target_net.load_state_dict(online_net.state_dict())

    runtime = time.time() - start
    if best_sensors is None or len(best_sensors) != sensor_budget or len(set(best_sensors)) != sensor_budget:
        raise RuntimeError("Best-episode sensor solution violates the requested budget.")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = f"{network_name}_seed_{seed}"
    checkpoint = out / f"best_dqn_{stem}.pth"
    torch.save(best_model_state, checkpoint)
    np.savez_compressed(out / f"dqn_eval_states_{stem}.npz",
                        states=best_episode_states,
                        node_names=np.asarray(env.nodes, dtype=str))
    pd.DataFrame({"Episode": range(1, episodes + 1), "Reward": reward_history}).to_csv(
        out / f"reward_history_{stem}.csv", index=False)
    metadata = {
        "network": network_name, "seed": int(seed), "episodes": episodes,
        "sensor_budget": int(sensor_budget), "coverage_weight": coverage_weight,
        "centrality_weight": centrality_weight, "checkpoint": checkpoint.name,
        "evaluation_states": f"dqn_eval_states_{stem}.npz",
        "best_reward": best_reward, "final_reward": float(reward_history[-1]),
        "best_sensor_nodes": best_sensors, "architecture": [state_dim, 128, 64, 32, action_dim],
        "protocol_note": "Best-episode states and checkpoint; evaluation states are genuine states visited in that episode."
    }
    (out / f"dqn_run_{stem}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return best_reward, float(reward_history[-1]), float(runtime), best_sensors
