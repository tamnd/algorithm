# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fir-filter/. The authors are listed in prov/A2Z6XD.jsonl.

import cmath
import math
import random
from fractions import Fraction

from fir_filter import amplitude, fir_filter, frequency_response, l1_gain, linear_phase_type

TOL = 1e-12


def direct(h, x):
    """The convolution sum, written out with the zero initial state."""
    return [sum(h[k] * x[n - k] for k in range(len(h)) if n - k >= 0) for n in range(len(x))]


def test_example_moving_average() -> None:
    h = [Fraction(1, 4)] * 4
    x = [0, 0, 4, 8, 8, 8, 0]
    assert fir_filter(h, x) == [0, 0, 1, 3, 5, 7, 6]


def test_impulse_response_is_h() -> None:
    h = [3, -1, 4, 1, -5]
    assert fir_filter(h, [1] + [0] * 7) == h + [0, 0, 0]


def test_against_direct_sum_exact() -> None:
    rng = random.Random(4101)
    for _ in range(300):
        h = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(rng.randint(1, 9))]
        x = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
        assert fir_filter(h, x) == direct(h, x)


def test_types() -> None:
    assert linear_phase_type([1, 2, 1]) == 1
    assert linear_phase_type([1, 3, 3, 1]) == 2
    assert linear_phase_type([1, 0, -1]) == 3
    assert linear_phase_type([1, -1]) == 4
    assert linear_phase_type([1, 2]) == 0


def test_linear_phase_from_exact_response() -> None:
    """H(e^(i w)) e^(i w M / 2) must be real (types 1, 2) or imaginary (types 3, 4) at every w."""
    rng = random.Random(4102)
    for _ in range(200):
        half = [rng.randint(-9, 9) for _ in range(rng.randint(1, 6))]
        kind = rng.randint(1, 4)
        if kind == 1:
            h = half + [rng.randint(-9, 9)] + half[::-1]
        elif kind == 2:
            h = half + half[::-1]
        elif kind == 3:
            h = half + [0] + [-v for v in half[::-1]]
        else:
            h = half + [-v for v in half[::-1]]
        assert linear_phase_type(h) == kind or all(v == 0 for v in h)
        m = len(h) - 1
        for j in range(64):
            w = -math.pi + 2 * math.pi * j / 63
            rot = frequency_response(h, w) * cmath.exp(1j * w * m / 2)
            scale = 1 + l1_gain(h)
            if kind in (1, 2):
                assert abs(rot.imag) <= TOL * scale
                assert abs(rot.real - amplitude(h, w)) <= TOL * scale
            else:
                assert abs(rot.real) <= TOL * scale
                assert abs(rot.imag - amplitude(h, w)) <= TOL * scale


def test_group_delay_is_half_the_order() -> None:
    """The phase -w M / 2 has slope -M / 2: check by a central difference where A is not zero."""
    h = [1, 4, 6, 4, 1]
    m = 4
    for w in (0.3, 0.9, 1.7, 2.5):
        e = 1e-6
        p1 = cmath.phase(frequency_response(h, w + e))
        p0 = cmath.phase(frequency_response(h, w - e))
        assert abs(-(p1 - p0) / (2 * e) - m / 2) < 1e-6


def test_nonsymmetric_filter_has_no_linear_phase() -> None:
    h = [2, 1]
    w = 1.0
    rot = frequency_response(h, w) * cmath.exp(1j * w / 2)
    assert abs(rot.imag) > 0.4


def test_bounded_input_bounded_output() -> None:
    rng = random.Random(4103)
    for _ in range(100):
        h = [rng.uniform(-3, 3) for _ in range(rng.randint(1, 10))]
        x = [rng.uniform(-1, 1) for _ in range(50)]
        bound = l1_gain(h) * max(abs(v) for v in x)
        assert all(abs(v) <= bound + 1e-12 for v in fir_filter(h, x))


def test_worst_case_input_reaches_the_bound() -> None:
    h = [Fraction(1, 2), Fraction(-1, 3), Fraction(1, 6)]
    x = [1, -1, 1]  # x[n - k] = sign(h[k]) at n = 2
    assert fir_filter(h, x)[2] == l1_gain(h)
