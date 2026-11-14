# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-spiral-toolpath/. The authors are listed in prov/RPHNQ4.jsonl.

import random
from fractions import Fraction as F

import pytest

from fermat_spiral_toolpath import fermat_rectangle, length, link_range, ring_count, segments


def box(seg):
    (x0, y0), (x1, y1) = seg
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def meet(a, b):
    """Intersection of two axis-parallel segments as a box, or None."""
    a, b = box(a), box(b)
    lo_x, lo_y, hi_x, hi_y = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    if lo_x > hi_x or lo_y > hi_y:
        return None
    return lo_x, lo_y, hi_x, hi_y


def union_area(rects):
    """Exact area of a union of boxes by coordinate compression (brute force)."""
    xs = sorted({r[0] for r in rects} | {r[2] for r in rects})
    ys = sorted({r[1] for r in rects} | {r[3] for r in rects})
    total = F(0)
    for i in range(len(xs) - 1):
        cx = (xs[i] + xs[i + 1]) / 2
        col = [r for r in rects if r[0] < cx < r[2]]
        for j in range(len(ys) - 1):
            cy = (ys[j] + ys[j + 1]) / 2
            if any(r[1] < cy < r[3] for r in col):
                total += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return total


def bead(path, w):
    """The square bead of side w swept along each segment."""
    h = w / 2
    return [(b[0] - h, b[1] - h, b[2] + h, b[3] + h) for b in map(box, segments(path))]


def random_case(rng):
    w = F(rng.choice([1, 1, 2, 3]), rng.choice([1, 2]))
    height = w * F(rng.randint(31, 130), 10)  # height > 3w, so n >= 2
    n = ring_count(height, w)
    width = max(height, 2 * n * w) + w * F(rng.randint(1, 60), 10)
    n, lo, hi = link_range(width, height, w)
    x = lo + (hi - lo) * F(rng.randint(1, 99), 100)
    return width, height, w, x


def check_simple(path):
    seg = segments(path)
    for i, a in enumerate(seg):
        assert a[0] != a[1] and (a[0][0] == a[1][0] or a[0][1] == a[1][1])  # nonzero, axis-parallel
        for j in range(i + 1, len(seg)):
            m = meet(a, seg[j])
            if j == i + 1:
                assert m == (a[1][0], a[1][1], a[1][0], a[1][1])  # only the shared vertex
            else:
                assert m is None


def test_page_example():
    p = fermat_rectangle(6, 4, 1, F(7, 2))
    h = F(1, 2)
    want = [(9 * h, h), (11 * h, h), (11 * h, 7 * h), (h, 7 * h), (h, h), (5 * h, h),
            (5 * h, 3 * h), (3 * h, 3 * h), (3 * h, 5 * h), (9 * h, 5 * h), (9 * h, 3 * h), (7 * h, 3 * h), (7 * h, h)]
    assert p == want
    assert length(p) == 23
    assert union_area(bead(p, F(1))) == 24  # covers the whole 6 x 4 rectangle


def test_simple_inside_and_ends_on_the_boundary():
    rng = random.Random(4)
    for _ in range(150):
        width, height, w, x = random_case(rng)
        p = fermat_rectangle(width, height, w, x)
        check_simple(p)
        assert all(w / 2 <= px <= width - w / 2 and w / 2 <= py <= height - w / 2 for px, py in p)
        (sx, sy), (ex, ey) = p[0], p[-1]
        assert sy == ey == w / 2 and sx - ex == w  # both ends on contour 1, side by side


def test_length_formula():
    rng = random.Random(5)
    for _ in range(150):
        width, height, w, x = random_case(rng)
        n = ring_count(height, w)
        assert length(fermat_rectangle(width, height, w, x)) == 2 * n * (width + height) - 4 * w * n * n - w


def test_coverage_and_overlap():
    rng = random.Random(6)
    exact = 0
    for _ in range(60):
        width, height, w, x = random_case(rng)
        if rng.random() < 0.3:  # make the height an even multiple of w
            height = 2 * w * rng.randint(2, 6)
            width = max(width, height + w)
            n, lo, hi = link_range(width, height, w)
            x = (lo + hi) / 2
        p = fermat_rectangle(width, height, w, x)
        n = ring_count(height, w)
        covered = union_area(bead(p, w))
        core = (width - 2 * n * w) * max(F(0), height - 2 * n * w)
        assert covered == width * height - core
        material = length(p) * w + w * w
        assert material >= covered
        if height == 2 * n * w:
            exact += 1
            assert covered == material == width * height  # no gap and no overlap
    assert exact > 5


def parallel_gap(a, b):
    """Distance of two parallel segments whose projections overlap with positive length, else None."""
    (ax0, ay0), (ax1, ay1) = a
    (bx0, by0), (bx1, by1) = b
    if ay0 == ay1 and by0 == by1:
        if min(max(ax0, ax1), max(bx0, bx1)) > max(min(ax0, ax1), min(bx0, bx1)):
            return abs(ay0 - by0)
    if ax0 == ax1 and bx0 == bx1:
        if min(max(ay0, ay1), max(by0, by1)) > max(min(ay0, ay1), min(by0, by1)):
            return abs(ax0 - bx0)
    return None


def test_spacing_of_passes_on_squares_and_rectangles():
    rng = random.Random(8)
    cases = [(F(7), F(7), F(1)), (F(21, 2), F(21, 2), F(1)), (F(9), F(9), F(1))]
    cases += [random_case(rng)[:3] for _ in range(40)]
    for width, height, w in cases:
        p = fermat_rectangle(width, height, w)
        seg = segments(p)
        gaps = [parallel_gap(seg[i], seg[j]) for i in range(len(seg)) for j in range(i + 1, len(seg))]
        n = ring_count(height, w)
        inner = height - (2 * n - 1) * w  # distance of the long sides of the innermost contour
        assert min(g for g in gaps if g is not None) == min(w, inner)


def test_feasibility_interval():
    rng = random.Random(7)
    for _ in range(60):
        width, height, w, _ = random_case(rng)
        n, lo, hi = link_range(width, height, w)
        for bad in (lo, hi, lo - w / 7, hi + w / 7):
            with pytest.raises(ValueError):
                fermat_rectangle(width, height, w, bad)
        check_simple(fermat_rectangle(width, height, w, lo + (hi - lo) / 1000))
        check_simple(fermat_rectangle(width, height, w, hi - (hi - lo) / 1000))
    with pytest.raises(ValueError):
        fermat_rectangle(6, 6, 1)  # n = 3 needs width > 6
    with pytest.raises(ValueError):
        fermat_rectangle(10, 2, 1)  # one contour only
    check_simple(fermat_rectangle(7, 6, 1))


def test_without_the_bounds_the_path_breaks():
    # At X = hi the first piece of each contour has length zero.
    width, height, w = F(10), F(7), F(1)
    n, lo, hi = link_range(width, height, w)
    p = fermat_rectangle(width, height, w, hi - F(1, 10 ** 6))
    assert min(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in segments(p)) == F(1, 10 ** 6)
