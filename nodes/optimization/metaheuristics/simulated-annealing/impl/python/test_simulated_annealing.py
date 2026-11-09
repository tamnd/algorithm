# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simulated-annealing/. The authors are listed in prov/R8R2C0.jsonl.

import itertools
import math
import random

from simulated_annealing import (
    acceptance_probability,
    boltzmann,
    cycle_neighbors,
    geometric_schedule,
    logarithmic_schedule,
    metropolis_matrix,
    metropolis_visits,
    simulated_annealing,
    tour_length,
    two_opt_neighbor,
)

# The landscape of the page: 8 states on a cycle.
V = [3, 1, 4, 2, 5, 0, 3, 6]
NB = cycle_neighbors(8)


def step(x, rng):
    return rng.choice(NB[x])


def test_acceptance_formula() -> None:
    for t in (0.1, 0.5, 1.0, 2.0, 10.0):
        assert acceptance_probability(0, t) == 1.0
        assert acceptance_probability(-3.5, t) == 1.0
        for d in (0.25, 1.0, 2.0, 4.0):
            assert math.isclose(acceptance_probability(d, t), math.exp(-d / t), rel_tol=1e-15)
    assert acceptance_probability(1.0, 0.0) == 0.0
    assert math.isclose(acceptance_probability(2, 1), 0.1353352832366127)


def test_detailed_balance_and_stationarity() -> None:
    for t in (0.3, 1.0, 5.0):
        pi = boltzmann(V, t)
        p = metropolis_matrix(V, NB, t)
        for i in range(8):
            assert math.isclose(sum(p[i]), 1.0, abs_tol=1e-12)
            for j in range(8):
                assert abs(pi[i] * p[i][j] - pi[j] * p[j][i]) < 1e-15
        for j in range(8):
            assert abs(sum(pi[i] * p[i][j] for i in range(8)) - pi[j]) < 1e-14


def test_empirical_distribution_is_boltzmann() -> None:
    steps = 200_000
    counts = metropolis_visits(V, NB, 1.0, 0, steps, random.Random(1))
    pi = boltzmann(V, 1.0)
    tv = 0.5 * sum(abs(c / steps - p) for c, p in zip(counts, pi))
    assert tv < 0.02
    assert max(range(8), key=lambda i: counts[i]) == 5


def test_best_is_running_minimum() -> None:
    trace = []
    best, eb = simulated_annealing(0, lambda s: V[s], step, geometric_schedule(2.0, 0.9), 200, random.Random(3), trace)
    running = V[0]
    for _, _, e, b in trace:
        running = min(running, e)
        assert b == running
    assert eb == running == V[best]


def test_zero_temperature_never_goes_up() -> None:
    trace = []
    simulated_annealing(0, lambda s: V[s], step, lambda k: 0.0, 100, random.Random(4), trace)
    energies = [V[0]] + [e for _, _, e, _ in trace]
    assert all(b <= a for a, b in zip(energies, energies[1:]))


def test_reaches_global_minimum_of_the_cycle() -> None:
    best, eb = simulated_annealing(0, lambda s: V[s], step, geometric_schedule(5.0, 0.99), 1000, random.Random(0))
    assert (best, eb) == (5, 0)
    best, eb = simulated_annealing(0, lambda s: V[s], step, logarithmic_schedule(4.0), 1000, random.Random(0))
    assert (best, eb) == (5, 0)


def test_reaches_optimal_tour() -> None:
    rng = random.Random(3)
    n = 8
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    dist = [[math.dist(a, b) for b in pts] for a in pts]
    opt = min(tour_length((0,) + p, dist) for p in itertools.permutations(range(1, n)))
    tour, length = simulated_annealing(
        tuple(range(n)), lambda t: tour_length(t, dist), two_opt_neighbor, geometric_schedule(0.5, 0.998), 2000, random.Random(0)
    )
    assert sorted(tour) == list(range(n)) and tour[0] == 0
    assert math.isclose(length, opt, abs_tol=1e-12)
    assert math.isclose(tour_length(tour, dist), length, abs_tol=1e-12)
