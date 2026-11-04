# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-find/. The authors are listed in prov/E7GCG2.jsonl.

import random

import pytest

from quick_find import QuickFind

TINY = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1), (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]


def test_example() -> None:
    uf = QuickFind(10)
    merged = []
    for p, q in TINY:
        merged.append(uf.union(p, q))
        uf.check_invariant()
    assert merged == [True] * 5 + [False] + [True] * 3 + [False, False]
    assert uf.id == [1, 1, 1, 8, 8, 1, 1, 1, 8, 8]
    assert uf.count == 2
    assert uf.connected(0, 7) and uf.connected(3, 9)
    assert not uf.connected(0, 3)


def test_edges() -> None:
    uf = QuickFind(0)
    assert uf.count == 0 and len(uf) == 0
    uf = QuickFind(1)
    assert uf.find(0) == 0
    assert not uf.union(0, 0)
    assert uf.count == 1
    with pytest.raises(IndexError):
        uf.find(1)
    with pytest.raises(ValueError):
        QuickFind(-1)


def test_rename_uses_saved_name() -> None:
    uf = QuickFind(6)
    uf.union(0, 1)
    uf.union(4, 1)
    uf.union(1, 5)
    assert uf.id == [5, 5, 2, 3, 5, 5]
    uf.check_invariant()


def test_random_against_components() -> None:
    rng = random.Random(23)
    for _ in range(600):
        n = rng.randrange(1, 13)
        uf = QuickFind(n)
        edges: list[tuple[int, int]] = []
        for _ in range(rng.randrange(25)):
            p, q = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.5:
                before = _same(n, edges, p, q)
                assert uf.union(p, q) == (not before)
                edges.append((p, q))
                uf.check_invariant()
            else:
                assert uf.connected(p, q) == _same(n, edges, p, q)
        assert uf.count == len({_root(n, edges, x) for x in range(n)})


def _root(n: int, edges: list[tuple[int, int]], x: int) -> int:
    """Return the least element reachable from x along the edges."""
    seen = {x}
    stack = [x]
    while stack:
        v = stack.pop()
        for a, b in edges:
            for u, w in ((a, b), (b, a)):
                if u == v and w not in seen:
                    seen.add(w)
                    stack.append(w)
    return min(seen)


def _same(n: int, edges: list[tuple[int, int]], p: int, q: int) -> bool:
    return _root(n, edges, p) == _root(n, edges, q)
