# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-dilation/. The authors are listed in prov/GK4YJV.jsonl.

import random

from morphological_dilation import dilate, rectangle, reflect

EXAMPLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
SQUARE = rectangle(-1, 1, -1, 1)
CROSS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def inside(x, y, w, h):
    return 0 <= x < w and 0 <= y < h


def parse(rows):
    return [[1 if c == "#" else 0 for c in r] for r in rows]


def brute_dilate_binary(f, se, outside):
    """The set definition: p is foreground when some p - b is foreground."""
    h, w = len(f), len(f[0])
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            hit = False
            for (u, v) in se:
                if inside(x - u, y - v, w, h):
                    hit = hit or f[y - v][x - u] == 1
                else:
                    hit = hit or outside == 1
            out[y][x] = 1 if hit else 0
    return out


def minkowski_sum(f, se):
    """Scatter each foreground pixel p to every p + b inside the image."""
    h, w = len(f), len(f[0])
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if f[y][x]:
                for (u, v) in se:
                    if inside(x + u, y + v, w, h):
                        out[y + v][x + u] = 1
    return out


def brute_erode(f, se, outside, top):
    """Erosion by its set definition, an independent reference for duality."""
    h, w = len(f), len(f[0])
    out = [[top] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            for (u, v) in se:
                t = f[y + v][x + u] if inside(x + u, y + v, w, h) else outside
                out[y][x] = min(out[y][x], t)
    return out


def brute_dilate_gray(f, se, outside, bottom):
    h, w = len(f), len(f[0])
    out = [[bottom] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            for (u, v) in se:
                t = f[y - v][x - u] if inside(x - u, y - v, w, h) else outside
                if t is not None:
                    out[y][x] = max(out[y][x], t)
    return out


def rand_image(rng, w, h, top):
    return [[rng.randint(0, top) for _ in range(w)] for _ in range(h)]


def rand_se(rng, r=2):
    cells = [(u, v) for u in range(-r, r + 1) for v in range(-r, r + 1)]
    return rng.sample(cells, rng.randint(1, 6))


def test_example():
    assert dilate(EXAMPLE, SQUARE) == parse(
        ["######..", "########", "########", "########", "######.."])
    assert dilate(EXAMPLE, CROSS) == parse(
        [".####...", "######.#", "########", "######.#", ".####..."])
    assert sum(map(sum, dilate(EXAMPLE, CROSS))) == 30


def test_asymmetric_element():
    assert dilate(EXAMPLE, [(0, 0), (1, 0)]) == parse(
        ["........", ".#####..", ".#######", ".#####..", "........"])


def test_gray_is_moving_maximum():
    assert dilate([[5, 3, 8, 8, 2, 7, 7, 6]], rectangle(-1, 1, 0, 0)) == [[5, 8, 8, 8, 8, 7, 7, 7]]


def test_edges():
    assert dilate([[0]], SQUARE) == [[0]]
    assert dilate([[0]], SQUARE, outside=1) == [[1]]
    assert dilate([[0, 1]], []) == [[0, 0]]  # the empty element dilates to nothing
    assert dilate([[0, 1, 1]], [(0, 0)]) == [[0, 1, 1]]
    assert dilate([], SQUARE) == []


def test_binary_against_set_definition():
    rng = random.Random(6201)
    for _ in range(600):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        f = rand_image(rng, w, h, 1)
        se = rand_se(rng)
        for outside in (None, 0, 1):
            assert dilate(f, se, outside) == brute_dilate_binary(f, se, outside)
        assert dilate(f, se) == minkowski_sum(f, se)


def test_gray_against_direct_maximum():
    rng = random.Random(6202)
    for _ in range(500):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f = rand_image(rng, w, h, 255)
        se = rand_se(rng)
        for outside in (None, 0, 255, 17):
            assert dilate(f, se, outside) == brute_dilate_gray(f, se, outside, 0)


def test_duality_with_reflected_element():
    rng = random.Random(6203)
    for _ in range(500):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        top = rng.choice([1, 255])
        f = rand_image(rng, w, h, top)
        comp = [[top - t for t in row] for row in f]
        se = rand_se(rng)
        o = rng.randint(0, top)
        lhs = [[top - t for t in row] for row in dilate(f, se, o)]
        assert lhs == brute_erode(comp, reflect(se), top - o, top)
        lhs = [[top - t for t in row] for row in dilate(f, se)]
        assert lhs == brute_erode(comp, reflect(se), top, top)


def test_union_and_element_distributivity():
    rng = random.Random(6204)
    for _ in range(300):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f1, f2 = rand_image(rng, w, h, 1), rand_image(rng, w, h, 1)
        b1, b2 = rand_se(rng), rand_se(rng)
        union = [[max(a, b) for a, b in zip(r1, r2)] for r1, r2 in zip(f1, f2)]
        d1, d2 = dilate(f1, b1), dilate(f2, b1)
        assert dilate(union, b1) == [[max(a, b) for a, b in zip(r1, r2)] for r1, r2 in zip(d1, d2)]
        e1, e2 = dilate(f1, b1), dilate(f1, b2)
        assert dilate(f1, b1 + b2) == [[max(a, b) for a, b in zip(r1, r2)] for r1, r2 in zip(e1, e2)]


def test_increasing_and_extensive():
    rng = random.Random(6205)
    for _ in range(300):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f1 = rand_image(rng, w, h, 9)
        f2 = [[min(9, t + rng.randint(0, 3)) for t in row] for row in f1]
        se = rand_se(rng)
        d1, d2 = dilate(f1, se), dilate(f2, se)
        assert all(a <= b for r1, r2 in zip(d1, d2) for a, b in zip(r1, r2))
        d0 = dilate(f1, se + [(0, 0)])
        assert all(a >= b for r1, r2 in zip(d0, f1) for a, b in zip(r1, r2))


def test_rectangle_by_two_segments():
    rng = random.Random(6206)
    for _ in range(300):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        f = rand_image(rng, w, h, 20)
        x0, y0 = rng.randint(-2, 1), rng.randint(-2, 1)
        x1, y1 = x0 + rng.randint(0, 3), y0 + rng.randint(0, 3)
        outside = rng.choice([None, 0, 7])
        direct = dilate(f, rectangle(x0, x1, y0, y1), outside)
        two = dilate(dilate(f, rectangle(x0, x1, 0, 0), outside), rectangle(0, 0, y0, y1), outside)
        assert two == direct
