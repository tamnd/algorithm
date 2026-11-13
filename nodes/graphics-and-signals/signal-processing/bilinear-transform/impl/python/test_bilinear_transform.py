# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-transform/. The authors are listed in prov/CV28SZ.jsonl.

import cmath
import math
import random
from fractions import Fraction

from bilinear_transform import (
    analog_response,
    bilinear,
    butterworth_lowpass,
    digital_response,
    s_to_z,
    unwarp,
    warp,
    z_to_s,
)


def poly_from_roots(rs):
    c = [1 + 0j]
    for r in rs:
        nxt = [0j] * (len(c) + 1)
        for i, v in enumerate(c):
            nxt[i + 1] += v
            nxt[i] -= r * v
        c = nxt
    return c


def test_left_half_plane_into_disk() -> None:
    rng = random.Random(7101)
    for _ in range(2000):
        t = rng.uniform(0.01, 10)
        s = complex(-rng.expovariate(1.0) * 10 - 1e-9, rng.uniform(-100, 100))
        assert abs(s_to_z(s, t)) < 1
        assert abs(s_to_z(-s.conjugate(), t)) > 1  # the mirror point is outside
        assert abs(z_to_s(s_to_z(s, t), t) - s) < 1e-9 * (1 + abs(s))


def test_imaginary_axis_onto_circle() -> None:
    for j in range(-50, 51):
        z = s_to_z(1j * j / 3, 0.5)
        assert abs(abs(z) - 1) < 1e-14


def test_disk_exact_fraction() -> None:
    """|1 + w|^2 - |1 - w|^2 = 4 Re(w) for w = s T / 2, in exact rational arithmetic."""
    rng = random.Random(7102)
    for _ in range(500):
        re = Fraction(-rng.randint(1, 1000), rng.randint(1, 1000))
        im = Fraction(rng.randint(-1000, 1000), rng.randint(1, 1000))
        t = Fraction(rng.randint(1, 50), rng.randint(1, 50))
        wr, wi = re * t / 2, im * t / 2
        num = (1 + wr) ** 2 + wi ** 2
        den = (1 - wr) ** 2 + wi ** 2
        assert num < den  # |z|^2 = num / den < 1
        assert num - den == 4 * wr


def test_first_order_exact() -> None:
    b, a = bilinear([Fraction(1)], [Fraction(1), Fraction(1)], Fraction(1))
    assert b == [Fraction(1, 3), Fraction(1, 3)]
    assert a == [1, Fraction(-1, 3)]


def test_response_is_warped_analog_response() -> None:
    rng = random.Random(7103)
    for _ in range(200):
        n = rng.randint(1, 5)
        poles = []
        while len(poles) < n:
            if n - len(poles) >= 2 and rng.random() < 0.5:
                p = complex(-rng.uniform(0.1, 3), rng.uniform(0.1, 3))
                poles += [p, p.conjugate()]
            else:
                poles.append(complex(-rng.uniform(0.1, 3), 0))
        a = [v.real for v in poly_from_roots(poles)]
        b = [rng.uniform(-2, 2) for _ in range(rng.randint(1, n + 1))]
        t = rng.uniform(0.1, 2)
        bz, az = bilinear(b, a, t)
        for _ in range(10):
            w = rng.uniform(-3.1, 3.1)
            d = digital_response(bz, az, w)
            h = analog_response(b, a, warp(w, t))
            assert abs(d - h) < 1e-9 * (1 + abs(h))
        # each analog pole lands on a digital pole inside the unit disk
        for p in poles:
            z = s_to_z(p, t)
            assert abs(z) < 1
            m = len(az) - 1  # evaluate z^m A(z), a polynomial in z
            assert abs(sum(v * z ** (m - i) for i, v in enumerate(az))) < 1e-8


def test_measured_half_power_frequency() -> None:
    """The analog cutoff W = 1 of 1/(s + 1) lands on the digital frequency 2 arctan(T/2)."""
    for t in (0.1, 0.5, 1.0, 2.0, 4.0):
        bz, az = bilinear([1.0], [1.0, 1.0], t)
        lo, hi = 0.0, math.pi
        for _ in range(100):
            mid = (lo + hi) / 2
            if abs(digital_response(bz, az, mid)) ** 2 > 0.5:
                lo = mid
            else:
                hi = mid
        assert abs(lo - unwarp(1.0, t)) < 1e-12
        assert abs(warp(lo, t) - 1.0) < 1e-9
    # without prewarping, a cutoff of 0.5 rad/sample at T = 1 lands at 2 arctan(1/4)
    assert abs(unwarp(0.5, 1.0) - 0.4899573262537283) < 1e-15


def test_digital_butterworth() -> None:
    for n in range(1, 8):
        for wc in (0.2, 0.5 * math.pi, 2.5):
            b, a = butterworth_lowpass(n, wc)
            assert abs(abs(digital_response(b, a, 0.0)) - 1) < 1e-12
            assert abs(abs(digital_response(b, a, wc)) ** 2 - 0.5) < 1e-10
            assert abs(digital_response(b, a, math.pi)) < 1e-10
            # the closed form of the digital magnitude: 1 / (1 + (tan(w/2) / tan(wc/2))^(2N))
            for w in (0.1, 1.0, 2.0, 3.0):
                g = 1 / (1 + (math.tan(w / 2) / math.tan(wc / 2)) ** (2 * n))
                # direct form coefficients of order 7 with poles near z = 1 lose digits
                assert abs(abs(digital_response(b, a, w)) ** 2 - g) < 1e-8


def test_butterworth_poles_and_polynomial_route_agree() -> None:
    n, wc = 4, 0.6
    t = 1.0
    big = warp(wc, t)
    poles = [big * cmath.exp(1j * math.pi * (2 * k + n - 1) / (2 * n)) for k in range(1, n + 1)]
    a_s = [v.real for v in poly_from_roots(poles)]
    bz, az = bilinear([big ** n], a_s, t)
    b2, a2 = butterworth_lowpass(n, wc)
    assert all(abs(u - v) < 1e-12 for u, v in zip(az, a2))
    assert all(abs(u - v) < 1e-12 for u, v in zip(bz, b2))
