# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ant-colony-optimization/. The authors are listed in prov/H2R48A.jsonl.

import itertools
import math
import random
from fractions import Fraction

from ant_colony_optimization import (
    ant_colony_optimization,
    build_tour,
    choice_probabilities,
    choose,
    tour_length,
)


def instance(n: int, seed: int) -> list[list[float]]:
    r = random.Random(seed)
    pts = [(r.random(), r.random()) for _ in range(n)]
    return [[math.dist(p, q) for q in pts] for p in pts]


def brute_force(d: list[list[float]]) -> float:
    n = len(d)
    return min(tour_length(d, (0,) + p) for p in itertools.permutations(range(1, n)))


def nearest_neighbor_length(d: list[list[float]]) -> float:
    n = len(d)
    tour, left = [0], set(range(1, n))
    while left:
        j = min(left, key=lambda c: d[tour[-1]][c])
        tour.append(j)
        left.remove(j)
    return tour_length(d, tour)


def test_choice_probabilities_follow_the_formula() -> None:
    rng = random.Random(3)
    d = instance(7, 3)
    tau = [[rng.uniform(0.1, 2.0) for _ in range(7)] for _ in range(7)]
    for alpha, beta in ((1.0, 2.0), (2.0, 0.0), (0.5, 3.0)):
        cand = [1, 2, 4, 6]
        probs = choice_probabilities(0, cand, tau, d, alpha, beta)
        weights = [tau[0][j] ** alpha * d[0][j] ** (-beta) for j in cand]
        for p, wt in zip(probs, weights):
            assert math.isclose(p, wt / sum(weights), rel_tol=1e-12)
        assert math.isclose(sum(probs), 1.0, rel_tol=1e-12)


def test_choose_uses_the_prefix_intervals() -> None:
    probs = [Fraction(1, 6), Fraction(1, 2), Fraction(1, 3)]
    assert choose(probs, Fraction(0)) == 0
    assert choose(probs, Fraction(1, 6) - Fraction(1, 10**9)) == 0
    assert choose(probs, Fraction(1, 6)) == 1
    assert choose(probs, Fraction(2, 3) - Fraction(1, 10**9)) == 1
    assert choose(probs, Fraction(2, 3)) == 2
    rng = random.Random(4)
    counts = [0, 0, 0]
    trials = 30000
    for _ in range(trials):
        counts[choose([float(p) for p in probs], rng.random())] += 1
    for k in range(3):
        p = float(probs[k])
        assert abs(counts[k] / trials - p) < 5 * math.sqrt(p * (1 - p) / trials)


def test_ants_build_permutations() -> None:
    rng = random.Random(5)
    d = instance(9, 5)
    tau = [[1.0] * 9 for _ in range(9)]
    for _ in range(200):
        assert sorted(build_tour(tau, d, 1.0, 2.0, rng)) == list(range(9))


def test_pheromone_stays_within_the_bounds() -> None:
    d = instance(9, 6)
    rho = 0.1
    tau_max = 1 / (rho * nearest_neighbor_length(d))
    tau_min = tau_max / 18
    seen = []

    def check(t, tau, best, best_len):
        for i in range(9):
            for j in range(9):
                assert tau_min <= tau[i][j] <= tau_max
        seen.append(best_len)

    ant_colony_optimization(d, 8, 1.0, 2.0, rho, tau_max, tau_min, tau_max, 60, random.Random(6), check)
    assert len(seen) == 60
    assert all(seen[t + 1] <= seen[t] for t in range(59))


def test_without_clamps_pheromone_is_bounded_by_the_deposit() -> None:
    # tau_t <= (1 - rho) tau_(t-1) + 1 / L(best) and L(best) >= L*, so tau_t <= max(tau0, 1 / (rho L*)).
    d = instance(8, 7)
    opt = brute_force(d)
    rho, tau0 = 0.2, 0.3
    bound = max(tau0, 1 / (rho * opt))

    def check(t, tau, best, best_len):
        assert max(max(row) for row in tau) <= bound * (1 + 1e-12)
        assert min(min(row) for row in tau) >= 0

    ant_colony_optimization(d, 6, 1.0, 2.0, rho, tau0, 0.0, float("inf"), 80, random.Random(7), check)


def test_fixed_seed_finds_the_optimal_tour() -> None:
    for n, seed in ((8, 1), (9, 2)):
        d = instance(n, seed)
        opt = brute_force(d)
        rho = 0.1
        tau_max = 1 / (rho * nearest_neighbor_length(d))
        tour, length, hist = ant_colony_optimization(d, 10, 1.0, 2.0, rho, tau_max, tau_max / (2 * n), tau_max, 100, random.Random(0))
        assert sorted(tour) == list(range(n))
        assert math.isclose(length, tour_length(d, tour))
        assert math.isclose(length, opt, rel_tol=1e-12)
