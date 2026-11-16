# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobian-pseudoinverse-method/. The authors are listed in prov/MNF4KJ.jsonl.
"""Tests of pseudoinverse inverse kinematics: the Penrose conditions, the
minimum-norm step against a KKT solve, the 2R check values, a 7R position
task, a 6R full pose task, and failure on a target out of reach."""

import math
import random

import rbm
from jacobian_pseudoinverse_method import body_jacobian, fk_body, ik_pose, ik_position, pinv, svd


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def rand_unit(rng):
    while True:
        v = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if 0.2 < n <= 1.0:
            return [x / n for x in v]


def rand_screws(rng, n):
    """Revolute screw axes S = (omega, -omega x p) in the space frame."""
    out = []
    for _ in range(n):
        w = rand_unit(rng)
        p = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        out.append(w + rbm.cross(p, w))
    return out


def fk_space(slist, m, q):
    t = rbm.eye(4)
    for s, x in zip(slist, q):
        t = rbm.mul(t, rbm.se3_exp([y * x for y in s]))
    return rbm.mul(t, m)


def space_jacobian(slist, q):
    t = rbm.eye(4)
    cols = []
    for s, x in zip(slist, q):
        cols.append(rbm.matvec(rbm.adjoint(t), s))
        t = rbm.mul(t, rbm.se3_exp([y * x for y in s]))
    return rbm.transpose(cols)


def position_jacobian(slist, m, q):
    """Rows of p' = v_s + omega x p, the velocity of the tool point."""
    js = space_jacobian(slist, q)
    t = fk_space(slist, m, q)
    p = [t[0][3], t[1][3], t[2][3]]
    out = rbm.zeros(3, len(q))
    for c in range(len(q)):
        w = [js[i][c] for i in range(3)]
        v = [js[i + 3][c] for i in range(3)]
        col = rbm.add(v, rbm.cross(w, p))
        for i in range(3):
            out[i][c] = col[i]
    return out


def fk2(q):
    return [math.cos(q[0]) + math.cos(q[0] + q[1]), math.sin(q[0]) + math.sin(q[0] + q[1])]


def jac2(q):
    s1, c1 = math.sin(q[0]), math.cos(q[0])
    s12, c12 = math.sin(q[0] + q[1]), math.cos(q[0] + q[1])
    return [[-s1 - s12, -s12], [c1 + c12, c12]]


def penrose(a, x, tol):
    ax = rbm.mul(a, x)
    xa = rbm.mul(x, a)
    assert maxdiff(rbm.mul(ax, a), a) < tol
    assert maxdiff(rbm.mul(xa, x), x) < tol
    assert maxdiff(ax, rbm.transpose(ax)) < tol
    assert maxdiff(xa, rbm.transpose(xa)) < tol


def test_svd_reconstructs():
    rng = random.Random(1)
    for m, n in [(2, 3), (3, 7), (6, 6), (6, 7), (4, 2)]:
        a = rand_matrix(rng, m, n)
        u, s, v = svd(a)
        back = rbm.zeros(m, n)
        for uj, sj, vj in zip(u, s, v):
            for i in range(m):
                for k in range(n):
                    back[i][k] += sj * uj[i] * vj[k]
        assert maxdiff(back, a) < 1e-12


def test_pinv_penrose_conditions():
    rng = random.Random(2)
    for m, n in [(2, 3), (3, 7), (6, 7), (5, 3)]:
        a = rand_matrix(rng, m, n)
        penrose(a, pinv(a), 1e-11)
    # rank 2 matrix of size 3 by 5: the product of 3x2 and 2x5 factors
    a = rbm.mul(rand_matrix(rng, 3, 2), rand_matrix(rng, 2, 5))
    x = pinv(a)
    penrose(a, x, 1e-10)
    # the zero matrix has the zero pseudoinverse
    assert maxdiff(pinv(rbm.zeros(2, 3)), rbm.zeros(3, 2)) == 0.0


def test_pinv_against_closed_forms():
    rng = random.Random(3)
    a = rand_matrix(rng, 3, 6)
    assert maxdiff(pinv(a), rbm.pinv_right(a)) < 1e-11
    b = rand_matrix(rng, 4, 4)
    assert maxdiff(pinv(b), rbm.inv(b)) < 1e-9
    # tall matrix with full column rank: (A^T A)^-1 A^T
    c = rand_matrix(rng, 5, 2)
    ct = rbm.transpose(c)
    assert maxdiff(pinv(c), rbm.mul(rbm.inv(rbm.mul(ct, c)), ct)) < 1e-11


def test_step_is_minimum_norm():
    rng = random.Random(4)
    for _ in range(5):
        j = rand_matrix(rng, 3, 7)
        e = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        step = rbm.matvec(pinv(j), e)
        # KKT system of min |d|^2 / 2 subject to J d = e
        kkt = rbm.zeros(10, 10)
        for i in range(7):
            kkt[i][i] = 1.0
        for r in range(3):
            for c in range(7):
                kkt[7 + r][c] = j[r][c]
                kkt[c][7 + r] = j[r][c]
        sol = rbm.solve(kkt, [0.0] * 7 + e)
        assert maxdiff(step, sol[:7]) < 1e-11
        # any other solution step + n with J n = 0 is longer
        nul = rbm.sub(rbm.eye(7), rbm.mul(pinv(j), j))
        z = [rng.uniform(-1.0, 1.0) for _ in range(7)]
        other = rbm.add(step, rbm.matvec(nul, z))
        assert maxdiff(rbm.matvec(j, other), e) < 1e-11
        assert rbm.norm(other) >= rbm.norm(step)


def test_2r_check_values():
    q = [0.0, math.pi / 2.0]
    assert maxdiff(fk2(q), [1.0, 1.0]) < 1e-15
    assert maxdiff(jac2(q), [[-1.0, -1.0], [1.0, 0.0]]) < 1e-15
    assert maxdiff(rbm.num_jacobian(fk2, [0.4, 1.1]), jac2([0.4, 1.1])) < 1e-6


def test_2r_reaches_both_solutions():
    up = ik_position(fk2, jac2, [1.0, 1.0], [0.3, 1.2])
    assert up is not None
    assert maxdiff(up, [0.0, math.pi / 2.0]) < 1e-9
    down = ik_position(fk2, jac2, [1.0, 1.0], [1.3, -1.2])
    assert down is not None
    assert maxdiff(down, [math.pi / 2.0, -math.pi / 2.0]) < 1e-9
    for q in (up, down):
        assert maxdiff(fk2(q), [1.0, 1.0]) < 1e-9


def test_2r_out_of_reach_fails():
    assert ik_position(fk2, jac2, [2.5, 0.0], [0.2, 0.5], max_iter=50) is None


def test_7r_position_round_trip():
    rng = random.Random(7)
    slist = rand_screws(rng, 7)
    m = rbm.make_T(rbm.eye(3), [1.0, 0.5, 0.2])

    def fk(q):
        t = fk_space(slist, m, q)
        return [t[0][3], t[1][3], t[2][3]]

    def jac(q):
        return position_jacobian(slist, m, q)

    q = [rng.uniform(-1.0, 1.0) for _ in range(7)]
    assert maxdiff(rbm.num_jacobian(fk, q), jac(q)) < 1e-6
    for _ in range(4):
        q_true = [rng.uniform(-math.pi, math.pi) for _ in range(7)]
        x_d = fk(q_true)
        q0 = [x + rng.uniform(-0.3, 0.3) for x in q_true]
        q = ik_position(fk, jac, x_d, q0)
        assert q is not None
        assert maxdiff(fk(q), x_d) < 1e-9


def test_body_jacobian_against_finite_differences():
    rng = random.Random(8)
    slist = rand_screws(rng, 6)
    m = rbm.make_T(rbm.rot_z(0.3), [0.5, 0.2, 0.7])
    blist = [rbm.matvec(rbm.adjoint(rbm.T_inv(m)), s) for s in slist]
    q = [rng.uniform(-1.0, 1.0) for _ in range(6)]
    t = fk_body(m, blist, q)
    assert maxdiff(t, fk_space(slist, m, q)) < 1e-12
    h = 1e-6
    ti = rbm.T_inv(t)
    jb = body_jacobian(blist, q)
    for i in range(6):
        qp, qm = list(q), list(q)
        qp[i] += h
        qm[i] -= h
        d = rbm.scale(rbm.sub(fk_body(m, blist, qp), fk_body(m, blist, qm)), 1.0 / (2.0 * h))
        col = rbm.vee6(rbm.mul(ti, d))
        assert maxdiff(col, [row[i] for row in jb]) < 1e-6


def test_6r_full_pose_round_trip():
    rng = random.Random(9)
    slist = rand_screws(rng, 6)
    m = rbm.make_T(rbm.rot_x(0.4), [0.6, -0.2, 0.9])
    blist = [rbm.matvec(rbm.adjoint(rbm.T_inv(m)), s) for s in slist]
    for _ in range(4):
        q_true = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        t_d = fk_body(m, blist, q_true)
        q0 = [x + rng.uniform(-0.2, 0.2) for x in q_true]
        q = ik_pose(m, blist, t_d, q0)
        assert q is not None
        assert maxdiff(fk_body(m, blist, q), t_d) < 1e-9


def test_planar_pose_check_values():
    # The 2R arm as a spatial chain: body screws of the page, M = (I, (2, 0, 0)).
    m = rbm.make_T(rbm.eye(3), [2.0, 0.0, 0.0])
    blist = [[0.0, 0.0, 1.0, 0.0, 2.0, 0.0], [0.0, 0.0, 1.0, 0.0, 1.0, 0.0]]
    t_d = rbm.make_T(rbm.rot_z(math.pi / 2.0), [1.0, 1.0, 0.0])
    q = ik_pose(m, blist, t_d, [0.2, 1.3])
    assert q is not None
    assert maxdiff(q, [0.0, math.pi / 2.0]) < 1e-9
