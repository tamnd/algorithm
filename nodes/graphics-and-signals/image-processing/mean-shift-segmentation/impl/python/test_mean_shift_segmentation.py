# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-shift-segmentation/. The authors are listed in prov/YT936C.jsonl.

import random
from fractions import Fraction

import pytest

from mean_shift_segmentation import (
    _points,
    _sq,
    epanechnikov_density,
    group_modes,
    in_window,
    mean_shift_filter,
    mean_shift_point,
    mean_shift_segmentation,
)

EXAMPLE = [
    [10, 12, 11, 50, 52],
    [11, 13, 10, 51, 49],
    [12, 30, 12, 50, 51],
]


def random_image(rng, h, w, colors, top):
    if colors == 1:
        return [[rng.randint(0, top) for _ in range(w)] for _ in range(h)]
    return [[tuple(rng.randint(0, top) for _ in range(colors)) for _ in range(w)] for _ in range(h)]


def direct_mean_shift(pts, start, hs, hr):
    """The definition with no shortcut: every pixel is tested for the window."""
    hs, hr = Fraction(hs), Fraction(hr)
    y = start
    while True:
        win = [p for p in pts if _sq(p[:2], y[:2]) / hs**2 + _sq(p[2:], y[2:]) / hr**2 <= 1]
        new = tuple(sum(p[t] for p in win) / Fraction(len(win)) for t in range(len(y)))
        if new == y:
            return y
        y = new


@pytest.mark.parametrize("colors", [1, 3])
def test_paths_rise_in_density_and_stop_at_a_fixed_point(colors):
    rng = random.Random(2002 + colors)
    for _ in range(60):
        img = random_image(rng, rng.randint(1, 5), rng.randint(1, 5), colors, rng.choice([5, 40]))
        hs, hr = rng.choice([1, 2, 3]), rng.choice([3, 8, 20])
        pts = _points(img)
        for p in pts:
            mode, path = mean_shift_point(pts, p, hs, hr)
            assert mode == direct_mean_shift(pts, p, hs, hr)
            # The mode is the mean of its own window.
            win = [q for q in pts if in_window(q, mode, Fraction(hs), Fraction(hr), "ball")]
            assert tuple(sum(q[t] for q in win) / Fraction(len(win)) for t in range(len(mode))) == mode
            # Each step raises the Epanechnikov density by at least n |step|^2,
            # with n the window size and distances in scaled coordinates.
            for a, b in zip(path, path[1:]):
                n = sum(1 for q in pts if in_window(q, a, Fraction(hs), Fraction(hr), "ball"))
                step = _sq(a[:2], b[:2]) / Fraction(hs) ** 2 + _sq(a[2:], b[2:]) / Fraction(hr) ** 2
                assert epanechnikov_density(pts, b, hs, hr) - epanechnikov_density(pts, a, hs, hr) >= n * step > 0


def test_product_window_can_cycle():
    # With the window |dx| <= h_s and |dc| <= h_r taken separately, the point
    # (1, 1, 7) moves to (1, 3/4, 29/4) and back.
    img = [[8, 4, 5], [9, 7, 9]]
    pts = _points(img)
    start = pts[4]
    assert start == (1, 1, 7)
    with pytest.raises(RuntimeError):
        mean_shift_point(pts, start, 1, 3, kernel="product", max_iter=50)
    # The joint ball has no such cycle.
    mode, _ = mean_shift_point(pts, start, 1, 3)
    assert mode == direct_mean_shift(pts, start, 1, 3)


def brute_force_groups(modes, hs, hr):
    n = len(modes)
    near = lambda a, b: _sq(a[:2], b[:2]) < hs * hs and _sq(a[2:], b[2:]) < hr * hr
    comp = [-1] * n
    for i in range(n):
        if comp[i] < 0:
            comp[i] = i
            stack = [i]
            while stack:
                a = stack.pop()
                for b in range(n):
                    if comp[b] < 0 and near(modes[a], modes[b]):
                        comp[b] = i
                        stack.append(b)
    return comp


def same_partition(a, b):
    return len(set(a)) == len(set(zip(a, b))) == len(set(b))


def test_grouping_is_the_transitive_closure():
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(1, 12)
        modes = [tuple(Fraction(rng.randint(0, 40), 4) for _ in range(3)) for _ in range(n)]
        hs, hr = rng.choice([1, 2, 3]), rng.choice([1, 2, 5])
        assert same_partition(group_modes(modes, hs, hr), brute_force_groups(modes, hs, hr))


@pytest.mark.parametrize("colors", [1, 3])
def test_segmentation_invariants(colors):
    rng = random.Random(77 + colors)
    for _ in range(25):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        img = random_image(rng, h, w, colors, rng.choice([3, 30]))
        hs, hr = rng.choice([1, 2]), rng.choice([2, 6, 15])
        lab = mean_shift_segmentation(img, hs, hr)
        _, modes = mean_shift_filter(img, hs, hr)
        groups = group_modes(modes, hs, hr)
        flat = [v for row in lab for v in row]
        n = max(flat) + 1
        for r in range(n):
            cells = [(x, y) for y in range(h) for x in range(w) if lab[y][x] == r]
            # A region lies in one cluster of modes and is 4-connected.
            assert len({groups[y * w + x] for x, y in cells}) == 1
            seen, stack = {cells[0]}, [cells[0]]
            while stack:
                x, y = stack.pop()
                for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if q in set(cells) and q not in seen:
                        seen.add(q)
                        stack.append(q)
            assert seen == set(cells)
        # Two adjacent regions belong to different clusters.
        for y in range(h):
            for x in range(w):
                for nx, ny in ((x + 1, y), (x, y + 1)):
                    if nx < w and ny < h and lab[y][x] != lab[ny][nx]:
                        assert groups[y * w + x] != groups[ny * w + nx]
        # Merging small regions leaves no region below the size, unless one is left.
        for m in (2, 4):
            merged = mean_shift_segmentation(img, hs, hr, min_size=m)
            sizes = {}
            for v in (v for row in merged for v in row):
                sizes[v] = sizes.get(v, 0) + 1
            assert len(sizes) == 1 or min(sizes.values()) >= m


def test_example():
    assert mean_shift_segmentation(EXAMPLE, 2, 8) == [[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 2, 0, 1, 1]]
    assert mean_shift_segmentation(EXAMPLE, 2, 8, min_size=2) == [[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]
    assert mean_shift_segmentation(EXAMPLE, 2, 25) == [[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]
    filtered, _ = mean_shift_filter(EXAMPLE, 2, 8)
    dark, bright = (Fraction(91, 8),), (Fraction(101, 2),)
    assert filtered[2][1] == (30,)
    assert all(filtered[y][x] == dark for y in range(3) for x in range(3) if (x, y) != (1, 2))
    assert all(filtered[y][x] == bright for y in range(3) for x in (3, 4))
    # The path of the top left pixel.
    pts = _points(EXAMPLE)
    _, path = mean_shift_point(pts, pts[0], 2, 8)
    assert path == [(0, 0, 10), (Fraction(1, 2), Fraction(1, 2), Fraction(23, 2)), (Fraction(6, 7), Fraction(5, 7), Fraction(79, 7)), (1, Fraction(7, 8), Fraction(91, 8))]


def test_bad_kernel():
    with pytest.raises(ValueError):
        mean_shift_point(_points([[1]]), (0, 0, 1), 1, 1, kernel="gauss")
