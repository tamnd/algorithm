# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/corotational-fem/. The authors are listed in prov/NYXCZF.jsonl.
"""Tests of corotational FEM on small 2D triangle meshes.

The force is checked against central differences of the corotated energy,
it vanishes at the rest shape and after a rigid motion, it has zero net force
and zero net torque, and the warped stiffness equals the true Hessian only at
a rotated rest shape. Plain linear FEM gives ghost forces under rotation.
A free spinning body keeps its momentum and angular momentum under
symplectic Euler, and a cantilever under gravity settles to an equilibrium
with the implicit step.
"""

import math
import random

import anim
from corotational_fem import (Mesh, corotated_energy, corotated_energy_density, corotational_forces,
                              grid_mesh, lame, linear_forces, rotate_points, step_explicit, step_implicit,
                              warped_stiffness)

MU, LAM = lame(1000.0, 0.3)


def flat(x):
    return [c for p in x for c in p]


def unflat(z):
    return [(z[2 * i], z[2 * i + 1]) for i in range(len(z) // 2)]


def perturbed(rest, rng, amount):
    return [(p[0] + rng.uniform(-amount, amount), p[1] + rng.uniform(-amount, amount)) for p in rest]


def small_mesh():
    rest, tris = grid_mesh(2, 1, 1.0, 0.5)
    return Mesh(rest, tris, MU, LAM)


def test_lame_check_values():
    mu, lam = lame(1.0, 0.3)
    assert abs(mu - 0.384615) < 1e-6
    assert abs(lam - 0.576923) < 1e-6


def test_force_is_minus_gradient_of_corotated_energy():
    rng = random.Random(11)
    mesh = small_mesh()
    for _ in range(5):
        x = rotate_points(perturbed(mesh.rest, rng, 0.15), rng.uniform(-3.0, 3.0))
        f, _ = corotational_forces(mesh, x)
        g = anim.num_grad(lambda z: corotated_energy(mesh, unflat(z)), flat(x))
        scale = max(abs(c) for c in g)
        for a, b in zip(flat(f), g):
            assert abs(a + b) <= 1e-6 * scale + 1e-9


def test_zero_force_at_rest_and_after_rigid_motion():
    mesh = small_mesh()
    for theta in (0.0, 0.7, 2.5, -3.0):
        x = rotate_points(mesh.rest, theta, center=(0.3, 0.1), shift=(2.0, -1.0))
        f, _ = corotational_forces(mesh, x)
        assert max(abs(c) for c in flat(f)) < 1e-10


def test_linear_fem_has_ghost_forces_under_rotation():
    mesh = small_mesh()
    x = rotate_points(mesh.rest, 1.0)
    fl = linear_forces(mesh, x)
    assert max(abs(c) for c in flat(fl)) > 10.0


def test_energy_is_frame_indifferent():
    rng = random.Random(5)
    for _ in range(20):
        f = [[1.0 + rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4)], [rng.uniform(-0.4, 0.4), 1.0 + rng.uniform(-0.4, 0.4)]]
        r = anim.rot2(rng.uniform(-math.pi, math.pi))
        a = corotated_energy_density(f, MU, LAM)
        b = corotated_energy_density(anim.mul(r, f), MU, LAM)
        assert abs(a - b) <= 1e-12 * max(1.0, a)


def test_zero_net_force_and_torque():
    rng = random.Random(3)
    mesh = small_mesh()
    x = perturbed(mesh.rest, rng, 0.2)
    f, _ = corotational_forces(mesh, x)
    scale = max(abs(c) for c in flat(f))
    assert abs(sum(p[0] for p in f)) < 1e-12 * scale * len(f)
    assert abs(sum(p[1] for p in f)) < 1e-12 * scale * len(f)
    torque = sum(anim.cross2(x[i], f[i]) for i in range(len(f)))
    assert abs(torque) < 1e-11 * scale * len(f)


def numeric_hessian(mesh, x, h=1e-6):
    z = flat(x)
    cols = []
    for k in range(len(z)):
        zp, zm = list(z), list(z)
        zp[k] += h
        zm[k] -= h
        fp, _ = corotational_forces(mesh, unflat(zp))
        fm, _ = corotational_forces(mesh, unflat(zm))
        cols.append([-(a - b) / (2 * h) for a, b in zip(flat(fp), flat(fm))])
    return [list(r) for r in zip(*cols)]


def test_warped_stiffness_exact_only_at_rotated_rest():
    mesh = small_mesh()
    x = rotate_points(mesh.rest, 0.9)
    _, rots = corotational_forces(mesh, x)
    kw = warped_stiffness(mesh, rots)
    kn = numeric_hessian(mesh, x)
    scale = max(abs(c) for row in kn for c in row)
    assert max(abs(kw[i][j] - kn[i][j]) for i in range(len(kw)) for j in range(len(kw))) < 1e-6 * scale
    stretched = [(1.3 * p[0], 0.8 * p[1]) for p in mesh.rest]
    x = rotate_points(stretched, 0.9)
    _, rots = corotational_forces(mesh, x)
    kw = warped_stiffness(mesh, rots)
    kn = numeric_hessian(mesh, x)
    assert max(abs(kw[i][j] - kn[i][j]) for i in range(len(kw)) for j in range(len(kw))) > 1e-2 * scale


def test_spinning_body_keeps_momentum_and_shape():
    mesh = small_mesh()
    x = list(mesh.rest)
    cx = sum(p[0] for p in x) / len(x)
    cy = sum(p[1] for p in x) / len(x)
    omega = 3.0
    v = [(-omega * (p[1] - cy), omega * (p[0] - cx)) for p in x]
    dt = 1e-3

    def momenta(x, v):
        px = sum(m * w[0] for m, w in zip(mesh.mass, v))
        py = sum(m * w[1] for m, w in zip(mesh.mass, v))
        lz = sum(m * anim.cross2(p, w) for m, p, w in zip(mesh.mass, x, v))
        return px, py, lz

    p0 = momenta(x, v)
    for _ in range(1000):
        x, v = step_explicit(mesh, x, v, dt)
    p1 = momenta(x, v)
    assert abs(p1[0] - p0[0]) < 1e-10 and abs(p1[1] - p0[1]) < 1e-10
    assert abs(p1[2] - p0[2]) < 1e-10 * abs(p0[2])
    area = sum(0.5 * anim.det([[x[t[1]][0] - x[t[0]][0], x[t[2]][0] - x[t[0]][0]],
                               [x[t[1]][1] - x[t[0]][1], x[t[2]][1] - x[t[0]][1]]]) for t in mesh.tris)
    assert abs(area - 0.5) < 0.01


def test_cantilever_settles_with_implicit_step():
    rest, tris = grid_mesh(4, 1, 1.0, 0.25)
    mesh = Mesh(rest, tris, MU, LAM)
    fixed = [i for i, p in enumerate(rest) if p[0] == 0.0]
    g = [(0.0, -9.81 * m) for m in mesh.mass]
    x, v = list(rest), [(0.0, 0.0)] * len(rest)
    for _ in range(150):
        x, v = step_implicit(mesh, x, v, 0.05, f_ext=g, fixed=fixed)
    f, _ = corotational_forces(mesh, x)
    free = [i for i in range(len(x)) if i not in fixed]
    resid = max(abs(f[i][c] + g[i][c]) for i in free for c in range(2))
    gmax = max(abs(g[i][1]) for i in free)
    assert resid < 1e-3 * gmax
    tip = min(x[i][1] for i in free)
    assert -0.6 < tip < -0.05
    for i in fixed:
        assert x[i] == rest[i]
