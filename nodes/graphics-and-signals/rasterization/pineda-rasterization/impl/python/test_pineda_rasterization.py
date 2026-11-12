# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pineda-rasterization/. The authors are listed in prov/JW7NSM.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from pineda_rasterization import edge, pineda_rasterize


def covers_center(tri, cx: Fraction, cy: Fraction) -> bool:
    """Reference test, written from the Direct3D wording of the top-left rule.

    A point on an edge is inside if the edge is a top edge (exactly horizontal,
    with the third vertex below it, y down) or a left edge (not horizontal, with
    the third vertex to its right). Fractions in pixel units, no edge constants.
    """
    pts = [(Fraction(x), Fraction(y)) for x, y in tri]
    for k in range(3):
        a, b, c = pts[k], pts[(k + 1) % 3], pts[(k + 2) % 3]
        if (b[0] - a[0]) * (c[1] - a[1]) == (b[1] - a[1]) * (c[0] - a[0]):
            return False
        side_c = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        side_p = (b[0] - a[0]) * (cy - a[1]) - (b[1] - a[1]) * (cx - a[0])
        if side_p * side_c < 0:
            return False
        if side_p == 0:
            if a[1] == b[1]:
                is_top_left = c[1] > a[1]
            else:
                x_on_edge = a[0] + (b[0] - a[0]) * (c[1] - a[1]) / (b[1] - a[1])
                is_top_left = c[0] > x_on_edge
            if not is_top_left:
                return False
    return True


def brute(v0, v1, v2, width, height, sub):
    tri = [(Fraction(x, sub), Fraction(y, sub)) for x, y in (v0, v1, v2)]
    return [
        (i, j)
        for j in range(height)
        for i in range(width)
        if covers_center(tri, Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2))
    ]


def test_edge_function_is_twice_signed_area() -> None:
    assert edge((0, 0), (4, 0), (0, 3)) == 12
    assert edge((0, 0), (0, 3), (4, 0)) == -12
    assert edge((1, 1), (3, 3), (5, 5)) == 0


def test_worked_example() -> None:
    got = pineda_rasterize((1, 1), (9, 1), (1, 9), 5, 5, sub=2)
    assert got == [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (0, 3)]
    assert got == brute((1, 1), (9, 1), (1, 9), 5, 5, 2)
    other = pineda_rasterize((9, 1), (9, 9), (1, 9), 5, 5, sub=2)
    assert other == [(3, 1), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
    assert sorted(got + other) == sorted((i, j) for i in range(4) for j in range(4))


def test_edge_cases() -> None:
    assert pineda_rasterize((0, 0), (16, 16), (32, 32), 4, 4) == []
    assert pineda_rasterize((5, 5), (5, 5), (5, 5), 4, 4) == []
    assert pineda_rasterize((-100, -100), (-50, -100), (-100, -50), 4, 4) == []
    full = pineda_rasterize((-1000, -1000), (3000, -1000), (-1000, 3000), 4, 4)
    assert full == [(i, j) for j in range(4) for i in range(4)]
    # A pixel center exactly on a horizontal top edge is covered, on a bottom edge it is not.
    assert (0, 0) in pineda_rasterize((0, 8), (32, 8), (0, 40), 4, 4)
    assert (0, 0) not in pineda_rasterize((0, 8), (0, -24), (32, 8), 4, 4)
    with pytest.raises(ValueError):
        pineda_rasterize((0, 0), (1, 0), (0, 1), 2, 2, sub=3)


def test_both_windings_agree() -> None:
    rng = random.Random(7)
    for _ in range(200):
        v = [(rng.randrange(-8, 72), rng.randrange(-8, 72)) for _ in range(3)]
        assert pineda_rasterize(v[0], v[1], v[2], 4, 4) == pineda_rasterize(v[0], v[2], v[1], 4, 4)


def test_against_brute_force() -> None:
    rng = random.Random(1)
    for n in range(600):
        sub = rng.choice([2, 4, 16])
        step = rng.choice([1, sub // 2])  # step sub/2 puts vertices on pixel centers and edges through centers
        lo, hi = -sub, 6 * sub
        v = [(rng.randrange(lo, hi) // step * step, rng.randrange(lo, hi) // step * step) for _ in range(3)]
        assert pineda_rasterize(v[0], v[1], v[2], 5, 5, sub) == brute(v[0], v[1], v[2], 5, 5, sub), (n, v, sub)


def jittered_mesh(rng: random.Random, cells: int, cell: int, jitter: list[int]):
    """A triangulated grid that covers more than the screen, with random diagonals and vertex orders."""
    grid = {}
    for gy in range(cells + 1):
        for gx in range(cells + 1):
            jx = 0 if gx in (0, cells) else rng.choice(jitter)
            jy = 0 if gy in (0, cells) else rng.choice(jitter)
            grid[gx, gy] = ((gx - 1) * cell + jx, (gy - 1) * cell + jy)
    tris = []
    for gy in range(cells):
        for gx in range(cells):
            a, b, c, d = grid[gx, gy], grid[gx + 1, gy], grid[gx + 1, gy + 1], grid[gx, gy + 1]
            pair = [(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]
            for t in pair:
                assert edge(*t) > 0
                t = list(t)
                rng.shuffle(t)
                tris.append(tuple(t))
    return tris


@pytest.mark.parametrize("seed", range(6))
def test_shared_edges_cover_each_pixel_once(seed: int) -> None:
    rng = random.Random(seed)
    sub = 16
    w = h = 8
    jitter = [-8, 0, 8] if seed % 2 == 0 else list(range(-6, 7))
    tris = jittered_mesh(rng, 6, 32, jitter)
    count = Counter()
    for t in tris:
        count.update(pineda_rasterize(t[0], t[1], t[2], w, h, sub))
    assert all(count[i, j] == 1 for j in range(h) for i in range(w))
    assert sum(count.values()) == w * h


def test_fan_around_a_pixel_center() -> None:
    c = (40, 40)  # the center of pixel (2, 2) with sub = 16
    ring = [(8, 8), (40, 8), (72, 8), (72, 40), (72, 72), (40, 72), (8, 72), (8, 40)]
    count = Counter()
    for k in range(8):
        count.update(pineda_rasterize(c, ring[k], ring[(k + 1) % 8], 5, 5, 16))
    assert count[2, 2] == 1
    assert all(v == 1 for v in count.values())
