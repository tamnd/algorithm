# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/str-packing/. The authors are listed in prov/4SAGYZ.jsonl.
import math
import random

import pytest

from str_packing import STRTree, intersects

PTS = [(1, 1), (2, 7), (3, 4), (4, 9), (5, 2), (6, 6), (7, 1), (8, 8),
       (9, 3), (10, 10), (11, 5), (12, 2), (13, 7), (14, 4), (15, 9), (16, 1)]
NAMES = "ABCDEFGHIJKLMNOP"


def test_page_example():
    t = STRTree([(NAMES[i], (x, y, x, y)) for i, (x, y) in enumerate(PTS)], 4)
    t.check_invariant()
    leaves = [("".join(e[1] for e in nd.entries), nd.rect) for nd in t.levels[0]]
    assert leaves == [("AGEC", (1, 1, 7, 4)), ("FBHD", (2, 6, 8, 9)),
                      ("PLIN", (9, 1, 16, 4)), ("KMOJ", (10, 5, 15, 10))]
    assert t.height() == 1 and t.root.rect == (1, 1, 16, 10)
    assert sorted(t.search((5, 5, 10, 9))) == ["F", "H"]
    assert t.search((0, 0, 0.5, 0.5)) == []


def test_edge_cases():
    t = STRTree([], 4)
    assert t.root is None and t.search((0, 0, 1, 1)) == []
    t = STRTree([("a", (0, 0, 1, 1))], 4)
    assert t.height() == 0 and t.search((1, 1, 2, 2)) == ["a"]
    t = STRTree([(i, (0, 0, 0, 0)) for i in range(10)], 3)  # all equal
    t.check_invariant()
    assert sorted(t.search((0, 0, 0, 0))) == list(range(10))
    with pytest.raises(ValueError):
        STRTree([], 1)


def test_random_against_brute_force():
    rng = random.Random(97)
    for _ in range(500):
        n = rng.randint(1, 120)
        M = rng.randint(2, 9)
        items = []
        for k in range(n):
            x, y = rng.uniform(0, 100), rng.uniform(0, 100)
            items.append((k, (x, y, x + rng.uniform(0, 8), y + rng.uniform(0, 8))))
        t = STRTree(items, M)
        t.check_invariant()
        # level sizes are ceil(previous / M), so the height is ceil(log_M n)
        size = n
        for nodes in t.levels:
            size = math.ceil(size / M)
            assert len(nodes) == size
        assert t.height() == (0 if n <= M else len(t.levels) - 1)
        h, cap = 0, M
        while cap < n:
            cap *= M
            h += 1
        assert t.height() == h
        for _ in range(5):
            x, y = rng.uniform(-5, 100), rng.uniform(-5, 100)
            q = (x, y, x + rng.uniform(0, 30), y + rng.uniform(0, 30))
            got = t.search(q)
            assert sorted(got) == sorted(k for k, r in items if intersects(q, r))
