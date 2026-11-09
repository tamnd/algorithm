# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-accepting/. The authors are listed in prov/89MGMB.jsonl.

import itertools
import math
import random

from threshold_accepting import linear_thresholds, threshold_accepting

V = [3, 1, 4, 2, 5, 0, 3, 6]
NB = [[(i - 1) % 8, (i + 1) % 8] for i in range(8)]


def step(x, rng):
    return rng.choice(NB[x])


def tour_length(t, dist):
    return sum(dist[t[i - 1]][t[i]] for i in range(len(t)))


def two_opt(t, rng):
    i, j = sorted(rng.sample(range(1, len(t)), 2))
    return t[:i] + t[i : j + 1][::-1] + t[j + 1 :]


def test_thresholds() -> None:
    assert linear_thresholds(4.0, 8) == [4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5]


def test_acceptance_rule_and_walk() -> None:
    for seed in range(20):
        trace = []
        best, fb = threshold_accepting(0, lambda s: V[s], step, linear_thresholds(4.0, 8), 7, random.Random(seed), trace)
        x = 0
        running = V[0]
        for tau, cur, y, fx, fy, acc in trace:
            assert cur == x and fx == V[x] and fy == V[y] and y in NB[x]
            assert acc == (fy - fx < tau)
            if acc:
                x = y
                running = min(running, V[x])
        assert fb == running == V[best]


def test_trap_that_needs_a_larger_threshold() -> None:
    # From state 1 every path to a lower state has a single rise of 3 or more.
    trace = []
    best, fb = threshold_accepting(1, lambda s: V[s], step, [3.0], 5000, random.Random(0), trace)
    assert (best, fb) == (1, 1)
    assert {y for _, _, y, _, _, acc in trace if acc} <= {0, 1}
    best, fb = threshold_accepting(1, lambda s: V[s], step, [3.5], 5000, random.Random(0))
    assert (best, fb) == (5, 0)


def test_small_threshold_is_descent() -> None:
    trace = []
    threshold_accepting(0, lambda s: V[s], step, [1e-9], 200, random.Random(5), trace)
    assert all(fy <= fx for _, _, _, fx, fy, acc in trace if acc)


def test_reaches_optimum() -> None:
    assert threshold_accepting(0, lambda s: V[s], step, linear_thresholds(4.0, 8), 5, random.Random(2)) == (5, 0)
    rng = random.Random(3)
    n = 8
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    dist = [[math.dist(a, b) for b in pts] for a in pts]
    opt = min(tour_length((0,) + p, dist) for p in itertools.permutations(range(1, n)))
    tour, length = threshold_accepting(
        tuple(range(n)), lambda t: tour_length(t, dist), two_opt, linear_thresholds(0.3, 10), 100, random.Random(0)
    )
    assert sorted(tour) == list(range(n))
    assert math.isclose(length, opt, abs_tol=1e-12)
