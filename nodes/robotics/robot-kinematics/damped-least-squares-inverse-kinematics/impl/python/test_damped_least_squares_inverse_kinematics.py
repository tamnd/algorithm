# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/damped-least-squares-inverse-kinematics/. The authors are listed in prov/J6EXM0.jsonl.
"""Tests of damped least squares inverse kinematics: the two forms of the
step, the step as the minimizer of the damped objective (against random
perturbations), the bound |dq| <= |e| / (2 lam), the limit lam -> 0 against
the pseudoinverse, the example of the page, the local linear rate, random
reachable targets, and a target out of reach."""

import math
import random

import rbm
from damped_least_squares_inverse_kinematics import dls_step, dls_step_normal, ik_dls, planar_fk, planar_jacobian


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def objective(j, e, lam, dq):
    r = rbm.sub(rbm.matvec(j, dq), e)
    return rbm.dot(r, r) + lam * lam * rbm.dot(dq, dq)


def maxdiff(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def test_two_forms_agree():
    rng = random.Random(1)
    for m, n in ((2, 2), (2, 3), (3, 2), (6, 6), (3, 7), (6, 4)):
        for _ in range(10):
            j = rand_matrix(rng, m, n)
            e = [rng.uniform(-1.0, 1.0) for _ in range(m)]
            lam = rng.uniform(0.01, 1.0)
            assert maxdiff(dls_step(j, e, lam), dls_step_normal(j, e, lam)) < 1e-9


def test_step_minimizes_damped_objective():
    rng = random.Random(2)
    for m, n in ((2, 3), (3, 3), (6, 7), (3, 2)):
        for _ in range(10):
            j = rand_matrix(rng, m, n)
            e = [rng.uniform(-1.0, 1.0) for _ in range(m)]
            lam = rng.uniform(0.05, 1.0)
            dq = dls_step(j, e, lam)
            best = objective(j, e, lam, dq)
            # The gradient J^T (J dq - e) + lam^2 dq is zero.
            r = rbm.sub(rbm.matvec(j, dq), e)
            grad = [g + lam * lam * d for g, d in zip(rbm.matvec(rbm.transpose(j), r), dq)]
            assert rbm.norm(grad) < 1e-10
            # No random perturbation does better.
            for _ in range(50):
                s = rng.choice((1e-3, 1e-1, 1.0))
                trial = [d + rng.uniform(-s, s) for d in dq]
                assert objective(j, e, lam, trial) >= best - 1e-12


def test_step_bound():
    rng = random.Random(3)
    for _ in range(200):
        m, n = rng.choice(((2, 2), (2, 3), (3, 6), (6, 6)))
        if rng.random() < 0.5:
            j = rand_matrix(rng, m, n)
        else:
            # rank one, so that J J^T is singular
            u = [rng.uniform(-3.0, 3.0) for _ in range(m)]
            v = [rng.uniform(-3.0, 3.0) for _ in range(n)]
            j = [[a * b for b in v] for a in u]
        e = [rng.uniform(-1.0, 1.0) for _ in range(m)]
        lam = rng.uniform(0.01, 1.0)
        assert rbm.norm(dls_step(j, e, lam)) <= rbm.norm(e) / (2.0 * lam) * (1.0 + 1e-9)
    # The bound is reached: one singular value equal to lam, and e along it.
    j = [[0.3, 0.0], [0.0, 2.0]]
    dq = dls_step(j, [1.0, 0.0], 0.3)
    assert abs(rbm.norm(dq) - 1.0 / 0.6) < 1e-12


def test_small_lambda_gives_pseudoinverse():
    rng = random.Random(4)
    for m, n in ((2, 2), (2, 3), (3, 5), (6, 7)):
        for _ in range(5):
            j = rand_matrix(rng, m, n)
            e = [rng.uniform(-1.0, 1.0) for _ in range(m)]
            ref = rbm.matvec(rbm.pinv_right(j), e)
            assert maxdiff(dls_step(j, e, 1e-7), ref) < 1e-6 * (1.0 + rbm.norm(ref))


L2 = [1.0, 1.0]


def fk2(q):
    return planar_fk(L2, q)


def jac2(q):
    return planar_jacobian(L2, q)


def test_planar_jacobian_against_finite_differences():
    rng = random.Random(5)
    lengths = [1.0, 0.8, 0.5, 0.3]
    for _ in range(10):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(4)]
        num = rbm.num_jacobian(lambda x: planar_fk(lengths, x), q, 1e-6)
        got = planar_jacobian(lengths, q)
        assert max(abs(a - b) for ra, rb in zip(num, got) for a, b in zip(ra, rb)) < 1e-6
    j = jac2([0.0, math.pi / 2.0])
    assert maxdiff(j[0] + j[1], [-1.0, -1.0, 1.0, 0.0]) < 1e-15
    assert maxdiff(fk2([0.0, math.pi / 2.0]), [1.0, 1.0]) < 1e-15


def test_example_of_the_page():
    q = [0.0, 0.01]
    e = rbm.sub([1.9, 0.2], fk2(q))
    j = jac2(q)
    newton = rbm.solve(j, e)
    assert maxdiff(newton, [-9.804667, 19.799833]) < 1e-6
    dq = dls_step(j, e, 0.1)
    assert maxdiff(dq, [0.056365, 0.077488]) < 1e-6
    assert rbm.norm(dq) <= rbm.norm(e) / 0.2
    q, hist, ok = ik_dls(fk2, jac2, [1.0, 1.0], [0.3, 1.2], 0.1)
    assert ok and len(hist) == 8
    for got, want in zip(hist, [0.294, 0.0415, 0.00138, 3.45e-5]):
        assert abs(got - want) < 0.005 * want
    assert maxdiff(q, [0.0, math.pi / 2.0]) < 1e-10
    q, hist, ok = ik_dls(fk2, jac2, [1.0, 1.0], [0.3, 1.2], 0.5)
    assert ok and len(hist) == 25


def test_local_linear_rate():
    # Near the solution (0, pi/2), the error ratio tends to lam^2 / (s^2 + lam^2), s the least singular value.
    s2 = (3.0 - math.sqrt(5.0)) / 2.0
    for lam in (0.1, 0.5):
        _, hist, ok = ik_dls(fk2, jac2, [1.0, 1.0], [0.3, 1.2], lam)
        assert ok
        rate = lam * lam / (s2 + lam * lam)
        ratios = [b / a for a, b in zip(hist, hist[1:]) if 1e-9 < b and a < 1e-3]
        assert ratios and all(abs(r - rate) < 0.02 * rate for r in ratios)


def test_random_reachable_targets():
    rng = random.Random(6)
    lengths = [1.0, 0.8, 0.5]
    for _ in range(30):
        q_star = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        x_d = planar_fk(lengths, q_star)
        q0 = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        q, hist, ok = ik_dls(lambda x: planar_fk(lengths, x), lambda x: planar_jacobian(lengths, x), x_d, q0, 0.1, max_iter=2000)
        assert ok
        assert maxdiff(planar_fk(lengths, q), x_d) < 1e-9


def test_out_of_reach():
    # With lam = 0.5 the arm stretches toward the target and stops at the nearest point.
    q, hist, ok = ik_dls(fk2, jac2, [2.5, 0.0], [0.2, 0.5], 0.5, max_iter=200)
    assert not ok
    assert abs(hist[-1] - 0.5) < 1e-12
    assert maxdiff(fk2(q), [2.0, 0.0]) < 1e-12
    # Every step stays bounded by |e| / (2 lam).
    q = [0.2, 0.5]
    for _ in range(50):
        e = rbm.sub([2.5, 0.0], fk2(q))
        dq = dls_step(jac2(q), e, 0.1)
        assert rbm.norm(dq) <= rbm.norm(e) / 0.2 * (1.0 + 1e-9)
        q = [a + b for a, b in zip(q, dq)]
