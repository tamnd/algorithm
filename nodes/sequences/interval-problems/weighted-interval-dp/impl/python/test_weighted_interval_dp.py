# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-interval-dp/. The authors are listed in prov/YZT11N.jsonl.
import itertools
import random

from weighted_interval_dp import weighted_interval_dp

KINDS = ("closed", "half-open", "open")


def compatible(x, y, kind):
    a, b = (x, y) if x[0] <= y[0] else (y, x)
    if a[0] == b[0]:
        return False  # same left end: both contain points just right of it (or it)
    return a[1] < b[0] if kind == "closed" else a[1] <= b[0]


def feasible(jobs, idx, kind):
    return all(compatible(jobs[i], jobs[j], kind) for i, j in itertools.combinations(idx, 2))


def brute(jobs, kind):
    best = 0
    for size in range(1, len(jobs) + 1):
        for idx in itertools.combinations(range(len(jobs)), size):
            if feasible(jobs, idx, kind):
                best = max(best, sum(jobs[i][2] for i in idx))
    return best


def check(jobs, kind):
    value, chosen = weighted_interval_dp(jobs, kind)
    assert len(set(chosen)) == len(chosen)
    assert feasible(jobs, chosen, kind)
    assert sum(jobs[i][2] for i in chosen) == value
    assert value == brute(jobs, kind)
    return value, chosen


A, B, C, D, E, F = range(6)
EXAMPLE = [(0, 3, 2), (3, 6, 4), (1, 5, 5), (5, 8, 3), (6, 9, 4), (8, 10, 2)]


def test_example():
    assert check(EXAMPLE, "closed") == (9, [C, E])
    assert check(EXAMPLE, "half-open") == (10, [C, D, F])
    assert check(EXAMPLE, "open") == (10, [C, D, F])


def test_touching():
    jobs = [(1, 3, 1), (3, 5, 1)]
    assert check(jobs, "closed")[0] == 1
    assert check(jobs, "half-open") == (2, [0, 1])
    # equal right ends and a closed point interval at the touch
    jobs = [(0, 2, 3), (1, 2, 3), (2, 2, 4), (2, 4, 1)]
    assert check(jobs, "closed") == (4, [2])  # every pair shares the point 2
    assert check([(0, 2, 3), (1, 2, 3), (2, 4, 1)], "half-open")[0] == 4


def test_edge_cases():
    assert weighted_interval_dp([]) == (0, [])
    assert weighted_interval_dp([(0, 1, 5)]) == (5, [0])
    # all overlap: the heaviest
    assert check([(0, 10, 1), (1, 9, 7), (2, 8, 3)], "closed") == (7, [1])
    # all disjoint: all of them
    assert check([(4, 5, 1), (0, 1, 1), (2, 3, 1)], "closed") == (3, [1, 2, 0])


def test_greedy_counterexamples():
    # earliest finish time and largest weight first both fail on the example
    assert check(EXAMPLE, "closed")[0] > 2 + 3
    assert check(EXAMPLE, "half-open")[0] > 5 + 4


def test_random_against_brute_force():
    rng = random.Random(549)
    for _ in range(700):
        kind = rng.choice(KINDS)
        n = rng.randint(0, 9)
        jobs = []
        for _ in range(n):
            l = rng.randint(0, 12)
            r = l + rng.randint(0 if kind == "closed" else 1, 5)
            jobs.append((l, r, rng.randint(1, 9)))
        check(jobs, kind)
