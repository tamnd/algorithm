# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bionj/. The authors are listed in prov/JGRS6V.jsonl.

import random
from fractions import Fraction

import pytest

from bionj import bionj


def random_tree(n, rng, max_len=10):
    """Random unrooted binary tree on leaves 0..n-1 with positive integer edge lengths."""
    if n == 2:
        return [(0, 1, rng.randint(1, max_len))]
    c = n
    edges = [(0, c, rng.randint(1, max_len)), (1, c, rng.randint(1, max_len)), (2, c, rng.randint(1, max_len))]
    nxt = n + 1
    for x in range(3, n):
        k = rng.randrange(len(edges))
        u, v, _ = edges[k]
        p = nxt
        nxt += 1
        edges[k] = (u, p, rng.randint(1, max_len))
        edges.append((p, v, rng.randint(1, max_len)))
        edges.append((x, p, rng.randint(1, max_len)))
    return edges


def floyd(n, edges):
    """Oracle: leaf distances by Floyd-Warshall over all nodes."""
    nodes = sorted({u for u, _, _ in edges} | {v for _, v, _ in edges})
    dist = {a: {b: (Fraction(0) if a == b else None) for b in nodes} for a in nodes}
    for u, v, w in edges:
        dist[u][v] = dist[v][u] = Fraction(w)
    for k in nodes:
        for a in nodes:
            if dist[a][k] is None:
                continue
            for b in nodes:
                if dist[k][b] is not None:
                    c = dist[a][k] + dist[k][b]
                    if dist[a][b] is None or c < dist[a][b]:
                        dist[a][b] = c
    return [[dist[i][j] for j in range(n)] for i in range(n)]


def splits(n, edges):
    """Nontrivial splits, each as the leaf set on the side without leaf 0."""
    adj = {}
    for u, v, _ in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    out = set()
    for u, v, _ in edges:
        seen, stack, side = {u, v}, [v], set()
        while stack:
            x = stack.pop()
            if x < n:
                side.add(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if 0 in side:
            side = set(range(n)) - side
        if 2 <= len(side) <= n - 2:
            out.add(frozenset(side))
    return out


def nj_reference(D):
    """Oracle: plain neighbor-joining, the special case lambda = 1/2."""
    n = len(D)
    d = {i: {j: Fraction(D[i][j]) for j in range(n)} for i in range(n)}
    active, edges, nxt = list(range(n)), [], n
    while len(active) > 2:
        r = len(active)
        R = {i: sum(d[i][k] for k in active if k != i) for i in active}
        pairs = [(a, b) for x, a in enumerate(active) for b in active[x + 1:]]
        i, j = min(pairs, key=lambda p: (r - 2) * d[p[0]][p[1]] - R[p[0]] - R[p[1]])
        li = d[i][j] / 2 + (R[i] - R[j]) / (2 * (r - 2))
        u, nxt = nxt, nxt + 1
        edges += [(i, u, li), (j, u, d[i][j] - li)]
        d[u] = {u: Fraction(0)}
        for k in active:
            if k not in (i, j):
                d[u][k] = d[k][u] = (d[i][k] + d[j][k] - d[i][j]) / 2
        active = [k for k in active if k not in (i, j)] + [u]
    edges.append((active[0], active[1], d[active[0]][active[1]]))
    return edges


EXAMPLE = [
    [0, 9, 11, 10, 9],
    [9, 0, 3, 8, 9],
    [11, 3, 0, 11, 7],
    [10, 8, 11, 0, 10],
    [9, 9, 7, 10, 0],
]


def test_example_from_page():
    trace = []
    edges = bionj(EXAMPLE, trace)
    assert trace[0] == (1, 2, Fraction(2, 3))
    assert edges[:2] == [(1, 5, 1), (2, 5, 2)]
    assert (trace[1][0], trace[1][1]) == (0, 4)
    # BIONJ groups A with E; plain neighbor-joining groups A with D.
    assert splits(5, edges) == {frozenset({1, 2}), frozenset({1, 2, 3})}
    assert splits(5, nj_reference(EXAMPLE)) == {frozenset({1, 2}), frozenset({1, 2, 4})}


def test_small_cases():
    assert bionj([[0, 4], [4, 0]]) == [(0, 1, 4)]
    edges = bionj([[0, 3, 4], [3, 0, 5], [4, 5, 0]])
    assert floyd(3, edges) == [[0, 3, 4], [3, 0, 5], [4, 5, 0]]
    zero = bionj([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert all(w == 0 for _, _, w in zero)
    with pytest.raises(ValueError):
        bionj([])


def test_random_additive_recovers_tree():
    rng = random.Random(17)
    for _ in range(500):
        n = rng.randint(2, 9)
        true = random_tree(n, rng)
        D = floyd(n, true)
        trace = []
        edges = bionj(D, trace)
        assert floyd(n, edges) == D
        assert splits(n, edges) == splits(n, true)
        assert all(0 <= lam <= 1 for _, _, lam in trace)


def test_lambda_minimizes_variance():
    rng = random.Random(23)
    for _ in range(500):
        r = rng.randint(3, 8)
        vi = [Fraction(rng.randint(1, 30)) for _ in range(r - 2)]
        vj = [Fraction(rng.randint(1, 30)) for _ in range(r - 2)]
        vij = Fraction(rng.randint(1, 30))

        def var(lam):
            return sum(lam * lam * a + lam * (1 - lam) * (a + b - vij) + (1 - lam) ** 2 * b for a, b in zip(vi, vj))

        star = Fraction(1, 2) + sum(b - a for a, b in zip(vi, vj)) / (2 * (r - 2) * vij)
        for k in range(-5, 11):
            assert var(star) <= var(Fraction(k, 5))
        assert var(star) <= var(star + Fraction(1, 1000))
        assert var(star) <= var(star - Fraction(1, 1000))


def test_same_as_nj_when_variances_balance():
    # On additive data BIONJ and NJ give the same tree, whatever lambda is.
    rng = random.Random(29)
    for _ in range(200):
        n = rng.randint(3, 8)
        D = floyd(n, random_tree(n, rng))
        assert splits(n, bionj(D)) == splits(n, nj_reference(D))


def test_random_matrices_give_valid_trees():
    rng = random.Random(31)
    for _ in range(300):
        n = rng.randint(2, 8)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(0, 15)
        edges = bionj(D)
        assert len(edges) == (1 if n == 2 else 2 * n - 3)
        deg = {}
        for u, v, _ in edges:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        assert all(k == (1 if x < n else 3) for x, k in deg.items())
