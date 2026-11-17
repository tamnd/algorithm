# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-flux-balance-analysis/. The authors are listed in prov/4C9MZV.jsonl.
"""Tests of dfba() on the overflow network.

For this network the FBA optimum has a closed form (overflow_rates), so the
dynamic model reduces to an ODE in (X, s, p). References:
- the explicit Euler steps of that ODE, done by hand (same steps, so the
  results agree to rounding, tolerance 1e-9);
- an RK4 solution of the ODE with step 1e-3 (error far below the Euler
  error), to check that the Euler error halves when dt halves;
- conserved X + Y s when the yield Y is constant;
- the exact exponential solution when the uptake is constant (Km = 0).
"""

import math

from dynamic_flux_balance_analysis import (BIO_OV, E_OV, KM, LB_OV, S_OV,
                                           UB_OV, UPTAKES_OV, VMAX, dfba,
                                           overflow_rates)

X0, S0 = 0.05, 10.0


def rhs(y, o_max=1.0, vmax=VMAX, km=KM):
    X, s, p = y
    s = max(s, 0.0)
    u = vmax * s / (km + s)
    mu, sec = overflow_rates(u, o_max)
    return [mu * X, -u * X, sec * X]


def rk4(y, h, n):
    for _ in range(n):
        k1 = rhs(y)
        k2 = rhs([a + h / 2 * b for a, b in zip(y, k1)])
        k3 = rhs([a + h / 2 * b for a, b in zip(y, k2)])
        k4 = rhs([a + h * b for a, b in zip(y, k3)])
        y = [a + h / 6 * (b + 2 * c + 2 * d + e)
             for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
    return y


def run(dt, steps, ub=UB_OV, uptakes=UPTAKES_OV, update="euler", s0=S0):
    return dfba(S_OV, LB_OV, ub, BIO_OV, E_OV, uptakes, X0, [s0, 0.0], dt,
                steps, update)


def test_matches_hand_euler():
    dt, steps = 0.01, 400
    tr = run(dt, steps)
    y = [X0, S0, 0.0]
    for t, X, z, v in tr:
        assert abs(X - y[0]) <= 1e-9 and abs(z[0] - y[1]) <= 1e-9
        assert abs(z[1] - y[2]) <= 1e-9
        d = rhs(y)
        y = [a + dt * b for a, b in zip(y, d)]


def test_overflow_then_respiration():
    tr = run(0.01, 400)
    first, late = tr[0][3], tr[350][3]
    assert first[3] > 0 and first[1] == 1.0  # overflow: oxygen at its bound
    assert late[3] == 0.0                    # respiration only at low s
    assert tr[-1][2][0] < 1e-3 and abs(tr[-1][2][1] - 2.8856) < 1e-3


def test_first_order_convergence():
    T = 4.0
    ref = rk4([X0, S0, 0.0], 1e-3, 4000)
    errs = []
    for dt in (0.04, 0.02, 0.01):
        tr = run(dt, int(round(T / dt)))
        _, X, z, _ = tr[-1]
        errs.append(abs(X - ref[0]) + abs(z[0] - ref[1]) + abs(z[1] - ref[2]))
    for a, b in zip(errs, errs[1:]):
        assert 1.6 <= a / b <= 2.4


def test_constant_yield_conserves_mass():
    # With a large oxygen bound there is no overflow: mu = (2/15) u.
    ub = list(UB_OV)
    ub[1] = 100
    Y = 2 / 15
    tr = run(0.05, 120, ub=ub)
    total = X0 + Y * S0
    for t, X, z, v in tr:
        assert abs(X + Y * z[0] - total) <= 1e-9
        assert z[0] >= -1e-12
    assert abs(tr[-1][1] - total) <= 1e-6


def test_exponential_update_is_exact_for_constant_uptake():
    uptakes = [(0, 0, VMAX, 0.0)]  # Km = 0: the uptake is VMAX while s > 0
    mu = (VMAX + 1) / 10
    tr = run(0.1, 20, uptakes=uptakes, update="exponential")
    for t, X, z, v in tr:
        assert abs(X - X0 * math.exp(mu * t)) <= 1e-12 * X
        s = S0 - VMAX / mu * X0 * math.expm1(mu * t)
        assert abs(z[0] - s) <= 1e-9
    # Euler underestimates the exponential growth.
    eu = run(0.1, 20, uptakes=uptakes)
    assert eu[-1][1] < tr[-1][1]


def test_empty_medium_and_large_step():
    tr = run(0.01, 10, s0=0.0)
    assert all(rec[1] == X0 for rec in tr)
    tr = run(0.5, 40)
    assert all(rec[2][0] >= -1e-12 for rec in tr)
