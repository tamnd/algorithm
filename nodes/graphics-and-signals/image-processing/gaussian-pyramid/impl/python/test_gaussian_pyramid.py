# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-pyramid/. The authors are listed in prov/5RH4SA.jsonl.

import random
from fractions import Fraction as F

from gaussian_pyramid import (
    burt_adelson_kernel,
    gaussian_pyramid,
    level_sizes,
    reduce_level,
    reflect101,
    to_level_zero,
    total_samples,
)

KERNELS = [burt_adelson_kernel(a) for a in (F(3, 8), F(2, 5), F(1, 2), F(3, 5))] + [[F(1, 9), F(2, 9), F(3, 9), F(2, 9), F(1, 9)]]


def random_image(rng, w, h):
    return [[rng.randrange(256) for _ in range(w)] for _ in range(h)]


def direct_reduce(g, w):
    """The 2D sum of Burt and Adelson, sum over m, n of w(m) w(n) g(2j + n, 2i + m)."""
    h, wd = len(g), len(g[0])
    out = []
    for j in range((h + 1) // 2):
        row = []
        for i in range((wd + 1) // 2):
            s = F(0)
            for n in range(-2, 3):
                for m in range(-2, 3):
                    s += w[m + 2] * w[n + 2] * g[reflect101(2 * j + n, h)][reflect101(2 * i + m, wd)]
            row.append(s)
        out.append(row)
    return out


def test_kernels_sum_to_one_and_binomial_case() -> None:
    for w in KERNELS:
        assert sum(w) == 1 and w == w[::-1]
    assert burt_adelson_kernel(F(3, 8)) == [F(c, 16) for c in (1, 4, 6, 4, 1)]
    assert burt_adelson_kernel(F(3, 5))[0] == F(-1, 20)


def test_reflect101() -> None:
    assert [reflect101(i, 5) for i in range(-3, 9)] == [3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0]
    assert [reflect101(i, 1) for i in range(-2, 3)] == [0] * 5
    assert [reflect101(i, 2) for i in range(-2, 4)] == [0, 1, 0, 1, 0, 1]


def test_reduce_matches_direct_2d_sum() -> None:
    rng = random.Random(8)
    for w in KERNELS:
        for wd, h in [(1, 1), (1, 4), (2, 2), (3, 5), (6, 4), (7, 7), (9, 8)]:
            g = random_image(rng, wd, h)
            assert reduce_level(g, w) == direct_reduce(g, w)


def test_constant_image_stays_constant() -> None:
    for w in KERNELS:
        for lvl in gaussian_pyramid([[7] * 6 for _ in range(5)], w):
            assert all(v == 7 for row in lvl for v in row)


def test_example_levels() -> None:
    w = burt_adelson_kernel(F(3, 8))
    image = [[0, 0, 16, 16, 16] for _ in range(5)]
    pyr = gaussian_pyramid(image, w)
    assert [(len(p[0]), len(p)) for p in pyr] == [(5, 5), (3, 3), (2, 2), (1, 1)]
    assert pyr[1] == [[F(2), F(11), F(16)]] * 3
    assert pyr[2] == [[F(33, 4), F(47, 4)]] * 2
    assert pyr[3] == [[F(10)]]


def test_level_sizes_and_limit() -> None:
    assert level_sizes(257, 257) == [(s, s) for s in (257, 129, 65, 33, 17, 9, 5, 3, 2, 1)]
    assert level_sizes(640, 480)[:4] == [(640, 480), (320, 240), (160, 120), (80, 60)]
    assert len(level_sizes(640, 480)) == 11
    pyr = gaussian_pyramid([[1] * 9 for _ in range(9)], KERNELS[0], levels=3)
    assert [len(p) for p in pyr] == [9, 5, 3]


def test_power_of_two_total_is_exact() -> None:
    for n in range(11):
        s = 1 << n
        assert total_samples(s, s) == (4 ** (n + 1) - 1) // 3
        assert 3 * total_samples(s, s) == 4 * s * s - 1


def test_floor_halving_stays_below_four_thirds() -> None:
    for wd in range(1, 65):
        for h in range(1, 65):
            total, x, y = 0, wd, h
            while x > 0 and y > 0:
                total += x * y
                x, y = x // 2, y // 2
            assert 3 * total < 4 * wd * h


def test_ceil_halving_bound_and_excess() -> None:
    for wd in range(1, 65):
        for h in range(1, 65):
            t, n = total_samples(wd, h), len(level_sizes(wd, h))
            assert 3 * t <= 4 * (wd - 1) * (h - 1) + 6 * (wd + h - 2) + 3 * n
    assert total_samples(3, 3) == 14 and 3 * 14 > 4 * 9
    assert total_samples(257, 257) == 88413
    assert F(88413) - F(4 * 257 * 257, 3) == F(1043, 3)
    assert sum((2 ** k + 1) ** 2 for k in range(9)) == 88412


def test_range_kept_by_nonnegative_kernels_only() -> None:
    rng = random.Random(11)
    for a in (F(0), F(3, 8), F(2, 5), F(1, 2)):
        w = burt_adelson_kernel(a)
        for _ in range(20):
            img = random_image(rng, 7, 6)
            lo, hi = min(map(min, img)), max(map(max, img))
            for lvl in gaussian_pyramid(img, w):
                assert all(lo <= v <= hi for row in lvl for v in row)
    assert reduce_level([[16, 0, 0, 0, 16]], burt_adelson_kernel(F(3, 5)))[0][1] == F(-8, 5)


def test_number_of_reduce_calls() -> None:
    for wd in range(1, 300):
        for h in (1, 2, 7, 300):
            m = max(wd, h)
            assert len(level_sizes(wd, h)) - 1 == (m - 1).bit_length()


def test_level_samples_map_inside_level_zero() -> None:
    for wd in range(1, 80):
        for lvl, (x, _) in enumerate(level_sizes(wd, 1)):
            assert to_level_zero(x - 1, 0, lvl)[0] <= wd - 1
