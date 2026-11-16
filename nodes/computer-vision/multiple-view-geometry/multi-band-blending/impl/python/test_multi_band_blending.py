# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-band-blending/. The authors are listed in prov/AXXSRR.jsonl.
"""Tests of multi-band blending."""

import random
from fractions import Fraction

import pytest

from multi_band_blending import (collapse, gaussian_pyramid, laplacian_from_gaussian,
                                 multi_band_blend, reflect101)

W5 = [Fraction(c, 16) for c in (1, 4, 6, 4, 1)]


def mirror(i, n):
    """Reflect-101 index, written apart from the module as a fold loop."""
    if n == 1:
        return 0
    while i < 0 or i >= n:
        i = -i if i < 0 else 2 * (n - 1) - i
    return i


def reduce_matrix(n):
    """The ceil(n/2) x n matrix of 1D REDUCE."""
    m = (n + 1) // 2
    r = [[Fraction(0)] * n for _ in range(m)]
    for i in range(m):
        for k in range(-2, 3):
            r[i][mirror(2 * i + k, n)] += W5[k + 2]
    return r


def expand_matrix(n):
    """The n x ceil(n/2) matrix of 1D EXPAND to length n."""
    m = (n + 1) // 2
    gain = 1 if n == 1 else 2
    e = [[Fraction(0)] * m for _ in range(n)]
    for x in range(n):
        for k in range(-2, 3):
            j = mirror(x - k, n)
            if j % 2 == 0:
                e[x][j // 2] += gain * W5[k + 2]
    return e


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def tr(a):
    return [list(c) for c in zip(*a)]


def oracle(A, B, M, levels):
    """Blend by explicit operator matrices: REDUCE(g) = R_h g R_w^T and
    EXPAND(g) = E_h g E_w^T."""
    h, w = len(A), len(A[0])
    sizes = [(h, w)]
    for _ in range(levels):
        sizes.append(((sizes[-1][0] + 1) // 2, (sizes[-1][1] + 1) // 2))

    def red(g, l):
        hh, ww = sizes[l]
        return matmul(matmul(reduce_matrix(hh), g), tr(reduce_matrix(ww)))

    def exp(g, l):
        hh, ww = sizes[l]
        return matmul(matmul(expand_matrix(hh), g), tr(expand_matrix(ww)))

    def gp(img):
        out = [img]
        for l in range(levels):
            out.append(red(out[-1], l))
        return out

    gm, ga, gb = gp(M), gp(A), gp(B)
    bands = []
    for l in range(levels + 1):
        if l < levels:
            ea, eb = exp(ga[l + 1], l), exp(gb[l + 1], l)
            la = [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(ga[l], ea)]
            lb = [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(gb[l], eb)]
        else:
            la, lb = ga[l], gb[l]
        bands.append([[m * a + (1 - m) * b for m, a, b in zip(rm, ra, rb)]
                      for rm, ra, rb in zip(gm[l], la, lb)])
    s = bands[-1]
    for l in range(levels - 1, -1, -1):
        e = exp(s, l)
        s = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(bands[l], e)]
    return s


def rand_image(rng, h, w, lo=0, hi=255):
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def rand_mask(rng, h, w):
    return [[Fraction(rng.randint(0, 8), 8) for _ in range(w)] for _ in range(h)]


def test_reflect101():
    for n in range(1, 7):
        for i in range(-12, 18):
            assert reflect101(i, n) == mirror(i, n)


def test_worked_example():
    A, B = [[16] * 8], [[0] * 8]
    M = [[1, 1, 1, 1, 0, 0, 0, 0]]
    assert multi_band_blend(A, B, M, 0) == [[16, 16, 16, 16, 0, 0, 0, 0]]
    want = [Fraction(63, 4), Fraction(31, 2), Fraction(111, 8), 10,
            Fraction(45, 8), Fraction(5, 2), Fraction(5, 8), 0]
    assert multi_band_blend(A, B, M, 1) == [want]
    assert gaussian_pyramid(M, 3)[1] == [[1, Fraction(15, 16), Fraction(5, 16), 0]]
    assert multi_band_blend(A, B, M, 3) == [[Fraction(337, 32)] * 8]


def test_overshoot_example():
    A = [[0, 0, 0, 0, 16, 16, 16, 16]]
    B = [[16] * 8]
    M = [[1, 1, 1, 1, 1, 1, 0, 0]]
    s = multi_band_blend(A, B, M, 1)[0]
    assert max(s) == Fraction(1039, 64)


def test_against_operator_oracle():
    rng = random.Random(1)
    for _ in range(60):
        h, w = rng.randint(1, 7), rng.randint(1, 7)
        levels = rng.randint(0, 3)
        A, B, M = rand_image(rng, h, w), rand_image(rng, h, w), rand_mask(rng, h, w)
        assert multi_band_blend(A, B, M, levels) == oracle(A, B, M, levels)


def test_special_masks_and_equal_images():
    rng = random.Random(2)
    for _ in range(40):
        h, w = rng.randint(1, 9), rng.randint(1, 9)
        levels = rng.randint(0, 4)
        A, B = rand_image(rng, h, w), rand_image(rng, h, w)
        ones = [[1] * w for _ in range(h)]
        zero = [[0] * w for _ in range(h)]
        assert multi_band_blend(A, B, ones, levels) == A
        assert multi_band_blend(A, B, zero, levels) == B
        assert multi_band_blend(A, A, rand_mask(rng, h, w), levels) == A
        c = Fraction(rng.randint(0, 8), 8)
        const = [[c] * w for _ in range(h)]
        want = [[c * a + (1 - c) * b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]
        assert multi_band_blend(A, B, const, levels) == want


def test_collapse_inverts_the_pyramid():
    rng = random.Random(3)
    for _ in range(30):
        h, w = rng.randint(1, 10), rng.randint(1, 10)
        img = rand_image(rng, h, w)
        assert collapse(laplacian_from_gaussian(gaussian_pyramid(img, rng.randint(0, 4)))) == img


def test_mask_pyramid_stays_in_unit_interval():
    rng = random.Random(4)
    for _ in range(30):
        h, w = rng.randint(1, 10), rng.randint(1, 10)
        for level in gaussian_pyramid(rand_mask(rng, h, w), 4):
            assert all(0 <= x <= 1 for row in level for x in row)


def test_floats_and_bad_input():
    rng = random.Random(5)
    A = [[rng.random() for _ in range(6)] for _ in range(5)]
    B = [[rng.random() for _ in range(6)] for _ in range(5)]
    M = [[1.0 if u < 3 else 0.0 for u in range(6)] for _ in range(5)]
    s = multi_band_blend(A, B, M, 2)
    assert len(s) == 5 and len(s[0]) == 6
    with pytest.raises(ValueError):
        multi_band_blend(A, B, M, -1)
    with pytest.raises(ValueError):
        multi_band_blend(A, B[:4], M, 1)
