# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabriel-graph/. The authors are listed in prov/T3DGB2.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from gabriel_graph import GabrielGraph

EXAMPLE = [(1, 3), (1, 11), (2, 8), (5, 1), (9, 6), (11, 1), (11, 4)]


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def incircle(a, b, c, d):
    """Positive if d is inside the circle through a, b, c (counterclockwise)."""
    rows = [(x[0] - d[0], x[1] - d[1], (x[0] - d[0]) ** 2 + (x[1] - d[1]) ** 2) for x in (a, b, c)]
    (a1, a2, a3), (b1, b2, b3), (c1, c2, c3) = rows
    return a1 * (b2 * c3 - b3 * c2) - a2 * (b1 * c3 - b3 * c1) + a3 * (b1 * c2 - b2 * c1)


def general_position(P):
    if any(orient(a, b, c) == 0 for a, b, c in itertools.combinations(P, 3)):
        return False
    for a, b, c, d in itertools.combinations(P, 4):
        if orient(a, b, c) < 0:
            b, c = c, b
        if incircle(a, b, c, d) == 0:
            return False
    return True


def delaunay(P):
    """Triangles whose circumcircle has no other point inside, and their edges (general position)."""
    n = len(P)
    E = set()
    T = []
    for i, j, k in itertools.combinations(range(n), 3):
        a, b, c = P[i], P[j], P[k]
        if orient(a, b, c) < 0:
            b, c = c, b
        if all(incircle(a, b, c, P[m]) < 0 for m in range(n) if m not in (i, j, k)):
            E |= {(i, j), (i, k), (j, k)}
            T.append((i, j, k))
    return E, T


def gabriel_by_delaunay_filter(P):
    """Keep a Delaunay edge pq iff every vertex r opposite to it sees pq at an acute angle."""
    E, T = delaunay(P)
    keep = set(E)
    for t in T:
        for r in t:
            i, j = sorted(x for x in t if x != r)
            dot = (P[i][0] - P[r][0]) * (P[j][0] - P[r][0]) + (P[i][1] - P[r][1]) * (P[j][1] - P[r][1])
            if dot <= 0:
                keep.discard((i, j))
    return E, keep


def rng_edges(P):
    n = len(P)
    return {
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if not any(max(d2(P[i], P[k]), d2(P[j], P[k])) < d2(P[i], P[j]) for k in range(n) if k not in (i, j))
    }


def mst_weight_and_edges(P):
    """Prim's algorithm on the complete graph (an independent reference)."""
    n = len(P)
    if n == 0:
        return 0, set()
    in_tree = [False] * n
    best = [None] * n
    parent = [-1] * n
    best[0] = 0
    E = set()
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i] and best[i] is not None), key=lambda i: best[i])
        in_tree[u] = True
        total += best[u]
        if parent[u] >= 0:
            E.add(tuple(sorted((u, parent[u]))))
        for v in range(n):
            if not in_tree[v] and (best[v] is None or d2(P[u], P[v]) < best[v]):
                best[v] = d2(P[u], P[v])
                parent[v] = u
    return total, E


def gabriel_by_circle(P):
    """Independent oracle: compare squared distances to the midpoint with the squared radius."""
    n = len(P)
    out = set()
    for i, j in itertools.combinations(range(n), 2):
        m = (Fraction(P[i][0] + P[j][0], 2), Fraction(P[i][1] + P[j][1], 2))
        r2 = d2(P[i], m)
        if all(d2(P[k], m) > r2 for k in range(n) if k not in (i, j)):
            out.add((i, j))
    return out


def test_example() -> None:
    g = GabrielGraph(EXAMPLE)
    g.check_invariant()
    assert g.edges() == [(0, 2), (0, 3), (1, 2), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)]
    assert not g.has_edge(0, 1)  # (2,8) is inside the disk on (1,3)(1,11)
    assert not g.has_edge(3, 6)  # (11,1) is inside the disk on (5,1)(11,4)
    assert g.neighbors(3) == [0, 4, 5]


def test_small_cases() -> None:
    assert GabrielGraph([]).edges() == []
    assert GabrielGraph([(0, 0)]).edges() == []
    assert GabrielGraph([(0, 0), (5, 7)]).edges() == [(0, 1)]
    with pytest.raises(ValueError):
        GabrielGraph([(1, 1), (1, 1)])


def test_collinear_gives_a_path() -> None:
    pts = [(3, 0), (0, 0), (7, 0), (1, 0), (12, 0)]
    order = sorted(range(len(pts)), key=lambda i: pts[i])
    want = sorted(tuple(sorted(e)) for e in zip(order, order[1:]))
    assert GabrielGraph(pts).edges() == want


def test_cocircular_square() -> None:
    # The four corners are on one circle. The diagonals have the other two corners on
    # their diametral circle, so they are not Gabriel edges; a Delaunay triangulation must
    # still choose one of them.
    g = GabrielGraph([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert g.edges() == [(0, 1), (0, 3), (1, 2), (2, 3)]


def test_point_on_the_circle_blocks() -> None:
    # (0, 1) is on the circle with diameter (-1,0)(1,0): closed disk, so no edge.
    g = GabrielGraph([(-1, 0), (1, 0), (0, 1)])
    assert not g.has_edge(0, 1)
    assert g.has_edge(0, 2) and g.has_edge(1, 2)


def test_random_against_oracle_and_chain() -> None:
    rng = random.Random(1969)
    checked_chain = 0
    for trial in range(600):
        n = rng.randint(0, 12)
        r = rng.choice([2, 4, 10, 100])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        rng.shuffle(pts)
        g = GabrielGraph(pts)
        E = set(g.edges())
        assert E == gabriel_by_circle(pts)
        if trial % 3 == 0:
            g.check_invariant()
        R = rng_edges(pts)
        assert R <= E  # holds with or without general position
        weight, M = mst_weight_and_edges(pts)
        assert M <= R  # every minimum spanning tree lies in the RNG, ties or not
        if len(pts) >= 3 and general_position(pts):
            D, filtered = gabriel_by_delaunay_filter(pts)
            assert E <= D
            assert E == filtered
            checked_chain += 1
        # The Gabriel graph contains a minimum spanning tree: its own MST has the same weight.
        sub = [(d2(pts[i], pts[j]), i, j) for i, j in E]
        sub.sort()
        parent = list(range(len(pts)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        w = 0
        for c, i, j in sub:
            a, b = find(i), find(j)
            if a != b:
                parent[a] = b
                w += c
        assert w == weight
    assert checked_chain > 100


def test_fractions() -> None:
    pts = [(Fraction(0), Fraction(0)), (Fraction(2), Fraction(0)), (Fraction(1), Fraction(1, 1000))]
    g = GabrielGraph(pts)
    assert not g.has_edge(0, 1)
    pts[2] = (Fraction(1), Fraction(1000001, 1000000))
    assert GabrielGraph(pts).has_edge(0, 1)
