# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paden-kahan-subproblems/. The authors are listed in prov/MGK2K1.jsonl.
"""Tests of the Paden-Kahan subproblems: each subproblem against a scan of
the angle, and the elbow arm against forward kinematics and against a
multi-start Newton search for all solutions."""

import math
import random

import rbm
from paden_kahan_subproblems import (
    elbow_arm,
    elbow_ik,
    fk,
    rotate_about,
    screw,
    subproblem1,
    subproblem2,
    subproblem3,
)


def rand_unit(rng):
    while True:
        v = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if 0.2 < n <= 1.0:
            return [x / n for x in v]


def rand_point(rng):
    return [rng.uniform(-1.0, 1.0) for _ in range(3)]


def angle_diff(a, b):
    d = math.fmod(a - b, 2.0 * math.pi)
    return min(abs(d), 2.0 * math.pi - abs(d))


def circle(w, r, p):
    """Return t -> Rot(w, t) (p - r) + r, by Rodrigues' formula with the parts of p - r fixed once."""
    u = rbm.sub(p, r)
    d = rbm.dot(w, u)
    par = rbm.add(r, rbm.scale(w, d))
    perp = rbm.sub(u, rbm.scale(w, d))
    side = rbm.cross(w, u)
    return lambda t: [a + math.cos(t) * b + math.sin(t) * c for a, b, c in zip(par, perp, side)]


def scan_roots(f, n=4000):
    """Return the roots of a 2 pi periodic f found by sign changes on a grid, refined by bisection."""
    xs = [-math.pi + 2.0 * math.pi * i / n for i in range(n + 1)]
    fs = [f(x) for x in xs]
    roots = []
    for i in range(n):
        if fs[i] == 0.0 or fs[i] * fs[i + 1] < 0.0:
            a, b, fa = xs[i], xs[i + 1], fs[i]
            for _ in range(60):
                mid = 0.5 * (a + b)
                fm = f(mid)
                if fa * fm <= 0.0:
                    b = mid
                else:
                    a, fa = mid, fm
            roots.append(0.5 * (a + b))
    return roots


def test_subproblem1_recovers_the_angle():
    rng = random.Random(1)
    for _ in range(200):
        w, r, p = rand_unit(rng), rand_point(rng), rand_point(rng)
        th = rng.uniform(-math.pi, math.pi)
        q = rotate_about(w, r, th, p)
        got = subproblem1(w, r, p, q)
        assert got is not None and angle_diff(got, th) < 1e-9


def test_subproblem1_no_solution():
    w, r, p = [0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]
    assert subproblem1(w, r, p, [0.0, 2.0, 0.0]) is None  # wrong radius
    assert subproblem1(w, r, p, [0.0, 1.0, 0.5]) is None  # wrong height


def test_subproblem3_against_scan():
    rng = random.Random(2)
    counts = {0: 0, 1: 0, 2: 0}
    for _ in range(40):
        w, r, p, q = rand_unit(rng), rand_point(rng), rand_point(rng), rand_point(rng)
        delta = rng.uniform(0.0, 2.5)
        c = circle(w, r, p)

        def f(t):
            return rbm.norm(rbm.sub(c(t), q)) - delta

        got = subproblem3(w, r, p, q, delta)
        want = scan_roots(f, 1000)
        assert len(got) == len(want)
        counts[len(got)] += 1
        for t in got:
            assert abs(f(t)) < 1e-9
            assert min(angle_diff(t, x) for x in want) < 1e-6
    assert counts[0] > 0 and counts[2] > 0


def test_subproblem2_against_scan():
    rng = random.Random(3)
    for trial in range(30):
        w1, w2, r, p = rand_unit(rng), rand_unit(rng), rand_point(rng), rand_point(rng)
        if trial % 2 == 0:
            t1, t2 = rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)
            q = rotate_about(w1, r, t1, rotate_about(w2, r, t2, p))
        else:  # a point at the right distance from r, usually without a solution
            d = rand_unit(rng)
            q = rbm.add(r, rbm.scale(d, rbm.norm(rbm.sub(p, r))))
        got = subproblem2(w1, w2, r, p, q)
        # Brute force: theta2 is a solution angle exactly when the point
        # Rot2(theta2) p has the height of q along w1.
        c2 = circle(w2, r, p)
        want = scan_roots(lambda t: rbm.dot(w1, rbm.sub(c2(t), q)), 1000)
        assert len(got) == len(want)
        for th1, th2 in got:
            img = rotate_about(w1, r, th1, rotate_about(w2, r, th2, p))
            assert rbm.norm(rbm.sub(img, q)) < 1e-9
            assert min(angle_diff(th2, x) for x in want) < 1e-6
        if trial % 2 == 0:
            assert any(angle_diff(a, t1) < 1e-8 and angle_diff(b, t2) < 1e-8 for a, b in got)


def pose_err(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(4) for j in range(4))


def space_jacobian(axes, theta):
    t = rbm.eye(4)
    cols = []
    for (w, r), th in zip(axes, theta):
        s = screw(w, r)
        cols.append(rbm.matvec(rbm.adjoint(t), s))
        t = rbm.mul(t, rbm.se3_exp([x * th for x in s]))
    return rbm.transpose(cols)


def newton(axes, m, g_d, th, iters=30):
    """Plain Newton-Raphson on the space twist error; returns theta or None."""
    th = list(th)
    for _ in range(iters):
        t = fk(axes, m, th)
        vs = rbm.matvec(rbm.adjoint(t), rbm.se3_log(rbm.mul(rbm.T_inv(t), g_d)))
        if rbm.norm(vs) < 1e-12:
            return th
        try:
            step = rbm.solve(space_jacobian(axes, th), vs)
        except ValueError:
            return None
        if rbm.norm(step) > 2.0:
            step = rbm.scale(step, 2.0 / rbm.norm(step))
        th = [a + b for a, b in zip(th, step)]
    return None


def same(a, b, tol=1e-6):
    return all(angle_diff(x, y) < tol for x, y in zip(a, b))


def test_elbow_ik_forward_kinematics():
    axes, m, pts = elbow_arm()
    rng = random.Random(4)
    for _ in range(60):
        th = [rng.uniform(-3.0, 3.0) for _ in range(6)]
        g = fk(axes, m, th)
        sols = elbow_ik(axes, m, pts, g)
        assert 1 <= len(sols) <= 8
        for s in sols:
            assert pose_err(fk(axes, m, s), g) < 1e-9
        assert any(same(s, th, 1e-7) for s in sols)
        for i in range(len(sols)):
            for j in range(i):
                assert not same(sols[i], sols[j])


def test_elbow_ik_against_multistart_newton():
    axes, m, pts = elbow_arm(1.0, 1.2, 0.9, 0.4)
    rng = random.Random(5)
    for _ in range(1):
        g = fk(axes, m, [rng.uniform(-2.5, 2.5) for _ in range(6)])
        sols = elbow_ik(axes, m, pts, g)
        found = []
        for _ in range(48):
            q = newton(axes, m, g, [rng.uniform(-math.pi, math.pi) for _ in range(6)])
            if q is not None and pose_err(fk(axes, m, q), g) < 1e-9:
                if not any(same(q, f) for f in found):
                    found.append(q)
        assert len(found) == len(sols) == 8
        for q in found:
            assert any(same(q, s) for s in sols)


def test_example_of_the_page():
    axes, m, pts = elbow_arm()
    th = [0.3, -0.4, 0.9, 0.5, 0.7, -0.6]
    sols = elbow_ik(axes, m, pts, fk(axes, m, th))
    assert len(sols) == 8
    thirds = sorted(round(s[2], 6) for s in sols)
    assert thirds == [-0.9] * 4 + [0.9] * 4


def test_out_of_reach():
    axes, m, pts = elbow_arm()
    g = rbm.make_T(rbm.eye(3), [0.0, 3.0, 1.0])  # wrist center 2.5 from the shoulder, reach 2
    assert elbow_ik(axes, m, pts, g) == []
