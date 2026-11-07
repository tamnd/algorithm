# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-dissection/. The authors are listed in prov/F4FW9V.jsonl.

import math
import random
from fractions import Fraction

from nested_dissection import (
    _components, cholesky_float, cholesky_pattern, fill_and_flops, graph_from_edges,
    grid_graph, grid_nested_dissection, level_separator, nested_dissection,
)

U = 2.0 ** -53


def random_graph(rng, n, p):
    return graph_from_edges(n, [(i, j) for i in range(n) for j in range(i) if rng.random() < p])


def geometric_graph(rng, n, r2):
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    return graph_from_edges(n, [(i, j) for i in range(n) for j in range(i)
                                if (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2 < r2])


def rcm(adj):
    n = len(adj)
    seen, order = [False] * n, []
    for s in sorted(range(n), key=lambda v: (len(adj[v]), v)):
        if seen[s]:
            continue
        seen[s] = True
        order.append(s)
        h = len(order) - 1
        while h < len(order):
            v = order[h]
            h += 1
            for w in sorted((w for w in adj[v] if not seen[w]), key=lambda w: (len(adj[w]), w)):
                seen[w] = True
                order.append(w)
    return order[::-1]


def test_edge_cases():
    assert nested_dissection([]) == []
    assert nested_dissection([[]]) == [0]
    assert grid_nested_dissection(1, 1) == [0]
    assert sorted(nested_dissection([[] for _ in range(20)])) == list(range(20))
    path = graph_from_edges(31, [(i, i + 1) for i in range(30)])
    o = nested_dissection(path, leaf=1)
    assert sorted(o) == list(range(31))
    # dissecting a path creates fill (52 entries against 30 for the natural order) but stays O(n log n)
    assert fill_and_flops(path, o)[0] == 52
    assert fill_and_flops(path, list(range(31)))[0] == 30


def test_permutation_on_random_graphs():
    rng = random.Random(21)
    for _ in range(120):
        n = rng.randint(1, 60)
        g = random_graph(rng, n, rng.uniform(0.02, 0.3))
        for leaf in (1, 4, 8):
            assert sorted(nested_dissection(g, leaf)) == list(range(n))


def test_grid_orders_are_permutations():
    for k1 in range(1, 12):
        for k2 in range(1, 12):
            o = grid_nested_dissection(k1, k2)
            assert sorted(o) == list(range(k1 * k2))


def test_level_separator_separates():
    rng = random.Random(22)
    checked = 0
    for _ in range(150):
        n = rng.randint(4, 80)
        g = geometric_graph(rng, n, rng.uniform(0.02, 0.1))
        for comp in _components(g, range(n)):
            sep = level_separator(g, comp)
            if sep is None:
                continue
            assert sep and set(sep) <= set(comp)
            pieces = _components(g, set(comp) - set(sep))
            assert len(pieces) >= 2
            checked += 1
    assert checked > 100


def test_no_fill_between_pieces():
    # in the order, the top separator is last, so no entry of L links the two sides
    rng = random.Random(23)
    for _ in range(40):
        n = rng.randint(20, 120)
        g = geometric_graph(rng, n, 0.03)
        if len(_components(g, range(n))) != 1:
            continue
        seps = []
        order = nested_dissection(g, 4, seps)
        if not seps:
            continue
        top = seps[0]
        assert order[-len(top):] == top
        pieces = _components(g, set(range(n)) - set(top))
        which = {v: t for t, c in enumerate(pieces) for v in c}
        cols = cholesky_pattern(g, order)
        for k, col in enumerate(cols):
            for i in col:
                a, b = order[k], order[i]
                if a in which and b in which:
                    assert which[a] == which[b]


def test_grid_growth_and_comparison():
    prev = None
    for k in (8, 16, 32):
        g = grid_graph(k, k)
        nd = fill_and_flops(g, nested_dissection(g))
        gnd = fill_and_flops(g, grid_nested_dissection(k, k))
        r = fill_and_flops(g, rcm(g))
        for fill, flops in (nd, gnd):
            assert fill <= 4.0 * k * k * math.log2(k)  # O(n log n) with n = k^2
            assert flops <= 14.0 * k ** 3  # O(n^(3/2))
        assert r[1] >= 0.15 * k ** 4 / 2  # RCM: about k^4 / 2 flops
        if k >= 16:
            assert nd[1] < r[1]
        ratio = nd[1] / r[1]
        if prev is not None:
            assert ratio < prev
        prev = ratio


def test_backward_error_of_cholesky_in_nd_order():
    rng = random.Random(24)
    for k in (4, 5, 6):
        g = grid_graph(k, k)
        n = k * k
        order = nested_dissection(g, leaf=2)
        f = [0] * n
        for p, v in enumerate(order):
            f[v] = p
        sym = cholesky_pattern(g, order)
        for _ in range(4):
            a = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in g[i]:
                    if j < i:
                        a[i][j] = a[j][i] = -rng.uniform(0.1, 1.0)
            for i in range(n):
                a[i][i] = sum(abs(x) for x in a[i]) * rng.uniform(1.0, 1.5) + 1e-3
            l = cholesky_float(a, order)
            gam = (n + 1) * U / (1 - (n + 1) * U)
            for i in range(n):
                for j in range(i):
                    if l[i][j] != 0:
                        assert i in sym[j]  # computed nonzeros lie in the symbolic pattern
                for j in range(i + 1):
                    exact = sum(Fraction(l[i][t]) * Fraction(l[j][t]) for t in range(j + 1))
                    absl = sum(abs(l[i][t]) * abs(l[j][t]) for t in range(j + 1))
                    err = abs(Fraction(a[order[i]][order[j]]) - exact)
                    assert err <= Fraction(gam * absl)


def test_leaf_size_controls_switch_to_minimum_degree():
    g = grid_graph(6, 6)
    whole = nested_dissection(g, leaf=36)
    seps = []
    nested_dissection(g, leaf=36, separators=seps)
    assert seps == []
    assert sorted(whole) == list(range(36))
    seps = []
    nested_dissection(g, leaf=4, separators=seps)
    assert len(seps) >= 3
