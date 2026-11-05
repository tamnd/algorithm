# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gnat/. The authors are listed in prov/2746FY.jsonl.

import math
import random

from gnat import GNAT

PTS = [(0, 0), (1, 1), (9, 0), (8, 1), (0, 9), (1, 8), (5, 5), (9, 9), (2, 3), (7, 6)]


def collect(node, out):
    if node is None:
        return
    out.extend(node.bucket)
    out.extend(node.splits)
    for k in node.kids:
        collect(k, out)


def test_example() -> None:
    g = GNAT(PTS, m=3, leaf_size=2)
    assert g.root.splits == [0, 7, 2]
    assert [round(v, 2) for v in g.root.ranges[1][0]] == [8.06, 12.73]
    assert [round(v, 2) for v in g.root.ranges[1][1]] == [0.0, 5.66]
    g.evals = 0
    assert g.range((6, 4), 2) == [6]
    assert g.evals == 4
    d, i = g.nearest((6, 4))
    assert i == 6 and abs(d - math.sqrt(2)) < 1e-12


def test_edge_cases() -> None:
    g = GNAT([])
    assert g.range((0, 0), 5) == [] and g.nearest((0, 0)) is None
    g = GNAT([(1, 1)] * 5, m=2, leaf_size=1)
    assert g.range((1, 1), 0) == [0, 1, 2, 3, 4]
    assert g.nearest((2, 1)) == (1.0, 0)


def test_random_against_scan() -> None:
    rng = random.Random(2746)
    for _ in range(500):
        dim = rng.randint(1, 3)
        n = rng.randint(0, 30)
        grid = rng.random() < 0.4
        pts = [tuple(float(rng.randint(0, 4)) if grid else rng.uniform(0, 10) for _ in range(dim))
               for _ in range(n)]
        g = GNAT(pts, m=rng.randint(2, 5), leaf_size=rng.randint(1, 4))
        ids = []
        collect(g.root, ids)
        assert sorted(ids) == list(range(n))
        for _ in range(3):
            q = tuple(rng.uniform(-1, 11) for _ in range(dim))
            r = rng.choice([0.0, 0.5, 1.0, 2.5, 6.0])
            want = [i for i, p in enumerate(pts) if math.dist(q, p) <= r]
            assert g.range(q, r) == want
            res = g.nearest(q)
            if n == 0:
                assert res is None
            else:
                want_nn = min((math.dist(q, p), i) for i, p in enumerate(pts))
                assert res == want_nn
