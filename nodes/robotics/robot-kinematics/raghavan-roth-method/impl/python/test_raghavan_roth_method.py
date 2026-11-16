# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raghavan-roth-method/. The authors are listed in prov/MTT21K.jsonl.
"""Tests of the elimination of Raghavan and Roth on the 3R position problem:
the determinant of the dialytic matrix against the product of the extraneous
factor and the quartic found by hand, the example of the page, every root
checked by forward kinematics, and the solution set against a brute force
of Newton's method from many starts."""

import math
import random

from raghavan_roth_method import (
    coefficient_polys, dialytic_matrix, direct_quartic, exact_divide, extraneous_factor, fk, peval,
    pmul, poly_det, pscale, roots, solve_3r)


def rand_arm(rng):
    return [(rng.uniform(0.2, 1.5), rng.uniform(-3.0, 3.0), rng.uniform(-1.0, 1.0)) for _ in range(3)]


def same(q, r, tol=1e-6):
    return max(abs(math.remainder(a - b, 2.0 * math.pi)) for a, b in zip(q, r)) < tol


def test_polynomial_helpers():
    a = [1.0, -3.0, 2.0]  # 2x^2 - 3x + 1 = (2x - 1)(x - 1)
    zs = sorted(z.real for z in roots(a))
    assert abs(zs[0] - 0.5) < 1e-12 and abs(zs[1] - 1.0) < 1e-12
    b = [2.0, 0.0, 1.0]
    q, res = exact_divide(pmul(a, b), b)
    assert max(abs(x - y) for x, y in zip(q, a)) < 1e-12 and res < 1e-12


def test_determinant_is_four_times_extraneous_factor_times_quartic():
    rng = random.Random(1)
    for _ in range(30):
        dh = rand_arm(rng)
        p = fk(dh, [rng.uniform(-3.0, 3.0) for _ in range(3)])
        delta = poly_det(dialytic_matrix(dh, p))
        assert len(delta) == 9  # degree 8
        prod = pscale(4.0, pmul(extraneous_factor(dh, p), direct_quartic(dh, p)))
        scale = max(abs(c) for c in delta)
        assert max(abs(x - y) for x, y in zip(delta, prod)) < 1e-10 * scale
        # The extraneous factor (1 + x3^2)^2 (h1^2 + h2^2) has no real root for these arms.
        e = extraneous_factor(dh, p)
        assert min(peval(e, -10.0 + 0.01 * k) for k in range(2001)) > 0.0


def test_example_of_the_page():
    dh = [(0.5, 2.0 * math.pi / 3.0, 0.5), (0.5, math.pi / 6.0, 1.0), (1.5, 0.0, 0.0)]
    p = fk(dh, [1.0, -0.5, -1.0])
    assert max(abs(a - b) for a, b in zip(p, [0.209252, 1.203738, -1.059310])) < 1e-6
    e = extraneous_factor(dh, p)
    assert max(abs(a - b) for a, b in zip(e, [4.0, 0.0, 2.75, 0.0, 1.0])) < 1e-12
    delta = poly_det(dialytic_matrix(dh, p))
    quartic, res = exact_divide(delta, pscale(4.0, e))
    assert res < 1e-10
    assert max(abs(a - b) for a, b in zip(quartic, [-0.559587, 4.377061, 4.164800, -9.122939, 2.474388])) < 1e-6
    sols = sorted(solve_3r(dh, p), key=lambda q: math.tan(q[2] / 2.0))
    assert len(sols) == 4
    expect = [[1.0, -0.5, -1.0], [-2.125286, -2.692609, 0.234761], [-2.873565, 2.405672, 1.757909], [2.098607, 2.860655, 2.479220]]
    for q, r in zip(sols, expect):
        assert same(q, r, 1e-6)
    xs = [math.tan(q[2] / 2.0) for q in sols]
    assert max(abs(a - b) for a, b in zip(xs, [-0.546302, 0.117923, 1.207093, 2.908236])) < 1e-6


def newton_solutions(dh, p, rng, starts=30):
    """Brute force: Newton's method on fk(q) = p from many random starts."""
    found = []
    for _ in range(starts):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        for _ in range(25):
            f = [a - b for a, b in zip(fk(dh, q), p)]
            if max(abs(x) for x in f) < 1e-13:
                break
            h = 1e-7
            cols = []
            for j in range(3):
                qp, qm = list(q), list(q)
                qp[j] += h
                qm[j] -= h
                cols.append([(a - b) / (2.0 * h) for a, b in zip(fk(dh, qp), fk(dh, qm))])
            jm = [[cols[j][i] for j in range(3)] for i in range(3)]
            det = (jm[0][0] * (jm[1][1] * jm[2][2] - jm[1][2] * jm[2][1])
                   - jm[0][1] * (jm[1][0] * jm[2][2] - jm[1][2] * jm[2][0])
                   + jm[0][2] * (jm[1][0] * jm[2][1] - jm[1][1] * jm[2][0]))
            if abs(det) < 1e-12:
                break
            # Cramer's rule for jm dq = -f.
            dq = []
            for j in range(3):
                mj = [row[:] for row in jm]
                for i in range(3):
                    mj[i][j] = -f[i]
                dj = (mj[0][0] * (mj[1][1] * mj[2][2] - mj[1][2] * mj[2][1])
                      - mj[0][1] * (mj[1][0] * mj[2][2] - mj[1][2] * mj[2][0])
                      + mj[0][2] * (mj[1][0] * mj[2][1] - mj[1][1] * mj[2][0]))
                dq.append(dj / det)
            q = [a + b for a, b in zip(q, dq)]
        if max(abs(a - b) for a, b in zip(fk(dh, q), p)) < 1e-10:
            q = [math.remainder(x, 2.0 * math.pi) for x in q]
            if all(not same(q, r) for r in found):
                found.append(q)
    return found


def test_against_newton_from_many_starts():
    rng = random.Random(2)
    counts = {}
    for _ in range(8):
        dh = rand_arm(rng)
        q_true = [rng.uniform(-3.0, 3.0) for _ in range(3)]
        p = fk(dh, q_true)
        sols = solve_3r(dh, p)
        assert 1 <= len(sols) <= 4
        counts[len(sols)] = counts.get(len(sols), 0) + 1
        for q in sols:
            assert max(abs(a - b) for a, b in zip(fk(dh, q), p)) < 1e-9
        assert any(same(q, q_true) for q in sols)
        brute = newton_solutions(dh, p, rng)
        # Every solution that Newton finds is one of ours, and with 30 starts Newton finds them all here.
        for q in brute:
            assert any(same(q, r) for r in sols)
        assert len(brute) == len(sols)
    assert counts.get(4, 0) >= 1 and counts.get(2, 0) >= 1


def test_back_substitution_satisfies_both_equations():
    rng = random.Random(3)
    for _ in range(20):
        dh = rand_arm(rng)
        p = fk(dh, [rng.uniform(-3.0, 3.0) for _ in range(3)])
        for q in solve_3r(dh, p):
            x3 = math.tan(q[2] / 2.0)
            w = 1.0 + x3 * x3
            p1, q1, k, p2, q2, ell = (peval(c, x3) / w for c in coefficient_polys(dh, p)[:6])
            c2, s2 = math.cos(q[1]), math.sin(q[1])
            assert abs(p1 * c2 + q1 * s2 + k) < 1e-9
            assert abs(p2 * c2 + q2 * s2 + ell) < 1e-9
