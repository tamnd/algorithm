# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/task-priority-inverse-kinematics/. The authors are listed in prov/791J72.jsonl.
"""Tests of task-priority inverse kinematics: the pseudoinverse against the
four Penrose conditions, the step against the closed two-task formula and
against random perturbations in the null space, strict priority in a stack
of three tasks, and the 3R example of the page against a brute force search
over the self-motion of the arm."""

import math
import random

from task_priority_inverse_kinematics import eye, ik_task_priority, matvec, mul, norm, pinv, priority_step, svd, transpose


def rand_matrix(rng, m, n, rank=None):
    if rank is None:
        return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]
    a = [[rng.uniform(-1.0, 1.0) for _ in range(rank)] for _ in range(m)]
    b = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(rank)]
    return mul(a, b)


def mdiff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def vdiff(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def test_svd_and_penrose_conditions():
    rng = random.Random(1)
    for m, n, rank in ((2, 3, None), (3, 2, None), (4, 4, None), (3, 5, 2), (5, 3, 1), (6, 7, None), (2, 3, 1)):
        for _ in range(5):
            a = rand_matrix(rng, m, n, rank)
            u, s, v = svd(a)
            rec = [[sum(sk * uk[i] * vk[j] for uk, sk, vk in zip(u, s, v)) for j in range(n)] for i in range(m)]
            assert mdiff(rec, a) < 1e-12
            x = pinv(a)
            assert mdiff(mul(mul(a, x), a), a) < 1e-10
            assert mdiff(mul(mul(x, a), x), x) < 1e-9
            ax, xa = mul(a, x), mul(x, a)
            assert mdiff(ax, transpose(ax)) < 1e-10
            assert mdiff(xa, transpose(xa)) < 1e-10
    # Full row rank: J^+ = J^T (J J^T)^-1, checked on a 2 by 3 matrix with the explicit 2 by 2 inverse.
    a = [[1.0, 2.0, 0.5], [0.0, 1.0, -1.0]]
    g = mul(a, transpose(a))
    d = g[0][0] * g[1][1] - g[0][1] * g[1][0]
    ginv = [[g[1][1] / d, -g[0][1] / d], [-g[1][0] / d, g[0][0] / d]]
    assert mdiff(pinv(a), mul(transpose(a), ginv)) < 1e-12


def test_two_tasks_against_the_closed_formula():
    rng = random.Random(2)
    n = 6
    for m1, m2 in ((2, 2), (3, 2), (2, 3), (3, 3)):
        for _ in range(10):
            j1, j2 = rand_matrix(rng, m1, n), rand_matrix(rng, m2, n)
            e1 = [rng.uniform(-1.0, 1.0) for _ in range(m1)]
            e2 = [rng.uniform(-1.0, 1.0) for _ in range(m2)]
            j1p = pinv(j1)
            p1 = [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(eye(n), mul(j1p, j1))]
            ref = [a + b for a, b in zip(matvec(j1p, e1), matvec(pinv(mul(j2, p1)), sub(e2, matvec(j2, matvec(j1p, e1)))))]
            dq = priority_step([(j1, e1), (j2, e2)])
            assert vdiff(dq, ref) < 1e-10
            # The first task is met exactly.
            assert vdiff(matvec(j1, dq), e1) < 1e-10


def null_basis(a, n):
    """Return an orthonormal basis of the null space of a, from the SVD of a."""
    u, s, v = svd(a)
    smax = max(s)
    return [vk for sk, vk in zip(s, v) if sk <= 1e-10 * smax]


def test_second_task_is_best_in_the_null_space():
    rng = random.Random(3)
    n = 6
    for _ in range(20):
        j1, j2 = rand_matrix(rng, 2, n), rand_matrix(rng, 3, n)
        e1 = [rng.uniform(-1.0, 1.0) for _ in range(2)]
        e2 = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        dq = priority_step([(j1, e1), (j2, e2)])
        best = norm(sub(matvec(j2, dq), e2))
        basis = null_basis(j1 + [[0.0] * n for _ in range(n - 2)], n)
        assert len(basis) == n - 2
        for _ in range(100):
            s = rng.choice((1e-3, 1e-1, 1.0))
            trial = list(dq)
            for b in basis:
                z = rng.uniform(-s, s)
                trial = [t + z * x for t, x in zip(trial, b)]
            assert vdiff(matvec(j1, trial), e1) < 1e-9
            assert norm(sub(matvec(j2, trial), e2)) >= best - 1e-12


def test_strict_priority_in_a_stack():
    rng = random.Random(4)
    n = 7
    for _ in range(10):
        tasks = [(rand_matrix(rng, m, n), [rng.uniform(-1.0, 1.0) for _ in range(m)]) for m in (2, 3, 3)]
        full = priority_step(tasks)
        for k in (1, 2):
            part = priority_step(tasks[:k])
            for j, _ in tasks[:k]:
                assert vdiff(matvec(j, full), matvec(j, part)) < 1e-9


LENGTHS = [1.0, 0.8, 0.5]


def fk(q):
    x = y = a = 0.0
    for length, t in zip(LENGTHS, q):
        a += t
        x += length * math.cos(a)
        y += length * math.sin(a)
    return [x, y]


def jac(q):
    ang = []
    a = 0.0
    for t in q:
        a += t
        ang.append(a)
    return [[-sum(LENGTHS[k] * math.sin(ang[k]) for k in range(i, 3)) for i in range(3)],
            [sum(LENGTHS[k] * math.cos(ang[k]) for k in range(i, 3)) for i in range(3)]]


def elbow(q):
    return [LENGTHS[0] * math.cos(q[0]), LENGTHS[0] * math.sin(q[0])]


def jac_elbow(q):
    return [[-LENGTHS[0] * math.sin(q[0]), 0.0, 0.0], [LENGTHS[0] * math.cos(q[0]), 0.0, 0.0]]


X_D = [1.2, 0.6]


def start_on_target():
    """A joint vector with the hand on X_D and q1 = 0."""
    dx, dy = X_D[0] - LENGTHS[0], X_D[1]
    c3 = (dx * dx + dy * dy - LENGTHS[1] ** 2 - LENGTHS[2] ** 2) / (2.0 * LENGTHS[1] * LENGTHS[2])
    q3 = math.acos(c3)
    q2 = math.atan2(dy, dx) - math.atan2(LENGTHS[2] * math.sin(q3), LENGTHS[1] + LENGTHS[2] * math.cos(q3))
    return [0.0, q2, q3]


def brute_force_elbow(c, steps=20000):
    """Least elbow error over the self-motion: q1 on a grid, the rest a 2R arm that must reach X_D.

    The best grid cell is refined by a ternary search, since the error is unimodal there.
    """
    def feasible(a):
        d = math.hypot(X_D[0] - LENGTHS[0] * math.cos(a), X_D[1] - LENGTHS[0] * math.sin(a))
        return abs(LENGTHS[1] - LENGTHS[2]) <= d <= LENGTHS[1] + LENGTHS[2]

    def err(a):
        return math.hypot(LENGTHS[0] * math.cos(a) - c[0], LENGTHS[0] * math.sin(a) - c[1])

    h = 2.0 * math.pi / steps
    best = min((err(a), a) for a in (-math.pi + h * i for i in range(steps)) if feasible(a))
    lo, hi = best[1] - h, best[1] + h
    for _ in range(60):
        m1, m2 = lo + (hi - lo) / 3.0, hi - (hi - lo) / 3.0
        if err(m1) < err(m2):
            hi = m2
        else:
            lo = m1
    a = 0.5 * (lo + hi)
    assert feasible(a)
    return err(a), a


def test_example_of_the_page():
    q0 = start_on_target()
    assert vdiff(q0, [0.0, 0.574014, 2.230016]) < 1e-6
    assert vdiff(fk(q0), X_D) < 1e-12
    c = [0.5 * math.cos(0.5), 0.5 * math.sin(0.5)]
    q = q0
    errs = []
    for _ in range(2):
        stack = [(jac(q), sub(X_D, fk(q))), (jac_elbow(q), sub(c, elbow(q)))]
        q = [a + b for a, b in zip(q, priority_step(stack))]
        errs.append((norm(sub(X_D, fk(q))), norm(sub(c, elbow(q)))))
    assert vdiff(q, [0.368392, -0.030953, 2.862660]) < 1e-6
    assert vdiff(errs[0], [0.0139, 0.532620]) < 1e-4
    q, steps = ik_task_priority([(fk, jac, X_D), (elbow, jac_elbow, c)], q0)
    assert steps == 42
    assert vdiff(q, [0.5, -0.536467, 2.873908]) < 1e-6
    assert norm(sub(X_D, fk(q))) < 1e-12
    err, a = brute_force_elbow(c)
    assert abs(norm(sub(c, elbow(q))) - err) < 1e-8 and abs(q[0] - a) < 1e-4


def test_other_secondary_targets_against_brute_force():
    for r, phi in ((0.3, 1.0), (0.6, -0.3), (0.5, 1.4)):
        c = [r * math.cos(phi), r * math.sin(phi)]
        q, steps = ik_task_priority([(fk, jac, X_D), (elbow, jac_elbow, c)], start_on_target(), max_iter=2000)
        assert steps < 2000
        assert norm(sub(X_D, fk(q))) < 1e-12
        err, a = brute_force_elbow(c)
        assert abs(norm(sub(c, elbow(q))) - err) < 1e-8
        assert abs(math.remainder(q[0] - a, 2.0 * math.pi)) < 1e-4


def wrist(q):
    """The end of link 2."""
    a1, a2 = q[0], q[0] + q[1]
    return [LENGTHS[0] * math.cos(a1) + LENGTHS[1] * math.cos(a2), LENGTHS[0] * math.sin(a1) + LENGTHS[1] * math.sin(a2)]


def jac_wrist(q):
    a1, a2 = q[0], q[0] + q[1]
    s1, c1, s2, c2 = math.sin(a1), math.cos(a1), math.sin(a2), math.cos(a2)
    return [[-LENGTHS[0] * s1 - LENGTHS[1] * s2, -LENGTHS[1] * s2, 0.0], [LENGTHS[0] * c1 + LENGTHS[1] * c2, LENGTHS[1] * c2, 0.0]]


def test_coupled_secondary_task():
    # The end of link 2 must lie on the circle of radius 0.5 about X_D; the best point is the one nearest to c.
    c = [0.5, 0.5]
    d = sub(c, X_D)
    best = [x + LENGTHS[2] * y / norm(d) for x, y in zip(X_D, d)]
    q, steps = ik_task_priority([(fk, jac, X_D), (wrist, jac_wrist, c)], start_on_target(), max_iter=2000)
    assert steps < 2000
    assert norm(sub(X_D, fk(q))) < 1e-12
    assert vdiff(wrist(q), best) < 1e-8
    # One pseudoinverse of the stacked Jacobian gives a compromise instead: the hand misses its target.
    q = start_on_target()
    for _ in range(300):
        j = jac(q) + jac_wrist(q)
        e = sub(X_D, fk(q)) + sub(c, wrist(q))
        q = [a + b for a, b in zip(q, matvec(pinv(j), e))]
    assert norm(sub(X_D, fk(q))) > 1e-2
