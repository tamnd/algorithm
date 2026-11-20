# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-modulus-algorithm/. The authors are listed in prov/BYWJFM.jsonl.

import cmath
import itertools
import math
import random
from fractions import Fraction

import pytest

import cbb
from constant_modulus_algorithm import (
    cma,
    cma_cost,
    cma_cost_gradient,
    dispersion_constant,
    mean_cma,
    phase_of_cursor,
    residual_isi,
)

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]
QAM16 = [complex(a, b) / math.sqrt(10) for a in (-3, -1, 1, 3) for b in (-3, -1, 1, 3)]


def test_dispersion_constant_check_values() -> None:
    raw = [(a, b) for a in (-3, -1, 1, 3) for b in (-3, -1, 1, 3)]
    m2 = Fraction(sum(a * a + b * b for a, b in raw), 16)
    m4 = Fraction(sum((a * a + b * b) ** 2 for a, b in raw), 16)
    assert (m2, m4) == (10, 132)
    assert m4 / m2 / m2 == Fraction(132, 100)  # R2 of unit-energy 16-QAM is 1.32 exactly
    assert abs(dispersion_constant(QAM16) - 1.32) < 1e-12
    assert abs(dispersion_constant(QPSK) - 1.0) < 1e-12
    assert abs(dispersion_constant([cmath.exp(2j * math.pi * m / 8) for m in range(8)]) - 1.0) < 1e-12


@pytest.mark.parametrize("points", [QPSK, QAM16])
def test_cost_formula_equals_the_exact_expectation(points) -> None:
    kappa = dispersion_constant(points)
    rng = random.Random(1)
    for _ in range(3):
        g = [complex(rng.gauss(0, 0.6), rng.gauss(0, 0.6)) for _ in range(3)]
        total = 0.0
        for a in itertools.product(points, repeat=3):
            z = sum(gi * ai for gi, ai in zip(g, a))
            total += (abs(z) ** 2 - kappa) ** 2
        exact = total / len(points) ** 3
        assert abs(exact - cma_cost(g, kappa)) < 1e-9


def test_gradient_matches_finite_differences() -> None:
    rng = random.Random(2)
    h = [1, 0.5j, -0.2]
    c = [complex(rng.gauss(0, 0.5), rng.gauss(0, 0.5)) for _ in range(4)]
    grad = cma_cost_gradient(c, h, 1.32)
    eps = 1e-6
    for i in range(4):
        def cost(dc):
            cc = list(c)
            cc[i] += dc
            return cma_cost(cbb.conv(cc, h), 1.32)
        dx = (cost(eps) - cost(-eps)) / (2 * eps)
        dy = (cost(1j * eps) - cost(-1j * eps)) / (2 * eps)
        assert abs(grad[i] - 0.5 * complex(dx, dy)) < 1e-6  # d/d conj(c) = (d/dx + j d/dy) / 2


def test_global_minima_are_single_taps_of_any_phase() -> None:
    # for kappa < 2 the smallest cost is kappa (kappa - 1), at one tap of modulus 1 and any phase
    rng = random.Random(3)
    for kappa in (1.0, 1.32):
        best = kappa * (kappa - 1)
        for phi in (0.0, 0.7, 2.0, -3.0):
            assert abs(cma_cost([0, cmath.exp(1j * phi), 0], kappa) - best) < 1e-12
        for _ in range(500):
            g = [complex(rng.gauss(0, 0.7), rng.gauss(0, 0.7)) for _ in range(3)]
            assert cma_cost(g, kappa) >= best - 1e-12


def test_a_phase_rotation_passes_through_unchanged() -> None:
    # CMA sees only |z|: rotating the input gives the same taps and rotated outputs
    rng = random.Random(4)
    h = [1, 0.4 - 0.3j]
    x = [rng.choice(QPSK) for _ in range(800)]
    y = cbb.awgn(rng, cbb.conv(x, h)[:800], 0.01)
    rot = cmath.exp(0.9j)
    c1, z1 = cma(y, 7, 0.01, 1.0)
    c2, z2 = cma([rot * v for v in y], 7, 0.01, 1.0)
    assert max(abs(u - v) for u, v in zip(c1, c2)) < 1e-9
    assert max(abs(rot * u - v) for u, v in zip(z1, z2)) < 1e-9


def run(h, points, n, mu, k, n0, seed):
    rng = random.Random(seed)
    x = [rng.choice(points) for _ in range(k)]
    y = cbb.awgn(rng, cbb.conv(x, h)[:k], n0)
    c, z = cma(y, n, mu, dispersion_constant(points))
    g = cbb.conv(c, h)
    d, rot = phase_of_cursor(g)
    # z[t] is the output at time t + N - 1 and estimates rot x[t + N - 1 - d]
    errors = 0
    for t in range(len(z) - 2000, len(z)):
        a = z[t] / rot
        dec = min(points, key=lambda p: abs(a - p))
        errors += dec != x[t + n - 1 - d]
    return g, errors


def test_qpsk_through_a_nonminimum_phase_channel() -> None:
    # h = (0.5, 1) has its zero outside the unit circle; second-order statistics cannot see that
    g, errors = run([0.5, 1], QPSK, 11, 0.01, 6000, 0.001, 5)
    assert residual_isi(g) < 0.01
    assert errors == 0


def test_16qam_through_a_complex_channel() -> None:
    g, errors = run([1, 0.3 + 0.25j, -0.1j], QAM16, 11, 0.002, 12000, 0.0005, 6)
    assert residual_isi(g) < 0.01
    assert errors == 0


def test_a_finite_equalizer_has_a_worse_local_minimum() -> None:
    # h = (1, 0.5), 2 taps, QPSK: the mean CMA update from a spike on tap 0 and on tap 1 ends in two minima
    h = [1, 0.5]
    lo = mean_cma([1, 0], h, 1.0, 0.01, 6000)
    hi = mean_cma([0, 1], h, 1.0, 0.01, 6000)
    j_lo = cma_cost(cbb.conv(lo, h), 1.0)
    j_hi = cma_cost(cbb.conv(hi, h), 1.0)
    assert abs(j_lo - 0.083758) < 1e-6 and abs(j_hi - 0.237492) < 1e-6
    for c in (lo, hi):
        assert max(abs(v) for v in cma_cost_gradient(c, h, 1.0)) < 1e-9
    # small random moves return to the same cost, so the worse point is a local minimum, not a saddle
    rng = random.Random(7)
    for _ in range(5):
        c = [v + complex(rng.gauss(0, 0.05), rng.gauss(0, 0.05)) for v in hi]
        c = mean_cma(c, h, 1.0, 0.01, 6000)
        assert abs(cma_cost(cbb.conv(c, h), 1.0) - j_hi) < 1e-9


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        cma([1j, 1], 0, 0.01, 1.0)
    with pytest.raises(ValueError):
        cma([1j, 1], 2, -0.01, 1.0)
    with pytest.raises(ValueError):
        dispersion_constant([0j])
