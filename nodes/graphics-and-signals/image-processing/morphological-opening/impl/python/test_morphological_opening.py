# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-opening/. The authors are listed in prov/97EJK2.jsonl.

import random

from morphological_opening import open_image, rectangle

SQUARE = rectangle(-1, 1, -1, 1)
CROSS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def parse(rows):
    return [[1 if c == "#" else 0 for c in r] for r in rows]


EXAMPLE = parse(["........", ".####...", ".#####.#", ".####...", "........"])


def translate_cut(se, z, w, h):
    """The translate B_z cut to the image."""
    return [(z[0] + u, z[1] + v) for (u, v) in se
            if 0 <= z[0] + u < w and 0 <= z[1] + v < h]


def brute_open_binary(f, se):
    """The union of the translates B_z (z in the image, cut to it) that fit inside X."""
    h, w = len(f), len(f[0])
    out = [[0] * w for _ in range(h)]
    for zy in range(h):
        for zx in range(w):
            cells = translate_cut(se, (zx, zy), w, h)
            if all(f[y][x] for (x, y) in cells):
                for (x, y) in cells:
                    out[y][x] = 1
    return out


def brute_open_gray(f, se, top):
    """The maximum, over the translates that cover p, of the minimum of f on the translate."""
    h, w = len(f), len(f[0])
    out = [[0] * w for _ in range(h)]
    for zy in range(h):
        for zx in range(w):
            cells = translate_cut(se, (zx, zy), w, h)
            low = min([top] + [f[y][x] for (x, y) in cells])
            for (x, y) in cells:
                out[y][x] = max(out[y][x], low)
    return out


def rand_image(rng, w, h, top, p=0.5):
    if top == 1:
        return [[1 if rng.random() < p else 0 for _ in range(w)] for _ in range(h)]
    return [[rng.randint(0, top) for _ in range(w)] for _ in range(h)]


def rand_se(rng, r=2):
    cells = [(u, v) for u in range(-r, r + 1) for v in range(-r, r + 1)]
    return rng.sample(cells, rng.randint(1, 6))


def leq(a, b):
    return all(x <= y for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_example():
    assert open_image(EXAMPLE, SQUARE) == parse(
        ["........", ".####...", ".####...", ".####...", "........"])
    assert open_image(EXAMPLE, CROSS) == parse(
        ["........", "..###...", ".#####..", "..###...", "........"])


def test_gray_row():
    # The bright plateaus narrower than the segment are cut down; wider ones stay.
    row = [[5, 3, 8, 8, 2, 7, 7, 7, 6]]
    assert open_image(row, rectangle(-1, 1, 0, 0), top=255) == [[3, 3, 3, 3, 2, 7, 7, 7, 6]]


def test_edges():
    assert open_image([], SQUARE) == []
    assert open_image([[1, 0, 1]], [(0, 0)]) == [[1, 0, 1]]
    assert open_image([[1, 1]], []) == [[0, 0]]


def test_binary_against_fitted_translates():
    rng = random.Random(6301)
    for _ in range(600):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        f = rand_image(rng, w, h, 1, rng.choice([0.5, 0.7, 0.85]))
        se = rand_se(rng)
        assert open_image(f, se) == brute_open_binary(f, se)


def test_gray_against_max_of_min():
    rng = random.Random(6302)
    for _ in range(400):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f = rand_image(rng, w, h, 30)
        se = rand_se(rng)
        assert open_image(f, se, top=30) == brute_open_gray(f, se, 30)


def test_idempotent_binary():
    rng = random.Random(6303)
    for _ in range(500):
        w, h = rng.randint(1, 8), rng.randint(1, 8)
        f = rand_image(rng, w, h, 1, rng.choice([0.5, 0.7, 0.85]))
        se = rand_se(rng)
        once = open_image(f, se)
        assert open_image(once, se) == once


def test_idempotent_gray():
    rng = random.Random(6304)
    for _ in range(400):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        f = rand_image(rng, w, h, 255)
        se = rand_se(rng)
        once = open_image(f, se, top=255)
        assert open_image(once, se, top=255) == once


def test_anti_extensive_and_increasing():
    rng = random.Random(6305)
    for _ in range(400):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        f1 = rand_image(rng, w, h, 9)
        f2 = [[min(9, t + rng.randint(0, 3)) for t in row] for row in f1]
        se = rand_se(rng)  # the origin need not be in se
        o1, o2 = open_image(f1, se, top=9), open_image(f2, se, top=9)
        assert leq(o1, f1)
        assert leq(o1, o2)


def test_larger_square_removes_more():
    rng = random.Random(6306)
    big = rectangle(-2, 2, -2, 2)
    for _ in range(300):
        w, h = rng.randint(1, 8), rng.randint(1, 8)
        f = rand_image(rng, w, h, 1, 0.8)
        small = open_image(f, SQUARE)
        large = open_image(f, big)
        assert leq(large, small)
        assert open_image(small, big) == large
