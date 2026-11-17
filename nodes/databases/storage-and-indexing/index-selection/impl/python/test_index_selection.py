# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-selection/. The authors are listed in prov/BFQ09A.jsonl.

import math
import random
from itertools import combinations

from index_selection import (Workload, best_of_greedy_and_single, brute_force,
                             from_knapsack, from_max_coverage, greedy)


def test_greedy_is_not_optimal_knapsack_case():
    wl = Workload([(1, 10), (1, 8), (1, 8)],
                  [("A", 6, 0), ("B", 5, 0), ("C", 5, 0)],
                  {(0, "A"): 1, (1, "B"): 1, (2, "C"): 1})
    g, order = greedy(wl, 10)
    assert order == ["A"] and wl.total(g) == 17 and wl.benefit(g) == 9
    opt = brute_force(wl, 10)
    assert opt == {"B", "C"} and wl.total(opt) == 12 and wl.benefit(opt) == 14


def db_example():
    queries = [(50, 100), (30, 100), (20, 100)]       # a = ?, a = ? and b = ?, c in range
    indexes = [("a", 4, 10), ("ab", 6, 10), ("c", 4, 10)]
    cost = {(0, "a"): 3, (0, "ab"): 3, (1, "a"): 10, (1, "ab"): 2, (2, "c"): 20}
    return Workload(queries, indexes, cost)


def test_greedy_is_not_optimal_database_case():
    wl = db_example()
    assert wl.total(set()) == 10000
    assert [wl.total({i}) for i in ("a", "ab", "c")] == [2460, 2220, 8410]
    g, order = greedy(wl, 10)
    assert order == ["a", "c"] and wl.total(g) == 870
    opt = brute_force(wl, 10)
    assert opt == {"ab", "c"} and wl.total(opt) == 630
    # with room for all three, the overlap makes "a" useless next to "ab"
    assert brute_force(wl, 14) == {"ab", "c"}


def random_workload(rng, nq, ni, maint):
    queries = [(rng.randint(1, 5), rng.randint(10, 60)) for _ in range(nq)]
    indexes = [(f"I{i}", rng.randint(1, 6), rng.randint(0, 20) if maint else 0) for i in range(ni)]
    cost = {}
    for q in range(nq):
        for i in range(ni):
            if rng.random() < 0.35:
                cost[(q, f"I{i}")] = rng.randint(0, 70)
    return Workload(queries, indexes, cost)


def exhaustive_min(wl, budget):
    return min(wl.total(s) for r in range(len(wl.names) + 1)
               for s in combinations(wl.names, r) if wl.used(s) <= budget)


def test_greedy_is_feasible_and_brute_force_is_optimal():
    rng = random.Random(97)
    for _ in range(300):
        wl = random_workload(rng, rng.randint(1, 6), rng.randint(0, 6), True)
        budget = rng.randint(0, 15)
        g, _ = greedy(wl, budget)
        b = brute_force(wl, budget)
        assert wl.used(g) <= budget and wl.used(b) <= budget
        assert wl.total(b) == exhaustive_min(wl, budget) <= wl.total(g) <= wl.total(set())


def test_knapsack_reduction():
    rng = random.Random(1978)
    for _ in range(200):
        n = rng.randint(0, 7)
        values = [rng.randint(1, 30) for _ in range(n)]
        sizes = [rng.randint(1, 10) for _ in range(n)]
        cap = rng.randint(0, 30)
        best = [0] * (cap + 1)                        # 0-1 knapsack by dynamic programming
        for v, s in zip(values, sizes):
            for c in range(cap, s - 1, -1):
                best[c] = max(best[c], best[c - s] + v)
        wl = from_knapsack(values, sizes)
        assert wl.benefit(brute_force(wl, cap)) == best[cap]
        # the better of greedy and the best single index is within a factor 2
        assert 2 * wl.benefit(best_of_greedy_and_single(wl, cap)) >= best[cap]


def test_max_coverage_reduction_and_greedy_bound():
    rng = random.Random(1998)
    for _ in range(200):
        n = rng.randint(1, 12)
        sets = [rng.sample(range(n), rng.randint(0, n)) for _ in range(rng.randint(1, 7))]
        k = rng.randint(1, len(sets))
        wl = from_max_coverage(n, sets)
        opt = max(len(set().union(*[set(sets[j]) for j in c]))
                  for c in combinations(range(len(sets)), k))
        assert wl.benefit(brute_force(wl, k)) == opt
        g, _ = greedy(wl, k)
        assert wl.benefit(g) >= (1 - 1 / math.e) * opt


def test_benefit_is_submodular_without_maintenance():
    rng = random.Random(5)
    for _ in range(100):
        wl = random_workload(rng, 5, 5, False)
        names = wl.names
        for _ in range(10):
            t = {i for i in names if rng.random() < 0.5}
            s = {i for i in t if rng.random() < 0.5}
            for i in names:
                if i in t:
                    continue
                gain_s = wl.benefit(s | {i}) - wl.benefit(s)
                gain_t = wl.benefit(t | {i}) - wl.benefit(t)
                assert gain_s >= gain_t >= 0
