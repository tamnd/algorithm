# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baraff-witkin-cloth/. The authors are listed in prov/7F3XVP.jsonl.

"""Tests of Baraff-Witkin cloth against central differences, a dense solve and exact identities."""

import math
import random

from anim import num_grad, q_from_axis_angle, q_rotate, solve
import baraff_witkin_cloth as bw


def flat(xs):
    return [c for p in xs for c in p]


def unflat(f):
    return [tuple(f[3 * i:3 * i + 3]) for i in range(len(f) // 3)]


def jiggle(rng, x, a):
    return [tuple(c + rng.uniform(-a, a) for c in p) for p in x]


def dense(mat, n):
    out = [[0.0] * (3 * n) for _ in range(3 * n)]
    for i, row in mat.items():
        for j, blk in row.items():
            for r in range(3):
                for c in range(3):
                    out[3 * i + r][3 * j + c] = blk[r][c]
    return out


def numeric_jacobian(fun, x):
    """Central differences of a list-of-3-vectors function, as a dense 3n by 3n matrix."""
    n = len(x)
    flat_x = flat(x)
    cols = []
    for k in range(3 * n):
        def comp(t, k=k):
            y = list(flat_x)
            y[k] += t
            return flat(fun(unflat(y)))
        p, m = comp(1e-6), comp(-1e-6)
        cols.append([(a - b) / 2e-6 for a, b in zip(p, m)])
    return [list(row) for row in zip(*cols)]


def test_bend_gradient_against_num_grad():
    rng = random.Random(1)
    for _ in range(10):
        pts = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(4)]
        _, g = bw.bend_angle(*pts)
        ng = num_grad(lambda f: bw.bend_angle(*unflat(f))[0], flat(pts))
        assert max(abs(a - b) for a, b in zip(flat(g), ng)) <= 1e-6 * max(abs(c) for c in ng)


def test_forces_against_num_grad_rest_and_rotation():
    rng = random.Random(2)
    uv, tris, x = bw.grid(4, 4, 0.1)
    cl = bw.Cloth(uv, tris, density=0.5, k_stretch=100.0, k_shear=10.0, k_bend=0.01)
    y = jiggle(rng, x, 0.02)
    f, _, _ = cl.forces(y, [(0.0, 0.0, 0.0)] * len(y))
    ng = num_grad(lambda fl: cl.energy(unflat(fl)), flat(y))
    assert max(abs(a + b) for a, b in zip(flat(f), ng)) <= 1e-6 * max(abs(c) for c in ng)
    # zero force at rest and after a rigid motion
    q = q_from_axis_angle((0.3, -1.0, 0.5), 0.9)
    for z in (x, [tuple(c + d for c, d in zip(q_rotate(q, p), (0.2, -0.4, 1.0))) for p in x]):
        f, _, _ = cl.forces(z, [(0.0, 0.0, 0.0)] * len(z))
        assert max(abs(c) for fi in f for c in fi) < 1e-10


def test_stretch_and_shear_jacobian_against_central_differences():
    rng = random.Random(3)
    uv, tris, x = bw.grid(3, 3, 0.1)
    cl = bw.Cloth(uv, tris, k_stretch=200.0, k_shear=30.0)
    y = jiggle(rng, x, 0.03)
    zero = [(0.0, 0.0, 0.0)] * len(y)
    _, kmat, _ = cl.forces(y, zero)
    got = dense(kmat, len(y))
    want = numeric_jacobian(lambda z: cl.forces(z, zero)[0], y)
    scale = max(abs(c) for row in want for c in row)
    for i in range(len(got)):
        for j in range(len(got)):
            assert abs(got[i][j] - want[i][j]) <= 1e-6 * scale
            assert got[i][j] == got[j][i] or abs(got[i][j] - got[j][i]) <= 1e-12 * scale


def test_bend_jacobian_is_exact_where_theta_is_zero():
    """The code keeps only -k dC dC^T of the bend Jacobian, which is exact at theta = 0."""
    rng = random.Random(4)
    uv, tris, x = bw.grid(3, 3, 0.1)
    cl = bw.Cloth(uv, tris, k_stretch=0.0, k_shear=0.0, k_bend=0.5)
    # a stretched flat sheet: every theta is zero
    y = [(1.3 * p[0] + rng.uniform(-0.01, 0.01), 0.8 * p[1] + rng.uniform(-0.01, 0.01), 0.0) for p in x]
    zero = [(0.0, 0.0, 0.0)] * len(y)
    got = dense(cl.forces(y, zero)[1], len(y))
    want = numeric_jacobian(lambda z: cl.forces(z, zero)[0], y)
    scale = max(abs(c) for row in want for c in row)
    assert max(abs(a - b) for ra, rb in zip(got, want) for a, b in zip(ra, rb)) <= 1e-6 * scale


def test_damping_velocity_jacobian_and_dissipation():
    rng = random.Random(5)
    uv, tris, x = bw.grid(3, 3, 0.1)
    cl = bw.Cloth(uv, tris, k_stretch=0.0, k_shear=0.0, k_bend=0.0, kd_stretch=2.0, kd_shear=1.0, kd_bend=0.3)
    y = jiggle(rng, x, 0.03)
    v = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in y]
    f, _, dmat = cl.forces(y, v)
    got = dense(dmat, len(y))
    want = numeric_jacobian(lambda w: cl.forces(y, w)[0], v)
    scale = max(abs(c) for row in want for c in row)
    assert max(abs(a - b) for ra, rb in zip(got, want) for a, b in zip(ra, rb)) <= 1e-6 * scale
    # d . v = -sum k_d Cdot^2 <= 0, and the damping forces sum to zero
    assert sum(a * b for a, b in zip(flat(f), flat(v))) < 0.0
    for c in range(3):
        assert abs(sum(fi[c] for fi in f)) < 1e-12


def test_damping_position_jacobian_drops_only_the_asymmetric_term():
    """Equation (12) minus the term dC/dx_i (dCdot/dx_j)^T equals the code's dd/dx."""
    rng = random.Random(6)
    uv, tris, x = bw.grid(3, 3, 0.1)
    cl = bw.Cloth(uv, tris, k_stretch=0.0, k_shear=0.0, kd_stretch=2.0, kd_shear=1.0)
    y = jiggle(rng, x, 0.03)
    v = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in y]
    n = len(y)
    got = dense(cl.forces(y, v)[1], n)
    for idx, c, grads, s, base, k, kd in cl.conditions(y):
        for b, j in enumerate(idx):
            # dCdot/dx_j = sum_l s[l][j] B v_l
            dcd = [sum(s[l][b] * sum(base[r][t] * v[idx[l]][t] for t in range(3)) for l in range(3))
                   for r in range(3)]
            for a, i in enumerate(idx):
                for r in range(3):
                    for t in range(3):
                        got[3 * i + r][3 * j + t] -= kd * grads[a][r] * dcd[t]
    want = numeric_jacobian(lambda z: cl.forces(z, v)[0], y)
    scale = max(abs(c) for row in want for c in row)
    assert max(abs(a - b) for ra, rb in zip(got, want) for a, b in zip(ra, rb)) <= 1e-6 * scale


def scene(rng, nx=4):
    uv, tris, x = bw.grid(nx, nx, 0.1)
    cl = bw.Cloth(uv, tris, density=0.4, k_stretch=500.0, k_shear=50.0, k_bend=1e-3,
                  kd_stretch=0.5, kd_shear=0.1, kd_bend=1e-4)
    y = jiggle(rng, x, 0.02)
    v = [tuple(rng.uniform(-0.5, 0.5) for _ in range(3)) for _ in y]
    return cl, y, v


def test_modified_pcg_without_constraints_matches_a_dense_solve():
    cl, y, v = scene(random.Random(7))
    amat, b = cl.system(y, v, 0.02)
    dv, iters = bw.modified_pcg(amat, b, {}, eps=1e-13)
    want = solve(dense(amat, cl.n), flat(b))
    assert max(abs(p - q) for p, q in zip(flat(dv), want)) <= 1e-9 * max(abs(q) for q in want)
    assert iters <= 3 * cl.n * 2


def test_modified_pcg_with_constraints_matches_the_reduced_solve():
    cl, y, v = scene(random.Random(8))
    amat, b = cl.system(y, v, 0.02)
    p = (0.0, 0.6, 0.8)
    cons = {0: bw.pin((0.1, -0.2, 0.3)), 3: bw.pin(), 6: bw.plane(p, -0.25),
            9: bw.plane((1.0, 0.0, 0.0), 0.0)}
    # the basis B of the free directions, dv = z + B alpha
    basis = []
    other = {6: [(1.0, 0.0, 0.0), (0.0, 0.8, -0.6)], 9: [(0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]}
    for i in range(cl.n):
        if i in other:
            dirs = other[i]
        elif i in cons:
            dirs = []
        else:
            dirs = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
        for d in dirs:
            col = [0.0] * (3 * cl.n)
            col[3 * i:3 * i + 3] = d
            basis.append(col)
    a = dense(amat, cl.n)
    z = [0.0] * (3 * cl.n)
    for i, (_, zi) in cons.items():
        z[3 * i:3 * i + 3] = zi
    az = [sum(a[r][c] * z[c] for c in range(3 * cl.n)) for r in range(3 * cl.n)]
    rhs = [sum(col[r] * (flat(b)[r] - az[r]) for r in range(3 * cl.n)) for col in basis]
    ab = [[sum(a[r][c] * col[c] for c in range(3 * cl.n)) for r in range(3 * cl.n)] for col in basis]
    red = [[sum(ci[r] * abj[r] for r in range(3 * cl.n)) for abj in ab] for ci in basis]
    alpha = solve(red, rhs)
    want = [z[r] + sum(al * col[r] for al, col in zip(alpha, basis)) for r in range(3 * cl.n)]
    dv, _ = bw.modified_pcg(amat, b, cons, eps=1e-13)
    assert max(abs(p - q) for p, q in zip(flat(dv), want)) <= 1e-9 * max(abs(q) for q in want)
    # the constrained components equal z after any number of iterations
    for it in (0, 1, 2, 5):
        dv, _ = bw.modified_pcg(amat, b, cons, eps=0.0, max_iter=it)
        for i, (s, zi) in cons.items():
            fixed = [dv[i][r] - sum(s[r][c] * dv[i][c] for c in range(3)) for r in range(3)]
            assert max(abs(fc - zc) for fc, zc in zip(fixed, zi)) < 1e-15


def test_momentum_of_one_step_without_constraints():
    rng = random.Random(9)
    cl, y, v = scene(rng)
    total = sum(cl.mass)
    p0 = [sum(m * vi[c] for m, vi in zip(cl.mass, v)) for c in range(3)]
    h = 0.02
    for k in range(1, 6):
        y, v, _ = cl.step(y, v, h, eps=1e-14, max_iter=400)
        for c in range(3):
            want = p0[c] + k * h * total * bw.GRAVITY[c]
            got = sum(m * vi[c] for m, vi in zip(cl.mass, v))
            assert abs(got - want) <= 1e-10 * max(1.0, abs(p0[c]), abs(want))


def test_large_step_stays_bounded_where_explicit_euler_fails():
    nx = 5
    uv, tris, x0 = bw.grid(nx, nx, 0.1)
    cl = bw.Cloth(uv, tris, density=0.4, k_stretch=1e6, k_shear=1e5, k_bend=1e-4)
    cons = {0: bw.pin(), nx - 1: bw.pin()}
    h = 1.0 / 30.0
    x, v = list(x0), [(0.0, 0.0, 0.0)] * len(x0)
    for _ in range(20):
        x, v, _ = cl.step(x, v, h, cons, eps=1e-6)
        assert cl.energy(x) < 1e-3 and max(math.sqrt(sum(c * c for c in vi)) for vi in v) < 1.0
    assert x[0] == x0[0] and x[nx - 1] == x0[nx - 1]
    # explicit Euler with the same step and forces
    x, v = list(x0), [(0.0, 0.0, 0.0)] * len(x0)
    for _ in range(6):
        f, _, _ = cl.forces(x, v)
        nv = [(0.0, 0.0, 0.0) if i in cons else
              tuple(v[i][c] + h * (f[i][c] + cl.f_ext[i][c]) / cl.mass[i] for c in range(3))
              for i in range(len(x))]
        x = [tuple(x[i][c] + h * v[i][c] for c in range(3)) for i in range(len(x))]
        v = nv
    assert cl.energy(x) > 1e6
