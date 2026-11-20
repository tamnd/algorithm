# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-dimensional-wiener-pilot-interpolation/. The authors are listed in prov/G9C3T4.jsonl.

import cmath
import math
import random

import cbb
from two_dimensional_wiener_pilot_interpolation import estimate, nearest, wiener_weights

# Test model: N = 16 subcarriers, 9 OFDM symbols, 3 taps at delays 0, 1, 2 with powers 0.5, 0.3, 0.2.
# Each tap is an AR(1) process in n with coefficient 0.9, so r(dn, dk) = 0.9^|dn| sum_l P_l e^(-j 2 pi l dk / N).
# Pilots on symbols 0, 4, 8 and subcarriers 0, 3, ..., 15; pilot noise variance 0.05.
N = 16
POWERS = (0.5, 0.3, 0.2)
A = 0.9
SIGMA2 = 0.05
PILOTS = [(n, k) for n in (0, 4, 8) for k in range(0, 16, 3)]
TARGETS = [(n, k) for n in range(9) for k in range(N)]


def corr(dn: int, dk: int) -> complex:
    return A ** abs(dn) * sum(p * cmath.exp(-2j * math.pi * l * dk / N) for l, p in enumerate(POWERS))


def mse_of(b: list[complex], target: tuple[int, int], pilots: list[tuple[int, int]]) -> float:
    """E|H(t) - b^H y|^2 = r(0, 0) - 2 Re(b^H c) + b^H (R + sigma^2 I) b, for any weights b."""
    c = [corr(p[0] - target[0], p[1] - target[1]) for p in pilots]
    ry = [[corr(p[0] - q[0], p[1] - q[1]) + (SIGMA2 if i == j else 0) for j, q in enumerate(pilots)] for i, p in enumerate(pilots)]
    return corr(0, 0).real - 2 * cbb.dot(b, c).real + cbb.dot(b, cbb.matvec(ry, b)).real


def channel(rng: random.Random) -> list[list[complex]]:
    """H[n][k] for 9 symbols, from AR(1) taps with stationary start."""
    taps = [cbb.cn(rng, p) for p in POWERS]
    out = []
    for n in range(9):
        if n:
            taps = [A * h + cbb.cn(rng, (1 - A * A) * p) for h, p in zip(taps, POWERS)]
        out.append([sum(h * cmath.exp(-2j * math.pi * l * k / N) for l, h in enumerate(taps)) for k in range(N)])
    return out


def test_closed_form_mse_matches_simulation() -> None:
    # 300 channel realizations, seed 1, 6 nearest pilots per target, average over all 144 positions.
    rng = random.Random(1)
    plan = []
    for t in TARGETS:
        idx = nearest(t, PILOTS, 6)
        w, m = wiener_weights(t, [PILOTS[i] for i in idx], corr, SIGMA2)
        plan.append((t, idx, w, m))
    predicted = sum(m for *_, m in plan) / len(plan)
    acc = 0.0
    trials = 300
    for _ in range(trials):
        h = channel(rng)
        y = [h[n][k] + cbb.cn(rng, SIGMA2) for n, k in PILOTS]
        for (n, k), idx, w, _ in plan:
            acc += abs(h[n][k] - sum(wi.conjugate() * y[i] for wi, i in zip(w, idx))) ** 2
    assert 0.9 < acc / (trials * len(plan)) / predicted < 1.1


def test_estimate_uses_the_same_weights() -> None:
    rng = random.Random(2)
    y = [cbb.cn(rng, 1.0) for _ in PILOTS]
    targets = [(2, 5), (6, 14), (4, 3)]
    got = estimate(targets, PILOTS, y, corr, SIGMA2, 6)
    for t, g in zip(targets, got):
        idx = nearest(t, PILOTS, 6)
        w, _ = wiener_weights(t, [PILOTS[i] for i in idx], corr, SIGMA2)
        assert abs(g - sum(wi.conjugate() * y[i] for wi, i in zip(w, idx))) < 1e-12


def test_no_other_weights_do_better() -> None:
    # Brute force: random changes of the weights, and bilinear interpolation of the 4 corner pilots,
    # never give a smaller closed-form MSE than the Wiener weights on the same pilots.
    rng = random.Random(3)
    for t in ((1, 1), (2, 4), (5, 7), (7, 13)):
        n0, k0 = 4 * (t[0] // 4), 3 * (t[1] // 3)
        corners = [(n0, k0), (n0, k0 + 3), (n0 + 4, k0), (n0 + 4, k0 + 3)]
        w, m = wiener_weights(t, corners, corr, SIGMA2)
        assert abs(mse_of(w, t, corners) - m) < 1e-12
        u, v = (t[0] - n0) / 4, (t[1] - k0) / 3
        bilinear = [(1 - u) * (1 - v), (1 - u) * v, u * (1 - v), u * v]
        assert mse_of(bilinear, t, corners) > m
        for _ in range(50):
            b = [wi + cbb.cn(rng, 0.01) for wi in w]
            assert mse_of(b, t, corners) >= m - 1e-12


def test_more_pilots_never_raise_the_mse() -> None:
    for t in ((1, 1), (3, 8), (6, 14)):
        ms = [wiener_weights(t, [PILOTS[i] for i in nearest(t, PILOTS, c)], corr, SIGMA2)[1] for c in (2, 4, 6, 9, 18)]
        assert all(a >= b - 1e-12 for a, b in zip(ms, ms[1:]))


def test_a_clean_pilot_is_returned_as_it_is() -> None:
    rng = random.Random(4)
    y = [cbb.cn(rng, 1.0) for _ in PILOTS]
    i = PILOTS.index((4, 9))
    got = estimate([(4, 9)], PILOTS, y, corr, 1e-12, 6)[0]
    assert abs(got - y[i]) < 1e-6
    _, m = wiener_weights((4, 9), [PILOTS[i]], corr, 1e-12)
    assert m < 1e-9
