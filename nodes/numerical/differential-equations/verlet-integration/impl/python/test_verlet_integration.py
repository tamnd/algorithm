# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verlet-integration/. The authors are listed in prov/S32WCK.jsonl.

import math
from fractions import Fraction as F

import pytest

from verlet_integration import (oscillator_matrix, step_count, stormer_positions,
                                velocity_verlet, verlet_step)

osc = lambda q: -q


def kepler(q):
    r3 = (q[0] ** 2 + q[1] ** 2) ** 1.5
    return [-q[0] / r3, -q[1] / r3]


def kepler_start(e=0.5):
    return [1 - e, 0.0], [0.0, math.sqrt((1 + e) / (1 - e))]


def H_kepler(q, v):
    return (v[0] ** 2 + v[1] ** 2) / 2 - 1 / math.hypot(q[0], q[1])


def test_exact_trace_in_fractions():
    r = velocity_verlet(osc, 0, F(1), F(0), F(1), F(1, 2), keep_path=True)
    assert [(q, v) for _, q, v in r.path] == [(1, 0), (F(7, 8), F(-15, 32)), (F(17, 32), F(-105, 128))]
    assert r.steps == 2 and r.force_evals == 3


def test_second_order():
    errs = []
    for h in (0.1, 0.05, 0.025, 0.0125):
        r = velocity_verlet(osc, 0.0, 1.0, 0.0, 10.0, h)
        errs.append(max(abs(r.q - math.cos(10)), abs(r.v + math.sin(10))))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(1.95 < p < 2.05 for p in orders)


def test_modified_energy_exactly_conserved_and_det_one():
    h = F(1, 3)
    M = oscillator_matrix(h, F(1))
    assert M[0][0] * M[1][1] - M[0][1] * M[1][0] == 1  # area preserving = symplectic in 1D
    q, v = F(1), F(0)
    for _ in range(20):
        assert v * v + (1 - h * h / 4) * q * q == F(35, 36)
        q, v, _ = verlet_step(osc, q, v, -q, h)


def test_stability_limit_h_omega_two():
    small = velocity_verlet(osc, 0.0, 1.0, 0.0, 1990.0, 1.99)
    assert abs(small.q) <= 1.0 + 1e-9 and small.steps == 1000
    big = velocity_verlet(osc, 0.0, 1.0, 0.0, 2010.0, 2.01)
    assert abs(big.q) > 1e80


def test_time_reversible():
    q0, v0 = kepler_start()
    a0 = kepler(q0)
    q, v, a = q0, v0, a0
    for _ in range(50):
        q, v, a = verlet_step(kepler, q, v, a, 0.05)
    for _ in range(50):
        q, v, a = verlet_step(kepler, q, v, a, -0.05)
    assert max(abs(x - y) for x, y in zip(q + v, q0 + v0)) < 1e-12


def test_symplectic_jacobian_kepler():
    q0, v0 = kepler_start()
    x0 = q0 + v0

    def phi(x):
        q, v = x[:2], x[2:]
        a = kepler(q)
        for _ in range(10):
            q, v, a = verlet_step(kepler, q, v, a, 0.1)
        return q + v

    eps = 1e-6
    J = [[0.0] * 4 for _ in range(4)]
    for k in range(4):
        xp = list(x0); xm = list(x0)
        xp[k] += eps; xm[k] -= eps
        fp, fm = phi(xp), phi(xm)
        for i in range(4):
            J[i][k] = (fp[i] - fm[i]) / (2 * eps)
    Om = [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]]
    JtOJ = [[sum(J[a][i] * Om[a][b] * J[b][j] for a in range(4) for b in range(4)) for j in range(4)]
            for i in range(4)]
    assert max(abs(JtOJ[i][j] - Om[i][j]) for i in range(4) for j in range(4)) < 1e-6


def test_kepler_energy_bounded_and_angular_momentum():
    q0, v0 = kepler_start()
    T = 2 * math.pi
    r = velocity_verlet(kepler, 0.0, q0, v0, 50 * T, T / 200, keep_path=True)
    errs = [abs(H_kepler(q, v) - H_kepler(q0, v0)) for _, q, v in r.path]
    assert max(errs) < 2e-3
    assert max(errs) < 1.01 * max(errs[: len(errs) // 10])  # no drift after the first 5 orbits
    L0 = q0[0] * v0[1] - q0[1] * v0[0]
    assert max(abs(q[0] * v[1] - q[1] * v[0] - L0) for _, q, v in r.path) < 1e-12


def test_stormer_two_step_form_gives_same_positions():
    q0, v0 = kepler_start()
    qs = stormer_positions(kepler, q0, v0, 0.01, 300)
    r = velocity_verlet(kepler, 0.0, q0, v0, 3.0, 0.01, keep_path=True)
    assert max(abs(a - b) for x, (_, y, _) in zip(qs, r.path) for a, b in zip(x, y)) < 1e-10
    assert stormer_positions(osc, 1.0, 0.0, 0.1, 0) == [1.0]


def test_edge_cases():
    r = velocity_verlet(osc, 0.0, 1.0, 0.0, 0.0, 0.1)
    assert r.steps == 0 and r.q == 1.0 and r.force_evals == 1
    r = velocity_verlet(osc, 0.0, 1.0, 0.0, 0.3, 5.0)  # h beyond the interval: one step of 0.3
    assert r.steps == 1 and r.t == 0.3 and abs(r.q - (1 - 0.3 ** 2 / 2)) < 1e-15
    r = velocity_verlet(osc, 0.0, 1.0, 0.0, 1.05, 0.1)  # last step off the grid, 0.05 long
    assert r.steps == 11 and r.t == 1.05 and abs(r.q - math.cos(1.05)) < 1e-3
    assert step_count(0.0, 1.0, 0.1) == 10
    with pytest.raises(ValueError):
        velocity_verlet(osc, 0.0, 1.0, 0.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        velocity_verlet(osc, 1.0, 1.0, 0.0, 0.0, 0.1)
