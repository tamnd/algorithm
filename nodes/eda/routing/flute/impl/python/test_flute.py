# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flute/. The authors are listed in prov/Q78Z3D.jsonl.

import random
from itertools import combinations

from flute import all_tables, flute, l1, lookup, mst_edges, powv_table


def mst_length(pts: list[tuple[int, int]]) -> int:
    return sum(l1(pts[a], pts[b]) for a, b in mst_edges(pts))


def exact_rsmt(pins: list[tuple[int, int]]) -> int:
    """Brute force: the least MST length over pins plus at most n - 2 points of the Hanan grid."""
    xs = sorted({p[0] for p in pins})
    ys = sorted({p[1] for p in pins})
    cand = [(x, y) for x in xs for y in ys if (x, y) not in set(pins)]
    best = mst_length(pins)
    for k in range(1, max(len(pins) - 1, 1)):
        for extra in combinations(cand, k):
            best = min(best, mst_length(pins + list(extra)))
    return best


def is_tree(pts: list[tuple[int, int]], edges: list[tuple[int, int]], npins: int) -> bool:
    n = len(pts)
    if len(edges) != max(n - 1, 0):
        return False
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            a = parent[a]
        return a

    for a, b in edges:
        if find(a) == find(b):
            return False
        parent[find(a)] = find(b)
    return n >= npins


def test_tables() -> None:
    assert powv_table((0, 1)) == (((1, 1), frozenset()),)
    for pi, entry in all_tables(3).items():
        assert [v for v, _ in entry] == [(1, 1, 1, 1)]
    assert [v for v, _ in powv_table((1, 0, 3, 2))] == [(1, 1, 1, 1, 1, 1)]
    assert {v for v, _ in powv_table((0, 2, 1, 3))} == {(1, 2, 1, 1, 1, 1), (1, 1, 1, 1, 2, 1)}
    assert sum(len(e) for e in all_tables(4).values()) == 40


def test_plus() -> None:
    pins = [(1, 0), (0, 1), (2, 1), (1, 2)]
    w, st = lookup(pins)
    assert w == 4 and st == [(1, 1)]
    total, pts, edges = flute(pins)
    assert total == 4 and is_tree(pts, edges, 4)


def test_edges() -> None:
    assert flute([]) == (0, [], [])
    assert flute([(3, 4)]) == (0, [(3, 4)], [])
    assert flute([(0, 0), (2, 5)])[0] == 7
    assert flute([(0, 0), (4, 0), (2, 3)])[0] == 7
    assert flute([(1, 1), (1, 1), (1, 1)])[0] == 0


def test_against_exact(seed: int = 29) -> None:
    rng = random.Random(seed)
    for _ in range(300):
        n = rng.randint(2, 4)
        pins = [(rng.randint(0, 8), rng.randint(0, 8)) for _ in range(n)]
        total, pts, edges = flute(pins)
        assert pts[:n] == pins and is_tree(pts, edges, n)
        assert total == sum(l1(pts[a], pts[b]) for a, b in edges)
        assert total == lookup(pins)[0] == exact_rsmt(list(dict.fromkeys(pins)))
    for _ in range(40):
        n = rng.randint(5, 6) if _ < 8 else 5
        pins = list(dict.fromkeys((rng.randint(0, 12), rng.randint(0, 12)) for _ in range(n)))
        total, pts, edges = flute(pins)
        assert pts[: len(pins)] == pins and is_tree(pts, edges, len(pins))
        assert total == sum(l1(pts[a], pts[b]) for a, b in edges)
        assert exact_rsmt(pins) <= total
