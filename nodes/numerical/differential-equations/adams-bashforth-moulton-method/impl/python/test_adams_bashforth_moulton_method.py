# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-bashforth-moulton-method/. The authors are listed in prov/VJTC0J.jsonl.

import math
from fractions import Fraction as F

import pytest

from adams_bashforth_moulton_method import abm, abm_coefficients

f_ex = lambda t, y: -2 * t * y * y
y_ex = lambda t: 1 / (1 + t * t)


def test_coefficients_and_milne_factor_exact() -> None:
    ab, am, milne = abm_coefficients(4)
    assert ab == [F(55, 24), F(-59, 24), F(37, 24), F(-9, 24)]
    assert am == [F(9, 24), F(19, 24), F(-5, 24), F(1, 24)]
    assert milne == F(-19, 270)
    assert abm_coefficients(2)[2] == F(-1, 6)
    for k in range(1, 7):
        ab, am, _ = abm_coefficients(k)
        assert sum(ab) == 1 and sum(am) == 1
        # Both formulas integrate polynomials of degree k - 1 exactly on [0, 1].
        for q in range(k):
            exact = F(1, q + 1)
            assert sum(b * F(-j) ** q for j, b in enumerate(ab)) == exact
            assert sum(b * F(1 - j) ** q for j, b in enumerate(am)) == exact


def test_observed_order() -> None:
    for k in range(1, 6):
        errs = []
        for N in (40, 80, 160, 320):
            ts, ys, _ = abm(f_ex, 0.0, 1.0, 2.0, 2.0 / N, k)
            errs.append(max(abs(y - y_ex(t)) for t, y in zip(ts, ys)))
        p = math.log2(errs[-2] / errs[-1])
        assert abs(p - k) < 0.25, (k, p)


def test_milne_estimate_tracks_local_error() -> None:
    ab, am, milne = (abm_coefficients(4)[0], abm_coefficients(4)[1], abm_coefficients(4)[2])
    ab, am, milne = [float(v) for v in ab], [float(v) for v in am], float(milne)
    ratios = []
    for h in (0.05, 0.025, 0.0125):
        t0 = 1.0
        fs = [f_ex(t0 - j * h, y_ex(t0 - j * h)) for j in range(4)]
        yp = y_ex(t0) + h * sum(ab[j] * fs[j] for j in range(4))
        yc = y_ex(t0) + h * (am[0] * f_ex(t0 + h, yp) + sum(am[j + 1] * fs[j] for j in range(3)))
        ratios.append(milne * (yc - yp) / (y_ex(t0 + h) - yc))
    assert all(r > 0 for r in ratios)
    assert abs(ratios[-1] - 1) < 0.15 and abs(ratios[-1] - 1) < abs(ratios[0] - 1)


def test_estimates_returned() -> None:
    ts, ys, est = abm(f_ex, 0.0, 1.0, 2.0, 0.025, 4)
    assert len(est) == len(ts) and est[:4] == [0.0, 0.0, 0.0, 0.0]
    assert 0 < max(est) < 1e-7


def test_more_corrections_approach_the_corrector() -> None:
    # With m corrections the result converges to the fixed point of the Adams-Moulton formula.
    _, y1, _ = abm(lambda t, y: -y, 0.0, 1.0, 1.0, 0.1, 2, corrections=1)
    _, y30, _ = abm(lambda t, y: -y, 0.0, 1.0, 1.0, 0.1, 2, corrections=30)
    z = -0.1
    r = (1 + z / 2) / (1 - z / 2)  # the trapezoidal factor
    assert abs(y30[-1] - y30[1] * r ** 9) < 1e-14
    assert abs(y1[-1] - y30[-1]) > 1e-6


def test_stability_interval_pece() -> None:
    def last(z, k, n=1000):
        _, ys, _ = abm(lambda t, y: z * y, 0.0, 1.0, float(n), 1.0, k)
        return abs(ys[-1])
    assert last(-1.9, 2) < 1e-3 and last(-2.1, 2) > 1e3
    assert last(-1.2, 4) < 1e-3 and last(-1.4, 4) > 1e3


def test_stiff_failure() -> None:
    f = lambda t, y: -1000.0 * (y - math.cos(t))
    _, ys, _ = abm(f, 0.0, 1.0, 1.0, 0.01, 4)
    assert not abs(ys[-1]) < 1e10
    _, ys, _ = abm(f, 0.0, 1.0, 1.0, 0.0005, 4)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-3


def test_vector_and_edges() -> None:
    ts, ys, _ = abm(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], math.pi, math.pi / 200, 4)
    assert abs(ys[-1][0] + 1) < 1e-7 and abs(ys[-1][1]) < 1e-7
    assert abm(lambda t, y: y, 0.0, 3.0, 0.0, 0.1) == ([0.0], [3.0], [0.0])
    ts, ys, _ = abm(lambda t, y: y, 0.0, 1.0, 0.05, 1.0, 4)
    assert ts == [0.0, 0.05] and abs(ys[1] - math.exp(0.05)) < 1e-8
    ts, _, _ = abm(lambda t, y: y, 0.0, 1.0, 1.0, 0.3, 2)
    assert len(ts) == 5 and ts[-1] == 1.0
    with pytest.raises(ValueError):
        abm(lambda t, y: y, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        abm(lambda t, y: y, 0.0, 1.0, 1.0, 0.1, corrections=0)
