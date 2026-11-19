# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixing-length-model/. The authors are listed in prov/QA49H0.jsonl.

import math

import pytest

from mixing_length_model import (
    KAPPA,
    channel_stress,
    eddy_viscosity,
    exact_profile_no_damping,
    log_intercept,
    log_intercept_no_damping,
    mixing_length,
    profile,
    velocity_gradient,
)


def test_gradient_solves_the_balance():
    for tau in (1.0, 0.3, -0.7):
        for l in (0.0, 0.5, 4.1, 100.0):
            g = velocity_gradient(tau, l)
            assert (1 + l * l * abs(g)) * g == pytest.approx(tau, rel=1e-12)


def test_mixing_length_and_damping():
    assert mixing_length(10.0) == pytest.approx(4.1)
    assert mixing_length(26.0, a_plus=26.0) == pytest.approx(0.41 * 26 * (1 - math.exp(-1)))
    assert eddy_viscosity(100.0, 0.5) == pytest.approx(41.0**2 * 0.5)


def test_closed_form_limits():
    # viscous sublayer: U+ = y+ + O(y+^3)
    assert exact_profile_no_damping(0.01) == pytest.approx(0.01, rel=1e-4)
    # log layer: the intercept tends to (ln(4 kappa) - 1) / kappa = -1.2324
    b = log_intercept_no_damping()
    assert b == pytest.approx(-1.232448, abs=1e-6)
    y = 1e6
    assert exact_profile_no_damping(y) - math.log(y) / KAPPA == pytest.approx(b, abs=1e-5)


def test_profile_matches_closed_form_with_second_order():
    errs = []
    for n in (250, 500, 1000, 2000):
        ys, u = profile(100.0, n)
        errs.append(abs(u[-1] - exact_profile_no_damping(100.0)))
    assert errs[-1] < 1e-5
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    for p in orders:
        assert abs(p - 2.0) < 0.2


def test_van_driest_log_law_constant():
    # with A+ = 26 and kappa = 0.41 the constant stress profile has B near 5.28
    b = log_intercept(1000.0, 40000, a_plus=26.0)
    assert 5.26 < b < 5.30
    ys, u = profile(1.0, 100, a_plus=26.0)
    assert u[-1] == pytest.approx(1.0, abs=1e-3)  # linear sublayer


def test_channel_profile_below_constant_stress():
    re_tau = 180.0
    _, u_const = profile(re_tau, 3600, a_plus=26.0)
    _, u_chan = profile(re_tau, 3600, a_plus=26.0, stress=channel_stress(re_tau))
    assert u_chan[-1] < u_const[-1]
    assert all(b >= a for a, b in zip(u_chan, u_chan[1:]))
    # the gradient is zero at the centerline, where the stress vanishes
    assert velocity_gradient(channel_stress(re_tau)(re_tau), 50.0) == 0.0


def test_bad_input():
    with pytest.raises(ValueError):
        profile(0.0, 10)
