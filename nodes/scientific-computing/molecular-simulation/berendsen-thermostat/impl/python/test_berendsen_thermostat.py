# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berendsen-thermostat/. The authors are listed in prov/VZN3KE.jsonl.
import math

import pytest

from berendsen_thermostat import berendsen_thermostat, free, harmonic, kinetic


def test_free_particles_relax_geometrically_to_the_target():
    # With no forces, K_(n+1) = lambda^2 K_n = K_n + (h / tau)(K0 - K_n),
    # so K_n - K0 = (K_init - K0)(1 - h / tau)^n exactly.
    n, h, tau = 4, 0.1, 1.0
    x = [[0.0] for _ in range(n)]
    v = [[2.0] for _ in range(n)]
    _, _, ks = berendsen_thermostat(x, v, [1.0] * n, free(), h, 40, 1.0, tau, n)
    k0, k_init = 2.0, 8.0
    for step, k in enumerate(ks, start=1):
        assert k == pytest.approx(k0 + (k_init - k0) * (1 - h / tau) ** step, rel=1e-12)
    assert ks[:3] == pytest.approx([7.4, 6.86, 6.374], rel=1e-12)


def test_tau_equal_to_h_sets_the_target_in_one_step():
    v = [[3.0, -1.0], [0.5, 2.0]]
    _, v1, ks = berendsen_thermostat([[0.0, 0.0]] * 2, v, [1.0, 2.0], free(), 0.1, 1, 1.5, 0.1, 4)
    assert ks[0] == pytest.approx(3.0, rel=1e-12)
    assert kinetic(v1, [1.0, 2.0]) == pytest.approx(3.0, rel=1e-12)


def test_mean_is_right_but_kinetic_energy_fluctuations_are_suppressed():
    # 20 oscillators in 1D, N_f = 20, kT = 1. In the canonical ensemble K has
    # mean 10 and variance 10. The weak coupling keeps the mean near 10 and
    # removes almost all of the fluctuation.
    n = 20
    x = [[1.0 + 0.05 * i] for i in range(n)]
    v = [[0.0] for _ in range(n)]
    _, _, ks = berendsen_thermostat(x, v, [1.0] * n, harmonic(1.0), 0.05, 3000, 1.0, 0.5, n)
    tail = ks[1000:]
    mean = sum(tail) / len(tail)
    var = sum((k - mean) ** 2 for k in tail) / len(tail)
    assert abs(mean - 10.0) < 0.1
    assert var < 1.0  # canonical value 10


def test_weak_coupling_limit_is_velocity_verlet():
    # tau much larger than the run: lambda is 1 to within h / tau.
    x, v, _ = berendsen_thermostat([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 200, 1.0, 1e12, 1)
    assert 0.5 * v[0][0] ** 2 + 0.5 * x[0][0] ** 2 == pytest.approx(0.5, abs=1e-3)
    assert x[0][0] == pytest.approx(math.cos(10.0), abs=0.01)


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        berendsen_thermostat([[0.0]], [[1.0]], [1.0], free(), 0.1, 1, 1.0, 0.05, 1)
