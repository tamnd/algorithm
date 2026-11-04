# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-quadtree/. The authors are listed in prov/HXZGKW.jsonl.

import random

import pytest

from linear_quadtree import LinearQuadtree, demorton, morton


def oracle(depth: int, black: set[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """The black leaves of the region quadtree, in Morton order, by recursion on cells."""
    out = []
    stack = [(0, 0, 1 << depth)]
    while stack:
        x, y, s = stack.pop()
        cells = [(i, j) for i in range(x, x + s) for j in range(y, y + s)]
        n = sum(1 for c in cells if c in black)
        if n == len(cells):
            out.append((x, y, s))
        elif n > 0:
            h = s // 2
            # push in reverse quadrant order so SW comes out first
            for bx, by in [(1, 1), (0, 1), (1, 0), (0, 0)]:
                stack.append((x + bx * h, y + by * h, h))
    return out


def test_morton() -> None:
    assert morton(2, 0, 2) == 4 and morton(1, 3, 2) == 11 and morton(3, 1, 2) == 7
    for z in range(256):
        assert morton(*demorton(z, 4), 4) == z


def test_page_example() -> None:
    black = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (3, 0), (2, 1), (1, 3)]
    t = LinearQuadtree.from_pixels(2, black)
    t.check_invariant()
    assert list(zip(t.codes, t.levels)) == [(0, 1), (4, 0), (5, 0), (6, 0), (11, 0)]
    assert t.area() == 8 and len(t) == 5
    assert t.locate((1, 1)) == (0, 0, 2)
    assert t.locate((3, 1)) is None
    assert t.blocks_in_cell(2, 0, 1) == [(2, 0, 1), (3, 0, 1), (2, 1, 1)]
    assert t.insert((3, 1))
    t.check_invariant()
    assert list(zip(t.codes, t.levels)) == [(0, 1), (4, 1), (11, 0)]
    assert t.delete((0, 0))
    t.check_invariant()
    assert list(zip(t.codes, t.levels)) == [(1, 0), (2, 0), (3, 0), (4, 1), (11, 0)]


def test_edges() -> None:
    t = LinearQuadtree(0)
    assert (0, 0) not in t and t.locate((0, 0)) is None
    assert t.insert((0, 0)) and not t.insert((0, 0))
    assert t.blocks() == [(0, 0, 1)]
    assert t.delete((0, 0)) and not t.delete((0, 0)) and len(t) == 0
    with pytest.raises(ValueError):
        t.insert((1, 0))
    with pytest.raises(ValueError):
        LinearQuadtree(-1)
    full = LinearQuadtree.from_pixels(3, [(i, j) for i in range(8) for j in range(8)])
    assert full.blocks() == [(0, 0, 8)]
    assert full.blocks_in_cell(4, 4, 1) == [(4, 4, 2)]
    assert full.delete((7, 7))
    full.check_invariant()
    assert len(full) == 9 and full.area() == 63
    with pytest.raises(ValueError):
        full.blocks_in_cell(1, 0, 1)


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for case in range(600):
        depth = rng.randint(0, 4)
        side = 1 << depth
        density = rng.random()
        black = {(i, j) for i in range(side) for j in range(side) if rng.random() < density}
        t = LinearQuadtree.from_pixels(depth, black)
        t.check_invariant()
        assert t.blocks() == oracle(depth, black)
        u = LinearQuadtree(depth)
        for p in rng.sample(sorted(black), len(black)):
            assert u.insert(p)
        assert u.codes == t.codes and u.levels == t.levels
        for _ in range(20):
            p = (rng.randrange(side), rng.randrange(side))
            assert (p in t) == (p in black)
            if rng.random() < 0.5:
                assert t.insert(p) == (p not in black)
                black.add(p)
            else:
                assert t.delete(p) == (p in black)
                black.discard(p)
            t.check_invariant()
        assert t.blocks() == oracle(depth, black)
        assert sorted(t.pixels()) == sorted(black)
        lvl = rng.randint(0, depth)
        cx = rng.randrange(side >> lvl) << lvl
        cy = rng.randrange(side >> lvl) << lvl
        got = t.blocks_in_cell(cx, cy, lvl)
        cell = {(i, j) for i in range(cx, cx + (1 << lvl)) for j in range(cy, cy + (1 << lvl))}
        covered = {(i, j) for x, y, s in got for i in range(x, x + s) for j in range(y, y + s)}
        assert covered == cell & black
