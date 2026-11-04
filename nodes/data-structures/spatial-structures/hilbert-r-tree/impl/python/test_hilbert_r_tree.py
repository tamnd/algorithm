# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hilbert-r-tree/. The authors are listed in prov/P4XVG6.jsonl.

import random

import pytest

from hilbert_r_tree import HilbertRTree, hilbert_index, meets

A, B, C, D, E = (0, 0, 1, 1), (6, 0, 7, 1), (0, 6, 1, 7), (6, 6, 7, 7), (3, 3, 4, 4)
F, G, H, I = (2, 0, 2, 1), (5, 5, 5, 6), (0, 3, 1, 3), (7, 3, 7, 4)


def leaves(t: HilbertRTree) -> list[list[tuple[int, int, int, int]]]:
    out, stack = [], [t.root]
    while stack:
        u = stack.pop()
        if u.leaf:
            out.append([r for _, r in u.entries])
        else:
            stack.extend(reversed(u.entries))
    return out


def test_hilbert_index() -> None:
    assert [hilbert_index(1, x, y) for x, y in [(0, 0), (0, 1), (1, 1), (1, 0)]] == [0, 1, 2, 3]
    assert hilbert_index(3, 5, 2) == 55
    assert sorted(hilbert_index(3, x, y) for x in range(8) for y in range(8)) == list(range(64))


def test_page_example() -> None:
    t = HilbertRTree(3, 4)
    keys = {r: t.key(r)[0] for r in [A, B, C, D, E, F, G, H, I]}
    assert keys == {A: 2, B: 242, C: 82, D: 162, E: 42, F: 17, G: 139, H: 61, I: 193}
    for r in [A, B, C, D]:
        t.insert(r)
    assert leaves(t) == [[A, C, D, B]] and t.height() == 0
    t.insert(E)
    assert leaves(t) == [[A, E, C], [D, B]] and t.height() == 1
    t.insert(F)
    t.insert(G)
    assert leaves(t) == [[A, F, E, C], [G, D, B]]
    t.insert(H)
    assert leaves(t) == [[A, F, E, H], [C, G, D, B]]
    t.insert(I)
    t.check_invariant()
    assert leaves(t) == [[A, F, E], [H, C, G], [D, I, B]]
    assert [c.mbr for c in t.root.entries] == [(0, 0, 4, 4), (0, 3, 5, 7), (6, 0, 7, 7)]
    assert not t.insert(I)
    assert sorted(t.window((0, 0, 2, 2))) == [A, F]
    assert t.delete(E) and t.delete(F) and not t.delete(F)
    t.check_invariant()
    assert leaves(t) == [[A, H], [C, G], [D, I, B]]
    assert t.delete(H)
    t.check_invariant()
    assert leaves(t) == [[A, C, G], [D, I, B]]


def test_edges() -> None:
    t = HilbertRTree(0, 4)
    assert t.window((0, 0, 0, 0)) == [] and not t.delete((0, 0, 0, 0))
    assert t.insert((0, 0, 0, 0)) and t.window((0, 0, 0, 0)) == [(0, 0, 0, 0)]
    assert t.delete((0, 0, 0, 0)) and len(t) == 0
    with pytest.raises(ValueError):
        t.insert((0, 0, 1, 0))
    with pytest.raises(ValueError):
        HilbertRTree(3, 3)
    u = HilbertRTree(6, 4)
    rs = [(x, y, x, y) for x in range(16) for y in range(16)]
    for r in rs:
        u.insert(r)
    u.check_invariant()
    assert u.height() >= 3
    for r in rs:
        assert u.delete(r)
    u.check_invariant()
    assert len(u) == 0 and u.root.leaf


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for case in range(600):
        depth = rng.randint(0, 5)
        side = 1 << depth
        t = HilbertRTree(depth, rng.randint(4, 7))
        live: set = set()
        for _ in range(rng.randint(1, 70)):
            x1, x2 = sorted(rng.randrange(side) for _ in range(2))
            y1, y2 = sorted(rng.randrange(side) for _ in range(2))
            r = (x1, y1, x2, y2)
            if live and rng.random() < 0.4:
                d = rng.choice(sorted(live))
                assert t.delete(d)
                live.discard(d)
            else:
                assert t.insert(r) == (r not in live)
                live.add(r)
        t.check_invariant()
        assert t.rects() == sorted(live, key=t.key)
        for _ in range(3):
            x1, x2 = sorted(rng.randrange(side) for _ in range(2))
            y1, y2 = sorted(rng.randrange(side) for _ in range(2))
            q = (x1, y1, x2, y2)
            assert sorted(t.window(q)) == sorted(r for r in live if meets(r, q))
