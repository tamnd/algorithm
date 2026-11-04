# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-r-tree/. The authors are listed in prov/8PZPPQ.jsonl.
import random

import pytest

from priority_r_tree import PRTree, intersects, mbr, pseudo_pr_leaves

PTS = {"A": (1, 1), "B": (2, 9), "C": (3, 4), "D": (4, 7), "E": (5, 2), "F": (6, 6),
       "G": (7, 10), "H": (8, 3), "I": (9, 8), "J": (10, 1), "K": (11, 5), "L": (12, 9),
       "M": (13, 3), "N": (14, 7), "O": (15, 1), "P": (16, 6)}
DATA = [(k, (x, y, x + 1, y + 1)) for k, (x, y) in PTS.items()]


def test_page_example():
    groups = pseudo_pr_leaves([(r, k) for k, r in DATA], 3)
    names = ["".join(k for _, k in g) for g in groups]
    assert names == ["ABC", "JOE", "PNM", "GLI", "DF", "HK"]
    t = PRTree(DATA, 3)
    t.check_invariant()
    assert t.height() == 2
    kids = [sorted("".join(k for _, k in leaf.entries) for _, leaf in u.entries)
            for _, u in t.root.entries]
    assert kids == [["ABC", "DF", "JOE"], ["GLI", "HK", "PNM"]]
    assert sorted(t.search((5, 5, 10, 9))) == ["D", "F", "I"]
    assert t.visited == 6


def test_small_and_errors():
    t = PRTree([], 3)
    assert t.search((0, 0, 1, 1)) == [] and t.height() == -1
    t.check_invariant()
    t = PRTree([("a", (0, 0, 1, 1))], 3)
    assert t.search((1, 1, 2, 2)) == ["a"] and t.height() == 0
    with pytest.raises(ValueError):
        PRTree([], 1)
    with pytest.raises(ValueError):
        PRTree([("a", (1, 0, 0, 1))], 3)


def test_priority_leaves_hold_extremes():
    rng = random.Random(3)
    items = []
    for k in range(40):
        x, y = rng.randint(0, 50), rng.randint(0, 50)
        items.append(((x, y, x + rng.randint(0, 9), y + rng.randint(0, 9)), k))
    groups = pseudo_pr_leaves(items, 4)
    first = groups[0]
    assert max(r[0] for r, _ in first) <= min(r[0] for r, _ in items if (r, _) not in first)
    assert sorted(k for g in groups for _, k in g) == list(range(40))


def test_random_against_brute_force():
    rng = random.Random(11)
    for trial in range(600):
        B = rng.randint(2, 6)
        data = []
        for k in range(rng.randint(0, 60)):
            x, y = rng.randint(0, 40), rng.randint(0, 40)
            s = rng.choice([0, 2, 10])
            data.append((k, (x, y, x + rng.randint(0, s), y + rng.randint(0, s))))
        t = PRTree(data, B)
        t.check_invariant()
        for _ in range(4):
            x, y = rng.randint(-5, 45), rng.randint(-5, 45)
            q = (x, y, x + rng.randint(0, 15), y + rng.randint(0, 15))
            want = sorted(k for k, r in data if intersects(q, r))
            assert sorted(t.search(q)) == want
