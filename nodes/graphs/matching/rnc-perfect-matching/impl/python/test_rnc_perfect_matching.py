# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rnc-perfect-matching/. The authors are listed in prov/7TA0S6.jsonl.

import itertools
import random

from rnc_perfect_matching import _adjugate, _determinant, rnc_perfect_matching


def has_perfect_matching(n, edges):
    """Oracle: match the lowest vertex with each neighbour in turn."""
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    def rec(left):
        if not left:
            return True
        v = min(left)
        return any(rec(left - {v, u}) for u in adj[v] if u in left)

    return rec(frozenset(range(n)))


def check(n, edges, seed):
    mate = rnc_perfect_matching(n, edges, rng=random.Random(seed))
    exists = has_perfect_matching(n, edges)
    if mate is None:
        assert not exists
        return None
    assert exists
    es = {(min(a, b), max(a, b)) for a, b in edges}
    for v in range(n):
        assert mate[mate[v]] == v and mate[v] != v
        assert (min(v, mate[v]), max(v, mate[v])) in es
    return mate


def test_empty_graph():
    assert rnc_perfect_matching(0, []) == []
    assert rnc_perfect_matching(2, [], trials=3) is None


def test_odd_cycles_and_odd_order():
    triangle = [(0, 1), (1, 2), (2, 0)]
    assert check(3, triangle, 1) is None
    c5 = [(i, (i + 1) % 5) for i in range(5)]
    assert check(5, c5, 2) is None
    # two triangles joined by an edge: 6 vertices, perfect matching through the bridge
    g = triangle + [(3, 4), (4, 5), (5, 3), (2, 3)]
    assert check(6, g, 3) is not None


def test_no_perfect_matching_even_order():
    # a center joined to three triangles: 10 vertices, deleting the center leaves 3 odd parts
    edges = []
    for t in range(3):
        a, b, c = 1 + 3 * t, 2 + 3 * t, 3 + 3 * t
        edges += [(a, b), (b, c), (c, a), (0, a)]
    assert check(10, edges, 4) is None


def test_worked_example():
    # the 4-cycle 0-1-2-3 plus the chord 0-2
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    assert check(4, edges, 5) is not None


def test_petersen_graph():
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    assert check(10, outer + spokes + inner, 6) is not None


def test_determinant_and_adjugate():
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randint(1, 5)
        a = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        det = sum(
            (-1) ** sum(1 for i in range(n) for j in range(i) if p[j] > p[i])
            * eval("*".join(str(a[i][p[i]]) for i in range(n)) or "1")
            for p in itertools.permutations(range(n))
        )
        assert _determinant(a) == det
        if det != 0:
            adj = _adjugate(a, det)
            for i in range(n):
                for j in range(n):
                    assert sum(a[i][k] * adj[k][j] for k in range(n)) == (det if i == j else 0)


def test_bad_input():
    for bad in ([(0, 0)], [(0, 5)]):
        try:
            rnc_perfect_matching(2, bad)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def test_random_against_brute_force():
    rng = random.Random(1987)
    found = none = 0
    for case in range(600):
        n = rng.randint(0, 10)
        p = rng.random()
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]
        if check(n, edges, case) is None:
            none += 1
        else:
            found += 1
    assert found > 100 and none > 100
