# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neighbor-joining/. The authors are listed in prov/7JNM0Y.jsonl.

import random
from fractions import Fraction

import pytest

from neighbor_joining import leaf_distances, neighbor_joining


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


def all_topologies(n):
    """All unrooted binary trees on leaves 0..n-1 (n >= 3), as edge lists without lengths."""
    out = []
    stack = [(3, [(0, n), (1, n), (2, n)], n + 1)]
    while stack:
        x, edges, nxt = stack.pop()
        if x == n:
            out.append(edges)
            continue
        for k in range(len(edges)):
            u, v = edges[k]
            new = edges[:k] + edges[k + 1:] + [(u, nxt), (nxt, v), (x, nxt)]
            stack.append((x + 1, new, nxt + 1))
    return out


def floyd(n, edges):
    """Oracle: all-pairs distances by Floyd-Warshall over all nodes."""
    nodes = sorted({u for u, _, _ in edges} | {v for _, v, _ in edges})
    INF = None
    dist = {a: {b: (Fraction(0) if a == b else INF) for b in nodes} for a in nodes}
    for u, v, w in edges:
        dist[u][v] = dist[v][u] = Fraction(w)
    for k in nodes:
        for a in nodes:
            if dist[a][k] is None:
                continue
            for b in nodes:
                if dist[k][b] is None:
                    continue
                c = dist[a][k] + dist[k][b]
                if dist[a][b] is None or c < dist[a][b]:
                    dist[a][b] = c
    return [[dist[i][j] for j in range(n)] for i in range(n)]


def splits(n, edges):
    """Nontrivial splits of a tree, each as the leaf set on the side without leaf 0."""
    adj = {}
    for e in edges:
        u, v = e[0], e[1]
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    out = set()
    for e in edges:
        u, v = e[0], e[1]
        seen = {u, v}
        stack = [v]
        side = set()
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


def path_edges(n, edges):
    """Number of edges on the path between each pair of leaves."""
    unit = [(e[0], e[1], 1) for e in edges]
    return floyd(n, unit)


def check_binary_tree(n, edges):
    deg = {}
    for u, v, _ in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    assert len(edges) == (1 if n == 2 else 2 * n - 3)
    for x, k in deg.items():
        assert k == (1 if x < n else 3)


EXAMPLE = [
    [0, 9, 8, 11, 8],
    [9, 0, 13, 16, 13],
    [8, 13, 0, 9, 10],
    [11, 16, 9, 0, 13],
    [8, 13, 10, 13, 0],
]


def test_example_from_page():
    edges = neighbor_joining(EXAMPLE)
    assert edges == [(2, 5, 3), (3, 5, 6), (0, 6, 2), (1, 6, 7), (4, 7, 5), (5, 7, 2), (6, 7, 1)]
    assert leaf_distances(5, edges) == [[Fraction(x) for x in row] for row in EXAMPLE]
    assert splits(5, edges) == {frozenset({2, 3}), frozenset({2, 3, 4})}


def test_two_and_three_taxa():
    assert neighbor_joining([[0, 5], [5, 0]]) == [(0, 1, 5)]
    edges = neighbor_joining([[0, 3, 4], [3, 0, 5], [4, 5, 0]])
    assert leaf_distances(3, edges) == [[0, 3, 4], [3, 0, 5], [4, 5, 0]]
    assert sorted(w for _, _, w in edges) == [1, 2, 3]
    with pytest.raises(ValueError):
        neighbor_joining([[0]])


def test_closest_pair_is_not_joined():
    # In EXAMPLE the smallest entries are d(0, 2) = d(0, 4) = 8, but neither pair is a cherry.
    first = {u for u, v, _ in neighbor_joining(EXAMPLE)[:2]}
    assert first == {2, 3}


def test_random_additive_recovers_tree():
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(2, 9)
        true = random_tree(n, rng)
        D = floyd(n, true)
        edges = neighbor_joining(D)
        check_binary_tree(n, edges)
        assert all(w > 0 for _, _, w in edges)
        assert leaf_distances(n, edges) == D
        assert floyd(n, edges) == D
        assert splits(n, edges) == splits(n, true)


def test_q_criterion_matches_saitou_nei_sum():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(3, 7)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(1, 20)
        edges = neighbor_joining(D)
        i, j = edges[0][0], edges[1][0]
        T = sum(D[a][b] for a in range(n) for b in range(a + 1, n))

        def S(a, b):
            rest = [k for k in range(n) if k != a and k != b]
            s1 = sum(D[a][k] + D[b][k] for k in rest)
            s2 = sum(D[k][l] for k in rest for l in rest if k < l)
            return Fraction(s1, 2 * (n - 2)) + Fraction(D[a][b], 2) + Fraction(s2, n - 2)

        best = min(S(a, b) for a in range(n) for b in range(a + 1, n))
        assert S(i, j) == best
        R = [sum(row) for row in D]
        assert S(i, j) == Fraction((n - 2) * D[i][j] - R[i] - R[j] + 2 * T, 2 * (n - 2))


def test_atteson_radius():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(4, 8)
        true = random_tree(n, rng)
        D = floyd(n, true)
        mu = min(w for _, _, w in true)
        P = [row[:] for row in D]
        for i in range(n):
            for j in range(i + 1, n):
                e = Fraction(rng.randint(-999, 999), 2000) * mu
                P[i][j] = P[j][i] = D[i][j] + e
        assert splits(n, neighbor_joining(P)) == splits(n, true)


def ols_lengths(n, topo, D):
    """Exact OLS edge lengths of a topology: solve (A^T A) b = A^T d with Fractions."""
    m = len(topo)
    adj = {}
    for k, (u, v) in enumerate(topo):
        adj.setdefault(u, []).append((v, k))
        adj.setdefault(v, []).append((u, k))
    rows, rhs = [], []
    for s in range(n):
        par = {s: None}
        stack = [s]
        while stack:
            x = stack.pop()
            for y, k in adj[x]:
                if y not in par:
                    par[y] = (x, k)
                    stack.append(y)
        for t in range(s + 1, n):
            row = [0] * m
            x = t
            while par[x] is not None:
                x, k = par[x]
                row[k] = 1
            rows.append(row)
            rhs.append(Fraction(D[s][t]))
    M = [[Fraction(sum(r[a] * r[b] for r in rows)) for b in range(m)] + [sum(r[a] * y for r, y in zip(rows, rhs))] for a in range(m)]
    for c in range(m):
        p = next(r for r in range(c, m) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(m):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[c][m] / M[c][c] for c in range(m)]


def test_minimum_evolution_over_all_topologies():
    rng = random.Random(5)
    topos = {n: all_topologies(n) for n in (4, 5, 6)}
    assert [len(topos[n]) for n in (4, 5, 6)] == [3, 15, 105]
    for trial in range(12):
        n = 4 + trial % 3
        true = random_tree(n, rng)
        D = floyd(n, true)
        nj_splits = splits(n, neighbor_joining(D))
        bme, ols = [], []
        for topo in topos[n]:
            tau = path_edges(n, topo)
            pauplin = sum(Fraction(2) ** (1 - tau[i][j]) * D[i][j] for i in range(n) for j in range(i + 1, n))
            bme.append((pauplin, splits(n, topo)))
            ols.append((sum(ols_lengths(n, topo, D)), splits(n, topo)))
        for scores in (bme, ols):
            scores.sort(key=lambda t: t[0])
            assert scores[0][1] == nj_splits
            assert scores[0][0] < scores[1][0]
            assert scores[0][0] == sum(w for _, _, w in true)
