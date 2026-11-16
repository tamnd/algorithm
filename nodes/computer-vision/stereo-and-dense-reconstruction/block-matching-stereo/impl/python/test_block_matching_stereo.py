# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-matching-stereo/. The authors are listed in prov/VSCW79.jsonl.

import random

import pytest

from block_matching_stereo import (
    block_match,
    block_match_brute,
    padded_integral,
    pixel_cost,
    window_cost,
)


def random_image(rng, w, h, lo=0, hi=255):
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def shifted_pair(scene, w, h, d):
    """A left image whose pixel (u, v) is the scene point at column u - d of
    the right image, so the true disparity is d everywhere."""
    right = [[scene[v][u] for u in range(w)] for v in range(h)]
    left = [[scene[v][max(u - d, 0)] for u in range(w)] for v in range(h)]
    return left, right


def test_worked_example():
    left = [[10, 10, 50, 90, 10, 10]] * 3
    right = [[10, 50, 90, 10, 10, 10]] * 3
    assert [window_cost(left, right, 3, 1, d, 1) for d in range(3)] == [360, 0, 480]
    assert [window_cost(left, right, 5, 1, d, 1) for d in range(3)] == [0, 0, 240]
    # the textureless pixel u = 5 has a tie, and the tie goes to d = 0
    assert block_match(left, right, 3, 1) == [[1, 1, 1, 1, 1, 0]] * 3


def test_matches_brute_force():
    rng = random.Random(1)
    for w, h, D, r in ((9, 7, 4, 1), (12, 6, 5, 2), (7, 5, 3, 0), (10, 8, 6, 3)):
        left, right = random_image(rng, w, h, 0, 20), random_image(rng, w, h, 0, 20)
        for squared in (False, True):
            assert block_match(left, right, D, r, squared) == block_match_brute(left, right, D, r, squared)


def test_padded_integral_gives_window_sums():
    rng = random.Random(2)
    e = random_image(rng, 6, 5, 0, 9)
    r = 2
    S = padded_integral(e, r)
    k = 2 * r + 1
    for v in range(5):
        for u in range(6):
            want = sum(e[min(max(v + j, 0), 4)][min(max(u + i, 0), 5)]
                       for j in range(-r, r + 1) for i in range(-r, r + 1))
            assert S[v + k][u + k] - S[v][u + k] - S[v + k][u] + S[v][u] == want


def test_recovers_a_constant_disparity():
    rng = random.Random(3)
    w, h, D, r = 40, 12, 10, 2
    for true_d in (0, 3, 7):
        left, right = shifted_pair(random_image(rng, w, h), w, h, true_d)
        disp = block_match(left, right, D, r)
        for v in range(h):
            for u in range(D + r, w):
                assert disp[v][u] == true_d


def test_two_layer_scene():
    # a background plane at disparity 2 and a square in front at disparity 6
    rng = random.Random(4)
    w, h, D, r = 48, 30, 9, 2
    back = random_image(rng, w + 10, h)
    front = random_image(rng, w + 10, h, 100, 255)
    x0, x1, y0, y1 = 20, 34, 9, 21  # the square in the left image

    def in_square(u, v):
        return y0 <= v < y1 and x0 <= u < x1

    # the left pixel u sees back[v][u] or front[v][u]; the same scene point
    # is at column u - 2 or u - 6 of the right image
    left = [[front[v][u] if in_square(u, v) else back[v][u] for u in range(w)] for v in range(h)]
    right = [[front[v][x + 6] if in_square(x + 6, v) else back[v][x + 2] for x in range(w)]
             for v in range(h)]
    truth = [[6 if in_square(u, v) else 2 for u in range(w)] for v in range(h)]
    disp = block_match(left, right, D, r)
    for v in range(h):
        for u in range(D + r, w):
            near_edge = y0 - r - 1 <= v < y1 + r + 1 and x0 - 4 - r - 1 <= u < x1 + r + 1
            inside = y0 + r <= v < y1 - r and x0 + r <= u < x1 - r
            if inside or not near_edge:
                assert disp[v][u] == truth[v][u]
    # the background just left of the square is hidden in the right image:
    # the left pixels x0 - 4 to x0 - 1 have no true match
    assert any(disp[v][u] != truth[v][u] for v in range(y0, y1) for u in range(x0 - 4, x0))


def test_flat_images_give_zero():
    flat = [[5] * 8 for _ in range(4)]
    assert block_match(flat, flat, 4, 1) == [[0] * 8 for _ in range(4)]


def test_pixel_cost_and_window_of_radius_zero():
    left = [[1, 4, 9], [2, 2, 2]]
    right = [[3, 3, 3], [0, 5, 1]]
    assert pixel_cost(left, right, 1) == [[2, 1, 6], [2, 2, 3]]
    assert pixel_cost(left, right, 1, squared=True) == [[4, 1, 36], [4, 4, 9]]
    for v in range(2):
        for u in range(3):
            assert window_cost(left, right, u, v, 1, 0) == pixel_cost(left, right, 1)[v][u]


def test_bad_arguments():
    img = [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        block_match(img, img, 0, 1)
    with pytest.raises(ValueError):
        block_match(img, img, 2, -1)
