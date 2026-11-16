# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cost-volume/. The authors are listed in prov/YWMV35.jsonl.

import math
import random

import pytest

from cost_volume import INVALID, CostVolume


def random_image(rng, w, h, lo=0, hi=255):
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def nested(left, right, D):
    """A second representation: C[v][u][d] as nested lists."""
    H, W = len(left), len(left[0])
    return [[[abs(left[v][u] - right[v][u - d]) if u >= d else math.inf for d in range(D)]
             for u in range(W)] for v in range(H)]


def test_worked_example():
    left = [[10, 10, 50, 90, 10, 10]]
    right = [[10, 50, 90, 10, 10, 10]]
    cv = CostVolume.build(left, right, 3)
    rows = [[cv.get(u, 0, d) for d in range(3)] for u in range(6)]
    assert rows == [[0, INVALID, INVALID], [40, 0, INVALID], [40, 0, 40],
                    [80, 0, 40], [0, 0, 80], [0, 0, 0]]
    assert cv.wta() == [[0, 1, 1, 1, 0, 0]]
    rv = cv.right_view()
    assert [[rv.get(x, 0, d) for d in range(3)] for x in range(6)] == [
        [0, 0, 40], [40, 0, 40], [40, 0, 80], [80, 0, 0], [0, 0, INVALID], [0, INVALID, INVALID]]


def test_layout_is_a_bijection():
    cv = CostVolume(5, 4, 3)
    seen = {cv.index(u, v, d) for v in range(4) for u in range(5) for d in range(3)}
    assert seen == set(range(60))
    with pytest.raises(IndexError):
        cv.index(5, 0, 0)
    with pytest.raises(IndexError):
        cv.index(0, 0, 3)
    with pytest.raises(ValueError):
        CostVolume(0, 1, 1)


def test_build_and_wta_against_nested_lists():
    rng = random.Random(1)
    for W, H, D in ((9, 5, 4), (7, 3, 7), (12, 6, 1)):
        left, right = random_image(rng, W, H, 0, 15), random_image(rng, W, H, 0, 15)
        cv = CostVolume.build(left, right, D)
        ref = nested(left, right, D)
        for v in range(H):
            for u in range(W):
                for d in range(D):
                    assert cv.get(u, v, d) == ref[v][u][d]
        want = [[ref[v][u].index(min(ref[v][u])) for u in range(W)] for v in range(H)]
        assert cv.wta() == want


def test_right_view_is_the_volume_of_the_swapped_pair():
    # the right view equals the volume built with the right image as
    # reference and the match (x + d, v) in the left image
    rng = random.Random(2)
    W, H, D = 10, 4, 5
    left, right = random_image(rng, W, H), random_image(rng, W, H)
    rv = CostVolume.build(left, right, D).right_view()
    for v in range(H):
        for x in range(W):
            for d in range(D):
                want = abs(right[v][x] - left[v][x + d]) if x + d < W else INVALID
                assert rv.get(x, v, d) == want


def test_slices_round_trip():
    rng = random.Random(3)
    W, H, D = 6, 5, 4
    cv = CostVolume.build(random_image(rng, W, H), random_image(rng, W, H), D)
    for d in range(D):
        s = cv.slice(d)
        assert s == [[cv.get(u, v, d) for u in range(W)] for v in range(H)]
        cv.set_slice(d, [[x * 2 for x in row] for row in s])
        assert cv.slice(d) == [[x * 2 for x in row] for row in s]


def test_shifted_pair_gives_the_true_disparity():
    rng = random.Random(4)
    W, H, D, true_d = 30, 6, 8, 5
    scene = random_image(rng, W + 10, H)
    right = [[scene[v][x + true_d] for x in range(W)] for v in range(H)]
    left = [[scene[v][u] for u in range(W)] for v in range(H)]
    cv = CostVolume.build(left, right, D)
    for v in range(H):
        for u in range(true_d, W):
            assert cv.get(u, v, true_d) == 0
    # a 3 x 3 box sum on each slice, then winner-takes-all
    for d in range(D):
        s = cv.slice(d)
        box = [[sum(s[y][x] for y in range(max(v - 1, 0), min(v + 2, H))
                    for x in range(max(u - 1, 0), min(u + 2, W)))
                for u in range(W)] for v in range(H)]
        cv.set_slice(d, box)
    disp = cv.wta()
    for v in range(H):
        for u in range(D + 1, W):
            assert disp[v][u] == true_d


def test_memory_size():
    cv = CostVolume(4, 3, 2)
    assert cv.nbytes(2) == 48
    assert 640 * 480 * 128 * 2 == 78643200
