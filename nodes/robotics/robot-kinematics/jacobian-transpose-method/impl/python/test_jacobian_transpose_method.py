# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobian-transpose-method/. The authors are listed in prov/NPCR98.jsonl.
"""Tests of the Jacobian transpose method: the step against a finite
difference gradient of the squared error, the gain of Buss and Kim against a grid
search, descent for small gains, the example of the page, the local rate,
the 2R arm against the closed form solutions, and a target out of reach."""

import math
import random

from jacobian_transpose_method import dot, ik_transpose, matvec, norm, planar_fk, planar_jacobian, transpose, transpose_step

L2 = [1.0, 1.0]


def fk2(q):
    return planar_fk(L2, q)


def jac2(q):
    return planar_jacobian(L2, q)


def half_sq_error(lengths, x_d, q):
    e = [a - b for a, b in zip(x_d, planar_fk(lengths, q))]
    return 0.5 * dot(e, e)


def maxdiff(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def test_planar_jacobian_and_check_values():
    rng = random.Random(1)
    lengths = [1.0, 0.8, 0.5]
    h = 1e-6
    for _ in range(10):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        j = planar_jacobian(lengths, q)
        for i in range(3):
            qp, qm = list(q), list(q)
            qp[i] += h
            qm[i] -= h
            col = [(a - b) / (2.0 * h) for a, b in zip(planar_fk(lengths, qp), planar_fk(lengths, qm))]
            assert maxdiff(col, [j[0][i], j[1][i]]) < 1e-6
    j = jac2([0.0, math.pi / 2.0])
    assert maxdiff(j[0] + j[1], [-1.0, -1.0, 1.0, 0.0]) < 1e-15
    assert maxdiff(fk2([0.0, math.pi / 2.0]), [1.0, 1.0]) < 1e-15


def test_step_is_the_negative_gradient():
    rng = random.Random(2)
    lengths = [1.0, 0.8, 0.5]
    h = 1e-6
    for _ in range(20):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        x_d = [rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)]
        e = [a - b for a, b in zip(x_d, planar_fk(lengths, q))]
        g = transpose_step(planar_jacobian(lengths, q), e, 1.0)
        for i in range(3):
            qp, qm = list(q), list(q)
            qp[i] += h
            qm[i] -= h
            num = (half_sq_error(lengths, x_d, qp) - half_sq_error(lengths, x_d, qm)) / (2.0 * h)
            assert abs(g[i] + num) < 1e-6


def test_buss_gain_against_grid_search():
    rng = random.Random(3)
    for m, n in ((2, 2), (2, 4), (3, 3), (6, 7)):
        for _ in range(10):
            j = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]
            e = [rng.uniform(-1.0, 1.0) for _ in range(m)]
            dq = transpose_step(j, e)
            g = matvec(transpose(j), e)
            alpha = dot(dq, g) / dot(g, g)
            assert alpha > 0.0

            def resid(a):
                return norm([x - a * y for x, y in zip(e, matvec(j, g))])

            best = min(resid(alpha * k / 1000.0) for k in range(0, 3001))
            assert resid(alpha) <= best + 1e-12


def test_small_gain_decreases_the_error():
    rng = random.Random(4)
    lengths = [1.0, 0.8, 0.5, 0.3]
    for _ in range(50):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(4)]
        x_d = [rng.uniform(-2.5, 2.5), rng.uniform(-2.5, 2.5)]
        e = [a - b for a, b in zip(x_d, planar_fk(lengths, q))]
        dq = transpose_step(planar_jacobian(lengths, q), e, 1e-3)
        q2 = [a + b for a, b in zip(q, dq)]
        assert half_sq_error(lengths, x_d, q2) < half_sq_error(lengths, x_d, q)


def test_example_of_the_page():
    q0 = [0.3, 1.2]
    e = [1.0 - a for a in fk2(q0)]
    g = matvec(transpose(jac2(q0)), e)
    assert maxdiff(g, [-0.266942, 0.005281]) < 1e-6
    assert maxdiff(transpose_step(jac2(q0), e), [-0.099972, 0.001978]) < 1e-6
    counts = {}
    for alpha in (0.1, 0.5, 2.0 / 3.0, None):
        q, hist, ok = ik_transpose(fk2, jac2, [1.0, 1.0], q0, alpha)
        assert ok and maxdiff(q, [0.0, math.pi / 2.0]) < 1e-9
        assert all(b <= a for a, b in zip(hist, hist[1:]))
        counts[alpha] = len(hist)
    assert counts == {0.1: 570, 0.5: 106, 2.0 / 3.0: 78, None: 15}
    # A gain above 2 / sigma_max^2 = 0.764 does not converge.
    q, hist, ok = ik_transpose(fk2, jac2, [1.0, 1.0], q0, 0.9, max_iter=2000)
    assert not ok and min(hist[1000:]) > 0.1


def test_local_rate():
    # Near (0, pi/2) the error ratio tends to max |1 - alpha s_i^2| with s_i^2 = (3 +- sqrt 5) / 2.
    s2 = [(3.0 + math.sqrt(5.0)) / 2.0, (3.0 - math.sqrt(5.0)) / 2.0]
    for alpha in (0.1, 0.5, 2.0 / 3.0):
        _, hist, ok = ik_transpose(fk2, jac2, [1.0, 1.0], [0.3, 1.2], alpha)
        rate = max(abs(1.0 - alpha * s) for s in s2)
        assert ok and abs(hist[-1] / hist[-2] - rate) < 1e-3


def closed_form_2r(x, y):
    c2 = (x * x + y * y - 2.0) / 2.0
    out = []
    for s in (1.0, -1.0):
        q2 = s * math.acos(c2)
        out.append((math.atan2(y, x) - math.atan2(math.sin(q2), 1.0 + math.cos(q2)), q2))
    return out


def test_2r_against_closed_form():
    rng = random.Random(5)
    done = 0
    for _ in range(40):
        r = rng.uniform(0.3, 1.9)
        a = rng.uniform(-math.pi, math.pi)
        x_d = [r * math.cos(a), r * math.sin(a)]
        q0 = [rng.uniform(-math.pi, math.pi), rng.uniform(-math.pi, math.pi)]
        q, hist, ok = ik_transpose(fk2, jac2, x_d, q0, None, max_iter=3000)
        if not ok:
            continue
        done += 1
        assert maxdiff(fk2(q), x_d) < 1e-9
        assert min(max(abs(math.remainder(u - v, 2.0 * math.pi)) for u, v in zip(q, s)) for s in closed_form_2r(*x_d)) < 1e-8
    assert done >= 36


def test_out_of_reach():
    # The arm stretches toward the target: a stationary point with J^T e = 0 and |e| = 0.5.
    for alpha in (0.1, None):
        q, hist, ok = ik_transpose(fk2, jac2, [2.5, 0.0], [0.2, 0.5], alpha, max_iter=3000)
        assert not ok
        assert abs(hist[-1] - 0.5) < 1e-12
        assert maxdiff(fk2(q), [2.0, 0.0]) < 1e-12
        e = [2.5 - fk2(q)[0], -fk2(q)[1]]
        assert norm(matvec(transpose(jac2(q)), e)) < 1e-12
