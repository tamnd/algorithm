# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plasma-particle-in-cell/. The authors are listed in prov/ZFSET4.jsonl.
import cmath
import math
import random

import pytest

from plasma_particle_in_cell import deposit, field_energy, gauss_field, interpolate, pic_run


def poisson_field_by_dft(rho, length):
    """Oracle: solve -(phi_{j+1} - 2 phi_j + phi_{j-1}) / dx^2 = rho_j - mean by a dense DFT, then E = -centred difference."""
    m = len(rho)
    dx = length / m
    rhat = [sum(rho[j] * cmath.exp(-2j * math.pi * j * k / m) for j in range(m)) for k in range(m)]
    phat = [0j] + [rhat[k] * dx * dx / (4 * math.sin(math.pi * k / m) ** 2) for k in range(1, m)]
    phi = [sum(phat[k] * cmath.exp(2j * math.pi * j * k / m) for k in range(m)).real / m for j in range(m)]
    return [-(phi[(j + 1) % m] - phi[j - 1]) / (2 * dx) for j in range(m)]


def test_page_example():
    assert deposit([0.5, 1.5, 2.5, 3.5], -1.0, 4, 4.0) == [0.0, 0.0, 0.0, 0.0]
    xs = [0.0, 1.5, 2.5, 3.5]
    rho = deposit(xs, -1.0, 4, 4.0)
    assert rho == [-0.5, 0.5, 0.0, 0.0]
    e = gauss_field(rho, 4.0)
    assert e == [-0.125, -0.125, 0.125, 0.125]
    assert interpolate(e, xs, 4.0) == [-0.125, 0.0, 0.125, 0.0]
    x, v, _ = pic_run(xs, [0.0] * 4, 4, 4.0, 0.5, 1)
    assert x == pytest.approx([0.015625, 1.5, 2.484375, 3.5], abs=1e-15)
    assert v == pytest.approx([0.03125, 0.0, -0.03125, 0.0], abs=1e-15)


def test_gauss_field_matches_poisson_oracle():
    rng = random.Random(1)
    for _ in range(40):
        m = rng.randint(1, 24)
        length = rng.uniform(0.5, 10)
        rho = [rng.uniform(-2, 2) for _ in range(m)]
        assert gauss_field(rho, length) == pytest.approx(poisson_field_by_dft(rho, length), abs=1e-9)


def test_neutral_plasma_has_zero_net_charge():
    rng = random.Random(2)
    for _ in range(50):
        m, length, n = rng.randint(2, 40), rng.uniform(1, 20), rng.randint(1, 300)
        xs = [rng.uniform(0, length) for _ in range(n)]
        rho = deposit(xs, -length / n, m, length)
        assert sum(rho) * length / m == pytest.approx(0, abs=1e-9)


def test_momentum_conserved_in_a_warm_plasma():
    rng = random.Random(3)
    length, m, n = 4 * math.pi, 32, 400
    xs = [rng.uniform(0, length) for _ in range(n)]
    vs = [rng.gauss(0, 1) for _ in range(n)]
    x, v, _ = pic_run(xs, vs, m, length, 0.1, 200)
    # the first half step changes the momentum by -(h/2) qm sum E_p = 0, so sum v is kept
    assert sum(v) == pytest.approx(sum(vs), abs=1e-10)


def test_cold_plasma_oscillates_at_the_plasma_frequency():
    length, n, m, h = 2 * math.pi, 256, 32, 0.05
    xs = [(i + 0.5) * length / n + 0.01 * math.cos((i + 0.5) * length / n) for i in range(n)]
    _, _, w = pic_run(xs, [0.0] * n, m, length, h, 400)
    # W(0) is close to the continuum field energy (1/2) delta^2 (L/2) of the displacement delta = 0.01
    assert w[0] == pytest.approx(0.5 * 0.01**2 * length / 2, rel=0.03)
    # the field energy oscillates at 2 omega_p = 2
    peaks = [i for i in range(1, len(w) - 1) if w[i] >= w[i - 1] and w[i] > w[i + 1]]
    period = (peaks[-1] - peaks[0]) * h / (len(peaks) - 1)
    assert math.pi / period == pytest.approx(1.0, abs=0.02)


def test_field_energy_formula():
    assert field_energy([1.0, -1.0, 2.0, 0.0], 2.0) == pytest.approx(0.5 * 6 * 0.5)
