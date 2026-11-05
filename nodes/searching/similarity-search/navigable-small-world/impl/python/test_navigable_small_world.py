# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/navigable-small-world/. The authors are listed in prov/XDDYQ2.jsonl.

import math
import random

from navigable_small_world import NSW

P = [(9, 5), (9, 1), (0, 4), (8, 9), (5, 4), (2, 5), (2, 2), (1, 6), (5, 2), (6, 9), (6, 7), (7, 3)]
NAMES = "abcdefghijkl"


def build(points, f=2, ef_c=2, entries=1, seed=0):
    g = NSW(f=f, ef_construction=ef_c, entries=entries, seed=seed)
    for p in points:
        g.insert(p)
    return g


def test_example() -> None:
    g = build(P)
    adj = {NAMES[i]: "".join(NAMES[j] for j in sorted(a)) for i, a in enumerate(g.adj)}
    assert adj == {"a": "bcdej", "b": "acdei", "c": "abfgh", "d": "abjk", "e": "abfil", "f": "cegh",
                   "g": "cf", "h": "cf", "i": "bel", "j": "adk", "k": "dj", "l": "ei"}
    q = (2, 9)
    g.evaluations = 0
    assert [i for _, i in g.search(q, 1, 1, [0])] == [9]
    assert g.evaluations == 7
    g.evaluations = 0
    assert [i for _, i in g.search(q, 1, 3, [0])] == [7]
    assert g.evaluations == 10


def test_edges() -> None:
    g = NSW()
    assert g.search((0, 0), 3, 5) == []
    g.insert((1.0, 1.0))
    assert g.search((0, 0), 3, 5) == [(math.dist((1, 1), (0, 0)), 0)]
    assert g.search((0, 0), 0, 5) == []
    try:
        NSW(f=0)
        raise AssertionError("f = 0 accepted")
    except ValueError:
        pass


def brute(points, q, k):
    return sorted((math.dist(p, q), i) for i, p in enumerate(points))[:k]


def test_random_against_brute_force() -> None:
    rng = random.Random(2014)
    for _ in range(500):
        n = rng.randint(1, 40)
        dim = rng.randint(1, 5)
        pts = [tuple(rng.uniform(0, 10) for _ in range(dim)) for _ in range(n)]
        f = rng.randint(1, 4)
        g = build(pts, f=f, ef_c=rng.randint(1, 6), entries=rng.randint(1, 3), seed=rng.randrange(10**6))
        # invariants: undirected, links at insertion, connected
        for i, a in enumerate(g.adj):
            assert i not in a
            for j in a:
                assert i in g.adj[j]
            assert sum(1 for j in a if j < i) >= min(f, i)
        seen, stack = {0}, [0]
        while stack:
            for j in g.adj[stack.pop()]:
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
        assert len(seen) == n
        q = tuple(rng.uniform(0, 10) for _ in range(dim))
        k = rng.randint(1, 5)
        # a full beam is exact
        assert g.search(q, k, n) == brute(pts, q, k)
        # any beam returns the best of what it evaluated
        ef = rng.randint(1, 8)
        got = g.search(q, k, ef)
        seen_pts = sorted((math.dist(pts[i], q), i) for i in g.last_visited)
        assert got == seen_pts[:k]
