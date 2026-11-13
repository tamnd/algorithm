# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-phase/. The authors are listed in prov/DG68QC.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from minimum_phase import autocorrelation, expand, flip, inverse_response, minimum_phase, partial_energy, poly_mul, variants


def random_factor(rng):
    if rng.random() < 0.5:
        while True:
            c0, c1 = Fraction(rng.randint(1, 9)), Fraction(rng.randint(-9, 9))
            if abs(c1) != abs(c0):
                return (c0, c1)
    while True:
        c0, c2 = Fraction(rng.randint(1, 9)), Fraction(rng.randint(1, 9))
        c1 = Fraction(rng.randint(-9, 9))
        if c0 != c2 and c1 * c1 < 4 * c0 * c2:
            return (c0, c1, c2)


def magnitude(h, w):
    return abs(sum(v * cmath.exp(-1j * w * n) for n, v in enumerate(h)))


def integer_sequences(length, energy):
    """Every integer sequence of the given length with sum of squares equal to energy."""
    if length == 0:
        if energy == 0:
            yield []
        return
    top = math.isqrt(energy)
    for v in range(-top, top + 1):
        for rest in integer_sequences(length - 1, energy - v * v):
            yield [v] + rest


def test_example_zeros_one_half_and_three() -> None:
    factors = [(2, -1), (1, -3)]  # 2 H(z) = (2 - z^-1)(1 - 3 z^-1): zeros 1/2 and 3
    seqs = {mask: h for mask, h in variants(factors)}
    assert seqs[(False, False)] == [2, -7, 3]
    assert seqs[(True, False)] == [-1, 5, -6]
    assert seqs[(False, True)] == [-6, 5, -1]
    assert seqs[(True, True)] == [3, -7, 2]
    assert minimum_phase(factors) == [-6, 5, -1]
    assert [partial_energy(h) for h in seqs.values()] == [[4, 53, 62], [36, 61, 62], [1, 26, 62], [9, 58, 62]]


def test_flips_keep_the_magnitude() -> None:
    rng = random.Random(7701)
    for _ in range(60):
        factors = [random_factor(rng) for _ in range(rng.randint(1, 4))]
        all_h = [h for _, h in variants(factors)]
        r = autocorrelation(all_h[0])
        for h in all_h:
            assert autocorrelation(h) == r  # exact: the same |H|^2 at every frequency
        for w in (0.3, 1.7, 2.9):
            mags = [magnitude([float(v) for v in h], w) for h in all_h]
            assert max(mags) - min(mags) < 1e-9 * (1 + max(mags))


def test_minimum_phase_has_largest_partial_energy() -> None:
    rng = random.Random(7702)
    for _ in range(80):
        factors = [random_factor(rng) for _ in range(rng.randint(1, 4))]
        hmin = minimum_phase(factors)
        emin = partial_energy(hmin)
        for _, h in variants(factors):
            e = partial_energy(h)
            assert e[-1] == emin[-1]
            assert all(a >= b for a, b in zip(emin, e))
        # all zeros outside: the maximum-phase filter is the time reverse of the minimum-phase one
        hmax = expand([tuple(f) if abs(f[-1]) > abs(f[0]) else flip(f) for f in factors])
        assert hmax == hmin[::-1]
        emax = partial_energy(hmax)
        for _, h in variants(factors):
            assert all(a <= b for a, b in zip(emax, partial_energy(h)))


def test_every_same_magnitude_integer_filter_is_a_flip() -> None:
    # brute force over all integer sequences with the same length and energy
    for factors in ([(2, -1), (1, -3)], [(1, 2), (1, 1, 2)], [(3, 1), (1, -2), (1, 1)]):
        all_h = [h for _, h in variants(factors)]
        r = autocorrelation(all_h[0])
        allowed = {tuple(h) for h in all_h} | {tuple(-v for v in h) for h in all_h}
        found = [s for s in integer_sequences(len(r), int(r[0])) if autocorrelation(s) == r]
        assert found
        assert {tuple(s) for s in found} <= allowed


def test_telescoping_identity() -> None:
    # H = Q (1 - c w), G = Q (-c + w): |h[n]|^2 - |g[n]|^2 = (1 - c^2)(q[n]^2 - q[n-1]^2)
    rng = random.Random(7703)
    for _ in range(50):
        q = [Fraction(rng.randint(-9, 9)) for _ in range(rng.randint(1, 6))]
        c = Fraction(rng.randint(-9, 9), rng.randint(1, 9))
        h = poly_mul(q, [1, -c])
        g = poly_mul(q, [-c, 1])
        qq = q + [Fraction(0)]
        for n in range(len(h)):
            prev = qq[n - 1] if n else 0
            assert h[n] ** 2 - g[n] ** 2 == (1 - c * c) * (qq[n] ** 2 - prev ** 2)


def test_inverse_is_causal_and_stable_only_for_minimum_phase() -> None:
    factors = [(2, -1), (1, -3)]
    good = inverse_response(minimum_phase(factors), 200)
    bad = inverse_response(expand(factors), 200)
    assert sum(abs(v) for v in good[100:]) < Fraction(1, 10**20)
    assert abs(bad[-1]) > 10**80


def test_zero_on_the_circle_is_rejected() -> None:
    with pytest.raises(ValueError):
        minimum_phase([(1, 1)])
