# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entropy-stable-scheme/. The authors are listed in prov/0A1T0M.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from entropy_stable_scheme import (
    central_flux, ec_flux, entropy, entropy_rate, es_flux, residual, solve, total_entropy,
)


def rand_fr(rng):
    return Fr(rng.randint(-40, 40), rng.randint(1, 12))


def test_tadmor_condition_holds_exactly():
    rng = random.Random(1)
    for _ in range(200):
        ul, ur = rand_fr(rng), rand_fr(rng)
        _, vl, pl = entropy(ul)
        _, vr, pr = entropy(ur)
        assert (vr - vl) * ec_flux(ul, ur) == pr - pl


def test_ec_flux_is_tadmors_path_integral():
    # F* = integral over theta in [0, 1] of f(u(v_L + theta (v_R - v_L))); Simpson is exact here.
    rng = random.Random(2)
    f = lambda u: u * u / 2
    for _ in range(50):
        ul, ur = rand_fr(rng), rand_fr(rng)
        mid = (ul + ur) / 2
        simpson = (f(ul) + 4 * f(mid) + f(ur)) / 6
        assert ec_flux(ul, ur) == simpson


def test_fluxes_are_consistent():
    for u in (Fr(-3, 2), Fr(0), Fr(7, 5)):
        assert ec_flux(u, u) == u * u / 2
        assert es_flux(u, u) == u * u / 2


def test_hand_example():
    assert ec_flux(Fr(1), Fr(0)) == Fr(1, 6)
    assert es_flux(Fr(1), Fr(0)) == Fr(2, 3)


def test_semi_discrete_entropy_rate_is_exactly_zero_for_the_ec_flux():
    rng = random.Random(3)
    for M in (2, 5, 17):
        u = [rand_fr(rng) for _ in range(M)]
        assert entropy_rate(u, Fr(1, M), ec_flux) == 0
        assert sum(residual(u, Fr(1, M), ec_flux)) == 0          # conservation


def test_semi_discrete_entropy_rate_of_the_es_flux_is_the_dissipation():
    rng = random.Random(4)
    for M in (3, 8, 20):
        u = [rand_fr(rng) for _ in range(M)]
        dx = Fr(1, M)
        diss = -sum(max(abs(u[j]), abs(u[(j + 1) % M])) * (u[(j + 1) % M] - u[j]) ** 2
                    for j in range(M)) / 2
        rate = entropy_rate(u, dx, es_flux)
        assert rate == diss
        assert rate <= 0


def test_central_flux_is_not_entropy_conservative():
    u = [Fr(1), Fr(0), Fr(-1), Fr(2)]
    assert entropy_rate(u, Fr(1, 4), central_flux) != 0


def test_fully_discrete_ec_entropy_drift_is_small_and_shrinks_with_dt():
    M = 64
    dx = 1.0 / M
    u0 = [0.5 + 0.25 * math.sin(2 * math.pi * (j + 0.5) * dx) for j in range(M)]
    s0 = total_entropy(u0, dx)
    drift = []
    for c in (0.4, 0.2):
        u = solve(list(u0), dx, c * dx, 0.2, ec_flux)
        drift.append(abs(total_entropy(u, dx) - s0))
    assert drift[0] < 1e-6 and drift[1] < drift[0] / 4


def test_es_scheme_captures_a_shock_without_new_extrema_but_ec_oscillates():
    M = 100
    dx = 1.0 / M
    u0 = [math.sin(2 * math.pi * (j + 0.5) * dx) for j in range(M)]
    es = solve(list(u0), dx, 0.2 * dx, 0.3, es_flux)
    ec = solve(list(u0), dx, 0.2 * dx, 0.3, ec_flux)
    assert max(abs(x) for x in es) <= 1.0
    assert total_entropy(es, dx) < total_entropy(u0, dx) - 0.05
    assert max(abs(x) for x in ec) > 1.5
    assert abs(total_entropy(ec, dx) - total_entropy(u0, dx)) < 1e-4


def test_rejects_bad_steps():
    with pytest.raises(ValueError):
        solve([0.0, 1.0], 0.5, 0.0, 1.0, es_flux)
