# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seam-carving/. The authors are listed in prov/9886BS.jsonl.

import itertools
import random

import pytest

from seam_carving import (
    energy,
    min_vertical_seam,
    remove_vertical_seam,
    seam_carve,
    seam_carve_height,
    seam_energy,
    transpose,
)

EXAMPLE = [
    [9, 9, 0, 9, 9],
    [9, 1, 9, 8, 9],
    [9, 9, 9, 9, 0],
    [9, 9, 9, 0, 9],
]


def all_seams(h, w):
    """Every connected vertical seam of an h by w image, by brute force."""
    for start in range(w):
        for steps in itertools.product((-1, 0, 1), repeat=h - 1):
            s = [start]
            for d in steps:
                s.append(s[-1] + d)
            if all(0 <= x < w for x in s):
                yield s


def connected(s, w):
    return all(0 <= x < w for x in s) and all(abs(s[y] - s[y - 1]) <= 1 for y in range(1, len(s)))


def test_page_example():
    # the energy table of the page example: a greedy walk from the top costs 13
    e = [[2, 4, 3, 5, 1], [3, 2, 5, 2, 3], [5, 2, 4, 2, 1], [2, 3, 1, 9, 9]]
    s = min_vertical_seam(e)
    assert s == [4, 3, 3, 2]
    assert seam_energy(e, s) == 6
    assert seam_energy(e, [4, 3, 4, 3]) == 13


def test_image_example():
    e = energy(EXAMPLE)
    assert e == [
        [0, 17, 9, 10, 0],
        [8, 0, 16, 0, 10],
        [0, 8, 0, 17, 9],
        [0, 0, 9, 9, 18],
    ]
    s = min_vertical_seam(e)
    assert s == [0, 1, 0, 0]
    assert seam_energy(e, s) == 0
    out = seam_carve(EXAMPLE, 1)
    assert out == [[9, 0, 9, 9], [9, 9, 8, 9], [9, 9, 9, 0], [9, 9, 0, 9]]


def test_energy_formula():
    img = [[1, 2, 4], [8, 16, 32]]
    e = energy(img)
    # x = 1, y = 0: |4 - 1| + |16 - 2| (the row above is clamped to row 0)
    assert e[0][1] == 3 + 14
    # corner (0, 0): |2 - 1| + |8 - 1|
    assert e[0][0] == 1 + 7


def test_edges():
    assert min_vertical_seam([[5]]) == [0]
    assert min_vertical_seam([[3, 1, 2]]) == [1]
    assert min_vertical_seam([[1], [2], [3]]) == [0, 0, 0]
    # a constant image: all seams cost 0, so the leftmost straight seam wins the ties
    assert min_vertical_seam(energy([[7] * 4 for _ in range(3)])) == [0, 0, 0]
    with pytest.raises(ValueError):
        min_vertical_seam([])
    with pytest.raises(ValueError):
        seam_carve([[1, 2]], 2)
    assert seam_carve([[1, 2], [3, 4]], 0) == [[1, 2], [3, 4]]


def test_random_against_all_seams():
    rng = random.Random(7007)
    for _ in range(600):
        h = rng.randint(1, 5)
        w = rng.randint(1, 5)
        e = [[rng.randint(0, 9) for _ in range(w)] for _ in range(h)]
        s = min_vertical_seam(e)
        assert len(s) == h and connected(s, w)
        best = min(seam_energy(e, t) for t in all_seams(h, w))
        assert seam_energy(e, s) == best


def test_remove_and_carve():
    rng = random.Random(42)
    for _ in range(200):
        h = rng.randint(1, 6)
        w = rng.randint(2, 7)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        s = min_vertical_seam(energy(img))
        out = remove_vertical_seam(img, s)
        for y in range(h):
            assert out[y] == img[y][: s[y]] + img[y][s[y] + 1:]
        k = rng.randint(0, w - 1)
        carved = seam_carve(img, k)
        assert len(carved) == h and all(len(r) == w - k for r in carved)
        # each output row is a subsequence of the input row
        for y in range(h):
            it = iter(img[y])
            assert all(v in it for v in carved[y])


def test_height():
    rng = random.Random(3)
    img = [[rng.randint(0, 9) for _ in range(4)] for _ in range(6)]
    out = seam_carve_height(img, 2)
    assert len(out) == 4 and all(len(r) == 4 for r in out)
    assert transpose(transpose(img)) == img
