# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neighbor-net/. The authors are listed in prov/DQBMCY.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from neighbor_net import circular_splits, design, find_ordering, neighbor_net, nnls, _solve


def metric_of(n, weighted):
    d = [[Fraction(0)] * n for _ in range(n)]
    for side, w in weighted.items():
        for i in range(n):
            for j in range(n):
                if (i in side) != (j in side):
                    d[i][j] += w
    return d


def canon(n, side):
    side = frozenset(side)
    return side if 0 not in side else frozenset(range(n)) - side


def is_circular_for(order, side):
    n = len(order)
    pos = [order.index(x) for x in range(n)]
    ps = sorted(pos[x] for x in side)
    # side is an interval of the circle if its positions, rotated, are consecutive
    gaps = sum(1 for t in range(len(ps)) if (ps[(t + 1) % len(ps)] - ps[t]) % n != 1)
    return len(ps) in (0, n) or gaps == 1


def objective(a, w, b):
    return sum(((sum(a[r][c] * w[c] for c in range(len(w))) - b[r]) ** 2 for r in range(len(b))), Fraction(0))


# The page example: pendants of weight 1, ab|cde of weight 3 and bc|ade of weight 2.
EXAMPLE = [
    [0, 4, 7, 5, 5],
    [4, 0, 5, 7, 7],
    [7, 5, 0, 4, 4],
    [5, 7, 4, 0, 2],
    [5, 7, 4, 2, 0],
]


def named(w):
    return {"".join(sorted("abcde"[x] for x in canon(5, s))): v for s, v in w.items()}


def test_example_order_and_weights():
    d = [[Fraction(x) for x in row] for row in EXAMPLE]
    order, w = neighbor_net(d)
    assert order == [0, 1, 2, 3, 4]
    assert named(w) == {"b": 1, "c": 1, "d": 1, "e": 1, "bcde": 1, "cde": 3, "bc": 2}


def test_example_perturbed():
    d = [[Fraction(x) for x in row] for row in EXAMPLE]
    d[0][2] = d[2][0] = Fraction(8)
    order, w = neighbor_net(d)
    assert order == [0, 1, 2, 3, 4]
    assert named(w) == {
        "b": Fraction(5, 8), "bc": Fraction(9, 4), "bcd": Fraction(1, 8), "bcde": 1, "c": 1,
        "cd": Fraction(1, 8), "cde": Fraction(13, 4), "d": Fraction(3, 4), "e": Fraction(3, 4),
    }


def test_small_inputs():
    assert neighbor_net([]) == ([], {})
    assert neighbor_net([[0]]) == ([0], {})
    order, w = neighbor_net([[0, 3], [3, 0]])
    assert order == [0, 1] and w == {frozenset([1]): 3}
    order, w = neighbor_net([[0, 3, 4], [3, 0, 5], [4, 5, 0]])
    assert {canon(3, s): v for s, v in w.items()} == {frozenset([1]): 2, frozenset([2]): 3, frozenset([1, 2]): 1}


def test_rejects_bad_matrix():
    with pytest.raises(ValueError):
        neighbor_net([[0, 1], [2, 0]])
    with pytest.raises(ValueError):
        neighbor_net([[1, 1], [1, 0]])


def test_circular_splits_count():
    for n in range(2, 8):
        s = circular_splits(list(range(n)))
        assert len(s) == len(set(s)) == n * (n - 1) // 2


def test_design_is_invertible():
    for n in range(2, 7):
        splits = circular_splits(list(range(n)))
        _, a = design(n, splits)
        sol = _solve([[Fraction(x) for x in row] for row in a], [Fraction(1)] * len(a))
        assert sol is not None


def test_nnls_against_subset_brute_force():
    rng = random.Random(7)
    for t in range(16):
        n = 5 if t < 3 else 4
        splits = circular_splits(list(range(n)))
        pairs, a = design(n, splits)
        b = [Fraction(rng.randint(0, 12)) for _ in pairs]
        w = nnls(a, b)
        assert all(x >= 0 for x in w)
        best = None
        cols = len(splits)
        for k in range(cols + 1):
            for sub in combinations(range(cols), k):
                if sub:
                    sol = _solve([[Fraction(sum(a[r][i] * a[r][j] for r in range(len(b)))) for j in sub] for i in sub],
                                 [sum((a[r][i] * b[r] for r in range(len(b))), Fraction(0)) for i in sub])
                    if sol is None or any(x < 0 for x in sol):
                        continue
                    z = [Fraction(0)] * cols
                    for t, i in enumerate(sub):
                        z[i] = sol[t]
                else:
                    z = [Fraction(0)] * cols
                val = objective(a, z, b)
                if best is None or val < best:
                    best = val
        assert objective(a, w, b) == best


def test_nnls_kkt():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(3, 6)
        splits = circular_splits(list(range(n)))
        pairs, a = design(n, splits)
        b = [Fraction(rng.randint(-3, 15)) for _ in pairs]
        w = nnls(a, b)
        for c in range(len(splits)):
            g = sum(a[r][c] * (b[r] - sum(a[r][t] * w[t] for t in range(len(w)))) for r in range(len(b)))
            assert g <= 0
            if w[c] > 0:
                assert g == 0


def random_circular(rng, n):
    perm = list(range(n))
    rng.shuffle(perm)
    weighted = {}
    for s in circular_splits(perm):
        if len(s) == 1 or len(s) == n - 1 or rng.random() < 0.5:
            weighted[canon(n, s)] = Fraction(rng.randint(1, 9), rng.choice([1, 2, 3]))
    return weighted


def test_circular_metric_is_recovered():
    rng = random.Random(2024)
    for _ in range(40):
        n = rng.randint(4, 7)
        weighted = random_circular(rng, n)
        d = metric_of(n, weighted)
        order, w = neighbor_net(d)
        assert sorted(order) == list(range(n))
        for s in weighted:
            assert is_circular_for(order, s)
        assert {canon(n, s): v for s, v in w.items()} == weighted


def test_tree_metric_is_recovered():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(4, 7)
        # random binary tree: join random pairs of clusters
        parts = [frozenset([i]) for i in range(n)]
        sides = set(parts)
        while len(parts) > 2:
            i, j = rng.sample(range(len(parts)), 2)
            new = parts[i] | parts[j]
            parts = [p for t, p in enumerate(parts) if t not in (i, j)] + [new]
            sides.add(new)
        weighted = {canon(n, s): Fraction(rng.randint(1, 6)) for s in sides if 0 < len(s) < n}
        d = metric_of(n, weighted)
        order, w = neighbor_net(d)
        assert {canon(n, s): v for s, v in w.items()} == weighted


def test_output_splits_are_circular_and_fit_is_best():
    rng = random.Random(99)
    for _ in range(30):
        n = rng.randint(4, 7)
        d = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = Fraction(rng.randint(1, 20))
        order, w = neighbor_net(d)
        assert sorted(order) == list(range(n))
        assert all(v > 0 for v in w.values())
        for s in w:
            assert is_circular_for(order, s)
        # the fit is no worse than all weights zero, a feasible point
        splits = circular_splits(order)
        pairs, a = design(n, splits)
        b = [d[i][j] for i, j in pairs]
        full = [w.get(s, Fraction(0)) for s in splits]
        assert objective(a, full, b) <= objective(a, [Fraction(0)] * len(splits), b)


def test_find_ordering_is_permutation_for_many_sizes():
    rng = random.Random(3)
    for n in range(1, 12):
        d = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = Fraction(rng.randint(1, 30))
        assert sorted(find_ordering(d)) == list(range(n))
