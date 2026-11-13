# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/felzenszwalb-distance-transform/. The authors are listed in prov/CZBFE7.jsonl.

import random

from felzenszwalb_distance_transform import dt1d, dt2d, edt


def brute_1d(f):
    n = len(f)
    out = []
    for p in range(n):
        vals = [(p - q) ** 2 + f[q] for q in range(n) if f[q] is not None]
        out.append(min(vals) if vals else None)
    return out


def brute_edt(image):
    """All pairs: the exact squared Euclidean distance to the nearest feature pixel."""
    h, w = len(image), len(image[0])
    feats = [(x, y) for y in range(h) for x in range(w) if image[y][x]]
    if not feats:
        return [[None] * w for _ in range(h)]
    return [[min((x - a) ** 2 + (y - b) ** 2 for (a, b) in feats) for x in range(w)]
            for y in range(h)]


def brute_2d(grid):
    h, w = len(grid), len(grid[0])
    cells = [(x, y, grid[y][x]) for y in range(h) for x in range(w) if grid[y][x] is not None]
    if not cells:
        return [[None] * w for _ in range(h)]
    return [[min((x - a) ** 2 + (y - b) ** 2 + t for (a, b, t) in cells) for x in range(w)]
            for y in range(h)]


def test_example_row():
    f = [None, None, 0, None, None, None, None, 0, None]
    assert dt1d(f) == [4, 1, 0, 1, 4, 4, 1, 0, 1]
    g = [9, 9, 2, 9, 9, 9, 0, 9, 9]
    assert dt1d(g) == [6, 3, 2, 3, 4, 1, 0, 1, 4]


def test_example_grid():
    image = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    assert edt(image) == [
        [2, 1, 2, 5, 10, 9],
        [1, 0, 1, 4, 5, 4],
        [2, 1, 2, 5, 2, 1],
        [5, 4, 5, 4, 1, 0],
    ]


def test_edges():
    assert dt1d([]) == []
    assert dt1d([None, None]) == [None, None]
    assert dt1d([7]) == [7]
    assert edt([[0, 0], [0, 0]]) == [[None, None], [None, None]]
    assert edt([[1]]) == [[0]]


def test_1d_against_brute_force():
    rng = random.Random(6701)
    for _ in range(2000):
        n = rng.randint(1, 14)
        f = [None if rng.random() < 0.3 else rng.randint(-20, 40) for _ in range(n)]
        assert dt1d(f) == brute_1d(f)


def test_1d_ties_and_equal_values():
    rng = random.Random(6702)
    for _ in range(1000):
        n = rng.randint(1, 12)
        f = [rng.choice([None, 0, 1, 4]) for _ in range(n)]
        assert dt1d(f) == brute_1d(f)


def test_edt_against_all_pairs():
    rng = random.Random(6703)
    for _ in range(400):
        w, h = rng.randint(1, 9), rng.randint(1, 9)
        p = rng.choice([0.05, 0.2, 0.5])
        image = [[1 if rng.random() < p else 0 for _ in range(w)] for _ in range(h)]
        assert edt(image) == brute_edt(image)


def test_sampled_function_against_brute_force():
    rng = random.Random(6704)
    for _ in range(300):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        grid = [[None if rng.random() < 0.4 else rng.randint(0, 30) for _ in range(w)]
                for _ in range(h)]
        assert dt2d(grid) == brute_2d(grid)


def test_rows_first_gives_the_same():
    rng = random.Random(6705)
    for _ in range(200):
        w, h = rng.randint(1, 8), rng.randint(1, 8)
        grid = [[None if rng.random() < 0.6 else rng.randint(0, 9) for _ in range(w)]
                for _ in range(h)]
        rows = [dt1d(r) for r in grid]
        cols = [dt1d([rows[y][x] for y in range(h)]) for x in range(w)]
        assert [[cols[x][y] for x in range(w)] for y in range(h)] == dt2d(grid)
