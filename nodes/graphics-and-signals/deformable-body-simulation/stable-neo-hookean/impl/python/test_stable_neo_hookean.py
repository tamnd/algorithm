# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stable-neo-hookean/. The authors are listed in prov/F0PH35.jsonl.
"""Tests of the stable neo-Hookean energy.

The stress is checked against the central difference gradient of the
energy for valid, flat and inverted F, and the element forces against the
gradient of the element energy for inverted tetrahedra. The model is
checked against rotations, the rest state needs the right alpha, and the
remapped parameters give the target Lame parameters in the linear limit.
The bar force pushes every compressed or inverted state toward J = 1.
"""

import math
import random

from anim import det, inv, mul, num_grad, q_normalize, q_to_mat3, transpose
from stable_neo_hookean import (
    bar_stress,
    cofactor,
    effective_poisson,
    element_energy,
    element_forces,
    energy_density,
    lame,
    pk1,
    remap,
    rest_alpha,
)

MU0, LAM0 = lame(1.0, 0.3)
MU, LAM = remap(MU0, LAM0)
EYE = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def rand_mat(rng, amount=0.8):
    return [[(1.0 if i == j else 0.0) + rng.uniform(-amount, amount) for j in range(3)] for i in range(3)]


def rotation(rng):
    return q_to_mat3(q_normalize(tuple(rng.gauss(0.0, 1.0) for _ in range(4))))


def flat(m):
    return [v for row in m for v in row]


def unflat(x):
    return [list(x[i * 3:(i + 1) * 3]) for i in range(3)]


def maxdiff(a, b):
    return max(abs(x - y) for x, y in zip(flat(a), flat(b)))


def test_lame_and_remap_values():
    assert abs(MU0 - 0.384615) < 1e-6
    assert abs(LAM0 - 0.576923) < 1e-6
    assert abs(MU - 0.512821) < 1e-6
    assert abs(LAM - 0.897436) < 1e-6
    assert abs(rest_alpha(MU, LAM) - (1.0 + MU / LAM - MU / (4.0 * LAM))) < 1e-15


def test_cofactor_is_det_times_inverse_transpose():
    rng = random.Random(1)
    for _ in range(20):
        f = rand_mat(rng)
        j = det(f)
        fit = transpose(inv(f))
        assert maxdiff(cofactor(f), [[j * v for v in row] for row in fit]) < 1e-12


def test_pk1_is_energy_gradient_also_when_inverted():
    rng = random.Random(2)
    signs = {True: 0, False: 0}
    for trial in range(40):
        f = rand_mat(rng)
        if trial % 2:
            f[0] = [-v for v in f[0]]
        if trial == 7:
            f[2] = [f[0][k] + f[1][k] for k in range(3)]
        signs[det(f) > 0] += 1
        g = num_grad(lambda x: energy_density(unflat(x), MU, LAM), flat(f))
        assert maxdiff(pk1(f, MU, LAM), unflat(g)) < 1e-6
    assert signs[True] > 5 and signs[False] > 5


def test_element_forces_for_inverted_tetrahedra():
    rng = random.Random(3)
    rest = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    for k in range(10):
        cur = [tuple(c + rng.uniform(-0.2, 0.2) for c in p) for p in rest]
        if k % 2:
            cur[3] = (cur[3][0], cur[3][1], -cur[3][2])

        def w(x):
            return element_energy(rest, [tuple(x[i * 3:(i + 1) * 3]) for i in range(4)], MU, LAM)

        g = num_grad(w, [c for p in cur for c in p])
        forces = [c for p in element_forces(rest, cur, MU, LAM) for c in p]
        assert max(abs(a + b) for a, b in zip(forces, g)) < 1e-6
        assert max(abs(sum(forces[i::3])) for i in range(3)) < 1e-12


def test_objective_and_isotropic():
    rng = random.Random(4)
    for _ in range(20):
        f = rand_mat(rng)
        q = rotation(rng)
        psi = energy_density(f, MU, LAM)
        assert abs(energy_density(mul(q, f), MU, LAM) - psi) < 1e-12
        assert abs(energy_density(mul(f, q), MU, LAM) - psi) < 1e-12
        assert maxdiff(pk1(mul(q, f), MU, LAM), mul(q, pk1(f, MU, LAM))) < 1e-12
        pft = mul(pk1(f, MU, LAM), transpose(f))
        assert maxdiff(pft, transpose(pft)) < 1e-12


def test_rest_needs_the_right_alpha():
    assert maxdiff(pk1(EYE, MU, LAM), [[0.0] * 3 for _ in range(3)]) < 1e-15
    p_one = pk1(EYE, MU, LAM, alpha=1.0)
    assert maxdiff(p_one, [[0.75 * MU if i == j else 0.0 for j in range(3)] for i in range(3)]) < 1e-15
    p_nolog = 1.0 + MU / LAM
    p = pk1(EYE, MU, LAM, alpha=p_nolog)
    assert maxdiff(p, [[-0.25 * MU if i == j else 0.0 for j in range(3)] for i in range(3)]) < 1e-15
    rng = random.Random(5)
    for _ in range(5):
        q = rotation(rng)
        assert maxdiff(pk1(q, MU, LAM), [[0.0] * 3 for _ in range(3)]) < 1e-12


def test_remap_gives_target_linear_limit():
    rng = random.Random(6)
    h = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    tr = h[0][0] + h[1][1] + h[2][2]
    lin = [[MU0 * (h[i][j] + h[j][i]) + (LAM0 * tr if i == j else 0.0) for j in range(3)] for i in range(3)]
    errs = []
    for eps in (1e-2, 5e-3):
        f = [[(1.0 if i == j else 0.0) + eps * h[i][j] for j in range(3)] for i in range(3)]
        p = pk1(f, MU, LAM)
        errs.append(max(abs(p[i][j] / eps - lin[i][j]) for i in range(3) for j in range(3)))
    assert errs[0] < 0.1
    assert 1.8 < errs[0] / errs[1] < 2.2
    assert abs(effective_poisson(MU, LAM) - 0.3) < 1e-12
    assert abs(effective_poisson(MU0, LAM0) - 0.269231) < 1e-6


def test_bar_force_points_to_rest():
    for k in range(-300, 301):
        s = k / 100.0
        f = [[s, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        p = pk1(f, MU, LAM)[0][0]
        assert abs(p - bar_stress(s, MU, LAM)) < 1e-12
        if s < 1.0:
            assert p < 0.0
        elif s > 1.0:
            assert p > 0.0
        else:
            assert abs(p) < 1e-15


def test_finite_energy_at_flat_and_inverted_states():
    assert math.isfinite(energy_density([[0.0] * 3 for _ in range(3)], MU, LAM))
    flat_f = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
    inv_f = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]]
    e_flat = energy_density(flat_f, MU, LAM)
    e_inv = energy_density(inv_f, MU, LAM)
    assert 0.0 < e_flat < e_inv
    p = pk1(flat_f, MU, LAM)
    assert p[2][2] < 0.0


def test_collapsed_point_is_a_saddle():
    zero = [[0.0] * 3 for _ in range(3)]
    assert maxdiff(pk1(zero, MU, LAM), zero) == 0.0
    e0 = energy_density(zero, MU, LAM)
    rng = random.Random(7)
    for _ in range(10):
        g = rand_mat(rng)
        eps = 1e-2
        diff = energy_density([[eps * v for v in row] for row in g], MU, LAM) - e0
        cubic = -LAM * rest_alpha(MU, LAM) * eps ** 3 * det(g)
        assert abs(diff - cubic) < 0.05 * abs(cubic) + 1e-8
