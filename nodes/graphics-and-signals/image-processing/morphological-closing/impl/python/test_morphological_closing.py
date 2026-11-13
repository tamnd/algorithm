# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-closing/. The authors are listed in prov/V188PY.jsonl.

import random

from morphological_closing import close_image, rectangle, reflect

SQUARE = rectangle(-1, 1, -1, 1)
CROSS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def parse(rows):
    return [[1 if c == "#" else 0 for c in r] for r in rows]


EXAMPLE = parse([
    "............",
    "............",
    "..###.####..",
    "..#.#.####..",
    "..###.#.##..",
    "............",
    "............"])


def cut(cells, w, h):
    return [(x, y) for (x, y) in cells if 0 <= x < w and 0 <= y < h]


def brute_open_gray(f, se, top):
    """Opening as the maximum over covering translates of the minimum on the translate."""
    h, w = len(f), len(f[0])
    out = [[0] * w for _ in range(h)]
    for zy in range(h):
        for zx in range(w):
            cells = cut([(zx + u, zy + v) for (u, v) in se], w, h)
            low = min([top] + [f[y][x] for (x, y) in cells])
            for (x, y) in cells:
                out[y][x] = max(out[y][x], low)
    return out


def brute_close_gray(f, se, top):
    """Closing as the minimum, over the translates of the reflected element that cover p,
    of the maximum of f on the translate."""
    h, w = len(f), len(f[0])
    out = [[top] * w for _ in range(h)]
    for zy in range(h):
        for zx in range(w):
            cells = cut([(zx - u, zy - v) for (u, v) in se], w, h)
            high = max([0] + [f[y][x] for (x, y) in cells])
            for (x, y) in cells:
                out[y][x] = min(out[y][x], high)
    return out


def brute_close_binary(f, se):
    """p stays background exactly when a translate of the reflected element holds p
    and misses the foreground."""
    h, w = len(f), len(f[0])
    out = [[1] * w for _ in range(h)]
    for zy in range(h):
        for zx in range(w):
            cells = cut([(zx - u, zy - v) for (u, v) in se], w, h)
            if not any(f[y][x] for (x, y) in cells):
                for (x, y) in cells:
                    out[y][x] = 0
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
    assert close_image(EXAMPLE, SQUARE) == parse([
        "............",
        "............",
        "..########..",
        "..########..",
        "..########..",
        "............",
        "............"])
    assert close_image(EXAMPLE, CROSS) == parse([
        "............",
        "............",
        "..###.####..",
        "..########..",
        "..###.#.##..",
        "............",
        "............"])


def test_border_grows_foreground():
    # With the outside ignored, a closing can add foreground along the border.
    f = parse(["....", ".##.", "...."])
    assert close_image(f, rectangle(-1, 1, 0, 0)) == parse(["....", "####", "...."])
    assert close_image(parse(["#.#"]), rectangle(-1, 1, 0, 0)) == parse(["###"])
    # On the whole plane the closing of a single pixel by the segment is the pixel itself.
    assert close_image(parse(["#.."]), rectangle(-1, 1, 0, 0)) == parse(["#.."])
    assert close_image(parse(["#."]), rectangle(-1, 1, 0, 0)) == parse(["##"])


def test_gray_row():
    row = [[5, 3, 8, 8, 2, 7, 7, 6]]
    assert close_image(row, rectangle(-1, 1, 0, 0), top=255) == [[5, 5, 8, 8, 7, 7, 7, 7]]


def test_binary_against_direct_scan():
    rng = random.Random(6401)
    for _ in range(600):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        f = rand_image(rng, w, h, 1, rng.choice([0.15, 0.3, 0.5]))
        se = rand_se(rng)
        assert close_image(f, se) == brute_close_binary(f, se)


def test_gray_against_min_of_max():
    rng = random.Random(6402)
    for _ in range(400):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        f = rand_image(rng, w, h, 30)
        se = rand_se(rng)
        assert close_image(f, se, top=30) == brute_close_gray(f, se, 30)


def test_duality_with_opening_of_complement():
    rng = random.Random(6403)
    for _ in range(400):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        top = rng.choice([1, 255])
        f = rand_image(rng, w, h, top)
        se = rand_se(rng)
        comp = [[top - t for t in row] for row in f]
        rhs = [[top - t for t in row] for row in brute_open_gray(comp, reflect(se), top)]
        assert close_image(f, se, top=top) == rhs


def test_idempotent_binary():
    rng = random.Random(6404)
    for _ in range(500):
        w, h = rng.randint(1, 8), rng.randint(1, 8)
        f = rand_image(rng, w, h, 1, rng.choice([0.15, 0.3, 0.5]))
        se = rand_se(rng)
        once = close_image(f, se)
        assert close_image(once, se) == once


def test_idempotent_gray():
    rng = random.Random(6405)
    for _ in range(400):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        f = rand_image(rng, w, h, 255)
        se = rand_se(rng)
        once = close_image(f, se, top=255)
        assert close_image(once, se, top=255) == once


def test_extensive_and_increasing():
    rng = random.Random(6406)
    for _ in range(400):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        f1 = rand_image(rng, w, h, 9)
        f2 = [[min(9, t + rng.randint(0, 3)) for t in row] for row in f1]
        se = rand_se(rng)
        c1, c2 = close_image(f1, se, top=9), close_image(f2, se, top=9)
        assert leq(f1, c1)
        assert leq(c1, c2)
