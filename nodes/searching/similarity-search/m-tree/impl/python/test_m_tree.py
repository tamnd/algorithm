# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/m-tree/. The authors are listed in prov/GE79TV.jsonl.

import math
import random

from m_tree import MTree

P = [(1, 1), (2, 6), (4, 4), (5, 1), (6, 7), (8, 3), (9, 8), (3, 9), (7, 5), (0, 4), (10, 2), (6, 2)]


def edit(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def check_invariants(t: MTree) -> int:
    """Covering radii, parent distances and equal leaf depth; returns the number of objects."""
    depths = set()

    def objects(node, parent, depth):
        found = []
        assert len(node.entries) <= t.M
        if parent is not None:
            assert len(node.entries) >= (t.M + 1) // 2
        for e in node.entries:
            if parent is None:
                assert e.dparent is None
            else:
                assert abs(e.dparent - t._d(e.obj, parent)) < 1e-9
            if node.leaf:
                found.append(e.obj)
                depths.add(depth)
            else:
                sub = objects(e.child, e.obj, depth + 1)
                assert all(t._d(e.obj, y) <= e.radius + 1e-9 for y in sub)
                found += sub
        return found

    n = len(objects(t.root, None, 0))
    assert len(depths) <= 1
    if t.M >= 3 and depths and max(depths) >= 1:
        h = max(depths) + 1
        assert n >= 2 * ((t.M + 1) // 2) ** (h - 1)
    return n


def build(points, d, capacity):
    t = MTree(d, capacity)
    for x in points:
        t.insert(x)
    return t


def test_example() -> None:
    t = MTree(math.dist, 4)
    costs = []
    for x in P:
        t.evaluations = 0
        t.insert(x)
        costs.append(t.evaluations)
    assert costs == [0, 0, 0, 0, 10, 2, 2, 12, 3, 3, 3, 13]
    assert check_invariants(t) == 12
    roots = [(e.obj, round(e.radius, 4)) for e in t.root.entries]
    assert roots == [((2, 6), 3.1623), ((6, 7), 3.1623), ((5, 1), 4.0), ((8, 3), 2.2361)]
    t.evaluations = 0
    assert sorted(t.range((9, 3), 1.5)) == [(8, 3), (10, 2)]
    assert t.evaluations == 7
    t.evaluations = 0
    assert [x for _, x in t.knn((9, 3), 2)] == [(8, 3), (10, 2)]
    assert t.evaluations == 7


def test_edges() -> None:
    t = MTree(math.dist, 2)
    assert t.range((0, 0), 1) == [] and t.knn((0, 0), 3) == []
    t.insert((1, 1))
    assert t.range((0, 0), 2) == [(1, 1)] and t.knn((0, 0), 0) == []
    for _ in range(9):
        t.insert((1, 1))
    assert check_invariants(t) == 10 and len(t.range((1, 1), 0)) == 10
    try:
        MTree(math.dist, 1)
        raise AssertionError("capacity 1 accepted")
    except ValueError:
        pass


def test_random_against_scan() -> None:
    rng = random.Random(1997)
    for trial in range(500):
        cap = rng.randint(2, 6)
        if trial % 2:
            dim = rng.choice([1, 2, 3])
            pts = [tuple(rng.randint(0, 9) for _ in range(dim)) for _ in range(rng.randint(0, 50))]
            d = math.dist
            q = tuple(rng.uniform(-1, 10) for _ in range(dim))
            r = rng.uniform(0, 5)
        else:
            pts = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(0, 35))]
            d = edit
            q = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
            r = rng.randint(0, 3)
        t = build(pts, d, cap)
        assert check_invariants(t) == len(pts)
        assert sorted(t.range(q, r)) == sorted(x for x in pts if d(q, x) <= r)
        k = rng.randint(1, 6)
        got = [dist for dist, _ in t.knn(q, k)]
        want = sorted(d(q, x) for x in pts)[:k]
        assert got == want
