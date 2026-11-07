# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-cuthill-mckee/. The authors are listed in prov/36W80E.jsonl.

import random
from fractions import Fraction

from reverse_cuthill_mckee import (
    _levels, bandwidth, cholesky_pattern, cuthill_mckee, envelope, fill_and_flops,
    graph_from_dense, graph_from_edges, permute, pseudo_peripheral, reverse_cuthill_mckee,
)


def random_graph(rng, n, p):
    return graph_from_edges(n, [(i, j) for i in range(n) for j in range(i) if rng.random() < p])


def grid(k):
    e = []
    for i in range(k):
        for j in range(k):
            v = i * k + j
            if j + 1 < k:
                e.append((v, v + 1))
            if i + 1 < k:
                e.append((v, v + k))
    return graph_from_edges(k * k, e)


def test_empty_and_single():
    assert reverse_cuthill_mckee([]) == []
    assert reverse_cuthill_mckee([[]]) == [0]
    assert reverse_cuthill_mckee([[], [], []]) == [2, 1, 0]


def test_is_a_permutation_and_reverse_of_cm():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 40)
        adj = random_graph(rng, n, rng.uniform(0.0, 0.3))
        o = reverse_cuthill_mckee(adj)
        assert sorted(o) == list(range(n))
        assert o == cuthill_mckee(adj)[::-1]
        assert bandwidth(adj, o) == bandwidth(adj, cuthill_mckee(adj))


def test_bandwidth_bounded_by_level_width():
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(2, 40)
        adj = random_graph(rng, n, rng.uniform(0.05, 0.3))
        cm = cuthill_mckee(adj)
        seen, w = set(), 1
        for v in cm:  # the first vertex of each component in CM order is its root
            if v not in seen:
                ls = _levels(adj, v)
                for lev in ls:
                    seen.update(lev)
                w = max(w, max(len(lev) for lev in ls))
        assert bandwidth(adj, cm) <= 2 * w - 1


def test_envelope_never_larger_than_cm():  # Liu and Sherman (1976)
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 40)
        adj = random_graph(rng, n, rng.uniform(0.02, 0.3))
        assert envelope(adj, reverse_cuthill_mckee(adj)) <= envelope(adj, cuthill_mckee(adj))


def test_fill_stays_in_envelope():
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(1, 35)
        adj = random_graph(rng, n, rng.uniform(0.05, 0.3))
        for order in (reverse_cuthill_mckee(adj), list(range(n))):
            f = [0] * n
            for k, v in enumerate(order):
                f[v] = k
            first = [min([f[w] for w in adj[v]] + [f[v]]) for v in order]  # by new number
            for k, rows in enumerate(cholesky_pattern(adj, order)):
                assert all(first[i] <= k for i in rows)
            assert fill_and_flops(adj, order)[0] <= envelope(adj, order)


def ldl_pattern(a):
    """Exact LDL^T in rationals; returns the set of (i, k), i > k, with l_ik != 0."""
    n = len(a)
    a = [[Fraction(v) for v in row] for row in a]
    pat = set()
    for k in range(n):
        for i in range(k + 1, n):
            if a[i][k] != 0:
                pat.add((i, k))
                lik = a[i][k] / a[k][k]
                for j in range(k + 1, n):
                    a[i][j] -= lik * a[k][j]
    return pat


def test_symbolic_pattern_matches_exact_factorization():
    rng = random.Random(5)
    for _ in range(25):
        n = rng.randint(2, 14)
        adj = random_graph(rng, n, 0.25)
        a = [[0] * n for _ in range(n)]
        for v in range(n):
            for w in adj[v]:
                if v < w:
                    a[v][w] = a[w][v] = -rng.randint(1, 9)
        for v in range(n):
            a[v][v] = 1 + sum(-x for x in a[v])  # diagonally dominant, SPD
        assert graph_from_dense(a) == adj
        o = reverse_cuthill_mckee(adj)
        sym = {(i, k) for k, rows in enumerate(cholesky_pattern(adj, o)) for i in rows}
        num = ldl_pattern(permute(a, o))
        assert num <= sym and len(sym - num) <= 1


def test_star_numbers_the_centre_late():
    n = 30
    adj = graph_from_edges(n, [(0, j) for j in range(1, n)])
    o = reverse_cuthill_mckee(adj)
    assert o.index(0) >= n - 2
    assert fill_and_flops(adj, o)[0] == n - 1  # no fill
    assert fill_and_flops(adj, list(range(n)))[0] == n * (n - 1) // 2  # centre first: full


def test_path_and_complete_graph():
    adj = graph_from_edges(10, [(i, i + 1) for i in range(9)][::-1])
    o = reverse_cuthill_mckee(adj)
    assert bandwidth(adj, o) == 1 and fill_and_flops(adj, o)[0] == 9
    k = graph_from_edges(6, [(i, j) for i in range(6) for j in range(i)])
    assert fill_and_flops(k, reverse_cuthill_mckee(k))[0] == 15


def test_grid_values():
    adj = grid(8)
    o = reverse_cuthill_mckee(adj)
    assert bandwidth(adj, o) == 8 and envelope(adj, o) == 364
    assert envelope(adj, list(range(64))) == 455
    assert pseudo_peripheral(adj, 27) in (0, 7, 56, 63)


def test_mesh_like_graph_gains():
    rng = random.Random(1)
    n = 300
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    adj = graph_from_edges(n, [(i, j) for i in range(n) for j in range(i)
                               if (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2 < 0.008])
    o = reverse_cuthill_mckee(adj)
    nat = list(range(n))
    assert bandwidth(adj, o) * 5 < bandwidth(adj, nat)
    assert fill_and_flops(adj, o)[1] * 5 < fill_and_flops(adj, nat)[1]
    assert envelope(adj, o) <= envelope(adj, cuthill_mckee(adj))
