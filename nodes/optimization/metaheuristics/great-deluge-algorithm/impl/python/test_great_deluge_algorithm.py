# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/great-deluge-algorithm/. The authors are listed in prov/HPWTJM.jsonl.

import itertools
import math
import random

from great_deluge_algorithm import great_deluge

V = [3, 1, 4, 2, 5, 0, 3, 6]
NB = [[(i - 1) % 8, (i + 1) % 8] for i in range(8)]


def step(x, rng):
    return rng.choice(NB[x])


def tour_length(t, dist):
    return sum(dist[t[i - 1]][t[i]] for i in range(len(t)))


def two_opt(t, rng):
    i, j = sorted(rng.sample(range(1, len(t)), 2))
    return t[:i] + t[i : j + 1][::-1] + t[j + 1 :]


def test_acceptance_rule_and_level() -> None:
    for seed in range(20):
        trace = []
        best, fb = great_deluge(0, lambda s: V[s], step, 6.5, 0.25, 300, random.Random(seed), trace)
        x, level, running = 0, 6.5, V[0]
        for lv, cur, y, fx, fy, acc in trace:
            assert lv == level and cur == x and fx == V[x] and fy == V[y] and y in NB[x]
            assert acc == (fy < level)
            if acc:
                x = y
                level -= 0.25
                running = min(running, V[x])
        assert fb == running == V[best]


def test_number_of_acceptances_is_bounded() -> None:
    # Each acceptance needs f(y) < level and lowers the level by rain, and f(y) >= f* = 0.
    for rain in (1.0, 0.5, 0.25, 0.1):
        bound = math.ceil((6.5 - 0) / rain)
        for seed in range(30):
            trace = []
            great_deluge(0, lambda s: V[s], step, 6.5, rain, 3000, random.Random(seed), trace)
            accepted = [t for t in trace if t[5]]
            assert len(accepted) <= bound
            # After the first acceptance, the current value is below level + rain.
            seen = False
            for lv, _, _, fx, _, acc in trace:
                if seen:
                    assert fx < lv + rain
                seen = seen or acc


def test_level_set_trap() -> None:
    # With the level at 4, the states with f < 4 near state 1 are {0, 1}; states 7 and 2 have f >= 4.
    trace = []
    best, fb = great_deluge(1, lambda s: V[s], step, 4.0, 1e-6, 2000, random.Random(0), trace)
    assert (best, fb) == (1, 1)
    assert {y for _, _, y, _, _, acc in trace if acc} <= {0, 1}


def test_reaches_optimum() -> None:
    assert great_deluge(0, lambda s: V[s], step, 6.5, 0.01, 20000, random.Random(0)) == (5, 0)
    rng = random.Random(3)
    n = 8
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    dist = [[math.dist(a, b) for b in pts] for a in pts]
    opt = min(tour_length((0,) + p, dist) for p in itertools.permutations(range(1, n)))
    t0 = tuple(range(n))
    tour, length = great_deluge(t0, lambda t: tour_length(t, dist), two_opt, tour_length(t0, dist), 0.01, 20000, random.Random(0))
    assert sorted(tour) == list(range(n))
    assert math.isclose(length, opt, abs_tol=1e-12)
