# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdc-scheduling/. The authors are listed in prov/11PCP9.jsonl.

import itertools
import random
from fractions import Fraction

from sdc_scheduling import (build_constraints, is_valid, latency, least_solution, lp_max, occ, sdc_schedule)


def random_instance(rng: random.Random, max_n: int):
    n = rng.randint(2, max_n)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.35]
    lat = [rng.choice([0, 0, 1, 2]) for _ in range(n)]
    dly = [rng.randint(1, 3) for _ in range(n)]
    kind = [rng.choice("ab") for _ in range(n)]
    limits = {k: rng.randint(1, 2) for k in "ab" if rng.random() < 0.7}
    return n, edges, lat, dly, kind, limits, 4


def satisfies(cons, upper, s):
    return all(s[v] - s[u] >= w for (u, v, w) in cons) and all(s[v] <= upper[v] for v in range(len(s)))


def box(n, cons, upper):
    low = least_solution(n, cons)
    if low is None or any(low[v] > upper[v] for v in range(n)):
        return []
    return [p for p in itertools.product(*[range(low[v], upper[v] + 1) for v in range(n)]) if satisfies(cons, upper, p)]


def test_example_of_the_page():
    # v0 = a + b, v1 = v0 + c, v2 = v1 + d, v3 = v0 * e, v4 = f * g, v5 = v3 + v4
    n, edges = 6, [(0, 1), (1, 2), (0, 3), (3, 5), (4, 5)]
    lat, dly = [0, 0, 0, 2, 2, 0], [2, 2, 2, 0, 0, 2]
    kind = ["add", "add", "add", "mul", "mul", "add"]
    assert sdc_schedule(n, edges, lat, dly, kind, {}, 5) == [0, 0, 1, 0, 0, 2]
    s = sdc_schedule(n, edges, lat, dly, kind, {"mul": 1}, 5)
    assert s == [0, 0, 1, 0, 2, 4] and latency(lat, s) == 5
    assert is_valid(n, edges, lat, dly, kind, {"mul": 1}, 5, s)
    # ALAP-like schedule within 5 steps: maximize the sum of the starts.
    t = sdc_schedule(n, edges, lat, dly, kind, {"mul": 1}, 5, latency_bound=5, weights=[-1] * n)
    assert t == [0, 4, 4, 0, 2, 4]


def test_simplex_small_lp():
    # maximize 3x + 2y with x + y <= 4, x + 3y <= 6, x <= 3: optimum 11 at (3, 1)
    val, x = lp_max([3, 2], [[1, 1], [1, 3], [1, 0]], [4, 6, 3])
    assert val == 11 and x == [3, 1]
    # infeasible: x >= 2 and x <= 1
    assert lp_max([1], [[-1], [1]], [-2, 1]) is None


def test_lp_optimum_is_integral_and_matches_exhaustive_search():
    rng = random.Random(11)
    checked = 0
    for _ in range(120):
        n, edges, lat, dly, kind, limits, period = random_instance(rng, 5)
        cons, _ = build_constraints(n, edges, lat, dly, kind, limits, period)
        bound = latency(lat, least_solution(n, cons)) + rng.randint(0, 2)
        cons, upper = build_constraints(n, edges, lat, dly, kind, limits, period, bound)
        points = box(n, cons, upper)
        assert points
        w = [rng.randint(-3, 3) for _ in range(n)]
        s = sdc_schedule(n, edges, lat, dly, kind, limits, period, bound, weights=w)
        assert s is not None and satisfies(cons, upper, s)
        best = min(sum(a * b for a, b in zip(w, p)) for p in points)
        assert sum(a * b for a, b in zip(w, s)) == best
        checked += 1
    assert checked == 120


def test_least_solution_is_below_every_solution():
    rng = random.Random(12)
    for _ in range(80):
        n, edges, lat, dly, kind, limits, period = random_instance(rng, 5)
        cons, _ = build_constraints(n, edges, lat, dly, kind, limits, period)
        low = least_solution(n, cons)
        cons, upper = build_constraints(n, edges, lat, dly, kind, limits, period, latency(lat, low) + 1)
        for p in box(n, cons, upper):
            assert all(p[v] >= low[v] for v in range(n))


def test_chaining_constraints_are_exact():
    rng = random.Random(13)
    for _ in range(80):
        n, edges, lat, dly, kind, _, period = random_instance(rng, 6)
        cons, _ = build_constraints(n, edges, lat, dly, kind, {}, period)
        bound = latency(lat, least_solution(n, cons)) + 1
        upper = [bound - occ(lat, v) for v in range(n)]
        for p in itertools.product(*[range(0, upper[v] + 1) for v in range(n)]):
            assert satisfies(cons, upper, p) == is_valid(n, edges, lat, dly, kind, {}, period, list(p))


def exhaustive_latency(n, edges, lat, dly, kind, limits, period, start):
    cons, _ = build_constraints(n, edges, lat, dly, kind, {}, period)
    low = least_solution(n, cons)
    lam = latency(lat, low)
    while True:
        windows = [range(low[v], lam - occ(lat, v) + 1) for v in range(n)]
        for p in itertools.product(*windows):
            if is_valid(n, edges, lat, dly, kind, limits, period, list(p)):
                return lam
        lam += 1
        assert lam <= start


def test_resource_chains_are_sound_but_not_always_optimal():
    rng = random.Random(14)
    gaps = 0
    for _ in range(150):
        n, edges, lat, dly, kind, limits, period = random_instance(rng, 7)
        s = sdc_schedule(n, edges, lat, dly, kind, limits, period)
        assert s is not None
        assert is_valid(n, edges, lat, dly, kind, limits, period, s)
        opt = exhaustive_latency(n, edges, lat, dly, kind, limits, period, latency(lat, s))
        assert latency(lat, s) >= opt
        gaps += latency(lat, s) > opt
    assert gaps < 150


def test_infeasible_timing_constraint():
    # s1 - s0 >= 2 from the data edge, and a maximum timing constraint s1 - s0 <= 1.
    assert sdc_schedule(2, [(0, 1)], [2, 1], [0, 0], ["m", "m"], {}, 5, extra=[(1, 0, -1)]) is None


def test_latency_bound_too_small():
    assert sdc_schedule(3, [(0, 1), (1, 2)], [1, 1, 1], [0, 0, 0], "aaa", {}, 5, latency_bound=2) is None


def test_fraction_period():
    s = sdc_schedule(3, [(0, 1), (1, 2)], [0, 0, 0], [Fraction(3, 2)] * 3, "aaa", {}, Fraction(3))
    assert s == [0, 0, 1]
