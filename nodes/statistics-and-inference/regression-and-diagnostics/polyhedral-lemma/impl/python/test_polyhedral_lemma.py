# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyhedral-lemma/. The authors are listed in prov/TA2HX1.jsonl.

import math
import random

import pytest

from polyhedral_lemma import (
    log_norm_sf, max_abs_selection, selective_interval, selective_p_value, selective_pivot,
    truncated_normal_cdf, truncation_limits,
)


def eye(p):
    return [[1.0 if i == j else 0.0 for j in range(p)] for i in range(p)]


def ks_uniform(values):
    v = sorted(values)
    n = len(v)
    return max(max((i + 1) / n - u, u - i / n) for i, u in enumerate(v))


def test_log_tail_is_continuous_and_accurate():
    for x in (0.0, 1.0, 5.0, 20.0, 29.0):
        assert math.isclose(log_norm_sf(x), math.log(0.5 * math.erfc(x / math.sqrt(2.0))), rel_tol=1e-13)
    left = math.log(0.5 * math.erfc(30.0 / math.sqrt(2.0)))
    assert math.isclose(log_norm_sf(30.0), left, rel_tol=1e-13)
    assert math.isclose(log_norm_sf(30.0 + 1e-9), left, rel_tol=1e-9)
    assert log_norm_sf(1e4) < -4.9e7


def test_truncated_cdf_far_in_the_tail():
    # Mean 0, truncated to [40, inf): T - 40 is close to exponential with rate 40.
    for d in (0.01, 0.05, 0.1):
        f = truncated_normal_cdf(40.0 + d, 0.0, 1.0, 40.0, math.inf)
        assert abs(f - (1.0 - math.exp(-40.0 * d - d * d / 2.0) * 40.0 / (40.0 + d))) < 2e-3
    assert truncated_normal_cdf(-40.05, 0.0, 1.0, -math.inf, -40.0) == pytest.approx(
        1.0 - truncated_normal_cdf(40.05, 0.0, 1.0, 40.0, math.inf), abs=1e-12)
    # Inside the bulk it is the plain formula.
    phi = lambda t: 0.5 * math.erfc(-t / math.sqrt(2.0))
    assert truncated_normal_cdf(0.3, 0.0, 1.0, -1.0, 2.0) == pytest.approx((phi(0.3) - phi(-1.0)) / (phi(2.0) - phi(-1.0)), rel=1e-12)


def test_limits_describe_the_event_on_the_line():
    rng = random.Random(20261114)
    for _ in range(200):
        p = 4
        a = [[rng.uniform(-1, 1) for _ in range(p)] for _ in range(6)]
        b = [rng.uniform(0.5, 2.0) for _ in range(6)]
        m = [[rng.uniform(-1, 1) for _ in range(p)] for _ in range(p)]
        sigma = [[math.fsum(m[i][k] * m[j][k] for k in range(p)) + (1.0 if i == j else 0.0) for j in range(p)] for i in range(p)]
        eta = [rng.uniform(-1, 1) for _ in range(p)]
        y = [0.0] * p  # A 0 = 0 <= b, so y is inside the polyhedron
        vm, vp, v0, t, var = truncation_limits(a, b, eta, sigma, y)
        assert v0 >= 0.0 and vm <= t <= vp
        s_eta = [math.fsum(sigma[i][k] * eta[k] for k in range(p)) for i in range(p)]
        c = [s / var for s in s_eta]
        z = [yi - ci * t for yi, ci in zip(y, c)]
        for s in [vm - 0.01, vm + 0.01, vp - 0.01, vp + 0.01, t]:
            if not math.isfinite(s):
                continue
            point = [zi + ci * s for zi, ci in zip(z, c)]
            inside = all(math.fsum(r * q for r, q in zip(row, point)) <= bj + 1e-12 for row, bj in zip(a, b))
            assert inside == (vm <= s <= vp)


def test_one_step_selection_hand_example():
    y = [2.5, -1.0, 0.8]
    j, s, a, b = max_abs_selection(y)
    assert (j, s) == (0, 1.0)
    eta = [1.0, 0.0, 0.0]
    vm, vp, v0, t, var = truncation_limits(a, b, eta, eye(3), y)
    assert (vm, vp, t) == (1.0, math.inf, 2.5)
    q = lambda x: 0.5 * math.erfc(x / math.sqrt(2.0))
    assert selective_p_value(a, b, eta, eye(3), y) == pytest.approx(q(2.5) / q(1.0), rel=1e-12)
    lo, hi = selective_interval(a, b, eta, eye(3), y)
    assert lo == pytest.approx(-0.34087, abs=1e-4)
    assert hi == pytest.approx(4.45540, abs=1e-4)
    assert lo < 2.5 - 1.96  # the selective interval is wider than the naive one on the left
    assert selective_pivot(a, b, eta, eye(3), y, lo) == pytest.approx(0.975, abs=1e-9)
    assert selective_pivot(a, b, eta, eye(3), y, hi) == pytest.approx(0.025, abs=1e-9)


def test_pivot_is_uniform_after_selection_monte_carlo():
    # One-step selection of the largest |y_j| among p = 5, then inference on the selected mean.
    # Tolerance: with 4000 draws the Kolmogorov-Smirnov distance of a true uniform sample exceeds
    # 0.0258 with probability about 0.01, so 0.03 is a safe bound for the fixed seed.
    rng = random.Random(20261114)
    p, reps = 5, 4000
    for mu in ([0.0] * p, [1.0, 0.5, 0.0, 0.0, -2.0]):
        pivots, naive = [], []
        for _ in range(reps):
            y = [m + rng.gauss(0.0, 1.0) for m in mu]
            j, s, a, b = max_abs_selection(y)
            eta = [0.0] * p
            eta[j] = s
            pivots.append(selective_pivot(a, b, eta, eye(p), y, s * mu[j]))
            naive.append(0.5 * math.erfc(-(s * y[j] - s * mu[j]) / math.sqrt(2.0)))
        assert ks_uniform(pivots) < 0.03
        assert ks_uniform(naive) > 0.15  # the pivot that ignores selection is far from uniform


def test_event_check():
    y = [2.5, -1.0, 0.8]
    _, _, a, b = max_abs_selection(y)
    with pytest.raises(ValueError):
        selective_pivot(a, b, [1.0, 0.0, 0.0], eye(3), [0.1, 3.0, 0.0])
    with pytest.raises(ValueError):
        truncated_normal_cdf(0.0, 0.0, 1.0, 1.0, 1.0)
