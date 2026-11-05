# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/italiano-dynamic-transitive-closure/. The authors are listed in prov/08JB9Z.jsonl.

import random

import pytest

from italiano_dynamic_transitive_closure import DecrementalDAGClosure, IncrementalClosure


def _closure(n: int, edges) -> list[set[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    out = []
    for s in range(n):
        seen = {s}
        st = [s]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        out.append(seen)
    return out


def _check(g, n: int, edges) -> None:
    cl = _closure(n, edges)
    es = set(edges)
    for x in range(n):
        for y in range(n):
            assert g.reachable(x, y) == (y in cl[x])
            p = g.path(x, y)
            if y in cl[x]:
                assert p[0] == x and p[-1] == y
                assert all((p[k], p[k + 1]) in es for k in range(len(p) - 1))
            else:
                assert p is None


def test_example() -> None:
    g = IncrementalClosure(5)
    for e in [(0, 1), (2, 3), (3, 4), (1, 2), (4, 0)]:
        g.insert(*e)
    assert g.reachable(3, 2)
    assert g.path(0, 4) == [0, 1, 2, 3, 4]
    d = DecrementalDAGClosure(5, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)])
    d.delete(1, 3)
    assert d.reachable(0, 4) and d.path(0, 4) == [0, 2, 3, 4]
    d.delete(2, 3)
    assert not d.reachable(0, 4) and d.reachable(3, 4)


def test_rejects_cycle() -> None:
    with pytest.raises(ValueError):
        DecrementalDAGClosure(2, [(0, 1), (1, 0)])


def test_random_incremental() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 8)
        g = IncrementalClosure(n)
        edges = []
        for _ in range(rng.randint(0, 25)):
            e = (rng.randrange(n), rng.randrange(n))
            g.insert(*e)
            edges.append(e)
            _check(g, n, edges)


def test_random_decremental_dag() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 8)
        perm = list(range(n))
        rng.shuffle(perm)
        edges = []
        for _ in range(rng.randint(0, 25)):
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                if perm[a] > perm[b]:
                    a, b = b, a
                edges.append((a, b))
        g = DecrementalDAGClosure(n, edges)
        _check(g, n, edges)
        rng.shuffle(edges)
        while edges:
            e = edges.pop()
            g.delete(*e)
            _check(g, n, edges)


def test_long_chain() -> None:
    n = 400
    g = IncrementalClosure(n)
    for i in range(n - 1, 0, -1):
        g.insert(i - 1, i)
    assert g.reachable(0, n - 1) and not g.reachable(n - 1, 0)
    g.insert(n - 1, 0)
    assert g.reachable(n - 1, 5)
    d = DecrementalDAGClosure(n, [(i, i + 1) for i in range(n - 1)])
    d.delete(n // 2, n // 2 + 1)
    assert not d.reachable(0, n - 1) and d.reachable(0, n // 2)
