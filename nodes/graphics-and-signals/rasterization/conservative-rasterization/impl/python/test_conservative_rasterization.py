# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-rasterization/. The authors are listed in prov/HFMB32.jsonl.

import random
from fractions import Fraction

import pytest

from conservative_rasterization import conservative_rasterize


def orient(a, b, c) -> int:
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def on_segment(a, b, p) -> bool:
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet(a, b, c, d) -> bool:
    """Closed segments ab and cd share a point (exact)."""
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return (o1 == 0 and on_segment(a, b, c)) or (o2 == 0 and on_segment(a, b, d)) or (
        o3 == 0 and on_segment(c, d, a)) or (o4 == 0 and on_segment(c, d, b))


def in_triangle(tri, p) -> bool:
    """p in the closed triangle (nonzero area)."""
    s = [orient(tri[k], tri[(k + 1) % 3], p) for k in range(3)]
    return all(x >= 0 for x in s) or all(x <= 0 for x in s)


def in_square(x0, y0, x1, y1, p) -> bool:
    return x0 <= p[0] <= x1 and y0 <= p[1] <= y1


def brute_over(tri, width, height, sub):
    """Closed square meets closed triangle: a vertex in the square, a corner in the triangle, or crossing edges."""
    out = []
    for j in range(height):
        for i in range(width):
            x0, y0, x1, y1 = i * sub, j * sub, (i + 1) * sub, (j + 1) * sub
            corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            hit = any(in_square(x0, y0, x1, y1, v) for v in tri) or any(in_triangle(tri, c) for c in corners)
            if not hit:
                hit = any(segments_meet(tri[k], tri[(k + 1) % 3], corners[m], corners[(m + 1) % 4]) for k in range(3) for m in range(4))
            if hit:
                out.append((i, j))
    return out


def brute_inner(tri, width, height, sub):
    """Closed square inside the closed triangle: its four corners are inside (the triangle is convex)."""
    out = []
    for j in range(height):
        for i in range(width):
            corners = [(i * sub, j * sub), ((i + 1) * sub, j * sub), ((i + 1) * sub, (j + 1) * sub), (i * sub, (j + 1) * sub)]
            if all(in_triangle(tri, c) for c in corners):
                out.append((i, j))
    return out


def covers_center(tri, cx, cy) -> bool:
    """Top-left rule from its Direct3D wording, with Fractions."""
    pts = [(Fraction(x), Fraction(y)) for x, y in tri]
    for k in range(3):
        a, b, c = pts[k], pts[(k + 1) % 3], pts[(k + 2) % 3]
        side_c = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if side_c == 0:
            return False
        side_p = (b[0] - a[0]) * (cy - a[1]) - (b[1] - a[1]) * (cx - a[0])
        if side_p * side_c < 0:
            return False
        if side_p == 0:
            if a[1] == b[1]:
                ok = c[1] > a[1]
            else:
                ok = c[0] > a[0] + (b[0] - a[0]) * (c[1] - a[1]) / (b[1] - a[1])
            if not ok:
                return False
    return True


def random_triangle(rng: random.Random, sub: int, span: int):
    while True:
        step = rng.choice([1, sub // 2, sub])
        tri = tuple((rng.randrange(-sub, span * sub) // step * step, rng.randrange(-sub, span * sub) // step * step) for _ in range(3))
        if orient(*tri) != 0:
            return tri


EX = ((8, 8), (72, 8), (8, 72))  # (0.5, 0.5), (4.5, 0.5), (0.5, 4.5) with sub = 16


def test_worked_example() -> None:
    over = conservative_rasterize(*EX, 8, 8, 16)
    inner = conservative_rasterize(*EX, 8, 8, 16, inner=True)
    assert over == [(i, j) for j in range(5) for i in range(5) if i + j <= 5]
    assert len(over) == 19
    assert inner == [(1, 1), (2, 1), (1, 2)]
    assert over == brute_over(EX, 8, 8, 16) and inner == brute_inner(EX, 8, 8, 16)


def test_small_and_thin_triangles() -> None:
    small = ((19, 19), (22, 19), (19, 22))  # (2.375, 2.375), (2.75, 2.375), (2.375, 2.75) with sub = 8
    assert conservative_rasterize(*small, 6, 6, 8) == [(2, 2)]
    assert conservative_rasterize(*small, 6, 6, 8, inner=True) == []
    thin = ((0, 0), (64, 0), (64, 4))  # (0, 0), (4, 0), (4, 0.25): no center, but touches pixels of row 0
    got = conservative_rasterize(*thin, 6, 6, 16)
    assert got == brute_over(thin, 6, 6, 16)
    assert {(i, 0) for i in range(4)} <= set(got)


def test_edge_cases() -> None:
    assert conservative_rasterize((0, 0), (16, 16), (32, 32), 4, 4) == []
    assert conservative_rasterize((-99, -99), (-50, -99), (-99, -50), 4, 4) == []
    big = ((-999, -999), (3000, -999), (-999, 3000))
    assert conservative_rasterize(*big, 4, 4) == [(i, j) for j in range(4) for i in range(4)]
    assert conservative_rasterize(*big, 4, 4, inner=True) == [(i, j) for j in range(4) for i in range(4)]
    with pytest.raises(ValueError):
        conservative_rasterize((0, 0), (3, 0), (0, 3), 4, 4, sub=3)


def test_against_brute_force() -> None:
    rng = random.Random(11)
    for n in range(350):
        sub = rng.choice([2, 4, 16])
        tri = random_triangle(rng, sub, 6)
        for t in (tri, (tri[0], tri[2], tri[1])):
            assert conservative_rasterize(*t, 6, 6, sub) == brute_over(t, 6, 6, sub), (n, t, sub)
            assert conservative_rasterize(*t, 6, 6, sub, inner=True) == brute_inner(t, 6, 6, sub), (n, t, sub)


def test_inner_within_centers_within_over() -> None:
    rng = random.Random(12)
    for _ in range(300):
        sub = rng.choice([2, 4, 16])
        tri = random_triangle(rng, sub, 8)
        over = set(conservative_rasterize(*tri, 8, 8, sub))
        inner = set(conservative_rasterize(*tri, 8, 8, sub, inner=True))
        centers = {(i, j) for j in range(8) for i in range(8) if covers_center(tri, Fraction(2 * i + 1, 2) * sub, Fraction(2 * j + 1, 2) * sub)}
        assert inner <= centers <= over


@pytest.mark.parametrize("seed", range(3))
def test_mesh_inner_sets_are_disjoint_and_over_sets_cover(seed: int) -> None:
    rng = random.Random(seed)
    cell, cells = 32, 6
    grid = {}
    for gy in range(cells + 1):
        for gx in range(cells + 1):
            inner = 0 < gx < cells and 0 < gy < cells
            jx = rng.choice([-8, 0, 8, -5, 6]) if inner else 0
            jy = rng.choice([-8, 0, 8, -5, 6]) if inner else 0
            grid[gx, gy] = ((gx - 1) * cell + jx, (gy - 1) * cell + jy)
    seen_inner: set[tuple[int, int]] = set()
    union_over: set[tuple[int, int]] = set()
    for gy in range(cells):
        for gx in range(cells):
            a, b, c, d = grid[gx, gy], grid[gx + 1, gy], grid[gx + 1, gy + 1], grid[gx, gy + 1]
            for t in ([(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]):
                got = set(conservative_rasterize(*t, 8, 8, 16, inner=True))
                assert not (got & seen_inner)
                seen_inner |= got
                union_over |= set(conservative_rasterize(*t, 8, 8, 16))
    assert union_over == {(i, j) for j in range(8) for i in range(8)}
