# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-raphson-inverse-kinematics/. The authors are listed in prov/85CD1Z.jsonl.
"""Tests of Newton-Raphson inverse kinematics: the 2R check values against
the closed form, the body Jacobian against finite differences, quadratic
convergence on random 6R arms, the example of the page, and failure at a
singular start."""

import math
import random

import rbm
from newton_raphson_inverse_kinematics import body_jacobian, fk_body, ik_newton, newton_position


def fk2(q):
    return [math.cos(q[0]) + math.cos(q[0] + q[1]), math.sin(q[0]) + math.sin(q[0] + q[1])]


def jac2(q):
    s1, c1 = math.sin(q[0]), math.cos(q[0])
    s12, c12 = math.sin(q[0] + q[1]), math.cos(q[0] + q[1])
    return [[-s1 - s12, -s12], [c1 + c12, c12]]


def closed_form_2r(x, y):
    """All solutions of the unit 2R arm by the law of cosines."""
    c2 = (x * x + y * y - 2.0) / 2.0
    out = []
    for s in (1.0, -1.0):
        q2 = s * math.acos(c2)
        q1 = math.atan2(y, x) - math.atan2(math.sin(q2), 1.0 + math.cos(q2))
        out.append((q1, q2))
    return out


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def test_2r_check_values():
    j = jac2([0.0, math.pi / 2.0])
    assert maxdiff(j, [[-1.0, -1.0], [1.0, 0.0]]) < 1e-15
    assert abs(rbm.det(j) - 1.0) < 1e-15
    assert maxdiff(fk2([0.0, math.pi / 2.0]), [1.0, 1.0]) < 1e-15
    q, hist = newton_position(fk2, jac2, [1.0, 1.0], [0.3, 1.2])
    for got, want in zip(hist, [0.294, 0.0517, 0.00119, 7.05e-7]):
        assert abs(got - want) < 0.005 * want
    assert maxdiff(q, [0.0, math.pi / 2.0]) < 1e-12
    q, _ = newton_position(fk2, jac2, [1.0, 1.0], [1.3, -1.2])
    assert maxdiff(q, [math.pi / 2.0, -math.pi / 2.0]) < 1e-12


def test_2r_against_closed_form():
    rng = random.Random(1)
    for _ in range(200):
        r = rng.uniform(0.3, 1.9)
        a = rng.uniform(-math.pi, math.pi)
        x, y = r * math.cos(a), r * math.sin(a)
        sols = closed_form_2r(x, y)
        q0 = [rng.uniform(-math.pi, math.pi), rng.uniform(-math.pi, math.pi)]
        q, _ = newton_position(fk2, jac2, [x, y], q0, max_iter=100)
        if q is None:
            continue
        assert maxdiff(fk2(q), [x, y]) < 1e-11
        assert min(max(abs(math.remainder(a - b, 2.0 * math.pi)) for a, b in zip(q, s)) for s in sols) < 1e-9


def rand_unit(rng):
    while True:
        v = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if 0.2 < n <= 1.0:
            return [x / n for x in v]


def rand_arm(rng, n=6):
    blist = []
    for _ in range(n):
        w = rand_unit(rng)
        p = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        blist.append(w + rbm.cross(p, w))
    m = rbm.make_T(rbm.so3_exp([rng.uniform(-1.0, 1.0) for _ in range(3)]), [rng.uniform(-1.0, 1.0) for _ in range(3)])
    return m, blist


def test_body_jacobian_against_finite_differences():
    rng = random.Random(2)
    h = 1e-6
    for _ in range(5):
        m, blist = rand_arm(rng)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        t_inv = rbm.T_inv(fk_body(m, blist, q))
        jb = body_jacobian(blist, q)
        for i in range(6):
            qp, qm = list(q), list(q)
            qp[i] += h
            qm[i] -= h
            dp = rbm.se3_log(rbm.mul(t_inv, fk_body(m, blist, qp)))
            dm = rbm.se3_log(rbm.mul(t_inv, fk_body(m, blist, qm)))
            col = [(a - b) / (2.0 * h) for a, b in zip(dp, dm)]
            assert maxdiff(col, [row[i] for row in jb]) < 1e-6


def test_quadratic_convergence_on_random_arms():
    rng = random.Random(3)
    done = 0
    for _ in range(12):
        m, blist = rand_arm(rng)
        q_star = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        jb = body_jacobian(blist, q_star)
        if abs(rbm.det(jb)) < 0.1:
            continue  # too close to a singularity for a clean test
        t_d = fk_body(m, blist, q_star)
        q0 = [x + rng.uniform(-0.05, 0.05) for x in q_star]
        q, hist = ik_newton(m, blist, t_d, q0)
        assert q is not None and len(hist) <= 8
        assert maxdiff(fk_body(m, blist, q), t_d) < 1e-9
        assert maxdiff(q, q_star) < 1e-8
        for a, b in zip(hist, hist[1:]):
            if a < 1e-2 and b > 1e-13:
                assert b <= 200.0 * a * a
        done += 1
    assert done >= 6


def elbow_arm():
    """The elbow arm of the page in body form: M = (I, (0, 2.5, 1)) and the body screw axes."""
    m = rbm.make_T(rbm.eye(3), [0.0, 2.5, 1.0])
    blist = [
        [0.0, 0.0, 1.0, -2.5, 0.0, 0.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, -2.5],
        [-1.0, 0.0, 0.0, 0.0, 0.0, -1.5],
        [0.0, 0.0, 1.0, -0.5, 0.0, 0.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    ]
    return m, blist


def test_example_of_the_page():
    m, blist = elbow_arm()
    q_star = [0.3, -0.4, 0.9, 0.5, 0.7, -0.6]
    t_d = fk_body(m, blist, q_star)
    assert maxdiff([t_d[i][3] for i in range(3)], [-0.748090, 1.797966, 0.466418]) < 1e-6
    q, hist = ik_newton(m, blist, t_d, [0.5, -0.6, 1.1, 0.3, 0.9, -0.8])
    for got, want in zip(hist, [0.504, 0.0412, 0.000827, 7.14e-7]):
        assert abs(got - want) < 0.005 * want
    assert maxdiff(q, q_star) < 1e-10
    # From a far start, the loop wanders and ends at another solution, the wrist flip.
    q, hist = ik_newton(m, blist, t_d, [1.0] * 6)
    assert q is not None and len(hist) == 11
    wrapped = [math.remainder(x, 2.0 * math.pi) for x in q]
    assert maxdiff(wrapped, [0.3, -0.4, 0.9, 0.5 - math.pi, math.pi - 0.7, -0.6 + math.pi]) < 1e-9
    assert maxdiff(fk_body(m, blist, q), t_d) < 1e-9


def test_singular_start_fails():
    m, blist = elbow_arm()
    assert abs(rbm.det(body_jacobian(blist, [0.0] * 6))) < 1e-12
    t_d = fk_body(m, blist, [0.3, -0.4, 0.9, 0.5, 0.7, -0.6])
    q, hist = ik_newton(m, blist, t_d, [0.0] * 6)
    assert q is None and len(hist) == 1


def test_out_of_reach_fails():
    q, hist = newton_position(fk2, jac2, [2.5, 0.0], [0.2, 0.5], max_iter=50)
    assert q is None and min(hist) > 0.4
