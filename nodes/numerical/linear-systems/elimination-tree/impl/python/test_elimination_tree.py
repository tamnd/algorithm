# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elimination-tree/. The authors are listed in prov/4Z4VSH.jsonl.
import math
import random
from fractions import Fraction as F

import pytest

from elimination_tree import (lower_rows, etree, ereach, postorder,
                              symbolic_cholesky, column_counts, height, permute)


def game(n, rows):
    """Reference: the elimination game. Returns column patterns of L."""
    adj = [set() for _ in range(n)]
    for k in range(n):
        for i in rows[k]:
            adj[i].add(k)
            adj[k].add(i)
    cols = []
    for j in range(n):
        higher = sorted(v for v in adj[j] if v > j)
        cols.append(higher)
        for a in higher:
            for b in higher:
                if a != b:
                    adj[a].add(b)
    return cols


def ldl_pattern(n, rows, rng):
    """Exact LDL^T of a diagonally dominant matrix with the given pattern;
    returns the numerical column patterns of L."""
    a = [[F(0)] * n for _ in range(n)]
    for k in range(n):
        for i in rows[k]:
            v = F(rng.choice([-3, -2, -1, 1, 2, 3]))
            a[k][i] = a[i][k] = v
    for i in range(n):
        a[i][i] = sum(abs(x) for x in a[i]) + 1
    for j in range(n):
        d = a[j][j]
        assert d > 0
        for i in range(j + 1, n):
            if a[i][j]:
                f = a[i][j] / d
                for k in range(j + 1, i + 1):
                    a[i][k] -= f * a[k][j]
    for i in range(n):
        for k in range(i):
            a[k][i] = a[i][k]
    return [[i for i in range(j + 1, n) if a[i][j] != 0] for j in range(n)]


def rand_rows(rng, n):
    p = rng.choice([0.1, 0.2, 0.35, 0.6])
    return lower_rows(n, [(i, j) for i in range(n) for j in range(i) if rng.random() < p])


def is_ancestor(parent, a, j):
    while j != -1:
        if j == a:
            return True
        j = parent[j]
    return False


def grid(k):
    e = []
    for r in range(k):
        for c in range(k):
            v = r * k + c
            if c + 1 < k:
                e.append((v, v + 1))
            if r + 1 < k:
                e.append((v, v + k))
    return lower_rows(k * k, e)


def test_page_example():
    edges = [(1, 4), (1, 6), (2, 3), (2, 5), (3, 8), (4, 7), (5, 8), (6, 7), (7, 8)]
    rows = lower_rows(8, [(a - 1, b - 1) for a, b in edges])
    st = {}
    p = etree(8, rows, st)
    assert [x + 1 for x in p] == [4, 3, 5, 6, 8, 7, 8, 0]
    assert st["steps"] == 13
    mark = [False] * 8
    assert [x + 1 for x in ereach(rows, 7, p, mark)] == [3, 5, 7]
    assert [x + 1 for x in ereach(rows, 6, p, mark)] == [4, 6]
    assert column_counts(8, rows, p) == [3, 3, 3, 3, 2, 2, 2, 1]
    assert sum(column_counts(8, rows, p)) - 8 - len(edges) == 2
    assert [x + 1 for x in postorder(p)] == [2, 3, 5, 1, 4, 6, 7, 8]
    assert height(p) == 4


def test_random_against_elimination_game():
    rng = random.Random(4041)
    for _ in range(600):
        n = rng.randint(1, 13)
        rows = rand_rows(rng, n)
        cols = game(n, rows)
        p = etree(n, rows)
        assert p == [min(c) if c else -1 for c in cols]
        assert symbolic_cholesky(n, rows, p) == cols
        assert column_counts(n, rows) == [len(c) + 1 for c in cols]
        for j in range(n):
            assert p[j] == -1 or p[j] > j
            for i in cols[j]:
                assert is_ancestor(p, i, j)


def test_fill_path_theorem():
    rng = random.Random(77)
    for _ in range(200):
        n = rng.randint(2, 10)
        rows = rand_rows(rng, n)
        adj = [set() for _ in range(n)]
        for k in range(n):
            for i in rows[k]:
                adj[i].add(k)
                adj[k].add(i)
        cols = symbolic_cholesky(n, rows)
        for j in range(n):
            for i in range(j + 1, n):
                seen, todo, hit = {j}, [j], False
                while todo:
                    v = todo.pop()
                    for w in adj[v]:
                        if w == i:
                            hit = True
                        elif w < j and w not in seen:
                            seen.add(w)
                            todo.append(w)
                assert hit == (i in cols[j])


def test_numeric_factor_inside_symbolic_pattern():
    rng = random.Random(9)
    equal = total = 0
    for _ in range(200):
        n = rng.randint(1, 9)
        rows = rand_rows(rng, n)
        sym = symbolic_cholesky(n, rows)
        num = ldl_pattern(n, rows, rng)
        for j in range(n):
            assert set(num[j]) <= set(sym[j])
        total += 1
        equal += num == sym
    assert equal >= 0.8 * total  # observed: exact cancellation is rare


def test_postorder_is_equivalent_ordering():
    rng = random.Random(123)
    for _ in range(300):
        n = rng.randint(1, 12)
        rows = rand_rows(rng, n)
        p = etree(n, rows)
        order = postorder(p)
        assert sorted(order) == list(range(n))
        pos = {v: t for t, v in enumerate(order)}
        for j in range(n):
            assert p[j] == -1 or pos[j] < pos[p[j]]
        r2 = permute(n, rows, order)
        p2 = etree(n, r2)
        assert p2 == [-1 if p[order[t]] == -1 else pos[p[order[t]]] for t in range(n)]
        assert sorted(column_counts(n, r2, p2)) == sorted(column_counts(n, rows, p))
        size = [1] * n
        for t in range(n):
            if p2[t] != -1:
                size[p2[t]] += size[t]
        for t in range(n):  # descendants of t are exactly t - size + 1 .. t
            for s in range(n):
                assert is_ancestor(p2, t, s) == (t - size[t] < s <= t)


def test_edge_cases():
    assert etree(1, [[]]) == [-1]
    assert column_counts(1, [[]]) == [1]
    n = 6
    diag = lower_rows(n, [])
    assert etree(n, diag) == [-1] * n and height(etree(n, diag)) == 0
    tri = lower_rows(n, [(i, i + 1) for i in range(n - 1)])
    assert etree(n, tri) == list(range(1, n)) + [-1]
    assert column_counts(n, tri) == [2] * (n - 1) + [1]
    hub_first = lower_rows(n, [(0, i) for i in range(1, n)])
    assert etree(n, hub_first) == list(range(1, n)) + [-1]
    assert sum(column_counts(n, hub_first)) == n * (n + 1) // 2
    hub_last = lower_rows(n, [(n - 1, i) for i in range(n - 1)])
    assert etree(n, hub_last) == [n - 1] * (n - 1) + [-1]
    assert sum(column_counts(n, hub_last)) == 2 * n - 1
    dense = lower_rows(n, [(i, j) for i in range(n) for j in range(i)])
    assert etree(n, dense) == list(range(1, n)) + [-1]
    blocks = lower_rows(6, [(0, 1), (1, 2), (3, 4), (4, 5)])
    assert etree(6, blocks) == [1, 2, -1, 4, 5, -1]
    assert lower_rows(3, [(2, 0), (0, 2), (1, 1)]) == [[], [], [0]]
    with pytest.raises(ValueError):
        lower_rows(3, [(0, 3)])


def test_grid_natural_order():
    for k in (3, 7, 15):
        rows = grid(k)
        n = k * k
        m = sum(len(r) for r in rows)
        p = etree(n, rows)
        assert p == list(range(1, n)) + [-1]
        assert sum(column_counts(n, rows, p)) - n - m == (k - 1) ** 3


def test_path_compression_steps():
    rng = random.Random(5)
    worst = 0.0
    for _ in range(300):
        n = rng.randint(2, 40)
        rows = rand_rows(rng, n)
        m = sum(len(r) for r in rows)
        st = {}
        etree(n, rows, st)
        assert st["steps"] >= m
        if m:
            worst = max(worst, st["steps"] / (m * (math.log2(n) + 1)))
    assert worst <= 1.0  # observed: far below the O(m log n) bound
    n = 2000
    rows = lower_rows(n, [(i, i + 1) for i in range(n - 1)] + [(n - 1, i) for i in range(n - 1)])
    st = {}
    etree(n, rows, st)
    assert st["steps"] <= 3 * n  # without compression this matrix costs ~n^2/2
