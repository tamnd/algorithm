# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-monte-carlo/. The authors are listed in prov/CX3297.jsonl.
import math
import random

import pytest

from implicit_monte_carlo import equilibrium_temperature, expected_census, imc_step


def test_fleck_factor_by_hand():
    # T = 1, a = c = sigma = c_v = 1, dt = 0.25: beta = 4, f = 1 / (1 + 1) = 0.5.
    _, _, info = imc_step(1.0, [], 0.25, 10, random.Random(0))
    assert info["f"] == pytest.approx(0.5)
    assert info["emitted"] == pytest.approx(0.5 * 0.25)


def test_energy_is_conserved_exactly():
    rng = random.Random(1)
    temp, census = 0.1, [1.0 / 500] * 500
    total = temp + sum(census)
    for _ in range(20):
        temp, census, _ = imc_step(temp, census, 0.3, 500, rng, n_census=500)
        assert temp + sum(census) == pytest.approx(total, rel=1e-12)


@pytest.mark.parametrize("temp,e_r,dt", [(0.1, 1.0, 0.5), (0.8, 0.2, 0.2), (1.0, 1.0, 2.0)])
def test_one_step_mean(temp, e_r, dt):
    n = 6000
    census = [e_r / n] * n
    _, out, info = imc_step(temp, census, dt, n, random.Random(2))
    exact = expected_census(e_r, temp, dt)
    # Each particle reaches census or not, so the variance is at most sum(w^2) / 4.
    bound = 4.0 * math.sqrt(info["launched_w2"] / 4.0)
    assert abs(sum(out) - exact) < bound


def test_relaxes_to_equilibrium():
    rng = random.Random(3)
    temp, census = 0.1, [1.0 / 400] * 400
    t_eq = equilibrium_temperature(1.0 + 0.1)
    assert t_eq + t_eq ** 4 == pytest.approx(1.1)
    for _ in range(60):
        temp, census, _ = imc_step(temp, census, 0.2, 400, rng, n_census=400)
    assert temp == pytest.approx(t_eq, abs=0.03)
    assert sum(census) == pytest.approx(t_eq ** 4, abs=0.03)


def test_large_step_overshoots():
    # With dt = 100 the frozen Fleck factor lets the cold material absorb almost all
    # the radiation in one step: T jumps above the radiation temperature 1.
    temp, census = 0.1, [1.0 / 2000] * 2000
    expected_t = 0.1 + 1.0 - expected_census(1.0, 0.1, 100.0)
    new_t, _, _ = imc_step(temp, census, 100.0, 2000, random.Random(4))
    assert expected_t > 1.09
    assert new_t == pytest.approx(expected_t, abs=0.01)
    assert new_t > 1.0
