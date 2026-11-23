# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/propose-test-release/. The authors are listed in prov/DV793R.jsonl.

import itertools
import math
import random

import dpkit
from propose_test_release import (
    distance_to_instability,
    laplace_noise,
    median,
    pass_probability,
    propose_test_release_median,
)


def _local_sensitivity(xs, lam):
    # Brute force: replace one value by 0 or lam (the extremes move the median the most).
    med = median(xs)
    best = 0.0
    for i in range(len(xs)):
        for v in (0, lam):
            ys = list(xs)
            ys[i] = v
            best = max(best, abs(median(ys) - med))
    return best


def _bfs_distance(xs, b, lam):
    # Breadth-first search over the multisets of the grid {0..lam}^n, one replacement for each step.
    start = tuple(sorted(xs))
    seen = {start}
    frontier = [start]
    dist = 0
    while frontier:
        if any(_local_sensitivity(y, lam) > b for y in frontier):
            return float(dist)
        nxt = []
        for y in frontier:
            for i in range(len(y)):
                for v in range(lam + 1):
                    z = tuple(sorted(y[:i] + (v,) + y[i + 1:]))
                    if z not in seen:
                        seen.add(z)
                        nxt.append(z)
        frontier = nxt
        dist += 1
    return math.inf


def test_distance_matches_breadth_first_search() -> None:
    count = 0
    for n in (1, 3, 5):
        for lam in (1, 2, 4):
            for xs in itertools.combinations_with_replacement(range(lam + 1), n):
                for b in (0, 0.5, 1, 2, lam):
                    assert distance_to_instability(xs, b, lam) == _bfs_distance(xs, b, lam)
                    count += 1
    assert count >= 500


def test_distance_has_sensitivity_one() -> None:
    rng = random.Random(1)
    for _ in range(500):
        n, lam = rng.choice([3, 5, 9, 21]), 30
        b = rng.choice([1, 2, 4, 8])
        xs = [rng.randrange(lam + 1) for _ in range(n)]
        ys = list(xs)
        ys[rng.randrange(n)] = rng.randrange(lam + 1)
        assert abs(distance_to_instability(xs, b, lam) - distance_to_instability(ys, b, lam)) <= 1


def test_distance_zero_means_unstable() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n, lam = rng.choice([1, 3, 5, 7]), 10
        b = rng.choice([0.5, 1, 3])
        xs = [rng.randrange(lam + 1) for _ in range(n)]
        assert (distance_to_instability(xs, b, lam) == 0) == (_local_sensitivity(xs, lam) > b)


def _output_law(xs, lam, b, epsilon, delta, grid, h):
    # The exact law of the output: the mass of "no answer" and the density on a grid times h.
    p = pass_probability(distance_to_instability(xs, b, lam), epsilon, delta)
    c, s = median(xs), b / epsilon
    return 1.0 - p, [p * h * math.exp(-abs(z - c) / s) / (2 * s) for z in grid]


def test_two_epsilon_delta_dp_by_hockey_stick() -> None:
    # Vadhan Proposition 3.2: (2 epsilon, delta)-DP. The proof gives delta/2; we check delta/2.
    lam, b, epsilon, delta = 4, 1.0, 0.5, 0.1
    h = 0.05
    grid = [-40 + h * (i + 0.5) for i in range(int(84 / h))]
    universe = range(lam + 1)
    laws = {}
    for xs in itertools.combinations_with_replacement(universe, 3):
        laws[xs] = _output_law(xs, lam, b, epsilon, delta, grid, h)
    worst = 0.0
    worst_one = 0.0
    for xs in laws:
        for ys in dpkit.neighbors_replace(xs, universe):
            ys = tuple(sorted(ys))
            (bx, dx), (by, dy) = laws[xs], laws[ys]
            for eps, store in ((2 * epsilon, "two"), (epsilon, "one")):
                e = math.exp(eps)
                hs = max(0.0, bx - e * by) + sum(max(0.0, a - e * c) for a, c in zip(dx, dy))
                if store == "two":
                    worst = max(worst, hs)
                else:
                    worst_one = max(worst_one, hs)
            assert bx <= math.exp(epsilon) * by + 1e-12
    assert worst <= delta / 2 + 1e-3
    assert worst_one > worst  # the test and the release each spend epsilon


def test_pass_probability_formula_and_sampling() -> None:
    rng = random.Random(3)
    xs = [rng.randrange(101) for _ in range(31)]
    for b, epsilon, delta in ((10, 1.0, 1e-3), (20, 0.5, 1e-2), (40, 1.0, 1e-6)):
        p = pass_probability(distance_to_instability(xs, b, 100), epsilon, delta)
        n = 3000
        hits = sum(propose_test_release_median(xs, 100, b, epsilon, delta, rng) is not None for _ in range(n))
        assert abs(hits / n - p) <= dpkit.hoeffding_margin(n, 1e-6)


def test_released_value_is_median_plus_laplace() -> None:
    rng = random.Random(4)
    xs = list(range(51))  # distance 25 to instability for b = 30, so the test passes
    outs = [propose_test_release_median(xs, 100, 30, 1.0, 1e-6, rng) for _ in range(3000)]
    assert all(o is not None for o in outs)
    n = len(outs)
    frac = sum(abs(o - 25) > 30 for o in outs) / n
    assert abs(frac - math.exp(-1.0)) <= dpkit.hoeffding_margin(n, 1e-6)


def test_example_values() -> None:
    xs = list(range(101))
    got = [(b, distance_to_instability(xs, b, 100)) for b in (5, 10, 15, 20, 30)]
    assert got == [(5, 5), (10, 10), (15, 15), (20, 20), (30, 30)]
    probs = [pass_probability(g, 1.0, 1e-6) for _, g in got]
    assert probs[0] < 1e-4 and 0.010 < probs[1] < 0.012 and 0.84 < probs[2] < 0.85
    assert probs[3] > 0.998 and probs[4] > 0.999999
    assert distance_to_instability(xs, 100, 100) == math.inf


def test_laplace_tail() -> None:
    rng = random.Random(5)
    n = 20000
    frac = sum(abs(laplace_noise(2.0, rng)) > 3.0 for _ in range(n)) / n
    assert abs(frac - math.exp(-1.5)) <= dpkit.hoeffding_margin(n, 1e-6)


def test_bad_parameters() -> None:
    rng = random.Random(6)
    for args in (([1], 1, 1.0, 0.0, 0.1), ([1], 1, 1.0, 1.0, 0.0), ([1], 1, 0.0, 1.0, 0.1), ([1, 2], 2, 1.0, 1.0, 0.1)):
        try:
            propose_test_release_median(*args, rng)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
