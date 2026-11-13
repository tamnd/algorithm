# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hit-or-miss-transform/. The authors are listed in prov/TADBZ8.jsonl.

import random

from hit_or_miss_transform import from_template, hit_or_miss, rotate


def parse(rows):
    return [[1 if c == "#" else 0 for c in r] for r in rows]


def points(img):
    return [(x, y) for y, row in enumerate(img) for x, v in enumerate(row) if v]


EXAMPLE = parse(["........", ".####...", ".#####.#", ".####...", "........"])
ISOLATED = from_template(["000", "010", "000"])
UPPER_RIGHT_CORNER = from_template([".0.", "110", ".1."])
RIGHT_END = from_template([".00", "110", ".00"])


def direct_scan(x, hit, miss, outside):
    """For each pixel, test the template cell by cell."""
    h, w = len(x), len(x[0])

    def value(qx, qy):
        return x[qy][qx] if 0 <= qx < w and 0 <= qy < h else outside

    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for xx in range(w):
            ok = all(value(xx + u, y + v) == 1 for (u, v) in hit)
            ok = ok and all(value(xx + u, y + v) == 0 for (u, v) in miss)
            out[y][xx] = 1 if ok else 0
    return out


def erode(x, se, outside):
    h, w = len(x), len(x[0])
    return [[1 if all((x[y + v][xx + u] if 0 <= xx + u < w and 0 <= y + v < h else outside) == 1
                      for (u, v) in se) else 0 for xx in range(w)] for y in range(h)]


def rand_pair(rng):
    cells = [(u, v) for u in range(-1, 2) for v in range(-1, 2)]
    rng.shuffle(cells)
    a, b = rng.randint(0, 5), rng.randint(0, 4)
    return cells[:a], cells[a:a + b]


def test_example_templates():
    assert points(hit_or_miss(EXAMPLE, *ISOLATED)) == [(7, 2)]
    assert points(hit_or_miss(EXAMPLE, *UPPER_RIGHT_CORNER)) == [(4, 1)]
    assert points(hit_or_miss(EXAMPLE, *RIGHT_END)) == [(5, 2)]


def test_rotations_find_all_corners():
    hit, miss = UPPER_RIGHT_CORNER
    found = []
    for _ in range(4):
        found += points(hit_or_miss(EXAMPLE, hit, miss))
        hit, miss = rotate(hit), rotate(miss)
    assert sorted(found) == [(1, 1), (1, 3), (4, 1), (4, 3)]


def test_border_counts_as_background():
    x = parse(["#..", "...", "..."])
    assert points(hit_or_miss(x, *ISOLATED)) == [(0, 0)]
    assert points(hit_or_miss(x, *ISOLATED, outside=1)) == []


def test_overlap_is_rejected():
    try:
        hit_or_miss(EXAMPLE, [(0, 0)], [(0, 0)])
    except ValueError:
        return
    raise AssertionError("an overlapping pair must raise ValueError")


def test_against_direct_scan():
    rng = random.Random(6501)
    for _ in range(800):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        x = [[rng.randint(0, 1) for _ in range(w)] for _ in range(h)]
        hit, miss = rand_pair(rng)
        for outside in (0, 1):
            assert hit_or_miss(x, hit, miss, outside) == direct_scan(x, hit, miss, outside)


def test_two_erosions():
    rng = random.Random(6502)
    for _ in range(500):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        x = [[rng.randint(0, 1) for _ in range(w)] for _ in range(h)]
        comp = [[1 - t for t in row] for row in x]
        hit, miss = rand_pair(rng)
        e1, e2 = erode(x, hit, 0), erode(comp, miss, 1)
        both = [[a & b for a, b in zip(r1, r2)] for r1, r2 in zip(e1, e2)]
        assert hit_or_miss(x, hit, miss) == both


def test_swap_with_complement():
    rng = random.Random(6503)
    for _ in range(500):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        x = [[rng.randint(0, 1) for _ in range(w)] for _ in range(h)]
        comp = [[1 - t for t in row] for row in x]
        hit, miss = rand_pair(rng)
        assert hit_or_miss(x, hit, miss, 0) == hit_or_miss(comp, miss, hit, 1)


def test_empty_miss_is_erosion():
    rng = random.Random(6504)
    for _ in range(300):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        x = [[rng.randint(0, 1) for _ in range(w)] for _ in range(h)]
        hit, _ = rand_pair(rng)
        assert hit_or_miss(x, hit, []) == erode(x, hit, 0)
