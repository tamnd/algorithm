# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lempel-even-cederbaum-st-numbering/. The authors are listed in prov/SJ9RE7.jsonl.

import random

import pytest

from lempel_even_cederbaum_st_numbering import st_numbering


def adj_from_edges(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def is_st_numbering(adj, s, t, num):
    n = len(adj)
    if sorted(num) != list(range(1, n + 1)):
        return False
    if num[s] != 1 or num[t] != n:
        return False
    for v in range(n):
        if v in (s, t):
            continue
        if not any(num[w] < num[v] for w in adj[v]):
            return False
        if not any(num[w] > num[v] for w in adj[v]):
            return False
    return True


def connected_without(adj, removed):
    n = len(adj)
    start = next((v for v in range(n) if v not in removed), None)
    if start is None:
        return True
    seen = {start}
    stack = [start]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in removed and w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) + len(removed) == n


def two_connected_with_st(adj, s, t):
    """Oracle: G + st is 2-connected (n >= 2; K2 counts as 2-connected)."""
    n = len(adj)
    a = [list(x) for x in adj]
    if t not in a[s]:
        a[s].append(t)
        a[t].append(s)
    if not connected_without(a, set()):
        return False
    if n <= 2:
        return True
    return all(connected_without(a, {v}) for v in range(n))


def random_two_connected(n, rng):
    """A random 2-connected graph built from a cycle by adding ears."""
    order = list(range(n))
    rng.shuffle(order)
    k = rng.randint(3, n) if n >= 3 else n
    edges = {frozenset((order[i], order[(i + 1) % k])) for i in range(k)}
    used = order[:k]
    rest = order[k:]
    while rest:
        a, b = rng.sample(used, 2)
        length = rng.randint(1, len(rest))
        path = [a] + rest[:length] + [b]
        rest = rest[length:]
        for i in range(len(path) - 1):
            edges.add(frozenset(path[i:i + 2]))
        used += path[1:-1]
    for _ in range(rng.randint(0, n)):
        a, b = rng.sample(range(n), 2)
        edges.add(frozenset((a, b)))
    return adj_from_edges(n, [tuple(e) for e in edges])


def test_triangle_and_k2():
    adj = adj_from_edges(3, [(0, 1), (1, 2), (0, 2)])
    assert st_numbering(adj, 0, 1) == [1, 3, 2]
    assert st_numbering(adj_from_edges(2, [(0, 1)]), 0, 1) == [1, 2]
    # K2 without the edge: st is added
    assert st_numbering([[], []], 1, 0) == [2, 1]


def test_k4_k5_k33():
    k4 = adj_from_edges(4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
    k5 = adj_from_edges(5, [(i, j) for i in range(5) for j in range(i + 1, 5)])
    k33 = adj_from_edges(6, [(i, j) for i in range(3) for j in range(3, 6)])
    for adj in (k4, k5, k33):
        n = len(adj)
        for s in range(n):
            for t in range(n):
                if s != t:
                    assert is_st_numbering(adj, s, t, st_numbering(adj, s, t))


def test_small_failures():
    with pytest.raises(ValueError):
        st_numbering([[]], 0, 0)  # a single vertex
    # a tree with 4 vertices is not 2-connected even with st added
    path = adj_from_edges(4, [(0, 1), (1, 2), (2, 3)])
    with pytest.raises(ValueError):
        st_numbering(path, 0, 1)
    # but the path 0-1-2-3 plus the edge 0-3 is a cycle
    assert is_st_numbering(path, 0, 3, st_numbering(path, 0, 3))
    star = adj_from_edges(4, [(0, 1), (0, 2), (0, 3)])
    with pytest.raises(ValueError):
        st_numbering(star, 1, 2)
    # two triangles sharing vertex 0
    bow = adj_from_edges(5, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)])
    with pytest.raises(ValueError):
        st_numbering(bow, 0, 1)
    # adding st = 1-3 makes the bowtie 2-connected
    assert is_st_numbering(bow, 1, 3, st_numbering(bow, 1, 3))


def test_random_against_oracle():
    rng = random.Random(11)
    for trial in range(800):
        n = rng.randint(2, 12)
        if rng.random() < 0.5:
            adj = random_two_connected(n, rng) if n >= 3 else adj_from_edges(2, [(0, 1)])
        else:
            m = rng.randint(0, n * (n - 1) // 2)
            pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
            adj = adj_from_edges(n, rng.sample(pairs, m))
        for v in range(n):
            rng.shuffle(adj[v])
        s, t = rng.sample(range(n), 2)
        if two_connected_with_st(adj, s, t):
            num = st_numbering(adj, s, t)
            assert is_st_numbering(adj, s, t, num)
        else:
            with pytest.raises(ValueError):
                st_numbering(adj, s, t)


def test_large_deep_dfs():
    # a long cycle with chords; DFS depth is about n
    n = 200000
    rng = random.Random(3)
    edges = [(i, (i + 1) % n) for i in range(n)]
    edges += [(rng.randrange(n), rng.randrange(n)) for _ in range(n // 10)]
    edges = [(u, v) for u, v in edges if u != v]
    adj = adj_from_edges(n, edges)
    num = st_numbering(adj, 0, n // 2)
    assert is_st_numbering(adj, 0, n // 2, num)
