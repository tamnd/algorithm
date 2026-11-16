# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-jacobian/. The authors are listed in prov/TB3AFJ.jsonl.
"""Tests of the geometric Jacobian against central finite differences of
the forward kinematics, the 2R check values, and the conversions to the
space and body twists."""

import math
import random

import rbm
from geometric_jacobian import forward_kinematics, geometric_jacobian, to_body_twist, to_space_twist

H = 1e-6


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


TWO_R = [("R", 0.0, 0.0, 1.0, 0.0), ("R", 0.0, 0.0, 1.0, 0.0)]


def rand_dh(rng, kinds):
    return [
        (k, rng.uniform(-0.5, 0.5), rng.uniform(-1.0, 1.0), rng.uniform(-0.5, 0.5), rng.uniform(-math.pi, math.pi))
        for k in kinds
    ]


def fd_geometric(dh, q):
    """Return (p', omega) columns by central differences of T(q)."""
    t = forward_kinematics(dh, q)
    rt = [[t[j][i] for j in range(3)] for i in range(3)]
    cols = []
    for i in range(len(q)):
        qp, qm = list(q), list(q)
        qp[i] += H
        qm[i] -= H
        tp, tm = forward_kinematics(dh, qp), forward_kinematics(dh, qm)
        d = rbm.scale(rbm.sub(tp, tm), 1.0 / (2.0 * H))
        lin = [d[0][3], d[1][3], d[2][3]]
        rdot = [row[:3] for row in d[:3]]
        w = rbm.vee3(rbm.mul(rdot, rt))
        cols.append(lin + w)
    return rbm.transpose(cols)


def test_2r_check_values():
    q = [0.0, math.pi / 2.0]
    t = forward_kinematics(TWO_R, q)
    assert maxdiff([t[0][3], t[1][3], t[2][3]], [1.0, 1.0, 0.0]) < 1e-15
    j = geometric_jacobian(TWO_R, q)
    want = [[-1.0, -1.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0]]
    assert maxdiff(j, want) < 1e-15
    # determinant of the planar block is L1 L2 sin(q2)
    for q2 in (0.3, 1.0, 2.5, -0.7):
        j = geometric_jacobian(TWO_R, [0.4, q2])
        det = j[0][0] * j[1][1] - j[0][1] * j[1][0]
        assert abs(det - math.sin(q2)) < 1e-14
    # space twist columns of the page: (0,0,1, 0,0,0) and (0,0,1, 0,-1,0)
    js = to_space_twist(geometric_jacobian(TWO_R, q), [1.0, 1.0, 0.0])
    assert maxdiff(js, [[0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [0.0, 0.0], [0.0, -1.0], [0.0, 0.0]]) < 1e-15


def test_against_finite_differences():
    rng = random.Random(21)
    for kinds in ("RRR", "RRPRRR", "RRRRRRR", "PRP"):
        dh = rand_dh(rng, kinds)
        for _ in range(3):
            q = [rng.uniform(-math.pi, math.pi) for _ in kinds]
            assert maxdiff(geometric_jacobian(dh, q), fd_geometric(dh, q)) < 1e-6


def test_conversions_to_twists():
    rng = random.Random(22)
    dh = rand_dh(rng, "RRPRRR")
    q = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
    t = forward_kinematics(dh, q)
    ti = rbm.T_inv(t)
    pe = [t[0][3], t[1][3], t[2][3]]
    j = geometric_jacobian(dh, q)
    js = to_space_twist(j, pe)
    jb = to_body_twist(j, t)
    for i in range(6):
        qp, qm = list(q), list(q)
        qp[i] += H
        qm[i] -= H
        d = rbm.scale(rbm.sub(forward_kinematics(dh, qp), forward_kinematics(dh, qm)), 1.0 / (2.0 * H))
        assert maxdiff([row[i] for row in js], rbm.vee6(rbm.mul(d, ti))) < 1e-6
        assert maxdiff([row[i] for row in jb], rbm.vee6(rbm.mul(ti, d))) < 1e-6
    # J_b = Ad(T^-1) J_s
    assert maxdiff(rbm.mul(rbm.adjoint(ti), js), jb) < 1e-12
