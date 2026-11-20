# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moving-target-indication/. The authors are listed in prov/YMQQ6D.jsonl.

import cmath
import math
import random

import pytest

from cbb import cn, conv
from moving_target_indication import (
    blind_speeds,
    canceller_weights,
    gaussian_clutter_rho,
    improvement_factor,
    mti_cancel,
    response,
    response_magnitude,
)

C = 299792458.0


def test_weights():
    assert canceller_weights(1) == [1]
    assert canceller_weights(2) == [1, -1]
    assert canceller_weights(3) == [1, -2, 1]
    assert canceller_weights(4) == [1, -3, 3, -1]
    assert sum(canceller_weights(7)) == 0


def test_worked_example():
    # Range bin 0: clutter 5. Bin 1: clutter 5 plus a target 2 j^p (f_d = PRF / 4). Bin 2: clutter 3.
    x = [[5, 5 + 2 * (1j ** p), 3] for p in range(5)]
    y2 = mti_cancel(x, 2)
    assert [row[1] for row in y2] == [-2 + 2j, -2 - 2j, 2 - 2j, 2 + 2j]
    assert all(row[0] == 0 and row[2] == 0 for row in y2)
    y3 = mti_cancel(x, 3)
    assert [row[1] for row in y3] == [-4j, 4, 4j]
    assert all(abs(row[1]) == 4 for row in y3)


def test_short_input():
    assert mti_cancel([], 2) == []
    assert mti_cancel([[1, 2, 3]], 2) == []
    with pytest.raises(ValueError):
        mti_cancel([[1, 2], [3]], 2)


def test_polynomial_clutter_is_removed_exactly():
    """The L-pulse canceller removes every clutter sequence that is a polynomial of degree L - 2 in p."""
    rng = random.Random(6101)
    for _ in range(300):
        n_pulses = rng.randint(2, 5)
        p_count, m = rng.randint(n_pulses, 12), rng.randint(1, 4)
        coef = [[rng.randint(-50, 50) for _ in range(n_pulses - 1)] for _ in range(m)]
        x = [[sum(c * p ** d for d, c in enumerate(coef[r])) for r in range(m)] for p in range(p_count)]
        assert all(v == 0 for row in mti_cancel(x, n_pulses) for v in row)


def test_matches_convolution_in_slow_time():
    rng = random.Random(6102)
    for _ in range(500):
        n_pulses = rng.randint(1, 5)
        p_count, m = rng.randint(n_pulses, 10), rng.randint(1, 3)
        x = [[cn(rng, 1.0) for _ in range(m)] for _ in range(p_count)]
        y = mti_cancel(x, n_pulses)
        for r in range(m):
            ref = conv([row[r] for row in x], [complex(v) for v in canceller_weights(n_pulses)])
            got = [row[r] for row in y]
            want = ref[n_pulses - 1:p_count]
            assert len(got) == len(want)
            assert all(abs(a - b) < 1e-12 for a, b in zip(got, want))


def test_doppler_response_matches_closed_form():
    rng = random.Random(6103)
    for _ in range(300):
        n_pulses = rng.randint(2, 5)
        f = rng.uniform(-1.5, 1.5)
        x = [[cmath.exp(2j * math.pi * f * p)] for p in range(n_pulses + 6)]
        for row in mti_cancel(x, n_pulses):
            assert abs(abs(row[0]) - response_magnitude(n_pulses, f)) < 1e-12
        assert abs(abs(response(n_pulses, f)) - response_magnitude(n_pulses, f)) < 1e-12


def test_blind_speeds():
    wavelength, prf = C / 3e9, 1000.0
    v = blind_speeds(wavelength, prf, 3)
    assert v[0] == pytest.approx(49.965, abs=1e-3)
    for n_pulses in (2, 3, 4):
        for k, speed in enumerate(v, start=1):
            fd = 2.0 * speed / wavelength
            assert fd / prf == pytest.approx(k)
            x = [[cmath.exp(2j * math.pi * fd * p / prf)] for p in range(10)]
            assert all(abs(row[0]) < 1e-9 for row in mti_cancel(x, n_pulses))
        # Half way between blind speeds the gain is the largest, 2^(L-1).
        fd = 2.0 * (v[0] / 2) / wavelength
        x = [[cmath.exp(2j * math.pi * fd * p / prf)] for p in range(10)]
        assert all(abs(abs(row[0]) - 2 ** (n_pulses - 1)) < 1e-9 for row in mti_cancel(x, n_pulses))


def test_improvement_factor_closed_forms():
    for r1, r2 in ((0.9, 0.81), (0.99, 0.95), (0.5, 0.1)):
        assert improvement_factor(2, [1.0, r1]) == pytest.approx(1 / (1 - r1))
        assert improvement_factor(3, [1.0, r1, r2]) == pytest.approx(6 / (6 - 8 * r1 + 2 * r2))
    rho = gaussian_clutter_rho(10.0, 1000.0, 3)
    assert 10 * math.log10(improvement_factor(2, rho)) == pytest.approx(27.05, abs=0.01)
    assert 10 * math.log10(improvement_factor(3, rho)) == pytest.approx(51.10, abs=0.01)


def test_improvement_factor_by_simulation_ar1_clutter():
    # AR(1) clutter c[p] = a c[p-1] + sqrt(1 - a^2) w[p] with a = 0.9 has rho_k = a^k.
    # 30000 pulses, seed 6104; the measured power ratio must be within 6 percent.
    a, n = 0.9, 30000
    rng = random.Random(6104)
    c = [cn(rng, 1.0)]
    for _ in range(n - 1):
        c.append(a * c[-1] + math.sqrt(1 - a * a) * cn(rng, 1.0))
    x = [[v] for v in c]
    p_in = sum(abs(v) ** 2 for v in c) / n
    for n_pulses in (2, 3):
        w = canceller_weights(n_pulses)
        y = mti_cancel(x, n_pulses)
        p_out = sum(abs(row[0]) ** 2 for row in y) / len(y)
        measured = sum(v * v for v in w) * p_in / p_out
        want = improvement_factor(n_pulses, [a ** k for k in range(n_pulses)])
        assert measured == pytest.approx(want, rel=0.06)
