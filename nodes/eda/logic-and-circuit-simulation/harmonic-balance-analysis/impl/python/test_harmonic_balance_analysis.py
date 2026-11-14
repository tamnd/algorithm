# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harmonic-balance-analysis/. The authors are listed in prov/WY97C5.jsonl.

import math
import random

from harmonic_balance_analysis import (
    VT_300,
    Netlist,
    Spectrum,
    evaluate_series,
    harmonic_balance,
    hb_system,
    residual,
    source_spectrum,
    transient,
)

F0 = 1e6
W = 2 * math.pi * F0
T = 1 / F0

# Diode parameters: the saturation current IS and the emission coefficient N
# are fitted model parameters (typical values for a small silicon diode).
IS, N = 1e-14, 1.0


def clipper():
    """1 V, 1 MHz source behind 1 kOhm (as its Norton form), 100 pF and a diode to ground."""
    net = Netlist(1)
    net.isource(0, 1, lambda t: 1e-3 * math.sin(W * t))
    net.resistor(1, 0, 1e3)
    net.capacitor(1, 0, 100e-12)
    net.diode(1, 0, IS, N)
    return net


def cubic():
    """1 mA, 1 MHz source into 100 pF and a conductor with i = 1e-3 (v + v^3)."""
    net = Netlist(1)
    net.isource(0, 1, lambda t: 1e-3 * math.sin(W * t))
    net.cubic(1, 0, 1e-3, 1e-3)
    net.capacitor(1, 0, 100e-12)
    return net


def reference(net, periods=5):
    """Trapezoidal transient with 1000 and 2000 steps per period, Richardson-extrapolated.

    Returns the values at t_j = (j + 1) T / 1000 of the last period.
    """
    r1 = transient(net, T, 1000, periods)
    r2 = transient(net, T, 2000, periods)
    return [r2[2 * j + 1][0] + (r2[2 * j + 1][0] - r1[j][0]) / 3 for j in range(1000)]


def test_dft_round_trip_and_exact_trigonometric_polynomials():
    sp = Spectrum(3)
    xs = [math.cos(2 * math.pi * i / 7) + 0.5 * math.sin(3 * 2 * math.pi * i / 7) + 2 for i in range(7)]
    X = sp.forward(xs)
    assert abs(X[3] - 2) < 1e-15
    assert abs(X[4] - 0.5) < 1e-15 and abs(X[2] - 0.5) < 1e-15
    assert abs(X[6] - (-0.25j)) < 1e-15 and abs(X[0] - 0.25j) < 1e-15
    back = sp.backward(X)
    assert max(abs(a - b) for a, b in zip(xs, back)) < 1e-14


def test_linear_rlc_is_exact_and_newton_takes_one_step():
    # source with harmonics 1 and 3: v(t) = cos(wt) + 0.3 sin(3wt), K = 3 holds them
    r, l, c = 50.0, 10e-6, 2e-9
    net = Netlist(2)
    net.vsource(1, 0, lambda t: math.cos(W * t) + 0.3 * math.sin(3 * W * t))
    net.resistor(1, 2, r)
    net.inductor(2, 0, l)
    net.capacitor(2, 0, c)
    X, it, _ = harmonic_balance(net, W, 3, step_limit=math.inf)
    assert it == 2  # the first step solves it; the second confirms
    K = 3
    for k, vk in ((1, 0.5), (3, -0.15j)):
        y = 1 / (1j * k * W * l) + 1j * k * W * c  # admittance of L parallel C
        v2 = vk / (1 + r * y)
        assert abs(X[1][K + k] - v2) < 1e-12
        assert abs(X[1][K - k] - v2.conjugate()) < 1e-12
    for k in (0, 2):
        assert abs(X[1][K + k]) < 1e-12


def test_k_zero_is_the_dc_operating_point():
    net = Netlist(1)
    net.isource(0, 1, 1e-3)
    net.resistor(1, 0, 1e3)
    net.diode(1, 0, IS, N)
    X, _, _ = harmonic_balance(net, W, 0)
    lo, hi = 0.0, 1.0  # bisection on 1e-3 = v / 1e3 + IS (exp(v / VT) - 1)
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid / 1e3 + IS * (math.exp(mid / (N * VT_300)) - 1) < 1e-3:
            lo = mid
        else:
            hi = mid
    assert abs(X[0][0].real - lo) < 1e-12


def test_jacobian_matches_finite_differences():
    rng = random.Random(51)
    for _ in range(3):
        net = Netlist(2)
        net.isource(0, 1, lambda t: 1e-3 * math.sin(W * t) + 2e-4)
        net.resistor(1, 0, rng.uniform(500, 2000))
        net.resistor(1, 2, rng.uniform(500, 2000))
        net.capacitor(1, 2, rng.uniform(10e-12, 100e-12))
        net.diode(2, 0, IS, N, rng.uniform(1e-9, 20e-9))
        net.cubic(1, 0, 1e-4, 1e-4)
        K = 2
        M = 2 * K + 1
        X = [[0j] * M for _ in range(2)]
        for a in range(2):
            for k in range(1, K + 1):
                z = complex(rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2))
                X[a][K + k], X[a][K - k] = z, z.conjugate()
            X[a][K] = complex(rng.uniform(0.3, 0.6))
        # a direction with conjugate symmetry keeps the samples real
        D = [[0j] * M for _ in range(2)]
        for a in range(2):
            for k in range(1, K + 1):
                z = complex(rng.gauss(0, 1), rng.gauss(0, 1))
                D[a][K + k], D[a][K - k] = z, z.conjugate()
            D[a][K] = complex(rng.gauss(0, 1))
        eps = 1e-6

        def shifted(s):
            return [[X[a][k] + s * D[a][k] for k in range(M)] for a in range(2)]

        Rp, Rm = residual(net, shifted(eps), W), residual(net, shifted(-eps), W)
        fd = [(p - m) / (2 * eps) for p, m in zip(Rp, Rm)]
        _, J = hb_system(net, X, W, source_spectrum(net, W, K))
        flat = D[0] + D[1]
        Jd = [sum(j * d for j, d in zip(row, flat)) for row in J]
        scale = max(abs(v) for v in fd)
        assert max(abs(a - b) for a, b in zip(fd, Jd)) < 1e-6 * scale


def test_samples_are_real_and_satisfy_collocation():
    net = clipper()
    X, _, samples = harmonic_balance(net, W, 8)
    for a in range(net.size):
        for k in range(1, 9):
            assert abs(X[a][8 + k] - X[a][8 - k].conjugate()) < 1e-12
    # the residual of the returned spectrum is zero to rounding
    assert max(abs(v) for v in residual(net, X, W)) < 1e-12
    assert len(samples) == 17


def test_cubic_converges_spectrally_against_a_transient():
    net = cubic()
    ref = reference(net)
    errs = {}
    for K in (4, 8, 16):
        X, _, _ = harmonic_balance(net, W, K)
        errs[K] = max(abs(evaluate_series(X, W, (j + 1) * T / 1000)[0] - ref[j]) for j in range(0, 1000, 5))
    # measured: 7.0e-3, 6.7e-5, 1.1e-8
    assert errs[4] < 1e-2 and errs[8] < 1e-4 and errs[16] < 1e-7
    assert errs[16] < errs[8] / 100 < errs[4] / 1e4


def test_diode_clipper_error_falls_with_k_against_a_transient():
    net = clipper()
    ref = reference(net)
    errs = {}
    for K in (4, 8, 16):
        X, _, _ = harmonic_balance(net, W, K)
        errs[K] = max(abs(evaluate_series(X, W, (j + 1) * T / 1000)[0] - ref[j]) for j in range(0, 1000, 5))
    # measured: 4.8e-2, 1.3e-2, 2.5e-3 (slower than the cubic: the diode is stiff)
    assert errs[16] < 3e-3 < errs[8] < 2e-2 < errs[4] < 6e-2
