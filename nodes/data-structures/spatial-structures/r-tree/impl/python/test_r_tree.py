# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-tree/. The authors are listed in prov/SKDGZ3.jsonl.

import random

import pytest

from r_tree import RTree, area, intersects, quadratic_split

PAGE = [
    ("a", (0, 0, 2, 2)),
    ("b", (1, 5, 3, 7)),
    ("c", (6, 0, 8, 1)),
    ("d", (7, 6, 9, 9)),
    ("e", (2, 1, 3, 3)),
    ("f", (6, 7, 7, 8)),
]


def leaf_groups(t: RTree) -> list[list[str]]:
    return sorted(sorted(x for _, x in c.entries) for _, c in t.root.entries)


def test_page_example() -> None:
    t = RTree(4, 2)
    for oid, r in PAGE[:4]:
        t.insert(oid, r)
        t.check_invariant()
    assert t.height() == 0
    t.insert(*PAGE[4])
    t.check_invariant()
    assert t.height() == 1
    assert leaf_groups(t) == [["a", "b", "e"], ["c", "d"]]
    t.insert(*PAGE[5])
    t.check_invariant()
    assert leaf_groups(t) == [["a", "b", "e"], ["c", "d", "f"]]
    assert sorted(t.search((2.5, 2.5, 7, 7))) == ["b", "d", "e", "f"]
    assert sorted(t.search((4, 3, 5, 5))) == []
    assert t.delete("c", (6, 0, 8, 1))
    t.check_invariant()
    assert leaf_groups(t) == [["a", "b", "e"], ["d", "f"]]
    assert t.delete("d", (7, 6, 9, 9))
    t.check_invariant()
    assert t.height() == 0
    assert sorted(x for x, _ in t.items()) == ["a", "b", "e", "f"]


def test_split_seeds() -> None:
    es = [(r, oid) for oid, r in PAGE[:5]]
    g1, g2 = quadratic_split(es, 2)
    assert sorted(x for _, x in g1 + g2) == ["a", "b", "c", "d", "e"]
    assert min(len(g1), len(g2)) >= 2


def test_edges() -> None:
    t = RTree(4)
    assert t.search((0, 0, 1, 1)) == []
    assert not t.delete("x", (0, 0, 1, 1))
    with pytest.raises(ValueError):
        t.insert("x", (1, 0, 0, 1))
    with pytest.raises(ValueError):
        RTree(4, 3)
    for k in range(30):
        t.insert(k, (0, 0, 0, 0))  # many equal points
        t.check_invariant()
    assert len(t.search((0, 0, 0, 0))) == 30
    assert t.search((0.5, 0.5, 1, 1)) == []


def test_random_against_model() -> None:
    rng = random.Random(99)
    for trial in range(500):
        M = rng.choice([3, 4, 5, 8])
        m = rng.randint(1, M // 2)
        t = RTree(M, m)
        model: dict[int, tuple[float, float, float, float]] = {}
        nxt = 0
        for _ in range(rng.randint(1, 60)):
            if model and rng.random() < 0.35:
                k = rng.choice(list(model))
                assert t.delete(k, model.pop(k))
            else:
                x, y = rng.randint(0, 30), rng.randint(0, 30)
                r = (x, y, x + rng.randint(0, 6), y + rng.randint(0, 6))
                t.insert(nxt, r)
                model[nxt] = r
                nxt += 1
        t.check_invariant()
        assert sorted(x for x, _ in t.items()) == sorted(model)
        for _ in range(3):
            x, y = rng.randint(-2, 34), rng.randint(-2, 34)
            q = (x, y, x + rng.randint(0, 10), y + rng.randint(0, 10))
            assert sorted(t.search(q)) == sorted(k for k, r in model.items() if intersects(r, q))
        assert not t.delete(-1, (0, 0, 1, 1))
