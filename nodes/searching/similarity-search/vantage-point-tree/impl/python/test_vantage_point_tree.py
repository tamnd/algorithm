# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vantage-point-tree/. The authors are listed in prov/ET45HH.jsonl.

import math
import random

from vantage_point_tree import VPTree

P = [(1, 1), (2, 6), (4, 4), (5, 1), (6, 7), (8, 3), (9, 8)]


def height(node) -> int:
    return 0 if node is None else 1 + max(height(node.inside), height(node.outside))


def edit(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def test_example() -> None:
    t = VPTree(P, math.dist, choose=lambda s: 0)
    assert t.evaluations == 10
    assert t.root.vp == (1, 1) and abs(t.root.mu - math.sqrt(26)) < 1e-12
    assert t.root.inside.vp == (5, 1) and t.root.outside.vp == (8, 3)
    assert height(t.root) == 3
    t.evaluations = 0
    assert sorted(t.range((8, 7), 2)) == [(6, 7), (9, 8)]
    assert t.evaluations == 4
    t.evaluations = 0
    assert t.nearest((7, 6)) == ((6, 7), math.sqrt(2))
    assert t.evaluations == 4


def test_edges() -> None:
    empty = VPTree([], math.dist)
    assert empty.range((0, 0), 5) == [] and empty.nearest((0, 0)) is None
    one = VPTree([(3, 4)], math.dist)
    assert one.range((0, 0), 5) == [(3, 4)] and one.range((0, 0), 4.9) == []
    same = VPTree([(1, 1)] * 6, math.dist)
    assert len(same.range((1, 1), 0)) == 6
    assert height(same.root) == 3


def test_height_bound() -> None:
    for n in range(1, 130):
        t = VPTree([(i, 0) for i in range(n)], math.dist, seed=n)
        assert height(t.root) == n.bit_length()
        assert t.evaluations <= n * n.bit_length()


def test_random_against_scan() -> None:
    rng = random.Random(1993)
    for trial in range(500):
        if trial % 2:
            n = rng.randint(0, 40)
            dim = rng.choice([1, 2, 3])
            pts = [tuple(rng.randint(0, 9) for _ in range(dim)) for _ in range(n)]
            d = math.dist
            q = tuple(rng.uniform(-1, 10) for _ in range(dim))
            r = rng.uniform(0, 6)
        else:
            n = rng.randint(0, 30)
            pts = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 5))) for _ in range(n)]
            d = edit
            q = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
            r = rng.randint(0, 3)
        t = VPTree(pts, d, seed=trial)
        assert sorted(t.range(q, r)) == sorted(x for x in pts if d(q, x) <= r)
        nn = t.nearest(q)
        if pts:
            assert nn is not None and nn[1] == min(d(q, x) for x in pts) and d(q, nn[0]) == nn[1]
        else:
            assert nn is None
