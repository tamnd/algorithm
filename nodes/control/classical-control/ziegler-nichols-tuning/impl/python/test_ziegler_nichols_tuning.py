# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ziegler-nichols-tuning/. The authors are listed in prov/7QVRVJ.jsonl.

import math
import random

import pytest

from ctlmat import polyadd, polymul, polyroots, polyval
from ctlsim import simulate
from ziegler_nichols_tuning import (phase, step_response_rule, tangent_fit,
                                    ultimate_cycle_rule, ultimate_point)

TU3 = 2 * math.pi / math.sqrt(3)   # ultimate period of 1/(s + 1)^3


def test_ultimate_point_third_order_lag():
    # (s + 1)^3 + 8 = (s + 3)(s^2 + 3): K_u = 8, w_u = sqrt(3).
    ku, tu, wu = ultimate_point([1.0], [1.0, 3.0, 3.0, 1.0])
    assert abs(ku - 8) < 1e-9
    assert abs(wu - math.sqrt(3)) < 1e-9
    assert abs(tu - TU3) < 1e-9


def test_ultimate_point_with_integrator():
    # s (s + 1)(s + 2) + 6 = (s + 3)(s^2 + 2): K_u = 6, w_u = sqrt(2).
    ku, tu, wu = ultimate_point([1.0], [1.0, 3.0, 2.0, 0.0])
    assert abs(ku - 6) < 1e-9
    assert abs(wu - math.sqrt(2)) < 1e-9


def test_ultimate_point_right_half_plane_zero():
    # (s + 1)^3 + 2 (1 - s) = (s + 3)(s^2 + 1): K_u = 2, w_u = 1.
    ku, tu, wu = ultimate_point([-1.0, 1.0], [1.0, 3.0, 3.0, 1.0])
    assert abs(ku - 2) < 1e-9
    assert abs(wu - 1) < 1e-9


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_first_order_plus_delay(seed):
    # P = e^(-theta s)/(s + 1): atan(w) + w theta = pi and K_u = sqrt(1 + w^2).
    rng = random.Random(seed)
    for _ in range(5):
        theta = rng.uniform(0.05, 5.0)
        ku, tu, wu = ultimate_point([1.0], [1.0, 1.0], delay=theta)
        assert abs(math.atan(wu) + wu * theta - math.pi) < 1e-10
        assert abs(ku - math.sqrt(1 + wu * wu)) < 1e-9 * ku


def test_phase_is_continuous():
    # The phase of 1/(s + 1)^3 is -3 atan(w), below -180 degrees for w > sqrt(3).
    for w in (0.1, 1.0, 1.7, 2.0, 10.0, 100.0):
        assert abs(phase([1.0], [1.0, 3.0, 3.0, 1.0], 0.0, w) + 3 * math.atan(w)) < 1e-12
    # A delay adds -w theta: 1/(s + 1) with theta = 2 at w = 3.
    assert abs(phase([1.0], [1.0, 1.0], 2.0, 3.0) + math.atan(3.0) + 6.0) < 1e-12


@pytest.mark.parametrize("seed", [11, 12, 13, 14])
def test_closed_loop_poles_cross_the_axis_at_ku(seed):
    # For a product of real lags, den + K num has roots +-j w_u at K = K_u,
    # all roots in the open left half plane for K < K_u and some root in
    # the right half plane for K > K_u.
    rng = random.Random(seed)
    n = rng.randint(3, 5)
    den = [1.0]
    for _ in range(n):
        den = polymul(den, [1.0, rng.uniform(0.3, 3.0)])
    num = [rng.uniform(0.5, 2.0)]
    ku, tu, wu = ultimate_point(num, den)
    closed = lambda k: polyadd(den, [k * c for c in num])
    p = closed(ku)
    assert abs(polyval(p, 1j * wu)) < 1e-9 * max(abs(c) for c in p)
    assert max(z.real for z in polyroots(closed(0.9 * ku))) < 0
    assert max(z.real for z in polyroots(closed(1.1 * ku))) > 0


def test_no_ultimate_point():
    # The phase of 1/(s + 1)^2 stays above -180 degrees.
    with pytest.raises(ValueError):
        ultimate_point([1.0], [1.0, 2.0, 1.0])
    # A negative gain needs the reverse action.
    with pytest.raises(ValueError):
        ultimate_point([-1.0], [1.0, 3.0, 3.0, 1.0])


def test_ultimate_cycle_rules():
    assert ultimate_cycle_rule(8.0, TU3, "P") == (4.0, None, 0)
    k, ti, td = ultimate_cycle_rule(8.0, TU3, "PI")
    assert abs(k - 3.6) < 1e-12 and abs(ti - TU3 / 1.2) < 1e-12 and td == 0
    k, ti, td = ultimate_cycle_rule(8.0, TU3, "PID")
    assert abs(k - 4.8) < 1e-12 and abs(ti - 1.813799) < 1e-6 and abs(td - 0.453450) < 1e-6


def lag3_step(t1=12.0, dt=0.01):
    ts, xs, _ = simulate(lambda t, x, u: [-x[0] + 1.0, -x[1] + x[0], -x[2] + x[1]],
                         [0.0, 0.0, 0.0], 0.0, t1, dt)
    assert len(ts) == round(t1 / dt) + 1
    return ts, [x[2] for x in xs]


def test_tangent_fit_closed_form():
    # y = 1 - e^(-t)(1 + t + t^2/2), y' = t^2 e^(-t)/2, steepest at t = 2.
    ts, ys = lag3_step()
    R, L, a = tangent_fit(ts, ys)
    assert abs(R - 2 * math.exp(-2)) < 1e-4
    assert abs(L - (9 - math.e ** 2) / 2) < 1e-4
    assert abs(a - (9 * math.exp(-2) - 1)) < 1e-4


def test_tangent_fit_input_size_and_errors():
    ts, ys = lag3_step()
    R1, L1, _ = tangent_fit(ts, ys)
    R2, L2, _ = tangent_fit(ts, [2.5 * y for y in ys], du=2.5)
    assert abs(R1 - R2) < 1e-12 and abs(L1 - L2) < 1e-12
    with pytest.raises(ValueError):
        tangent_fit(ts, [-y for y in ys])
    with pytest.raises(ValueError):
        tangent_fit(ts[:3], ys[:3])


def test_step_response_rules():
    a, L = 0.25, 0.8
    assert step_response_rule(a, L, "P") == (4.0, None, 0)
    k, ti, td = step_response_rule(a, L, "PI")
    assert abs(k - 3.6) < 1e-12 and abs(ti - L / 0.3) < 1e-12 and td == 0
    assert step_response_rule(a, L, "PID") == (4.8, 1.6, 0.4)
    with pytest.raises(ValueError):
        step_response_rule(a, L, "PD")


def pid_loop(K, Ti, Td, N=20.0, r=1.0, load=0.0, t1=60.0, dt=0.01):
    # 1/(s + 1)^3 with K (r - y) + (K/Ti) int(r - y) - K Td s/(1 + s Td/N) y.
    def f(t, x, _):
        y = x[2]
        D = -K * N * (y - x[4]) if Td > 0 else 0.0
        u = K * (r - y) + x[3] + D + load
        dxf = N / Td * (y - x[4]) if Td > 0 else 0.0
        return [-x[0] + u, -x[1] + x[0], -x[2] + x[1], K / Ti * (r - y), dxf]

    ts, xs, _ = simulate(f, [0.0] * 5, 0.0, t1, dt)
    return [x[2] for x in xs]


def maxima(ys, ref):
    return [ys[k] - ref for k in range(1, len(ys) - 1)
            if ys[k] > ref and ys[k] >= ys[k - 1] and ys[k] > ys[k + 1]]


def test_ziegler_nichols_pid_loop():
    ku, tu, _ = ultimate_point([1.0], [1.0, 3.0, 3.0, 1.0])
    K, Ti, Td = ultimate_cycle_rule(ku, tu, "PID")
    ys = pid_loop(K, Ti, Td)
    assert abs(ys[-1] - 1) < 1e-6
    pk = maxima(ys, 1.0)
    # Measurements of this run: overshoot 0.523, decay ratio 0.138.
    assert 0.45 < pk[0] < 0.60
    assert pk[1] / pk[0] < 0.25
