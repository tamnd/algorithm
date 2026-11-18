# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neo-hookean-model/. The authors are listed in prov/DY1W7J.jsonl.
"""Tests of the compressible neo-Hookean model.

The stress is checked against the central difference gradient of the
energy density, the element forces against the gradient of the element
energy, and the model against rotations of the deformed and the rest shape.
The linear limit gives the Lame parameters with no remap. The energy and
the restoring stress grow without bound as J goes to 0, and F with J <= 0
is rejected.
"""

import math
import random

import pytest

from anim import det, mul, num_grad, q_normalize, q_to_mat3, transpose
from neo_hookean_model import (
    bar_energy,
    bar_stress,
    element_energy,
    element_forces,
    energy_density,
    lame,
    pk1,
)

MU, LAM = lame(1.0, 0.3)


def rand_mat(rng, d, amount=0.5):
    while True:
        m = [[(1.0 if i == j else 0.0) + rng.uniform(-amount, amount) for j in range(d)] for i in range(d)]
        if det(m) > 0.1:
            return m


def rotation(rng, d):
    if d == 2:
        t = rng.uniform(-math.pi, math.pi)
        return [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]
    return q_to_mat3(q_normalize(tuple(rng.gauss(0.0, 1.0) for _ in range(4))))


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
        for _ in range(20):
            f = rand_mat(rng, d)
            g = num_grad(lambda x: energy_density(unflat(x, d), MU, LAM), flat(f))
            assert maxdiff(pk1(f, MU, LAM), unflat(g, d)) < 1e-6


def test_element_forces_are_minus_energy_gradient():
    rng = random.Random(2)
    for d in (2, 3):
        rest = [tuple(1.0 if i == k - 1 else 0.0 for i in range(d)) for k in range(d + 1)]
        for _ in range(10):
            cur = [tuple(c + rng.uniform(-0.15, 0.15) for c in p) for p in rest]

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
            pft = mul(pk1(f, MU, LAM), transpose(f))
            assert maxdiff(pft, transpose(pft)) < 1e-12


def test_rest_state_and_rotations():
    rng = random.Random(4)
    for d in (2, 3):
        eye = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
        assert energy_density(eye, MU, LAM) == 0.0
        assert maxdiff(pk1(eye, MU, LAM), [[0.0] * d for _ in range(d)]) == 0.0
        q = rotation(rng, d)
        assert abs(energy_density(q, MU, LAM)) < 1e-12
        assert maxdiff(pk1(q, MU, LAM), [[0.0] * d for _ in range(d)]) < 1e-12


def test_linear_limit_has_lame_parameters():
    rng = random.Random(5)
    h = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    tr = h[0][0] + h[1][1] + h[2][2]
    lin = [[MU * (h[i][j] + h[j][i]) + (LAM * tr if i == j else 0.0) for j in range(3)] for i in range(3)]
    errs = []
    for eps in (1e-2, 5e-3):
        f = [[(1.0 if i == j else 0.0) + eps * h[i][j] for j in range(3)] for i in range(3)]
        p = pk1(f, MU, LAM)
        errs.append(max(abs(p[i][j] / eps - lin[i][j]) for i in range(3) for j in range(3)))
    assert errs[0] < 0.1
    assert 1.8 < errs[0] / errs[1] < 2.2


def test_bar_formulas():
    for s in (0.05, 0.3, 0.8, 1.0, 1.4, 3.0):
        f = [[s, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        assert abs(energy_density(f, MU, LAM) - bar_energy(s, MU, LAM)) < 1e-12
        p = pk1(f, MU, LAM)
        assert abs(p[0][0] - bar_stress(s, MU, LAM)) < 1e-12
        assert abs(p[1][1] - LAM * math.log(s)) < 1e-12


def test_barrier_under_compression():
    prev_e, prev_p = 0.0, 0.0
    for k in range(1, 60):
        s = 0.8 ** k
        e = bar_energy(s, MU, LAM)
        p = bar_stress(s, MU, LAM)
        assert e > prev_e
        assert p < prev_p < 0.0 or (k == 1 and p < 0.0)
        prev_e, prev_p = e, p
    assert prev_e > 50.0
    assert prev_p < -1e5
    assert bar_energy(1e-100, MU, LAM) > 1.5e4


def test_rejects_flat_and_inverted():
    for f in ([[1.0, 0.0], [0.0, 0.0]], [[-1.0, 0.0], [0.0, 1.0]], [[1, 0, 0], [0, 1, 0], [0, 0, -0.5]]):
        with pytest.raises(ValueError):
            energy_density(f, MU, LAM)
        with pytest.raises(ValueError):
            pk1(f, MU, LAM)


def test_form_without_log_term_is_not_at_rest():
    def psi(x):
        f = unflat(x, 3)
        return 0.5 * MU * (sum(v * v for v in x) - 3.0) + 0.5 * LAM * (det(f) - 1.0) ** 2

    g = num_grad(psi, [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    expected = [MU, 0.0, 0.0, 0.0, MU, 0.0, 0.0, 0.0, MU]
    assert max(abs(a - b) for a, b in zip(g, expected)) < 1e-8


def test_volume_term_convex_only_up_to_e():
    for j in (0.2, 1.0, 2.0, math.e - 0.01, math.e + 0.01, 5.0):
        h = 1e-4
        g = lambda x: math.log(x) ** 2
        second = (g(j + h) - 2 * g(j) + g(j - h)) / (h * h)
        assert abs(second - 2.0 * (1.0 - math.log(j)) / (j * j)) < 1e-4
        assert (second > 0.0) == (j < math.e)
