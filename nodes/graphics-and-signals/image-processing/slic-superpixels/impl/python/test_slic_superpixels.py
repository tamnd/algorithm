# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slic-superpixels/. The authors are listed in prov/2WFPAC.jsonl.

import random
from fractions import Fraction

import pytest

from slic_superpixels import (
    _as_colors,
    assign,
    distance2,
    enforce_connectivity,
    grid_seeds,
    in_window,
    initial_centers,
    slic,
    update,
)


def random_image(rng, h, w, colors=1, top=255):
    if colors == 1:
        return [[rng.randint(0, top) for _ in range(w)] for _ in range(h)]
    return [[tuple(rng.randint(0, top) for _ in range(colors)) for _ in range(w)] for _ in range(h)]


def is_connected(labels, j):
    h, w = len(labels), len(labels[0])
    cells = {(x, y) for y in range(h) for x in range(w) if labels[y][x] == j}
    start = next(iter(cells))
    seen, stack = {start}, [start]
    while stack:
        x, y = stack.pop()
        for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if p in cells and p not in seen:
                seen.add(p)
                stack.append(p)
    return seen == cells


def brute_force_assign(img, centers, s2, m, old):
    """Every pixel against every center: the first center with the least D
    among those whose window covers the pixel."""
    out = [row[:] for row in old]
    for y, row in enumerate(img):
        for x, c in enumerate(row):
            cover = [(distance2(c, x, y, cen, s2, m), j) for j, cen in enumerate(centers) if in_window(x, y, cen, s2)]
            if cover:
                out[y][x] = min(cover)[1]
    return out


def random_centers(rng, img, k):
    h, w = len(img), len(img[0])
    dim = len(img[0][0])
    return [
        (
            tuple(Fraction(rng.randint(0, 2550), 10) for _ in range(dim)),
            Fraction(rng.randint(0, 10 * (w - 1)), 10),
            Fraction(rng.randint(0, 10 * (h - 1)), 10),
        )
        for _ in range(k)
    ]


@pytest.mark.parametrize("colors", [1, 3])
def test_assignment_is_the_nearest_covering_center(colors):
    rng = random.Random(2012 + colors)
    for _ in range(150):
        h, w = rng.randint(1, 8), rng.randint(1, 8)
        img = _as_colors(random_image(rng, h, w, colors))
        k = rng.randint(1, 6)
        centers = random_centers(rng, img, k)
        s2 = Fraction(h * w, k)
        m = rng.choice([1, 5, 10, 40])
        old = [[rng.randint(-1, k - 1) for _ in range(w)] for _ in range(h)]
        assert assign(img, centers, s2, m, old) == brute_force_assign(img, centers, s2, m, old)


def test_update_gives_exact_means():
    rng = random.Random(7)
    for _ in range(100):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        img = _as_colors(random_image(rng, h, w, 3))
        k = rng.randint(1, 4)
        labels = [[rng.randint(0, k - 1) for _ in range(w)] for _ in range(h)]
        old = random_centers(rng, img, k)
        new = update(img, labels, old)
        for j in range(k):
            pix = [(img[y][x], x, y) for y in range(h) for x in range(w) if labels[y][x] == j]
            if not pix:
                assert new[j] == old[j]
                continue
            n = len(pix)
            color = tuple(sum(p[0][t] for p in pix) / Fraction(n) for t in range(3))
            assert new[j] == (color, Fraction(sum(p[1] for p in pix), n), Fraction(sum(p[2] for p in pix), n))


@pytest.mark.parametrize("colors", [1, 3])
def test_superpixel_invariants(colors):
    rng = random.Random(34 + colors)
    for _ in range(40):
        h, w = rng.randint(2, 12), rng.randint(2, 12)
        raw = random_image(rng, h, w, colors, top=rng.choice([3, 255]))
        k = rng.randint(1, max(1, h * w // 4))
        labels, centers, it = slic(raw, k, m=rng.choice([1, 10, 40]), max_iter=10)
        img = _as_colors(raw)
        n = len(centers)
        # Every pixel is in a superpixel, and labels appear in raster order.
        flat = [v for row in labels for v in row]
        assert all(0 <= v < n for v in flat) and set(flat) == set(range(n))
        assert [v for i, v in enumerate(flat) if v not in flat[:i]] == list(range(n))
        # Each superpixel is 4-connected after the postprocessing.
        assert all(is_connected(labels, j) for j in range(n))
        # The centers are the exact means of their superpixels.
        assert update(img, labels, centers) == centers
        assert 1 <= it <= 10


def test_converged_centers_are_a_fixed_point():
    rng = random.Random(99)
    for _ in range(30):
        h, w = rng.randint(3, 10), rng.randint(3, 10)
        img = _as_colors(random_image(rng, h, w, 1, top=9))
        k = rng.randint(1, 6)
        centers, s2 = initial_centers(img, k)
        labels = [[-1] * w for _ in range(h)]
        for _ in range(60):
            labels = assign(img, centers, s2, 10, labels)
            new = update(img, labels, centers)
            if new == centers:
                break
            centers = new
        else:
            continue
        # Stopped with E = 0: one more step changes nothing.
        assert assign(img, centers, s2, 10, labels) == labels


def energy(img, labels, centers, s2, m):
    return sum(distance2(img[y][x], x, y, centers[labels[y][x]], s2, m) for y in range(len(img)) for x in range(len(img[0])))


def test_windowed_assignment_can_raise_the_energy():
    # In k-means no step raises the sum of squared distances. In SLIC a pixel
    # can leave the window of its center when the center moves, and must take
    # a farther center.
    img = _as_colors([[6, 0], [8, 9], [4, 1]])
    centers, s2 = initial_centers(img, 5)
    labels = [[-1] * 2 for _ in range(3)]
    rises = []
    after_update = None
    for _ in range(10):
        labels = assign(img, centers, s2, 1, labels)
        e = energy(img, labels, centers, s2, 1)
        if after_update is not None:
            rises.append(e > after_update)
        new = update(img, labels, centers)
        after_update = energy(img, labels, new, s2, 1)
        assert after_update <= e  # the update step never raises it
        if new == centers:
            break
        centers = new
    assert any(rises)


def test_grid_seeds():
    assert grid_seeds(9, 9, 9) == [(1, 1), (4, 1), (7, 1), (1, 4), (4, 4), (7, 4), (1, 7), (4, 7), (7, 7)]
    assert grid_seeds(5, 3, 1) == [(2, 1)]
    for w, h, k in ((10, 4, 3), (7, 7, 5), (1, 9, 4), (20, 20, 400)):
        seeds = grid_seeds(w, h, k)
        assert all(0 <= x < w and 0 <= y < h for x, y in seeds)
        assert len(set(seeds)) == len(seeds)


def test_seeds_move_off_an_edge():
    # The seed of a 3 by 3 image is its middle pixel, which sits on a vertical
    # edge; it moves to the flat column on the left.
    img = _as_colors([[0, 0, 9], [0, 0, 9], [0, 0, 9]])
    [(c, x, y)], s2 = initial_centers(img, 1)
    assert (x, y) == (0, 0) and c == (0,) and s2 == 9


def test_postprocessing_moves_orphans():
    img = _as_colors([[0, 0, 0], [0, 0, 0]])
    centers = [((Fraction(0),), Fraction(0), Fraction(0)), ((Fraction(0),), Fraction(2), Fraction(1))]
    labels = [[0, 0, 1], [1, 0, 1]]
    assert enforce_connectivity(img, labels, centers, Fraction(3), 10) == [[0, 0, 1], [0, 0, 1]]


def test_two_flat_halves():
    # With little weight on position, no superpixel crosses the step edge.
    img = [[10] * 4 + [200] * 4 for _ in range(8)]
    labels, centers, _ = slic(img, 4, m=1)
    for j in range(len(centers)):
        sides = {x < 4 for y in range(8) for x in range(8) if labels[y][x] == j}
        assert len(sides) == 1
    assert len(centers) == 4


def test_one_superpixel():
    labels, centers, _ = slic([[1, 2], [3, 4]], 1)
    assert labels == [[0, 0], [0, 0]]
    assert centers == [((Fraction(5, 2),), Fraction(1, 2), Fraction(1, 2))]
