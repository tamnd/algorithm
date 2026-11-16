# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-and-body-jacobian/. The authors are listed in prov/DQFEN4.jsonl.
"""Tests of the space and body Jacobians: central finite differences of
the forward kinematics, the 2R check values, the adjoint relation, and the
velocity of the tool point."""

import math
import random

import rbm
from space_and_body_jacobian import (
    body_jacobian,
    body_screws,
    fk_body,
    fk_space,
    space_jacobian,
    space_to_body,
)

H = 1e-6


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def rand_unit(rng):
    while True:
        v = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if 0.2 < n <= 1.0:
            return [x / n for x in v]


def rand_arm(rng, n):
    """Random screw axes: revolute (omega, -omega x p), and prismatic (0, v) for every third joint."""
    out = []
    for i in range(n):
        if i % 3 == 2:
            out.append([0.0, 0.0, 0.0] + rand_unit(rng))
        else:
            w = rand_unit(rng)
            p = [rng.uniform(-1.0, 1.0) for _ in range(3)]
            out.append(w + rbm.cross(p, w))
    return out


def fd_twists(fk, q):
    """Return the space and body Jacobians by central differences of T(q)."""
    t = fk(q)
    ti = rbm.T_inv(t)
    cols_s, cols_b = [], []
    for i in range(len(q)):
        qp, qm = list(q), list(q)
        qp[i] += H
        qm[i] -= H
        d = rbm.scale(rbm.sub(fk(qp), fk(qm)), 1.0 / (2.0 * H))
        cols_s.append(rbm.vee6(rbm.mul(d, ti)))
        cols_b.append(rbm.vee6(rbm.mul(ti, d)))
    return rbm.transpose(cols_s), rbm.transpose(cols_b)


TWO_R_S = [[0.0, 0.0, 1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0, -1.0, 0.0]]
TWO_R_M = rbm.make_T(rbm.eye(3), [2.0, 0.0, 0.0])


def test_2r_check_values():
    q = [0.0, math.pi / 2.0]
    blist = body_screws(TWO_R_S, TWO_R_M)
    assert maxdiff(blist, [[0.0, 0.0, 1.0, 0.0, 2.0, 0.0], [0.0, 0.0, 1.0, 0.0, 1.0, 0.0]]) < 1e-15
    t = fk_space(TWO_R_S, TWO_R_M, q)
    assert maxdiff(t, rbm.make_T(rbm.rot_z(math.pi / 2.0), [1.0, 1.0, 0.0])) < 1e-15
    js = space_jacobian(TWO_R_S, q)
    want_s = [[0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [0.0, 0.0], [0.0, -1.0], [0.0, 0.0]]
    assert maxdiff(js, want_s) < 1e-15
    jb = body_jacobian(blist, q)
    want_b = [[0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]]
    assert maxdiff(jb, want_b) < 1e-15
    # velocity of the tool point p = (1, 1, 0): p' = v_s + omega x p
    p = [1.0, 1.0, 0.0]
    lin = []
    for c in range(2):
        w = [js[i][c] for i in range(3)]
        v = [js[i + 3][c] for i in range(3)]
        lin.append(rbm.add(v, rbm.cross(w, p))[:2])
    assert maxdiff(rbm.transpose(lin), [[-1.0, -1.0], [1.0, 0.0]]) < 1e-15


def test_against_finite_differences():
    rng = random.Random(5)
    for n in (2, 4, 6, 7):
        slist = rand_arm(rng, n)
        m = rbm.make_T(rbm.rpy(0.3, -0.2, 0.5), [0.4, 0.1, 0.8])
        blist = body_screws(slist, m)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(n)]
        fs, fb = fd_twists(lambda x: fk_space(slist, m, x), q)
        assert maxdiff(space_jacobian(slist, q), fs) < 1e-6
        assert maxdiff(body_jacobian(blist, q), fb) < 1e-6


def test_adjoint_relation_and_both_forms_of_fk():
    rng = random.Random(6)
    slist = rand_arm(rng, 6)
    m = rbm.make_T(rbm.rot_y(0.7), [0.2, -0.5, 1.0])
    blist = body_screws(slist, m)
    for _ in range(5):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        t = fk_space(slist, m, q)
        assert maxdiff(t, fk_body(m, blist, q)) < 1e-12
        js = space_jacobian(slist, q)
        jb = body_jacobian(blist, q)
        assert maxdiff(space_to_body(js, t), jb) < 1e-12
        assert maxdiff(rbm.mul(rbm.adjoint(t), jb), js) < 1e-12


def test_first_column_is_the_first_axis():
    rng = random.Random(7)
    slist = rand_arm(rng, 5)
    blist = body_screws(slist, rbm.make_T(rbm.eye(3), [1.0, 0.0, 0.0]))
    q = [rng.uniform(-1.0, 1.0) for _ in range(5)]
    js = space_jacobian(slist, q)
    jb = body_jacobian(blist, q)
    assert maxdiff([row[0] for row in js], slist[0]) == 0.0
    assert maxdiff([row[4] for row in jb], blist[4]) == 0.0
    # at q = 0 every column is the screw axis itself
    zero = [0.0] * 5
    assert maxdiff(space_jacobian(slist, zero), rbm.transpose(slist)) < 1e-15
    assert maxdiff(body_jacobian(blist, zero), rbm.transpose(blist)) < 1e-15
