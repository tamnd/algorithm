# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-star-tree/. The authors are listed in prov/DENQWV.jsonl.
import random

import pytest

from r_star_tree import RStarTree, intersects, rstar_split


E = {"a": (0, 0, 2, 2), "b": (1, 5, 3, 7), "c": (6, 0, 8, 1), "d": (7, 6, 9, 9),
     "e": (2, 1, 3, 3), "f": (6, 7, 7, 8), "g": (1, 3, 2, 4), "h": (3, 6, 4, 8)}


def leaves(t):
    nodes = [t.root] if t.root.leaf else [c for _, c in t.root.entries]
    return sorted((u.rect(), "".join(sorted(x for _, x in u.entries))) for u in nodes)


def test_page_example():
    t = RStarTree(4, 2, 1)
    for k in "abcde":
        t.insert(k, E[k])
    assert leaves(t) == [((0, 0, 3, 7), "abe"), ((6, 0, 9, 9), "cd")]
    for k in "fg":
        t.insert(k, E[k])
    assert leaves(t) == [((0, 0, 3, 7), "abeg"), ((6, 0, 9, 9), "cdf")]
    t.insert("h", E["h"])  # reinsert h once, then split on y
    assert leaves(t) == [((0, 0, 3, 4), "aeg"), ((1, 5, 4, 8), "bh"), ((6, 0, 9, 9), "cdf")]
    t.check_invariant()
    assert sorted(t.search((2.5, 2.5, 7, 7))) == list("bdefh")
    assert t.search((4.5, 1.5, 5.5, 4.5)) == []
    assert t.delete("c", E["c"])
    assert leaves(t)[2] == ((6, 6, 9, 9), "df")
    assert t.delete("d", E["d"])
    assert leaves(t) == [((0, 0, 3, 4), "aeg"), ((1, 5, 7, 8), "bfh")]
    assert not t.delete("d", E["d"])


def test_split_rule():
    es = [(E[k], k) for k in "abegh"]
    g1, g2 = rstar_split(es, 2)
    assert {x for _, x in g1} == set("aeg") and {x for _, x in g2} == set("bh")


def test_edge_cases():
    t = RStarTree(4, 2, 1)
    assert t.search((0, 0, 1, 1)) == [] and not t.delete(1, (0, 0, 1, 1))
    for k in range(30):
        t.insert(k, (5, 5, 5, 5))  # all equal points
    t.check_invariant()
    assert len(t.search((5, 5, 5, 5))) == 30
    for k in range(30):
        assert t.delete(k, (5, 5, 5, 5))
    t.check_invariant()
    assert t.root.leaf and not t.root.entries
    with pytest.raises(ValueError):
        RStarTree(4, 3)
    with pytest.raises(ValueError):
        t.insert(0, (1, 1, 0, 0))


def test_random_against_brute_force():
    rng = random.Random(1990)
    for trial in range(500):
        M = rng.randint(3, 8)
        t = RStarTree(M)
        live = {}
        for k in range(rng.randint(0, 60)):
            x, y = rng.uniform(0, 100), rng.uniform(0, 100)
            r = (x, y, x + rng.uniform(0, 10), y + rng.uniform(0, 10))
            t.insert(k, r)
            live[k] = r
            if rng.random() < 0.25 and live:
                d = rng.choice(list(live))
                assert t.delete(d, live.pop(d))
        t.check_invariant()
        assert sorted(t.items()) == sorted(live.items())
        for _ in range(4):
            x, y = rng.uniform(-5, 100), rng.uniform(-5, 100)
            q = (x, y, x + rng.uniform(0, 30), y + rng.uniform(0, 30))
            assert sorted(t.search(q)) == sorted(k for k, r in live.items() if intersects(q, r))
