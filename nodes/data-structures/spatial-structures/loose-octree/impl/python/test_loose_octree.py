# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loose-octree/. The authors are listed in prov/7DA53Q.jsonl.

import random

import pytest

from loose_octree import LooseOctree, Node, meets


def shape(u: Node) -> object:
    return (sorted(u.boxes), {o: shape(c) for o, c in enumerate(u.children) if c is not None})


A = ((1, 1, 1), (2, 2, 2))
B = ((3, 3, 0), (5, 5, 0))
C = ((0, 0, 0), (7, 3, 3))
D = ((6, 1, 6), (6, 1, 6))


def test_page_example() -> None:
    t = LooseOctree(3)
    assert t.place(A) == (3, (1, 1, 1))
    assert t.place(B) == (2, (2, 2, 0))
    assert t.place(C) == (0, (0, 0, 0))
    assert t.place(D) == (3, (6, 1, 6))
    for b in [A, B, C, D]:
        assert t.insert(b)
        t.check_invariant()
    assert not t.insert(B)
    assert t.node_count() == 9
    assert t.root.boxes == [C]
    assert t.root.children[3] is not None and t.root.children[3].children[0].boxes == [B]
    assert sorted(t.query(((3, 3, 0), (4, 4, 1)))) == sorted([B, C])
    assert t.delete(A) and not t.delete(A)
    t.check_invariant()
    assert t.node_count() == 6
    assert t.move(D, ((2, 2, 2), (2, 2, 2)))
    t.check_invariant()
    assert t.node_count() == 6 and t.place(((2, 2, 2), (2, 2, 2))) == (3, (2, 2, 2))


def test_edges() -> None:
    t = LooseOctree(0)
    p = ((0, 0, 0), (0, 0, 0))
    assert t.insert(p) and t.root.boxes == [p] and t.query(p) == [p]
    assert t.delete(p) and len(t) == 0 and not t.move(p, p)
    with pytest.raises(ValueError):
        t.insert(((0, 0, 0), (1, 0, 0)))
    with pytest.raises(ValueError):
        LooseOctree(-1)
    u = LooseOctree(10)
    small = ((511, 0, 0), (512, 1, 1))
    assert u.place(small) == (10, (511, 0, 0))
    assert u.insert(small) and u.node_count() == 11


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for case in range(600):
        depth = rng.randint(0, 5)
        side = 1 << depth
        t = LooseOctree(depth)
        live: set = set()

        def rand_box() -> tuple:
            e = rng.randint(0, max(1, side // rng.choice([1, 2, 4, 8])) - 1)
            lo = tuple(rng.randrange(side - e) for _ in range(3))
            hi = tuple(min(side - 1, lo[i] + rng.randint(0, e)) for i in range(3))
            return (lo, hi)

        for _ in range(rng.randint(1, 30)):
            if live and rng.random() < 0.3:
                d = rng.choice(sorted(live))
                if rng.random() < 0.5:
                    assert t.delete(d)
                    live.discard(d)
                else:
                    nb = rand_box()
                    if nb not in live:
                        assert t.move(d, nb)
                        live.discard(d)
                        live.add(nb)
            b = rand_box()
            assert t.insert(b) == (b not in live)
            live.add(b)
        t.check_invariant()
        assert sorted(t.boxes()) == sorted(live)
        u = LooseOctree(depth)
        for b in rng.sample(sorted(live), len(live)):
            u.insert(b)
        assert shape(u.root) == shape(t.root)
        for _ in range(3):
            q = rand_box()
            assert sorted(t.query(q)) == sorted(b for b in live if meets(b, q))
