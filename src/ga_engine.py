"""Genetic algorithm sensor-placement engine."""
import random
import time

import networkx as nx
import wntr

from config import GA_PARAMS, COVERAGE_RADIUS


def _repair_chromosome(chromosome, candidate_nodes, sensor_budget, rng=None):
    """Return exactly sensor_budget distinct candidate nodes."""
    rng = rng or random
    if sensor_budget < 1:
        raise ValueError("sensor_budget must be at least 1.")
    if sensor_budget > len(set(candidate_nodes)):
        raise ValueError("Sensor budget exceeds distinct candidate nodes.")
    unique_nodes = list(dict.fromkeys(chromosome))[:sensor_budget]
    available = [node for node in candidate_nodes if node not in unique_nodes]
    missing = sensor_budget - len(unique_nodes)
    if len(available) < missing:
        raise ValueError("Not enough distinct candidate nodes.")
    if missing:
        unique_nodes.extend(rng.sample(available, missing))
    if len(unique_nodes) != sensor_budget or len(set(unique_nodes)) != sensor_budget:
        raise RuntimeError("Chromosome repair failed.")
    return unique_nodes


def _mutate(individual, candidate_nodes, mutation_rate, rng=None):
    rng = rng or random
    child = list(individual)
    for index in range(len(child)):
        if rng.random() < mutation_rate:
            alternatives = [n for n in candidate_nodes if n not in child]
            if alternatives:
                child[index] = rng.choice(alternatives)
    return _repair_chromosome(child, candidate_nodes, len(individual), rng)


def _compute_coverage(graph, sensor_nodes, coverage_radius=COVERAGE_RADIUS):
    covered = set()
    for sensor in sensor_nodes:
        covered.update(nx.single_source_shortest_path_length(
            graph, sensor, cutoff=coverage_radius
        ).keys())
    return len(covered)


def run_ga(network_name, network_file, sensor_budget, seed, ga_params=None):
    """Return best-so-far fitness, final-generation fitness, runtime, sensor nodes."""
    params = dict(GA_PARAMS)
    if ga_params:
        params.update(ga_params)
    population_size = int(params["population"])
    generations = int(params["generations"])
    mutation_rate = float(params["mutation"])
    crossover_rate = float(params["crossover"])
    tournament_size = int(params["tournament"])
    if population_size < 2:
        raise ValueError("population must be at least 2.")
    if generations < 1:
        raise ValueError("generations must be at least 1.")
    if not 1 <= tournament_size <= population_size:
        raise ValueError("tournament must be between 1 and population.")
    if not 0 <= mutation_rate <= 1 or not 0 <= crossover_rate <= 1:
        raise ValueError("mutation and crossover must be in [0, 1].")

    rng = random.Random(seed)
    start = time.time()
    wn = wntr.network.WaterNetworkModel(network_file)
    graph = wn.to_graph()
    candidates = list(graph.nodes())
    if sensor_budget < 1 or sensor_budget > len(set(candidates)):
        raise ValueError("Invalid sensor budget for candidate graph.")

    def fitness(chromosome):
        return _compute_coverage(graph, chromosome)

    def individual():
        return rng.sample(candidates, sensor_budget)

    population = [individual() for _ in range(population_size)]
    best_score, best_chromosome = -1, None
    for _ in range(generations):
        next_population = []
        while len(next_population) < population_size:
            p1 = max(rng.sample(population, tournament_size), key=fitness)
            p2 = max(rng.sample(population, tournament_size), key=fitness)
            if rng.random() < crossover_rate and sensor_budget >= 2:
                cut = rng.randint(1, sensor_budget - 1)
                child = p1[:cut] + p2[cut:]
            else:
                child = p1.copy()
            child = _repair_chromosome(child, candidates, sensor_budget, rng)
            child = _mutate(child, candidates, mutation_rate, rng)
            next_population.append(child)
        population = next_population
        generation_best = max(population, key=fitness)
        score = fitness(generation_best)
        if score > best_score:
            best_score, best_chromosome = score, generation_best.copy()

    final_score = max(fitness(x) for x in population)
    best_chromosome = _repair_chromosome(best_chromosome, candidates, sensor_budget, rng)
    runtime = time.time() - start
    return float(fitness(best_chromosome)), float(final_score), float(runtime), best_chromosome
