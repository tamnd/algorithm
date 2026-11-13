# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-erosion/. The authors are listed in prov/8EKNQA.jsonl.

import random

from morphological_erosion import erode, erode_by_parts, rectangle, reflect

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


def brute_erode_binary(f, se, outside):
    """The set definition: p is kept when every p + b is foreground."""
    h, w = len(f), len(f[0])
    fg = {(x, y) for y in range(h) for x in range(w) if f[y][x]}
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            ok = True
            for (u, v) in se:
                q = (x + u, y + v)
                if inside(q[0], q[1], w, h):
                    ok = ok and q in fg
                else:
                    ok = ok and outside != 0
            out[y][x] = 1 if ok else 0
    return out


def brute_erode_gray(f, se, outside, top):
    h, w = len(f), len(f[0])
    out = [[top] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            vals = [f[y + v][x + u] if inside(x + u, y + v, w, h) else outside for (u, v) in se]
            vals = [t for t in vals if t is not None]
            out[y][x] = min(vals + [top])
    return out


def minkowski_dilate(f, se, outside, bottom):
    """Dilation as a Minkowski sum: scatter each pixel p to p + b."""
    h, w = len(f), len(f[0])
    out = [[bottom] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            for (u, v) in se:
                if inside(x + u, y + v, w, h):
                    out[y + v][x + u] = max(out[y + v][x + u], f[y][x])
    if outside is not None:
        for y in range(h):
            for x in range(w):
                if any(not inside(x - u, y - v, w, h) for (u, v) in se):
                    out[y][x] = max(out[y][x], outside)
    return out


def rand_image(rng, w, h, top):
    return [[rng.randint(0, top) for _ in range(w)] for _ in range(h)]


def rand_se(rng, r=2):
    cells = [(u, v) for u in range(-r, r + 1) for v in range(-r, r + 1)]
    return rng.sample(cells, rng.randint(1, 6))


def test_example():
    assert erode(EXAMPLE, SQUARE) == [
        [0] * 8, [0] * 8, [0, 0, 1, 1, 0, 0, 0, 0], [0] * 8, [0] * 8]
    assert erode(EXAMPLE, CROSS) == [
        [0] * 8, [0] * 8, [0, 0, 1, 1, 1, 0, 0, 0], [0] * 8, [0] * 8]


def test_border_rules():
    y = [[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0]]
    assert erode(y, SQUARE) == [[1, 1, 0, 0]] * 3
    assert erode(y, SQUARE, outside=0) == [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    # An asymmetric element at the last column: the outside is ignored.
    assert erode(EXAMPLE, [(0, 0), (1, 0)])[2] == [0, 1, 1, 1, 1, 0, 0, 1]


def test_gray_is_moving_minimum():
    assert erode([[5, 3, 8, 8, 2, 7, 7, 6]], rectangle(-1, 1, 0, 0), top=255) == [[3, 3, 3, 2, 2, 2, 6, 6]]


def test_edges():
    assert erode([[1]], SQUARE) == [[1]]
    assert erode([[1]], SQUARE, outside=0) == [[0]]
    assert erode([[0, 1]], []) == [[1, 1]]  # the empty element erodes to everything
    assert erode([[0, 1, 1]], [(0, 0)]) == [[0, 1, 1]]  # the origin alone is the identity
    assert erode([], SQUARE) == []


def test_binary_against_set_definition():
    rng = random.Random(6101)
    for _ in range(600):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        f = rand_image(rng, w, h, 1)
        se = rand_se(rng)
        for outside in (None, 0, 1):
            assert erode(f, se, outside) == brute_erode_binary(f, se, outside)


def test_gray_against_direct_minimum():
    rng = random.Random(6102)
    for _ in range(500):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f = rand_image(rng, w, h, 255)
        se = rand_se(rng)
        for outside in (None, 0, 255, 17):
            assert erode(f, se, outside, top=255) == brute_erode_gray(f, se, outside, 255)


def test_duality_with_reflected_element():
    rng = random.Random(6103)
    for _ in range(500):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        top = rng.choice([1, 255])
        f = rand_image(rng, w, h, top)
        comp = [[top - t for t in row] for row in f]
        se = rand_se(rng)
        # the outside ignored on both sides
        lhs = [[top - t for t in row] for row in erode(f, se, None, top)]
        assert lhs == minkowski_dilate(comp, reflect(se), None, 0)
        # an outside value o on one side is top - o on the other
        o = rng.randint(0, top)
        lhs = [[top - t for t in row] for row in erode(f, se, o, top)]
        assert lhs == minkowski_dilate(comp, reflect(se), top - o, 0)


def test_increasing_and_anti_extensive():
    rng = random.Random(6104)
    for _ in range(300):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f1 = rand_image(rng, w, h, 9)
        f2 = [[min(9, t + rng.randint(0, 3)) for t in row] for row in f1]
        se = rand_se(rng)
        e1, e2 = erode(f1, se, top=9), erode(f2, se, top=9)
        assert all(a <= b for r1, r2 in zip(e1, e2) for a, b in zip(r1, r2))
        se0 = se + [(0, 0)]
        e0 = erode(f1, se0, top=9)
        assert all(a <= b for r1, r2 in zip(e0, f1) for a, b in zip(r1, r2))


def test_rectangle_by_two_segments():
    rng = random.Random(6105)
    for _ in range(300):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        f = rand_image(rng, w, h, 20)
        x0, y0 = rng.randint(-2, 1), rng.randint(-2, 1)
        x1, y1 = x0 + rng.randint(0, 3), y0 + rng.randint(0, 3)
        outside = rng.choice([None, 0, 7])
        direct = erode(f, rectangle(x0, x1, y0, y1), outside, top=20)
        parts = [rectangle(x0, x1, 0, 0), rectangle(0, 0, y0, y1)]
        assert erode_by_parts(f, parts, outside, top=20) == direct
