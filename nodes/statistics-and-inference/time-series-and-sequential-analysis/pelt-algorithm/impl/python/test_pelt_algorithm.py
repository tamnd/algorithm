# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pelt-algorithm/. The authors are listed in prov/8P0SSC.jsonl.
import itertools
import math
import random
from fractions import Fraction

from pelt_algorithm import optimal_partitioning, pelt, rss_cost


def l1_cost(xs):
    """Sum of |x_i - median| over the segment: another cost with the PELT property for K = 0."""
    def cost(s, t):
        seg = sorted(xs[s:t])
        med = seg[(len(seg) - 1) // 2]
        return sum(abs(x - med) for x in seg)
    return cost


def penalized(cost, n, beta, cps):
    bounds = [0] + list(cps) + [n]
    return sum(cost(a, b) for a, b in zip(bounds, bounds[1:])) + beta * len(cps)


def brute_force(n, cost, beta):
    best = None
    for m in range(n):
        for cps in itertools.combinations(range(1, n), m):
            v = penalized(cost, n, beta, cps)
            if best is None or v < best:
                best = v
    return best


def test_worked_example():
    xs = [Fraction(v) for v in [1, 0, 1, 5, 6, 5, 6, 1, 0]]
    sizes = []
    value, cps = pelt(len(xs), rss_cost(xs), Fraction(4), sizes=sizes)
    assert value == Fraction(61, 6)
    assert cps == [3, 7]
    assert sizes == [1, 2, 3, 4, 2, 3, 4, 5, 2]


def test_edge_cases():
    xs = [Fraction(3)]
    assert pelt(1, rss_cost(xs), Fraction(1)) == (Fraction(0), [])
    xs = [Fraction(v) for v in [0, 0, 10, 10]]
    assert pelt(4, rss_cost(xs), Fraction(1))[1] == [2]
    assert pelt(4, rss_cost(xs), Fraction(1000))[1] == []
    # A zero penalty and a constant series: one segment still wins on ties.
    assert pelt(5, rss_cost([Fraction(2)] * 5), Fraction(0))[1] == []


def test_equals_optimal_partitioning_exact():
    rng = random.Random(2012)
    for trial in range(500):
        n = rng.randint(1, 30)
        xs = [Fraction(rng.randint(-5, 5)) + (Fraction(rng.randint(0, 3)) * 3 if (i // 7) % 2 else 0)
              for i in range(n)]
        beta = Fraction(rng.randint(0, 40), rng.randint(1, 4))
        cost = rss_cost(xs) if trial % 2 else l1_cost(xs)
        assert pelt(n, cost, beta) == optimal_partitioning(n, cost, beta)


def test_equals_brute_force_over_all_partitions():
    rng = random.Random(1989)
    for trial in range(200):
        n = rng.randint(1, 10)
        xs = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        beta = Fraction(rng.randint(0, 20), rng.randint(1, 3))
        cost = rss_cost(xs) if trial % 2 else l1_cost(xs)
        value, cps = pelt(n, cost, beta)
        assert value == brute_force(n, cost, beta)
        assert penalized(cost, n, beta, cps) == value


def test_smaller_k_is_exact_and_too_large_k_is_not():
    rng = random.Random(5)
    broken = 0
    for _ in range(100):
        n = rng.randint(1, 20)
        xs = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        beta = Fraction(rng.randint(1, 10))
        ref = optimal_partitioning(n, rss_cost(xs), beta)
        # K = -2 prunes less than the valid K = 0, so the answer stays exact.
        assert pelt(n, rss_cost(xs), beta, k=Fraction(-2)) == ref
        # K = 2 violates C(a..s) + C(s+1..b) + K <= C(a..b) for the RSS cost; it may prune the optimum.
        value = pelt(n, rss_cost(xs), beta, k=Fraction(2))[0]
        assert value >= ref[0]
        broken += value > ref[0]
    assert broken > 0


def test_pruning_keeps_candidate_sets_small_with_regular_changes():
    rng = random.Random(3)
    n = 2000
    xs = []
    mu = 0
    for i in range(n):
        if i % 100 == 0:
            mu = rng.choice([-2, -1, 0, 1, 2])
        xs.append(rng.gauss(mu, 1.0))
    sizes = []
    value, cps = pelt(n, rss_cost(xs), 2 * math.log(n), sizes=sizes)
    assert sum(sizes) / n < 150
    ref = optimal_partitioning(300, rss_cost(xs[:300]), 2 * math.log(n))
    assert abs(pelt(300, rss_cost(xs[:300]), 2 * math.log(n))[0] - ref[0]) < 1e-9
