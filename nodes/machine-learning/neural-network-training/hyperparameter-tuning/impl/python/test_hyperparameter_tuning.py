# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperparameter-tuning/. The authors are listed in prov/47B9Z8.jsonl.

import math
import random
from fractions import Fraction as F

from hyperparameter_tuning import (
    bracket_budget,
    grid_search,
    hyperband,
    hyperband_schedule,
    max_bracket,
    prob_hit_top_fraction,
    random_search,
    successive_halving,
    successive_halving_schedule,
)


def test_hyperband_table_for_r_81_eta_3():
    sched = hyperband_schedule(81, 3)
    table = {s: [(n, int(r)) for n, r in rounds] for s, rounds in sched}
    assert table == {
        4: [(81, 1), (27, 3), (9, 9), (3, 27), (1, 81)],
        3: [(34, 3), (11, 9), (3, 27), (1, 81)],
        2: [(15, 9), (5, 27), (1, 81)],
        1: [(8, 27), (2, 81)],
        0: [(5, 81)],
    }
    budgets = [bracket_budget(rounds) for _, rounds in sched]
    assert budgets == [405, 363, 351, 378, 405]
    assert sum(budgets) == 1902
    assert all(b <= 5 * 81 for b in budgets)


def test_schedule_arithmetic_for_other_settings():
    for eta in (2, 3, 4):
        for r_max in range(1, 300, 7):
            s_max = max_bracket(r_max, eta)
            assert eta ** s_max <= r_max < eta ** (s_max + 1)
            big_b = (s_max + 1) * r_max
            for s, rounds in hyperband_schedule(r_max, eta):
                n, r = rounds[0]
                assert n == math.ceil(F(big_b, r_max) * F(eta ** s, s + 1))
                assert rounds[-1][1] == r_max
                assert bracket_budget(rounds) <= big_b + (s + 1) * r
            assert bracket_budget(hyperband_schedule(r_max, eta)[-1][1]) == big_b


def test_successive_halving_keeps_the_best_and_charges_the_schedule():
    rng = random.Random(1)
    quality = [rng.random() for _ in range(81)]
    calls = []

    def evaluate(c, r):
        calls.append(r)
        return quality[c] + 1 / float(r)

    rounds = successive_halving_schedule(81, F(1), 3, 4)
    best, loss, spent = successive_halving(list(range(81)), evaluate, rounds, 3)
    assert best == min(range(81), key=quality.__getitem__)
    assert spent == 405 == sum(calls)
    assert [calls.count(F(3) ** i) for i in range(5)] == [81, 27, 9, 3, 1]


def test_hyperband_spends_the_exact_budget_and_finds_a_good_configuration():
    rng = random.Random(2)

    def sample(g):
        return g.random()

    def evaluate(x, r):
        # True loss (x - 0.3)^2, observed with an error that shrinks with the resource.
        return (x - 0.3) ** 2 + 0.5 / float(r)

    best, loss, spent = hyperband(sample, evaluate, 81, 3, rng)
    assert spent == 1902
    assert abs(best - 0.3) < 0.05


def test_random_search_probability_and_simulation():
    p = prob_hit_top_fraction(F(1, 20), 60)
    assert abs(float(p) - 0.9539) < 1e-4
    rng = random.Random(3)
    hits = sum(any(rng.random() < 0.05 for _ in range(60)) for _ in range(4000))
    assert abs(hits / 4000 - float(p)) < 0.02


def test_random_search_covers_the_important_axis_better_than_grid():
    def evaluate(c):
        return (c["lr"] - 0.37) ** 2 + 0.001 * c["wd"]

    seen_grid = []
    grid_best = grid_search({"lr": [0.1, 0.5, 0.9], "wd": [0.1, 0.5, 0.9]},
                            lambda c: seen_grid.append(c["lr"]) or evaluate(c))
    seen_rand = []

    def sample(g):
        return {"lr": g.random(), "wd": g.random()}

    rand_best = random_search(sample, lambda c: seen_rand.append(c["lr"]) or evaluate(c), 9, random.Random(4))
    assert len(set(seen_grid)) == 3 and len(set(seen_rand)) == 9
    assert grid_best[0]["lr"] == 0.5
    assert rand_best[1] < grid_best[1]
