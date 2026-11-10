# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meyerson-algorithm/. The authors are listed in prov/DW570S.jsonl.

import itertools
import math
import random
from fractions import Fraction

from meyerson_algorithm import meyerson


def exact_expected_cost(points, dist, f):
    """Exact expected cost of Meyerson's rule, by enumeration of all coin flips."""
    total = Fraction(0)
    stack = [(0, (), Fraction(1), Fraction(0))]
    while stack:
        i, fac, prob, cost = stack.pop()
        if i == len(points):
            total += prob * cost
            continue
        p = points[i]
        if not fac:
            stack.append((i + 1, fac + (p,), prob, cost + f))
            continue
        delta = min(dist(p, q) for q in fac)
        q_open = min(Fraction(delta) / f, Fraction(1))
        if q_open > 0:
            stack.append((i + 1, fac + (p,), prob * q_open, cost + f))
        if q_open < 1:
            stack.append((i + 1, fac, prob * (1 - q_open), cost + delta))
    return total


def opt_cost(points, sites, dist, f):
    """Optimal offline cost with facilities at any subset of the sites."""
    best = None
    for r in range(1, len(sites) + 1):
        for S in itertools.combinations(sites, r):
            c = f * r + sum(min(dist(p, s) for s in S) for p in points)
            if best is None or c < best:
                best = c
    return best


def graph_metric(rng, n):
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for v in range(1, n):
        u = rng.randrange(v)
        d[u][v] = d[v][u] = min(d[u][v], rng.randint(1, 10))
    for _ in range(rng.randint(0, n) if n >= 2 else 0):
        u, v = rng.sample(range(n), 2)
        d[u][v] = d[v][u] = min(d[u][v], rng.randint(1, 10))
    for x in range(n):
        for u in range(n):
            for v in range(n):
                if d[u][x] + d[x][v] < d[u][v]:
                    d[u][v] = d[u][x] + d[x][v]
    return d


def adversarial_bound(n):
    return max(2 + 2 * math.ceil(math.log2(n)), 8) if n > 1 else 8


def line_opt(xs, f):
    """Exact optimum on a line: clusters are intervals with a facility at a median."""
    xs = sorted(xs)
    n = len(xs)
    pre = [0]
    for x in xs:
        pre.append(pre[-1] + x)

    def interval(i, j):
        m = (i + j) // 2
        left = xs[m] * (m - i) - (pre[m] - pre[i])
        right = (pre[j + 1] - pre[m + 1]) - xs[m] * (j - m)
        return f + left + right

    best = [0] + [None] * n
    for j in range(1, n + 1):
        best[j] = min(best[i] + interval(i, j - 1) for i in range(j))
    return best[n]


def test_example() -> None:
    pos = {"a": 0, "b": 1, "c": 3, "d": 10}
    dist = lambda p, q: abs(pos[p] - pos[q])
    points = ["a", "b", "c", "d"]
    e = exact_expected_cost(points, dist, Fraction(4))
    assert e == Fraction(213, 16)
    assert opt_cost(points, list(pos), dist, 4) == 11
    rng = random.Random(0)
    cost, fac, served = meyerson(points, dist, 4, rng)
    assert fac[0] == "a" and "d" in fac and len(served) == 4


def test_expected_cost_adversarial_order() -> None:
    rng = random.Random(2001)
    for _ in range(150):
        N = rng.randint(1, 7)
        d = graph_metric(rng, N)
        dist = lambda p, q: d[p][q]
        n = rng.randint(1, 7)
        points = [rng.randrange(N) for _ in range(n)]
        f = Fraction(rng.randint(1, 30), rng.randint(1, 3))
        e = exact_expected_cost(points, dist, f)
        opt = opt_cost(points, list(range(N)), dist, f)
        assert e >= opt
        assert e <= adversarial_bound(n) * opt


def test_expected_cost_random_order() -> None:
    rng = random.Random(8)
    for _ in range(40):
        N = rng.randint(1, 6)
        d = graph_metric(rng, N)
        dist = lambda p, q: d[p][q]
        n = rng.randint(1, 5)
        points = [rng.randrange(N) for _ in range(n)]
        f = Fraction(rng.randint(1, 20), rng.randint(1, 2))
        perms = list(itertools.permutations(points))
        avg = sum(exact_expected_cost(list(p), dist, f) for p in perms) / len(perms)
        assert avg <= 8 * opt_cost(points, list(range(N)), dist, f)


def test_seeded_trials_on_a_line() -> None:
    gen = random.Random(5)
    xs = [gen.randint(0, 1000) for _ in range(300)]
    f = 200
    opt = line_opt(xs, f)
    dist = lambda p, q: abs(p - q)
    costs = [meyerson(xs, dist, f, random.Random(seed))[0] for seed in range(100)]
    assert all(c >= opt for c in costs)
    assert sum(costs) / len(costs) <= adversarial_bound(len(xs)) * opt
    order = list(xs)
    shuffled = []
    for seed in range(100):
        r = random.Random(1000 + seed)
        r.shuffle(order)
        shuffled.append(meyerson(order, dist, f, r)[0])
    assert sum(shuffled) / len(shuffled) <= 8 * opt


def test_monte_carlo_matches_exact() -> None:
    pos = [0, 2, 3, 7, 8, 15]
    dist = lambda p, q: abs(p - q)
    f = 5
    exact = exact_expected_cost(pos, dist, Fraction(f))
    trials = [meyerson(pos, dist, f, random.Random(s))[0] for s in range(4000)]
    mean = sum(trials) / len(trials)
    assert abs(mean - float(exact)) < 0.05 * float(exact)


def test_edges() -> None:
    dist = lambda p, q: abs(p - q)
    assert meyerson([], dist, 3, random.Random(1)) == (0, [], [])
    cost, fac, _ = meyerson([4, 4, 4], dist, 3, random.Random(1))
    assert (cost, fac) == (3, [4])
    cost, fac, _ = meyerson([0, 10, 20], dist, 3, random.Random(1))
    assert (cost, fac) == (9, [0, 10, 20])
    try:
        meyerson([1], dist, 0, random.Random(1))
    except ValueError:
        pass
    else:
        raise AssertionError("the facility cost must be positive")
