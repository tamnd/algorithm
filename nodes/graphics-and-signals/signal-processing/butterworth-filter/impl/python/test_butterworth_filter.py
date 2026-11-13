# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/butterworth-filter/. The authors are listed in prov/VAFAXE.jsonl.

import math
import random
from fractions import Fraction

from butterworth_filter import (
    butterworth_poles,
    cutoff_for_passband,
    denominator,
    magnitude_squared,
    minimum_order,
    response,
)


def squared_magnitude_poly(a):
    """Coefficients q[j] of Q(w) = |D(i w)|^2 = D(i w) D(-i w) for a real polynomial D.

    Complex numbers are pairs (re, im) so that Fraction input stays exact.
    """
    n = len(a) - 1
    # D(i w) = sum a[k] i^k w^k; i^k cycles 1, i, -1, -i.
    unit = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    p = [(a[k] * unit[k % 4][0], a[k] * unit[k % 4][1]) for k in range(n + 1)]
    pc = [(re, -im) for re, im in p]  # D(-i w) for real D is the conjugate
    q = [0] * (2 * n + 1)
    for i, (r1, i1) in enumerate(p):
        for j, (r2, i2) in enumerate(pc):
            q[i + j] += r1 * r2 - i1 * i2
    return q


def series_inverse(q, terms):
    """The first terms coefficients of the power series of 1 / Q, with q[0] != 0."""
    c = []
    for j in range(terms):
        s = (1 if j == 0 else 0) - sum(q[i] * c[j - i] for i in range(1, min(j, len(q) - 1) + 1))
        c.append(s / q[0])
    return c


def test_poles_left_half_plane() -> None:
    for n in range(1, 12):
        ps = butterworth_poles(n, 2.5)
        assert all(p.real < 0 for p in ps)
        assert all(abs(abs(p) - 2.5) < 1e-12 for p in ps)
        for p in ps:
            assert min(abs(p.conjugate() - r) for r in ps) < 1e-12


def test_low_orders() -> None:
    assert all(abs(u - v) < 1e-12 for u, v in zip(denominator(1), [1, 1]))
    assert all(abs(u - v) < 1e-12 for u, v in zip(denominator(2), [1, 2 ** 0.5, 1]))
    assert all(abs(u - v) < 1e-12 for u, v in zip(denominator(3), [1, 2, 2, 1]))
    assert all(abs(u - v) < 1e-12 for u, v in zip(denominator(4), [1, 2.613125929752753, 3.414213562373095, 2.613125929752753, 1]))


def test_magnitude_against_closed_formula() -> None:
    rng = random.Random(6101)
    for _ in range(300):
        n = rng.randint(1, 10)
        wc = rng.uniform(0.2, 5)
        w = rng.uniform(0, 4 * wc)
        assert abs(abs(response(n, wc, w)) ** 2 - magnitude_squared(n, wc, w)) < 1e-10


def test_half_power_at_cutoff() -> None:
    for n in range(1, 10):
        assert abs(abs(response(n, 3.0, 3.0)) ** 2 - 0.5) < 1e-12


def test_maximally_flat_exact_fraction() -> None:
    """Orders 1 and 3 have rational D(s); the Taylor series of |H|^2 is exact."""
    for n, a in ((1, [1, 1]), (3, [1, 2, 2, 1])):
        a = [Fraction(v) for v in a]
        q = squared_magnitude_poly(a)
        assert q == [1] + [0] * (2 * n - 1) + [1]  # Q(w) = 1 + w^(2N)
        c = series_inverse(q, 4 * n + 1)
        assert c[0] == 1
        assert all(v == 0 for v in c[1:2 * n])  # derivatives 1 .. 2N - 1 vanish
        assert c[2 * n] == -1  # the derivative of order 2N does not


def test_maximally_flat_float() -> None:
    for n in range(1, 9):
        q = squared_magnitude_poly(denominator(n))
        c = series_inverse(q, 2 * n + 1)
        assert abs(c[0] - 1) < 1e-9
        assert all(abs(v) < 1e-9 for v in c[1:2 * n])
        assert abs(c[2 * n] + 1) < 1e-9


def test_other_second_order_is_not_flat() -> None:
    q = squared_magnitude_poly([Fraction(1), Fraction(1), Fraction(1)])  # s^2 + s + 1
    assert q == [1, 0, -1, 0, 1]
    c = series_inverse(q, 5)
    assert c[2] == 1  # the second derivative of |H|^2 at 0 is 2, not 0


def test_magnitude_decreases() -> None:
    for n in range(1, 8):
        vals = [abs(response(n, 1.0, j / 10)) for j in range(60)]
        assert all(u > v for u, v in zip(vals, vals[1:]))


def test_minimum_order() -> None:
    n = minimum_order(1.0, 2.0, 1.0, 40.0)
    assert n == 8
    wc = cutoff_for_passband(n, 1.0, 1.0)
    assert abs(10 * math.log10(1 / magnitude_squared(n, wc, 1.0)) - 1.0) < 1e-9
    assert 10 * math.log10(1 / magnitude_squared(n, wc, 2.0)) >= 40.0
    assert 10 * math.log10(1 / magnitude_squared(n - 1, cutoff_for_passband(n - 1, 1.0, 1.0), 2.0)) < 40.0
