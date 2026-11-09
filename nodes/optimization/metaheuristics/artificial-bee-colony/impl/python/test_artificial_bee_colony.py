# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/artificial-bee-colony/. The authors are listed in prov/DVD07D.jsonl.

import math
import random

from artificial_bee_colony import abc_fitness, artificial_bee_colony, neighbor, rastrigin, roulette, sphere


def test_fitness_transform() -> None:
    assert abc_fitness(0.0) == 1.0
    assert abc_fitness(3.0) == 0.25
    assert abc_fitness(-2.0) == 3.0
    values = [-5.0, -1.0, -1e-9, 0.0, 1e-9, 0.5, 2.0, 100.0]
    fits = [abc_fitness(v) for v in values]
    assert all(a > b for a, b in zip(fits, fits[1:]))
    # The pitfall of the page: below about 1e-16, 1 / (1 + f) rounds to 1.0.
    assert abc_fitness(1e-17) == abc_fitness(0.0)


def test_neighbor_changes_one_coordinate() -> None:
    x = [[1.0, 2.0, 3.0], [0.0, -1.0, 4.0], [2.0, 2.0, 2.0]]
    lo, hi = [-5.0] * 3, [5.0] * 3
    v = neighbor(x, 0, 1, 1, 0.5, lo, hi)
    assert v == [1.0, 2.0 + 0.5 * (2.0 - (-1.0)), 3.0]
    assert neighbor(x, 0, 1, 1, -1.0, lo, hi) == [1.0, -1.0, 3.0]
    assert neighbor(x, 1, 0, 2, 1.0, lo, hi) == [0.0, -1.0, 5.0]  # 4 + (4 - 3) = 5, at the bound
    assert neighbor(x, 1, 2, 2, 1.0, lo, hi) == [0.0, -1.0, 5.0]  # 4 + (4 - 2) = 6, clipped to 5
    assert x[0] == [1.0, 2.0, 3.0]


def test_roulette_intervals_and_frequencies() -> None:
    w = [abc_fitness(v) for v in (0.0, 1.0, 3.0)]  # 1, 1/2, 1/4, total 7/4
    assert roulette(w, 0.0) == 0
    assert roulette(w, 4 / 7 - 1e-12) == 0
    assert roulette(w, 4 / 7 + 1e-12) == 1
    assert roulette(w, 6 / 7 + 1e-12) == 2
    rng = random.Random(1)
    trials = 30000
    counts = [0, 0, 0]
    for _ in range(trials):
        counts[roulette(w, rng.random())] += 1
    for k, p in enumerate((4 / 7, 2 / 7, 1 / 7)):
        assert abs(counts[k] / trials - p) < 5 * math.sqrt(p * (1 - p) / trials)


def test_greedy_trials_and_scouts() -> None:
    sources, limit = 8, 15
    prev = {}
    log = []

    def check(c, x, fx, trial, scout):
        if scout < 0:
            assert max(trial) <= limit  # no scout only if no source is over the limit
        for i in range(sources):
            assert math.isclose(fx[i], rastrigin(x[i]), abs_tol=0)
            if i == scout:
                # One cycle gives a source at most 1 + sources tries.
                assert trial[i] == 0 and prev["trial"][i] + 1 + sources > limit
                continue
            if prev:
                if x[i] == prev["x"][i]:
                    assert fx[i] == prev["fx"][i] and trial[i] >= prev["trial"][i] + 1
                else:
                    assert fx[i] < prev["fx"][i] and trial[i] <= sources + 1
        log.append(scout)
        prev.update(x=x, fx=fx, trial=trial)

    _, best_f, hist = artificial_bee_colony(rastrigin, [-5.12] * 3, [5.12] * 3, sources, limit, 200, random.Random(2), check)
    assert any(s >= 0 for s in log)
    assert all(hist[c + 1] <= hist[c] for c in range(len(hist) - 1))
    assert best_f == hist[-1]


def test_fixed_seed_on_sphere_and_rastrigin() -> None:
    best, bf, _ = artificial_bee_colony(sphere, [-5.12] * 5, [5.12] * 5, 20, 100, 500, random.Random(0))
    assert bf < 1e-15 and math.isclose(bf, sphere(best))
    best, bf, _ = artificial_bee_colony(rastrigin, [-5.12] * 5, [5.12] * 5, 20, 100, 500, random.Random(0))
    assert bf < 1e-12 and all(abs(v) < 1e-6 for v in best)
