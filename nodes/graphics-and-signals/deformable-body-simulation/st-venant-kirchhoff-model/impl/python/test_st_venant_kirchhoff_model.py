# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/st-venant-kirchhoff-model/. The authors are listed in prov/H0C71P.jsonl.
"""Tests of the St. Venant-Kirchhoff model.

The stress is checked against the central difference gradient of the
energy density (also for inverted F), the element forces against the
gradient of the element energy, and the model against rotations of the
deformed and the rest shape. The bar formulas give the largest compressive
force at s = 1/sqrt(3), zero force at s = 0, and a force toward the
inverted state for -1 < s < 0.
"""

import math
import random

from anim import det, mul, num_grad, q_normalize, q_to_mat3, transpose
from st_venant_kirchhoff_model import (
    bar_stress,
    element_energy,
    element_forces,
    energy_density,
    lame,
    linearized_stress,
    pk1,
    pk2,
)

MU, LAM = lame(1.0, 0.3)


def rand_mat(rng, d, amount=0.6):
    return [[(1.0 if i == j else 0.0) + rng.uniform(-amount, amount) for j in range(d)] for i in range(d)]


def rotation(rng, d):
    if d == 2:
        t = rng.uniform(-math.pi, math.pi)
        return [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]
    q = q_normalize(tuple(rng.gauss(0.0, 1.0) for _ in range(4)))
    return q_to_mat3(q)


def flat(m):
    return [v for row in m for v in row]


def unflat(x, d):
    return [list(x[i * d:(i + 1) * d]) for i in range(d)]


def maxdiff(a, b):
    return max(abs(x - y) for x, y in zip(flat(a), flat(b)))


def test_lame_check_values():
    assert abs(MU - 0.384615) < 1e-6
    assert abs(LAM - 0.576923) < 1e-6


def test_pk1_is_energy_gradient():
    rng = random.Random(1)
    for d in (2, 3):
        for trial in range(20):
            f = rand_mat(rng, d)
            if trial % 4 == 0:
                f[0] = [-v for v in f[0]]
            g = num_grad(lambda x: energy_density(unflat(x, d), MU, LAM), flat(f))
            assert maxdiff(pk1(f, MU, LAM), unflat(g, d)) < 1e-6


def test_element_forces_are_minus_energy_gradient():
    rng = random.Random(2)
    for d in (2, 3):
        for _ in range(10):
            rest = [tuple(rng.uniform(-1, 1) for _ in range(d)) for _ in range(d + 1)]
            if d == 2:
                m = (rest[1][0] - rest[0][0]) * (rest[2][1] - rest[0][1]) - (rest[1][1] - rest[0][1]) * (rest[2][0] - rest[0][0])
            else:
                m = det([[rest[k + 1][i] - rest[0][i] for k in range(3)] for i in range(3)])
            if abs(m) < 0.05:
                continue
            if m < 0:
                rest[1], rest[2] = rest[2], rest[1]
            cur = [tuple(c + rng.uniform(-0.4, 0.4) for c in p) for p in rest]

            def w(x):
                pts = [tuple(x[k * d:(k + 1) * d]) for k in range(d + 1)]
                return element_energy(rest, pts, MU, LAM)

            g = num_grad(w, [c for p in cur for c in p])
            forces = [c for p in element_forces(rest, cur, MU, LAM) for c in p]
            assert max(abs(a + b) for a, b in zip(forces, g)) < 1e-6
            assert max(abs(sum(forces[i::d])) for i in range(d)) < 1e-12


def test_objective_and_isotropic():
    rng = random.Random(3)
    for d in (2, 3):
        for _ in range(20):
            f = rand_mat(rng, d)
            q = rotation(rng, d)
            psi = energy_density(f, MU, LAM)
            assert abs(energy_density(mul(q, f), MU, LAM) - psi) < 1e-12
            assert abs(energy_density(mul(f, q), MU, LAM) - psi) < 1e-12
            assert maxdiff(pk1(mul(q, f), MU, LAM), mul(q, pk1(f, MU, LAM))) < 1e-12


def test_rest_state_and_rotations_have_no_stress():
    rng = random.Random(4)
    for d in (2, 3):
        eye = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
        assert maxdiff(pk1(eye, MU, LAM), [[0.0] * d for _ in range(d)]) == 0.0
        q = rotation(rng, d)
        assert energy_density(q, MU, LAM) < 1e-24
        assert maxdiff(pk1(q, MU, LAM), [[0.0] * d for _ in range(d)]) < 1e-12


def test_pk2_symmetric_and_torque_free():
    rng = random.Random(5)
    for d in (2, 3):
        for _ in range(20):
            f = rand_mat(rng, d)
            s = pk2(f, MU, LAM)
            assert maxdiff(s, transpose(s)) < 1e-14
            pft = mul(pk1(f, MU, LAM), transpose(f))
            assert maxdiff(pft, transpose(pft)) < 1e-12


def test_linear_limit():
    rng = random.Random(6)
    h = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    lin = linearized_stress(h, MU, LAM)
    errs = []
    for eps in (1e-2, 5e-3):
        f = [[(1.0 if i == j else 0.0) + eps * h[i][j] for j in range(3)] for i in range(3)]
        p = pk1(f, MU, LAM)
        errs.append(max(abs(p[i][j] / eps - lin[i][j]) for i in range(3) for j in range(3)))
    assert errs[0] < 0.1
    assert 1.8 < errs[0] / errs[1] < 2.2


def test_bar_formulas():
    for s in (-1.5, -0.7, -0.2, 0.0, 0.3, 0.9, 1.0, 1.4):
        f = [[s, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        psi = (MU + 0.5 * LAM) * (s * s - 1.0) ** 2 / 4.0
        assert abs(energy_density(f, MU, LAM) - psi) < 1e-14
        p = pk1(f, MU, LAM)
        assert abs(p[0][0] - bar_stress(s, MU, LAM)) < 1e-14
        assert abs(p[1][1] - LAM * (s * s - 1.0) / 2.0) < 1e-14


def test_compression_force_peaks_then_reverses():
    n = 20000
    best_s, best_p = None, 0.0
    for k in range(1, n):
        s = k / n
        p = bar_stress(s, MU, LAM)
        assert p < 0.0
        if p < best_p:
            best_s, best_p = s, p
    assert abs(best_s - 1.0 / math.sqrt(3.0)) < 1e-4
    assert bar_stress(0.0, MU, LAM) == 0.0
    for k in range(1, 100):
        s = -k / 100.0
        assert bar_stress(s, MU, LAM) > 0.0
    inverted = [[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert energy_density(inverted, MU, LAM) == 0.0
    assert maxdiff(pk1(inverted, MU, LAM), [[0.0] * 3 for _ in range(3)]) == 0.0


def test_bar_energy_not_convex_near_flat():
    c = MU + 0.5 * LAM
    for s in (-0.5, 0.0, 0.5):
        h = 1e-4
        second = (bar_stress(s + h, MU, LAM) - bar_stress(s - h, MU, LAM)) / (2 * h)
        assert abs(second - c * (3 * s * s - 1.0)) < 1e-6
        assert second < 0.0
