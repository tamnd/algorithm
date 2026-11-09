# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-knapsack/. The authors are listed in prov/V5J5TR.jsonl.

import random
from fractions import Fraction as Fr

from multi_objective_knapsack import knapsack_front


def beats(u, v) -> bool:
    """u dominates v for maximization."""
    return all(a >= b for a, b in zip(u, v)) and tuple(u) != tuple(v)


def all_subsets(weights, profits, capacity):
    n = len(weights)
    p = len(profits[0]) if n else 0
    out = []
    for mask in range(1 << n):
        w = sum(weights[j] for j in range(n) if mask >> j & 1)
        if w <= capacity:
            v = tuple(sum(profits[j][i] for j in range(n) if mask >> j & 1) for i in range(p))
            out.append((v, mask))
    return out


def brute_front(weights, profits, capacity):
    """Check all pairs of feasible profit vectors."""
    vs = {v for v, _ in all_subsets(weights, profits, capacity)}
    return sorted(v for v in vs if not any(beats(u, v) for u in vs))


def check_masks(weights, profits, capacity, result):
    for v, mask in result:
        assert sum(weights[j] for j in range(len(weights)) if mask >> j & 1) <= capacity
        got = tuple(
            sum(profits[j][i] for j in range(len(weights)) if mask >> j & 1)
            for i in range(len(v))
        )
        assert got == v


def test_example() -> None:
    weights = [2, 3, 4, 5]
    profits = [(5, 1), (4, 3), (2, 6), (1, 8)]
    res = knapsack_front(weights, profits, 8)
    assert [v for v, _ in res] == [(5, 11), (6, 9), (7, 7), (9, 4)]
    assert dict(res)[(5, 11)] == 0b1010
    check_masks(weights, profits, 8, res)
    # (7, 7) and (6, 9) lie below the segment from (9, 4) to (5, 11): no
    # positive weighted sum finds them.
    for a in range(1, 30):
        for b in range(1, 30):
            vals = {v: a * v[0] + b * v[1] for v, _ in res}
            best = max(vals.values())
            assert vals[(7, 7)] < best and vals[(6, 9)] < best


def test_random_against_all_subsets() -> None:
    rng = random.Random(2009)
    for trial in range(300):
        n = rng.randint(0, 10)
        p = rng.randint(1, 3)
        hi = rng.choice([3, 10, 50])
        weights = [rng.randint(0, hi) for _ in range(n)]
        profits = [tuple(rng.randint(0, hi) for _ in range(p)) for _ in range(n)]
        if n == 0:
            profits = [tuple(0 for _ in range(p))]
            weights = [0]
        capacity = rng.randint(0, max(1, sum(weights)))
        res = knapsack_front(weights, profits, capacity)
        assert [v for v, _ in res] == brute_front(weights, profits, capacity), trial
        check_masks(weights, profits, capacity, res)


def test_fractions() -> None:
    weights = [Fr(1, 2), Fr(1, 3), Fr(1, 4)]
    profits = [(1, Fr(1, 2)), (Fr(1, 3), 1), (Fr(1, 2), Fr(1, 2))]
    for cap in [Fr(0), Fr(1, 3), Fr(7, 12), Fr(5, 6), Fr(1)]:
        res = knapsack_front(weights, profits, cap)
        assert [v for v, _ in res] == brute_front(weights, profits, cap)


def pairs_instance(k):
    """2^k nondominated points: two items of weight 2^i for each i, with the
    profits (2^i, 0) and (0, 2^i), and the capacity 2^k - 1."""
    weights, profits = [], []
    for i in range(k):
        weights += [2 ** i, 2 ** i]
        profits += [(2 ** i, 0), (0, 2 ** i)]
    return weights, profits, 2 ** k - 1


def test_exponential_front() -> None:
    for k in range(1, 6):
        weights, profits, cap = pairs_instance(k)
        res = knapsack_front(weights, profits, cap)
        assert [v for v, _ in res] == [(s, 2 ** k - 1 - s) for s in range(2 ** k)]
    weights, profits, cap = pairs_instance(4)
    assert [v for v, _ in knapsack_front(weights, profits, cap)] == brute_front(weights, profits, cap)


def test_scalarizations_find_front_points() -> None:
    rng = random.Random(77)
    for _ in range(150):
        n = rng.randint(1, 9)
        weights = [rng.randint(1, 9) for _ in range(n)]
        profits = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)]
        cap = rng.randint(0, sum(weights))
        front = [v for v, _ in knapsack_front(weights, profits, cap)]
        feas = [v for v, _ in all_subsets(weights, profits, cap)]
        # A weighted sum with positive weights is maximized only at front points.
        for lam in [(1, 1), (1, 4), (5, 2)]:
            best = max(lam[0] * v[0] + lam[1] * v[1] for v in feas)
            assert {v for v in feas if lam[0] * v[0] + lam[1] * v[1] == best} <= set(front)
        # Each front point is an optimum of the epsilon-constraint problem
        # max y1 subject to y2 >= its own y2, and the only optimum with the
        # largest y2 among the optima.
        for y in front:
            sub = [v for v in feas if v[1] >= y[1]]
            top = max(v[0] for v in sub)
            assert top == y[0]
            assert max(v[1] for v in sub if v[0] == top) == y[1]
