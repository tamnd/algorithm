# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-pyramid/. The authors are listed in prov/KYWMGX.jsonl.

import math
import random
from fractions import Fraction as F

from laplacian_pyramid import (
    burt_adelson_kernel,
    expand,
    gaussian_pyramid,
    laplacian_pyramid,
    reconstruct,
    reduce_level,
)

GAUSSIAN_LIKE = [burt_adelson_kernel(a) for a in (F(3, 8), F(2, 5), F(1, 2), F(3, 5), F(3, 10))]
NOT_EQUAL_CONTRIBUTION = [F(1, 9), F(2, 9), F(3, 9), F(2, 9), F(1, 9)]
KERNELS = GAUSSIAN_LIKE + [NOT_EQUAL_CONTRIBUTION]
SIZES = [(1, 1), (2, 3), (5, 5), (8, 6), (9, 9), (13, 7), (17, 17)]


def random_image(rng, w, h):
    return [[rng.randrange(256) for _ in range(w)] for _ in range(h)]


def test_exact_reconstruction_for_every_kernel() -> None:
    rng = random.Random(8)
    for w in KERNELS:
        for wd, h in SIZES:
            img = random_image(rng, wd, h)
            lap = laplacian_pyramid(img, w)
            assert reconstruct(lap, w) == img
            assert [(len(b[0]), len(b)) for b in lap] == [(len(g[0]), len(g)) for g in gaussian_pyramid(img, w)]


def test_expand_matches_burt_adelson_formula_inside() -> None:
    """Away from the border, EXPAND is 4 times the sum of w(m) w(n) g((x - m) / 2, (y - n) / 2) over integer terms."""
    rng = random.Random(3)
    for w in KERNELS:
        g = random_image(rng, 5, 5)
        e = expand(g, 9, 9, w)
        for y in range(2, 7):
            for x in range(2, 7):
                s = F(0)
                for n in range(-2, 3):
                    for m in range(-2, 3):
                        if (x - m) % 2 == 0 and (y - n) % 2 == 0:
                            s += w[m + 2] * w[n + 2] * g[(y - n) // 2][(x - m) // 2]
                assert e[y][x] == 4 * s


def test_equal_contribution_kernels_reproduce_constants() -> None:
    for w in GAUSSIAN_LIKE:
        for wd, h in [(5, 5), (8, 6), (9, 4)]:
            coarse = [[7] * ((wd + 1) // 2) for _ in range((h + 1) // 2)]
            assert expand(coarse, wd, h, w) == [[7] * wd for _ in range(h)]
            lap = laplacian_pyramid([[7] * wd for _ in range(h)], w)
            assert all(v == 0 for band in lap[:-1] for row in band for v in row)


def test_other_kernel_leaves_a_checkerboard_but_still_inverts() -> None:
    e = expand([[9] * 3 for _ in range(3)], 5, 5, NOT_EQUAL_CONTRIBUTION)
    assert e[0][:3] == [F(100, 9), F(80, 9), F(100, 9)]
    assert e[1][:3] == [F(80, 9), F(64, 9), F(80, 9)]
    img = [[9] * 5 for _ in range(5)]
    lap = laplacian_pyramid(img, NOT_EQUAL_CONTRIBUTION)
    assert any(v != 0 for row in lap[0] for v in row)
    assert reconstruct(lap, NOT_EQUAL_CONTRIBUTION) == img


def test_any_deterministic_expand_inverts_in_integers() -> None:
    """Round every level and every EXPAND down to an integer: the bands are integers and still invert."""
    w = burt_adelson_kernel(F(3, 8))

    def int_expand(g, width, height, kernel):
        return [[math.floor(v) for v in row] for row in expand(g, width, height, kernel)]

    rng = random.Random(5)
    for wd, h in SIZES:
        img = random_image(rng, wd, h)
        levels = [img]
        while len(levels[-1]) > 1 or len(levels[-1][0]) > 1:
            levels.append([[math.floor(v) for v in row] for row in reduce_level(levels[-1], w)])
        lap = laplacian_pyramid(img, w, int_expand, levels)
        assert all(isinstance(v, int) for band in lap for row in band for v in row)
        assert reconstruct(lap, w, int_expand) == img


def test_example_step_edge() -> None:
    w = burt_adelson_kernel(F(3, 8))
    img = [[0, 0, 16, 16, 16] for _ in range(5)]
    lap = laplacian_pyramid(img, w)
    assert lap[0] == [[F(-17, 4), F(-13, 2), F(11, 2), F(5, 2), F(5, 4)]] * 5
    assert lap[1] == [[F(-57, 8), F(1), F(41, 8)]] * 3
    assert lap[2] == [[F(-7, 4), F(7, 4)]] * 2
    assert lap[3] == [[F(10)]]
    assert reconstruct(lap, w) == img


def test_floating_point_sum_is_not_exact() -> None:
    a, b = 0.1, 0.7
    assert (a - b) + b != a
    assert (F(1, 10) - F(7, 10)) + F(7, 10) == F(1, 10)
