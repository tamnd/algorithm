# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-boltzmann-inversion/. The authors are listed in prov/JKHDRS.jsonl.
import math
import random

import pytest

from iterative_boltzmann_inversion import dilute_g, iterative_boltzmann_inversion, virial_g_1d

DR = 0.05
M = 81
R = [k * DR for k in range(M)]


def soft(a, b, c=1.5, w=4.0):
    return [a * math.exp(-x * x) - b * math.exp(-w * (x - c) ** 2) for x in R]


def test_dilute_gas_is_solved_by_the_first_inversion():
    v_true = soft(2.0, 0.5)
    sim = dilute_g(1.0)
    v, errors = iterative_boltzmann_inversion(sim(v_true), sim, 1.0)
    assert errors == [0.0]
    assert max(abs(a - b) for a, b in zip(v, v_true)) < 1e-12


def test_one_update_step_by_hand():
    v_true = soft(2.0, 0.5)
    sim = virial_g_1d(1.0, 0.1, DR)
    g_star = sim(v_true)
    v1, errors = iterative_boltzmann_inversion(g_star, sim, 1.0, max_iter=1)
    v0 = [-math.log(g) for g in g_star]
    g0 = sim(v0)
    assert len(errors) == 1
    for k in range(M):
        assert v1[k] == pytest.approx(v0[k] + math.log(g0[k] / g_star[k]), abs=1e-14)
    assert v0[0] == pytest.approx(1.878199, abs=1e-6)
    assert v1[0] == pytest.approx(1.992859, abs=1e-6)


def test_virial_fluid_converges_geometrically_to_the_true_potential():
    v_true = soft(2.0, 0.5)
    sim = virial_g_1d(1.0, 0.1, DR)
    v, errors = iterative_boltzmann_inversion(sim(v_true), sim, 1.0, tol=1e-10)
    assert len(errors) == 17
    assert max(abs(a - b) for a, b in zip(v, v_true)) < 1e-9
    ratios = [errors[i + 1] / errors[i] for i in range(len(errors) - 1)]
    assert all(q < 0.35 for q in ratios)


def test_damping_slows_but_keeps_convergence():
    v_true = soft(2.0, 0.5)
    sim = virial_g_1d(1.0, 0.1, DR)
    g_star = sim(v_true)
    _, full = iterative_boltzmann_inversion(g_star, sim, 1.0, tol=1e-10)
    v, half = iterative_boltzmann_inversion(g_star, sim, 1.0, tol=1e-10, alpha=0.5, max_iter=200)
    assert len(half) > len(full)
    assert half[-1] < 1e-10
    assert max(abs(a - b) for a, b in zip(v, v_true)) < 1e-8


@pytest.mark.parametrize("seed", range(5))
def test_random_soft_potentials_are_recovered(seed):
    rng = random.Random(seed)
    kt = rng.uniform(0.8, 1.5)
    v_true = soft(rng.uniform(0.5, 3.0), rng.uniform(0.0, 0.8), rng.uniform(1.0, 2.0), rng.uniform(2.0, 6.0))
    sim = virial_g_1d(kt, rng.uniform(0.02, 0.1), DR)
    v, errors = iterative_boltzmann_inversion(sim(v_true), sim, kt, tol=1e-11)
    assert errors[-1] < 1e-11
    assert max(abs(a - b) for a, b in zip(v, v_true)) < 1e-8


def test_points_with_zero_target_are_not_updated():
    v_true = [50.0 if x < 0.5 else y for x, y in zip(R, soft(2.0, 0.5))]
    sim = dilute_g(1.0)
    g_star = sim(v_true)
    v, errors = iterative_boltzmann_inversion(g_star, sim, 1.0, tol=1e-6)
    for k in range(M):
        if R[k] < 0.5:
            assert v[k] == pytest.approx(-math.log(1e-8))
        else:
            assert v[k] == pytest.approx(v_true[k], abs=1e-12)
