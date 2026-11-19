# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-epsilon-model/. The authors are listed in prov/FJGR38.jsonl.

import math
import random

import pytest

from k_epsilon_model import (
    C_1,
    C_2,
    C_MU,
    SIGMA_EPS,
    decay_exponent,
    eddy_viscosity,
    exact_decay,
    log_layer_kappa,
    log_layer_state,
    rk4_decay,
)


def test_eddy_viscosity_example():
    assert eddy_viscosity(1.0, 10.0) == pytest.approx(0.009)
    with pytest.raises(ValueError):
        eddy_viscosity(1.0, 0.0)


def test_decay_exponent():
    assert decay_exponent() == pytest.approx(1.086957, abs=1e-6)
    assert decay_exponent(2.0) == pytest.approx(1.0)


def test_exact_decay_satisfies_the_odes():
    k0, e0 = 1.0, 1.0
    t, d = 0.7, 1e-6
    k, e = exact_decay(k0, e0, t)
    kp, ep = exact_decay(k0, e0, t + d)
    km, em = exact_decay(k0, e0, t - d)
    assert (kp - km) / (2 * d) == pytest.approx(-e, rel=1e-7)
    assert (ep - em) / (2 * d) == pytest.approx(-C_2 * e * e / k, rel=1e-7)
    # at t = t0 = n k0 / eps0 the energy has dropped by 2^(-n)
    n = decay_exponent()
    assert exact_decay(k0, e0, n)[0] == pytest.approx(2.0 ** (-n))
    assert exact_decay(k0, e0, n)[0] == pytest.approx(0.47076, abs=1e-5)


def test_rk4_matches_exact_for_random_starts():
    rng = random.Random(41)
    for _ in range(5):
        k0 = rng.uniform(0.1, 5.0)
        e0 = rng.uniform(0.1, 5.0)
        t = rng.uniform(1.0, 10.0)
        k, e = rk4_decay(k0, e0, t, 400)
        ke, ee = exact_decay(k0, e0, t)
        assert k == pytest.approx(ke, rel=1e-8)
        assert e == pytest.approx(ee, rel=1e-8)


def test_rk4_is_fourth_order():
    ke, _ = exact_decay(1.0, 1.0, 2.0)
    errs = [abs(rk4_decay(1.0, 1.0, 2.0, m)[0] - ke) for m in (40, 80, 160)]
    for a, b in zip(errs, errs[1:]):
        assert abs(math.log2(a / b) - 4.0) < 0.2


def test_late_time_slope_is_minus_n():
    t1, t2 = 1e3, 2e3
    k1, _ = rk4_decay(1.0, 1.0, t1, 4000)
    k2, _ = rk4_decay(1.0, 1.0, t2, 8000)
    slope = math.log(k2 / k1) / math.log(t2 / t1)
    assert slope == pytest.approx(-decay_exponent(), abs=2e-3)


def test_log_layer():
    assert log_layer_kappa() == pytest.approx(0.43267, abs=1e-5)
    # the eddy viscosity of the log layer is kappa u_tau y, as in the mixing length model
    k, eps, nut = log_layer_state(0.5, 0.01)
    assert k == pytest.approx(0.25 / 0.3)
    assert nut == pytest.approx(0.41 * 0.5 * 0.01)
    # production equals dissipation: nu_t (dU/dy)^2 with dU/dy = u_tau / (kappa y)
    dudy = 0.5 / (0.41 * 0.01)
    assert nut * dudy * dudy == pytest.approx(eps)
    # -<u'v'> / k = sqrt(C_mu)
    assert 0.25 / k == pytest.approx(math.sqrt(C_MU))
    assert SIGMA_EPS * math.sqrt(C_MU) * (C_2 - C_1) == pytest.approx(log_layer_kappa() ** 2)
