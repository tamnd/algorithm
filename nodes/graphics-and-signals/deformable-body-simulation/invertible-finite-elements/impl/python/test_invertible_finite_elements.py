# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invertible-finite-elements/. The authors are listed in prov/8XGGPB.jsonl.
"""Tests of invertible finite elements on small 2D triangle meshes.

The signed SVD rebuilds F with rotations U and V and puts the negative entry
on the smallest singular value. The diagonal stress agrees with the usual
neo-Hookean stress for det F > 0, the forces are the negative gradient of
the energy (for inverted elements too with the corotated model), the stress
is rotation equivariant and C1 at the threshold, and inverted and flat
elements recover their rest shape.
"""

import math
import random

import pytest

import anim
from invertible_finite_elements import (Mesh, diagonal_stress, direct_neo_hookean_stress,
                                        invertible_forces, neo_hookean_diag, signed_area, signed_svd2,
                                        step, total_energy)

MU, LAM = 0.384615, 0.576923


def rand_f(rng, spread=1.5):
    return [[rng.uniform(-spread, spread) for _ in range(2)] for _ in range(2)]


def close(a, b, tol):
    return all(abs(a[i][j] - b[i][j]) <= tol for i in range(2) for j in range(2))


def stress(f, model, c=0.3):
    u, s, v = signed_svd2(f)
    ph = diagonal_stress(s, MU, LAM, model, c)
    return anim.mul(anim.mul(u, [[ph[0], 0.0], [0.0, ph[1]]]), anim.transpose(v))


def test_signed_svd():
    rng = random.Random(1)
    for _ in range(2000):
        f = rand_f(rng)
        u, s, v = signed_svd2(f)
        g = anim.mul(anim.mul(u, [[s[0], 0.0], [0.0, s[1]]]), anim.transpose(v))
        assert close(f, g, 1e-12)
        assert abs(anim.det(u) - 1.0) < 1e-12 and abs(anim.det(v) - 1.0) < 1e-12
        assert s[0] >= abs(s[1]) - 1e-12
        assert (s[1] < 0.0) == (anim.det(f) < 0.0)


def test_diagonal_stress_matches_direct_neo_hookean():
    rng = random.Random(2)
    for _ in range(300):
        r = anim.rot2(rng.uniform(-3, 3))
        q = anim.rot2(rng.uniform(-3, 3))
        f = anim.mul(anim.mul(r, [[rng.uniform(0.5, 2.0), 0.0], [0.0, rng.uniform(0.5, 2.0)]]), q)
        assert close(stress(f, "neo-hookean"), direct_neo_hookean_stress(f, MU, LAM), 1e-10)


def test_plain_neo_hookean_fails_when_inverted():
    with pytest.raises(ValueError):
        direct_neo_hookean_stress([[1.0, 0.0], [0.0, -0.5]], MU, LAM)


def flat(x):
    return [c for p in x for c in p]


def unflat(z):
    return [(z[2 * i], z[2 * i + 1]) for i in range(len(z) // 2)]


def check_gradient(mesh, x, model):
    f = invertible_forces(mesh, x, model, c=-1e9 if model == "corotated" else 0.3)
    g = anim.num_grad(lambda z: total_energy(mesh, unflat(z), model), flat(x))
    scale = max(abs(c) for c in g)
    for a, b in zip(flat(f), g):
        assert abs(a + b) <= 1e-6 * scale + 1e-9


def test_force_is_minus_gradient_corotated_with_inversion():
    rng = random.Random(3)
    mesh = Mesh([(0, 0), (1, 0), (0, 1), (1, 1)], [(0, 1, 3), (0, 3, 2)], MU, LAM)
    inverted = 0
    for _ in range(30):
        x = [(p[0] + rng.uniform(-0.8, 0.8), p[1] + rng.uniform(-0.8, 0.8)) for p in mesh.rest]
        inverted += any(signed_area(x, t) < 0 for t in mesh.tris)
        check_gradient(mesh, x, "corotated")
    assert inverted > 5


def test_force_is_minus_gradient_neo_hookean():
    rng = random.Random(4)
    mesh = Mesh([(0, 0), (1, 0), (0, 1), (1, 1)], [(0, 1, 3), (0, 3, 2)], MU, LAM)
    done = 0
    while done < 20:
        x = [(p[0] + rng.uniform(-0.2, 0.2), p[1] + rng.uniform(-0.2, 0.2)) for p in mesh.rest]
        sv = [signed_svd2(anim.mul([[x[t[1]][0] - x[t[0]][0], x[t[2]][0] - x[t[0]][0]],
                                    [x[t[1]][1] - x[t[0]][1], x[t[2]][1] - x[t[0]][1]]], mesh.dm_inv[e]))[1]
              for e, t in enumerate(mesh.tris)]
        if min(min(s) for s in sv) < 0.35:
            continue
        check_gradient(mesh, x, "neo-hookean")
        done += 1


def test_rotation_equivariance_including_inverted():
    rng = random.Random(5)
    for _ in range(300):
        f = rand_f(rng)
        r = anim.rot2(rng.uniform(-3, 3))
        q = anim.rot2(rng.uniform(-3, 3))
        for model in ("neo-hookean", "corotated"):
            p = stress(f, model)
            assert close(stress(anim.mul(r, f), model), anim.mul(r, p), 1e-9 * (1 + max(map(abs, flat(p)))))
            assert close(stress(anim.mul(f, q), model), anim.mul(p, q), 1e-9 * (1 + max(map(abs, flat(p)))))


def test_zero_stress_at_rest_and_rotation():
    for theta in (0.0, 1.0, 3.0):
        for model in ("neo-hookean", "corotated"):
            assert close(stress(anim.rot2(theta), model), [[0, 0], [0, 0]], 1e-12)


def test_extrapolation_is_c1_at_threshold():
    c, h = 0.3, 1e-7
    for s1 in (0.5, 1.0, 2.0):
        below = diagonal_stress((s1, c - h), MU, LAM, "neo-hookean", c)
        above = diagonal_stress((s1, c + h), MU, LAM, "neo-hookean", c)
        assert max(abs(a - b) for a, b in zip(below, above)) < 1e-5
        _, jac = neo_hookean_diag((s1, c), MU, LAM)
        d_below = [(diagonal_stress((s1, c - h), MU, LAM, "neo-hookean", c)[i]
                    - diagonal_stress((s1, c - 2 * h), MU, LAM, "neo-hookean", c)[i]) / h for i in range(2)]
        assert abs(d_below[1] - jac[1][1]) < 1e-4 * abs(jac[1][1])
        assert abs(d_below[0] - jac[0][1]) < 1e-4 * max(1.0, abs(jac[0][1]))


def run_recovery(mesh, x, model, fixed, steps=3000, dt=0.01):
    v = [(0.0, 0.0)] * len(x)
    for _ in range(steps):
        x, v = step(mesh, x, v, dt, model=model, c=0.3, fixed=fixed, damping=2.0)
    return x


@pytest.mark.parametrize("model", ["neo-hookean", "corotated"])
def test_inverted_triangle_recovers(model):
    mesh = Mesh([(0, 0), (1, 0), (0, 1)], [(0, 1, 2)], MU, LAM)
    x = [(0.0, 0.0), (1.0, 0.0), (0.3, -0.5)]
    assert signed_area(x, mesh.tris[0]) < 0
    x = run_recovery(mesh, x, model, fixed=[0, 1])
    assert abs(x[2][0]) < 1e-3 and abs(x[2][1] - 1.0) < 1e-3


@pytest.mark.parametrize("model", ["neo-hookean", "corotated"])
def test_flat_triangle_recovers(model):
    mesh = Mesh([(0, 0), (1, 0), (0, 1)], [(0, 1, 2)], MU, LAM)
    x = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.0)]
    f = invertible_forces(mesh, x, model)
    assert all(math.isfinite(c) for p in f for c in p)
    assert f[2][1] > 0.0
    x = run_recovery(mesh, x, model, fixed=[0, 1])
    assert abs(x[2][0]) < 1e-3 and abs(x[2][1] - 1.0) < 1e-3


def test_crushed_mesh_recovers():
    rest = [(i * 0.5, j * 0.5) for j in range(3) for i in range(3)]
    tris = []
    for j in range(2):
        for i in range(2):
            a = 3 * j + i
            tris += [(a, a + 1, a + 4), (a, a + 4, a + 3)]
    mesh = Mesh(rest, tris, MU, LAM)
    x = list(rest)
    x[4] = (1.2, 0.1)
    x[7] = (0.5, -0.3)
    assert sum(signed_area(x, t) < 0 for t in tris) >= 3
    fixed = [0, 1, 2, 3, 5, 6, 8]
    x = run_recovery(mesh, x, "neo-hookean", fixed, steps=3000, dt=0.005)
    for i in (4, 7):
        assert math.dist(x[i], rest[i]) < 1e-3
    assert all(signed_area(x, t) > 0 for t in tris)
