# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasteleyn-method/. The authors are listed in prov/GT7NZ8.jsonl.

import random
from functools import lru_cache

import pytest

from kasteleyn_method import faces_of, kasteleyn_count, pfaffian_orientation, twice_area


def brute_count(n, edges):
    """Reference: match the lowest free vertex in every possible way."""
    nbr = [0] * n
    for u, v in edges:
        nbr[u] |= 1 << v
        nbr[v] |= 1 << u

    @lru_cache(maxsize=None)
    def go(free):
        if free == 0:
            return 1
        v = (free & -free).bit_length() - 1
        rest = free & ~(1 << v)
        total = 0
        m = nbr[v] & rest
        while m:
            w = m & -m
            total += go(rest & ~w)
            m ^= w
        return total

    return go((1 << n) - 1)


def perm_sign(seq):
    seq = list(seq)
    sign = 1
    for i in range(len(seq)):
        while seq[i] != i:
            j = seq[i]
            seq[i], seq[j] = seq[j], seq[i]
            sign = -sign
    return sign


def matchings(n, edges):
    """All perfect matchings, as lists of edges."""
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    out = []

    def go(free, chosen):
        if not free:
            out.append(list(chosen))
            return
        v = min(free)
        for w in adj[v] & free:
            chosen.append((v, w))
            go(free - {v, w}, chosen)
            chosen.pop()

    go(frozenset(range(n)), [])
    return out


def orientation(pos, edges):
    adj = {v: [] for v in range(len(pos))}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    orient = {}
    done = set()
    for r in range(len(pos)):
        if r not in done:
            o = pfaffian_orientation(pos, adj, r)
            done |= {v for e in o for v in e} | {r}
            orient.update(o)
    return adj, orient


def grid(rows, cols):
    pos = [(x, y) for y in range(rows) for x in range(cols)]
    edges = []
    for y in range(rows):
        for x in range(cols):
            v = y * cols + x
            if x + 1 < cols:
                edges.append((v, v + 1))
            if y + 1 < rows:
                edges.append((v, v + cols))
    return pos, edges


def orient2(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)


def inside_segment(p, q, x):
    if orient2(p, q, x) != 0:
        return False
    return min(p[0], q[0]) <= x[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= x[1] <= max(p[1], q[1])


def random_plane_graph(rng, n, size, tries):
    cells = [(x, y) for x in range(size) for y in range(size)]
    pos = rng.sample(cells, n)
    edges = []
    have = set()
    for _ in range(tries):
        if n < 2:
            break
        u, v = rng.sample(range(n), 2)
        if frozenset((u, v)) in have:
            continue
        p, q = pos[u], pos[v]
        if any(inside_segment(p, q, pos[w]) for w in range(n) if w != u and w != v):
            continue
        bad = False
        for a, b in edges:
            if len({a, b, u, v}) < 4:
                continue
            r, s = pos[a], pos[b]
            if orient2(p, q, r) * orient2(p, q, s) < 0 and orient2(r, s, p) * orient2(r, s, q) < 0:
                bad = True
                break
        if not bad:
            edges.append((u, v))
            have.add(frozenset((u, v)))
    return pos, edges


def test_worked_example():
    pos, edges = grid(2, 3)
    assert edges == [(0, 1), (0, 3), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5)]
    adj, orient = orientation(pos, edges)
    assert set(orient.values()) == {(0, 1), (1, 2), (2, 5), (4, 5), (3, 4), (4, 1), (0, 3)}
    assert kasteleyn_count(pos, edges) == 3


def test_edges():
    assert kasteleyn_count([], []) == 1
    assert kasteleyn_count([(0, 0)], []) == 0
    assert kasteleyn_count([(0, 0), (1, 0)], [(0, 1)]) == 1
    assert kasteleyn_count([(0, 0), (1, 0)], []) == 0
    assert kasteleyn_count([(0, 0), (1, 0), (5, 5), (6, 5)], [(0, 1), (2, 3)]) == 1
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert kasteleyn_count(square, [(0, 1), (1, 2), (2, 3), (3, 0)]) == 2
    k4 = [(0, 0), (4, 0), (0, 4), (1, 1)]
    assert kasteleyn_count(k4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]) == 3
    with pytest.raises(ValueError):
        kasteleyn_count([(0, 0), (1, 0)], [(0, 1), (1, 0)])
    with pytest.raises(ValueError):
        kasteleyn_count([(0, 0), (0, 0)], [(0, 1)])


def test_grids():
    domino = {(8, 8): 12988816, (6, 6): 6728, (4, 4): 36, (2, 2): 2}
    for (r, c), want in domino.items():
        assert kasteleyn_count(*grid(r, c)) == want
    for r in range(1, 6):
        for c in range(1, 6):
            pos, edges = grid(r, c)
            assert kasteleyn_count(pos, edges) == brute_count(len(pos), edges)
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    for c in range(1, 11):
        assert kasteleyn_count(*grid(2, c)) == fib[c]


def test_faces_and_orientation():
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(2, 10)
        pos, edges = random_plane_graph(rng, n, 6, 40)
        adj, orient = orientation(pos, edges)
        assert set(orient) == {frozenset(e) for e in edges}
        for r in range(n):
            sub = pfaffian_orientation(pos, adj, r)
            if not sub:
                continue
            verts = {v for e in sub for v in e}
            faces = faces_of(pos, {v: adj[v] for v in verts})
            areas = [twice_area(pos, f) for f in faces]
            outer = areas.index(min(areas))
            ne = len(sub)
            assert len(faces) == ne - len(verts) + 2
            for i, f in enumerate(faces):
                if i == outer:
                    continue
                assert areas[i] > 0
                cw = sum(1 for a, b in f if orient[frozenset((a, b))] == (b, a))
                assert cw % 2 == 1


def test_every_matching_has_the_same_sign():
    rng = random.Random(3)
    for _ in range(150):
        n = 2 * rng.randint(1, 5)
        pos, edges = random_plane_graph(rng, n, 5, 60)
        _, orient = orientation(pos, edges)
        signs = set()
        for m in matchings(n, edges):
            seq = [x for e in m for x in orient[frozenset(e)]]
            signs.add(perm_sign(seq))
        assert len(signs) <= 1


def test_random_against_brute_force():
    rng = random.Random(20260611)
    for _ in range(600):
        n = 2 * rng.randint(0, 7) if rng.random() < 0.85 else rng.randint(1, 13)
        size = rng.choice([4, 5, 7])
        pos, edges = random_plane_graph(rng, n, size, rng.randint(10, 150))
        assert kasteleyn_count(pos, edges) == brute_count(n, edges)
