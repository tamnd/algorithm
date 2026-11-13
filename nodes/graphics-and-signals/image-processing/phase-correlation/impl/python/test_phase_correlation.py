# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-correlation/. The authors are listed in prov/D7EB05.jsonl.

import random

import pytest

from phase_correlation import (
    circular_shift,
    correlation_surface,
    cross_power_spectrum,
    dft2,
    dft2_direct,
    phase_correlation,
    signed_shift,
)


def rand_image(rng, w, h):
    return [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]


@pytest.mark.parametrize("w,h", [(4, 4), (5, 3), (8, 4), (6, 7)])
def test_dft2_matches_direct_sum(w, h):
    rng = random.Random(w * 10 + h)
    img = rand_image(rng, w, h)
    a = dft2(img)
    b = dft2_direct(img)
    for ra, rb in zip(a, b):
        for x, y in zip(ra, rb):
            assert abs(x - y) < 1e-6
    back = dft2(a, invert=True)
    for r0, r1 in zip(img, back):
        for x, y in zip(r0, r1):
            assert abs(x - y) < 1e-8


@pytest.mark.parametrize("w,h,seed", [(4, 4, 1), (5, 3, 2), (8, 4, 3), (3, 5, 4), (6, 6, 5)])
def test_every_circular_shift_is_recovered(w, h, seed):
    rng = random.Random(seed)
    f = rand_image(rng, w, h)
    for dy in range(h):
        for dx in range(w):
            g = circular_shift(f, dx, dy)
            x, y, peak = phase_correlation(f, g)
            assert (x, y) == (dx, dy)
            surf = correlation_surface(f, g)
            # With no zero bins the surface is a unit delta at the shift.
            for yy, row in enumerate(surf):
                for xx, val in enumerate(row):
                    want = 1.0 if (xx, yy) == (dx, dy) else 0.0
                    assert abs(val - want) < 1e-9


def test_spectrum_of_random_images_has_no_zero_bins_for_these_seeds():
    for w, h, seed in [(4, 4, 1), (5, 3, 2), (8, 4, 3), (3, 5, 4), (6, 6, 5)]:
        f = rand_image(random.Random(seed), w, h)
        assert min(abs(v) for r in dft2_direct(f) for v in r) > 1e-6


@pytest.mark.parametrize("a,b", [(2, 5), (0.5, 100), (3, -20)])
def test_invariant_under_gain_and_offset(a, b):
    rng = random.Random(9)
    f = rand_image(rng, 6, 5)
    g = circular_shift(f, 4, 2)
    g2 = [[a * v + b for v in r] for r in g]
    # The DC bin of g2 stays positive for these values, so its phase is 0 as before.
    assert sum(map(sum, g2)) > 0
    s1 = correlation_surface(f, g)
    s2 = correlation_surface(f, g2)
    for r1, r2 in zip(s1, s2):
        for x, y in zip(r1, r2):
            assert abs(x - y) < 1e-9
    assert phase_correlation(f, g2)[:2] == (4, 2)


def test_normalized_spectrum_has_unit_magnitude_and_linear_phase():
    rng = random.Random(21)
    f = rand_image(rng, 5, 4)
    g = circular_shift(f, 2, 3)
    r = cross_power_spectrum(dft2(f), dft2(g))
    import cmath
    import math
    for l, row in enumerate(r):
        for k, v in enumerate(row):
            want = cmath.exp(-2j * math.pi * (k * 2 / 5 + l * 3 / 4))
            assert abs(v - want) < 1e-9


def test_zero_bins_are_set_to_zero_and_shift_still_found():
    # A constant row pattern: only the column frequencies survive, so many bins are 0.
    f = [[1, 7, 3, 2], [1, 7, 3, 2], [1, 7, 3, 2], [1, 7, 3, 2]]
    g = circular_shift(f, 1, 0)
    r = cross_power_spectrum(dft2(f), dft2(g))
    zero = sum(1 for row in r for v in row if v == 0)
    assert zero == 12
    x, y, peak = phase_correlation(f, g)
    assert x == 1
    # The vertical shift is not observable: every row of the surface is the same.
    surf = correlation_surface(f, g)
    for row in surf:
        assert abs(row[1] - 0.25) < 1e-9


def test_signed_shift():
    assert signed_shift(7, 1, 8, 4) == (-1, 1)
    assert signed_shift(4, 3, 8, 4) == (4, -1)
    assert signed_shift(2, 2, 5, 5) == (2, 2)
    assert signed_shift(3, 3, 5, 5) == (-2, -2)


def test_worked_example_from_the_page():
    f = [[1, 2, 0, 0], [0, 3, 0, 1], [4, 0, 0, 0]]
    g = circular_shift(f, 1, 2)
    assert g == [[1, 0, 3, 0], [0, 4, 0, 0], [0, 1, 2, 0]]
    assert dft2(f)[0][0] == 11
    x, y, peak = phase_correlation(f, g)
    assert (x, y) == (1, 2) and abs(peak - 1) < 1e-12
    assert signed_shift(1, 2, 4, 3) == (1, -1)
    # Plain circular cross-correlation for comparison: the peak is 31, the next value 15.
    cc = [[sum(f[yy][xx] * g[(yy + dy) % 3][(xx + dx) % 4] for yy in range(3) for xx in range(4))
           for dx in range(4)] for dy in range(3)]
    assert cc == [[13, 10, 15, 2], [15, 10, 13, 2], [2, 31, 2, 6]]
