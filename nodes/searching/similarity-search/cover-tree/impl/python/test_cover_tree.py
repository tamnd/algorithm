# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cover-tree/. The authors are listed in prov/GE45W4.jsonl.

import math
import random

from cover_tree import CoverTree

LINE = [(0,), (8,), (4,), (2,), (6,), (1,), (7,), (3,)]


def check_invariants(t: CoverTree) -> None:
    levels = t.levels()
    par = t.parent_at()
    for i, ci in levels.items():
        # nesting
        if i - 1 in levels:
            assert set(ci) <= set(levels[i - 1])
        # separation
        for a in range(len(ci)):
            for b in range(a + 1, len(ci)):
                assert t.dist(t.points[ci[a]], t.points[ci[b]]) > 2.0 ** i
        # covering
        if i + 1 in levels:
            for p in ci:
                q = par[(p, i)]
                assert q in levels[i + 1]
                assert t.dist(t.points[p], t.points[q]) <= 2.0 ** (i + 1)
    # every distinct point appears at the bottom level
    stored = set(levels[min(levels)]) if levels else set()
    dups = {d for v in t.dups.values() for d in v}
    assert stored | dups == set(range(len(t.points)))


def test_example() -> None:
    t = CoverTree()
    for p in LINE:
        t.insert(p)
    assert (t.top, t.bottom) == (3, -1)
    assert t.levels() == {3: [0], 2: [0, 1], 1: [0, 1, 2], 0: [0, 1, 2, 3, 4],
                          -1: [0, 1, 2, 3, 4, 5, 6, 7]}
    assert t.children[0] == {3: [1], 2: [2], 1: [3], 0: [5]}
    d, i = t.nearest((5.4,))
    assert i == 4 and abs(d - 0.6) < 1e-12
    check_invariants(t)


def test_edge_cases() -> None:
    t = CoverTree()
    assert t.nearest((1.0,)) is None
    t.insert((1.0,))
    assert t.nearest((5.0,)) == (4.0, 0)
    t.insert((1.0,))
    assert t.dups == {0: [1]}
    t.insert((1.25,))
    check_invariants(t)
    assert t.nearest((1.2,))[1] == 2


def test_random_against_brute_force() -> None:
    rng = random.Random(45)
    for _ in range(500):
        dim = rng.randint(1, 3)
        n = rng.randint(1, 25)
        grid = rng.random() < 0.3
        pts = [tuple(float(rng.randint(0, 5)) if grid else rng.uniform(-10, 10)
                     for _ in range(dim)) for _ in range(n)]
        t = CoverTree()
        for p in pts:
            t.insert(p)
        check_invariants(t)
        for _ in range(3):
            q = tuple(rng.uniform(-12, 12) for _ in range(dim))
            d, i = t.nearest(q)
            assert abs(d - min(math.dist(q, p) for p in pts)) < 1e-9
            assert abs(math.dist(q, pts[i]) - d) < 1e-12
