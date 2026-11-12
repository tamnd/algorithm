# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dendrogram/. The authors are listed in prov/2GBS7F.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from dendrogram import Dendrogram

EX = [0, 2, 3, 7, 13, 21]
SINGLE = [(1, 2, 1), (0, 6, 2), (3, 7, 4), (4, 8, 6), (5, 9, 8)]
COMPLETE = [(1, 2, 1), (0, 6, 3), (3, 4, 6), (7, 8, 13), (5, 9, 21)]


def line(xs):
    return [[abs(a - b) for b in xs] for a in xs]


def lca_height(t, i, j):
    up = set()
    v = i
    while v >= 0:
        up.add(v)
        v = t.parent[v]
    v = j
    while v not in up:
        v = t.parent[v]
    return t.height[v], v


def is_ultrametric(u):
    n = len(u)
    return all(u[x][z] <= max(u[x][y], u[y][z]) for x in range(n) for y in range(n) for z in range(n))


def matrices(n, values):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for vals in itertools.product(values, repeat=len(pairs)):
        m = [[0] * n for _ in range(n)]
        for (i, j), v in zip(pairs, vals):
            m[i][j] = m[j][i] = v
        yield m


def monotone_dendrograms(n, values):
    """Every merge order with non-decreasing heights from values."""

    def rec(roots, nxt, last, merges):
        if len(roots) == 1:
            yield list(merges)
            return
        for a, b in itertools.combinations(sorted(roots), 2):
            for h in values:
                if h >= last:
                    merges.append((a, b, h))
                    yield from rec((roots - {a, b}) | {nxt}, nxt + 1, h, merges)
                    merges.pop()

    yield from rec(frozenset(range(n)), n, values[0], [])


def frozen(m):
    return tuple(tuple(r) for r in m)


def threshold_partition(u, t):
    """Classes of the relation u(i, j) <= t, numbered by smallest point."""
    n = len(u)
    labels = [-1] * n
    c = 0
    for i in range(n):
        if labels[i] < 0:
            for j in range(n):
                if j == i or u[i][j] <= t:
                    labels[j] = c
            c += 1
    return labels


def naive_single_cophenetic(d):
    """Minimax path distance by Floyd-Warshall."""
    n = len(d)
    u = [row[:] for row in d]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                u[i][j] = min(u[i][j], max(u[i][k], u[k][j]))
    for i in range(n):
        u[i][i] = 0
    return u


def binary_trees(items):
    items = tuple(items)
    if len(items) == 1:
        yield items[0]
        return
    first, rest = items[0], items[1:]
    for r in range(0, len(rest)):
        for extra in itertools.combinations(rest, r):
            a = (first,) + extra
            b = tuple(x for x in rest if x not in extra)
            for ta in binary_trees(a):
                for tb in binary_trees(b):
                    yield (ta, tb)


def to_merges(tree, n):
    merges = []

    def rec(t):
        if isinstance(t, int):
            return t, 1
        a, sa = rec(t[0])
        b, sb = rec(t[1])
        merges.append((a, b, sa + sb))
        return n + len(merges) - 1, sa + sb

    rec(tree)
    return merges


def leaves_of(t):
    return [t] if isinstance(t, int) else leaves_of(t[0]) + leaves_of(t[1])


def lca_cost(tree, w):
    """Sum over pairs of w(i, j) times the number of leaves under their lca."""
    if isinstance(tree, int):
        return 0
    la, lb = leaves_of(tree[0]), leaves_of(tree[1])
    here = (len(la) + len(lb)) * sum(w[i][j] for i in la for j in lb)
    return here + lca_cost(tree[0], w) + lca_cost(tree[1], w)


def average_linkage_similarity(w):
    """Merge the two clusters of largest average similarity."""
    n = len(w)
    clusters = {i: [i] for i in range(n)}
    merges = []
    while len(clusters) > 1:
        a, b = max(
            itertools.combinations(sorted(clusters), 2),
            key=lambda p: Fraction(sum(w[i][j] for i in clusters[p[0]] for j in clusters[p[1]]),
                                   len(clusters[p[0]]) * len(clusters[p[1]])),
        )
        merges.append((a, b, len(merges) + 1))
        clusters[n + len(merges) - 1] = clusters.pop(a) + clusters.pop(b)
    return merges


def test_worked_example():
    D = line(EX)
    t = Dendrogram(6, COMPLETE)
    c = t.cophenetic()
    assert c[0][1] == c[0][2] == 3 and c[1][2] == 1 and c[3][4] == 6
    assert c[0][3] == c[2][4] == 13 and c[0][5] == c[4][5] == 21
    assert t.cut_k(3) == [0, 0, 0, 1, 1, 2]
    assert t.cut_height(6) == [0, 0, 0, 1, 1, 2]
    assert t.cut_height(5) == [0, 0, 0, 1, 2, 3]
    assert t.cut_k(1) == [0] * 6 and t.cut_k(6) == list(range(6))
    assert t.cophenetic_correlation(D) == pytest.approx(0.8247, abs=1e-4)
    s = Dendrogram(6, SINGLE)
    assert s.cophenetic_correlation(D) == pytest.approx(0.8608, abs=1e-4)
    assert s.cut_k(3) == [0, 0, 0, 0, 1, 2]
    assert s.is_monotone() and t.is_monotone()


def test_edges():
    assert Dendrogram(1, []).cophenetic() == [[0]]
    assert Dendrogram(1, []).cut_k(1) == [0]
    assert Dendrogram(0, []).cophenetic() == []
    with pytest.raises(ValueError):
        Dendrogram(3, [(0, 1, 1)])
    with pytest.raises(ValueError):
        Dendrogram(3, [(0, 1, 1), (0, 2, 2)])
    assert not Dendrogram(3, [(0, 1, 5), (2, 3, 4)]).is_monotone()


def test_cophenetic_is_lca_height():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(1, 10)
        roots, merges, h = list(range(n)), [], 0
        while len(roots) > 1:
            a, b = rng.sample(roots, 2)
            h += rng.randrange(0, 3)
            roots = [r for r in roots if r not in (a, b)] + [n + len(merges)]
            merges.append((a, b, h))
        t = Dendrogram(n, merges)
        c = t.cophenetic()
        for i in range(n):
            for j in range(n):
                if i != j:
                    assert c[i][j] == lca_height(t, i, j)[0]
        assert is_ultrametric(c)
        for k in range(1, n + 1):
            labels = t.cut_k(k)
            assert len(set(labels)) == k
        for x in range(0, h + 2):
            assert t.cut_height(x) == threshold_partition(c, x)


@pytest.mark.parametrize("n", [2, 3, 4])
def test_ultrametrics_are_cophenetic_matrices(n):
    values = (1, 2, 3)
    ultra = {frozen(m) for m in matrices(n, values) if is_ultrametric(m)}
    coph = set()
    for merges in monotone_dendrograms(n, values):
        t = Dendrogram(n, merges)
        c = t.cophenetic()
        coph.add(frozen(c))
        for x in (0, 1, 2, 3):
            assert t.cut_height(x) == threshold_partition(c, x)
    assert coph == ultra


@pytest.mark.parametrize("n", [2, 3, 4])
def test_single_linkage_is_subdominant(n):
    values = (1, 2, 3)
    ultra = [m for m in matrices(n, values) if is_ultrametric(m)]
    for d in matrices(n, values):
        u = naive_single_cophenetic(d)
        assert is_ultrametric(u)
        assert all(u[i][j] <= d[i][j] for i in range(n) for j in range(n))
        for v in ultra:
            if all(v[i][j] <= d[i][j] for i in range(n) for j in range(n)):
                assert all(v[i][j] <= u[i][j] for i in range(n) for j in range(n))


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_dasgupta_cost_against_brute_force(n):
    trees = list(binary_trees(range(n)))
    double_factorial = 1
    for k in range(3, 2 * n - 2, 2):
        double_factorial *= k
    assert len(trees) == double_factorial
    rng = random.Random(n)
    for _ in range(20):
        w = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                w[i][j] = w[j][i] = rng.randrange(0, 6)
        total = sum(w[i][j] for i in range(n) for j in range(i + 1, n))
        costs = []
        for tree in trees:
            t = Dendrogram(n, to_merges(tree, n))
            cost = t.dasgupta_cost(w)
            assert cost == lca_cost(tree, w)
            per_pair = sum(w[i][j] * t.size[lca_height(t, i, j)[1]] for i in range(n) for j in range(i + 1, n))
            assert cost == per_pair
            costs.append(cost)
        best_revenue = n * total - min(costs)
        avg = Dendrogram(n, average_linkage_similarity(w))
        assert 3 * (n * total - avg.dasgupta_cost(w)) >= best_revenue


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_clique_cost_is_the_same_for_every_tree(n):
    w = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    for tree in binary_trees(range(n)):
        assert Dendrogram(n, to_merges(tree, n)).dasgupta_cost(w) == (n ** 3 - n) // 3
