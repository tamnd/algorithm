# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kleinman-iteration/. The authors are listed in prov/1GNVWG.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
from kleinman_iteration import care_residual, dare_residual, hewer, kleinman, lyap, stein


def maxabs(a):
    return max(abs(v) for row in a for v in row)


def is_psd_exact(m):
    """All principal minors of an exact symmetric matrix are at least 0."""
    n = len(m)
    if any(m[i][j] != m[j][i] for i in range(n) for j in range(n)):
        return False
    for size in range(1, n + 1):
        for idx in itertools.combinations(range(n), size):
            if cm.det([[m[i][j] for j in idx] for i in idx]) < 0:
                return False
    return True


def match(xs, ys, tol):
    rest = list(ys)
    for x in xs:
        y = min(rest, key=lambda v: abs(v - x))
        if abs(y - x) > tol * (1 + abs(x)):
            return False
        rest.remove(y)
    return not rest


def hurwitz(m):
    return all(e.real < 0 for e in cm.polyroots(cm.charpoly(m)))


def schur_stable(m):
    return all(abs(e) < 1 for e in cm.polyroots(cm.charpoly(m)))


def rand_mat(rng, n, m, lo=-2.0, hi=2.0):
    return [[rng.uniform(lo, hi) for _ in range(m)] for _ in range(n)]


def rand_pd(rng, n, shift):
    c = rand_mat(rng, n, n, -1.0, 1.0)
    return cm.add(cm.mul(cm.transpose(c), c), cm.scale(shift, cm.eye(n)))


def hamiltonian(A, B, Q, R):
    g = cm.mul(B, cm.solve(R, cm.transpose(B)))
    return cm.block([[A, cm.scale(-1, g)], [cm.scale(-1, Q), cm.scale(-1, cm.transpose(A))]])


def random_problem(rng):
    """A random CARE with a stabilizing K0; half of the plants are unstable."""
    n = rng.randint(1, 3)
    A = rand_mat(rng, n, n)
    if rng.random() < 0.5:
        m = rng.randint(1, 2)
        s = max(sum(abs(v) for v in row) for row in A) + 0.3
        A = cm.sub(A, cm.scale(s, cm.eye(n)))
        B = rand_mat(rng, n, m)
        K0 = cm.zeros(m, n)
    else:
        m = n
        B = cm.add(cm.eye(n), rand_mat(rng, n, n, -0.3, 0.3))
        K0 = cm.solve(B, cm.add(A, cm.eye(n)))
    return A, B, rand_pd(rng, n, 0.1), rand_pd(rng, m, 0.5), K0


def test_double_integrator_exact():
    A, B, Q, R = [[0, 1], [0, 0]], [[0], [1]], cm.eye(2), [[1]]
    P, K, Ps = kleinman(A, B, Q, R, [[1, 1]], steps=4)
    diag = [p[0][0] for p in Ps]
    assert diag == [2, Fraction(7, 4), Fraction(97, 56), Fraction(18817, 10864)]
    assert all(p[0][1] == 1 and p[1][0] == 1 and p[1][1] == p[0][0] for p in Ps)
    assert K == [[1, Fraction(18817, 10864)]]
    # Newton's method for x^2 = 3 from 2 gives the same numbers.
    x = Fraction(2)
    for d in diag:
        assert d == x
        x = (x + 3 / x) / 2


def test_scalar_discrete_fibonacci():
    P, K, Ps = hewer([[1]], [[1]], [[1]], [[1]], [[1]], steps=4)
    assert [p[0][0] for p in Ps] == [2, Fraction(13, 8), Fraction(610, 377), Fraction(1346269, 832040)]
    golden = (1 + math.sqrt(5)) / 2
    assert abs(float(P[0][0]) - golden) < 1e-12


def test_quadratic_convergence():
    A, B, Q, R = [[0.0, 1.0], [0.0, 0.0]], [[0.0], [1.0]], cm.eye(2), [[1.0]]
    r3 = math.sqrt(3.0)
    P, K, Ps = kleinman(A, B, Q, R, [[1.0, 1.0]])
    errs = [maxabs(cm.sub(p, [[r3, 1.0], [1.0, r3]])) for p in Ps]
    assert errs[-1] <= 1e-15
    for e0, e1 in zip(errs, errs[1:]):
        assert e1 <= 0.3 * e0 * e0 + 1e-15
    assert len(Ps) <= 7


def test_lyap_and_stein():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 4)
        F = rand_mat(rng, n, n)
        s = max(sum(abs(v) for v in row) for row in F) + 0.1
        Fh = cm.sub(F, cm.scale(s, cm.eye(n)))
        W = rand_pd(rng, n, 0.0)
        X = lyap(Fh, W)
        assert maxabs(cm.add(cm.add(cm.mul(cm.transpose(Fh), X), cm.mul(X, Fh)), W)) <= 1e-10 * (1 + maxabs(X))
        Fs = cm.scale(0.9 / s, F)
        Y = stein(Fs, W)
        assert maxabs(cm.sub(cm.add(cm.mul(cm.transpose(Fs), cm.mul(Y, Fs)), W), Y)) <= 1e-10 * (1 + maxabs(Y))


def test_exact_monotone_and_stabilizing():
    rng = random.Random(17)
    for _ in range(40):
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        s = max(sum(abs(v) for v in row) for row in A) + 1
        A = cm.sub(A, cm.scale(s, cm.eye(n)))
        B = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
        C = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        Q = cm.add(cm.mul(cm.transpose(C), C), cm.eye(n))
        R = [[rng.randint(1, 3) if i == j else 0 for j in range(m)] for i in range(m)]
        P, K, Ps = kleinman(A, B, Q, R, cm.zeros(m, n), steps=3)
        Pf, _, _ = kleinman([[float(v) for v in row] for row in A], B, Q, R, cm.zeros(m, n))
        Ks = [cm.zeros(m, n)] + [cm.solve(R, cm.mul(cm.transpose(B), p)) for p in Ps]
        for p, k in zip(Ps, Ks):
            assert all(isinstance(v, Fraction) for row in p for v in row)
            assert hurwitz(cm.sub(A, cm.mul(B, k)))
            assert all(v >= -1e-12 for v in vec_minors(cm.sub(p, Pf)))
        for p0, p1 in zip(Ps, Ps[1:]):
            assert is_psd_exact(cm.sub(p0, p1))


def vec_minors(m):
    n = len(m)
    out = []
    for size in range(1, n + 1):
        for idx in itertools.combinations(range(n), size):
            out.append(cm.det([[float(m[i][j]) for j in idx] for i in idx]))
    return out


def test_random_care_against_hamiltonian():
    rng = random.Random(2025)
    for _ in range(400):
        A, B, Q, R, K0 = random_problem(rng)
        P, K, Ps = kleinman(A, B, Q, R, K0)
        assert len(Ps) < 50
        assert maxabs(care_residual(A, B, Q, R, P)) <= 1e-9 * (1 + maxabs(P)) ** 2 * (1 + maxabs(A) + maxabs(B) ** 2)
        assert cm.is_pos_def(P)
        acl = cm.sub(A, cm.mul(B, K))
        eigs = cm.polyroots(cm.charpoly(acl))
        assert all(e.real < 0 for e in eigs)
        hroots = cm.polyroots(cm.charpoly(hamiltonian(A, B, Q, R)))
        assert match(eigs, [r for r in hroots if r.real < 0], 1e-6)
        for p0, p1 in zip(Ps, Ps[1:]):
            d = cm.sub(p0, p1)
            assert min(cm._sym_eigvals(d)) >= -1e-9 * (1 + maxabs(p0))


def test_random_dare_against_recursion():
    rng = random.Random(8)
    for _ in range(100):
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A = rand_mat(rng, n, n, -1.0, 1.0)
        s = max(sum(abs(v) for v in row) for row in A)
        A = cm.scale(rng.uniform(0.2, 1.6) / max(s, 1e-9), A)
        B = rand_mat(rng, n, m)
        Q, R = rand_pd(rng, n, 0.2), rand_pd(rng, m, 0.5)
        if not schur_stable(A):
            continue
        P, K, Ps = hewer(A, B, Q, R, cm.zeros(m, n))
        ref = cm.zeros(n)
        for _ in range(3000):
            pb = cm.mul(ref, B)
            k = cm.solve(cm.add(R, cm.mul(cm.transpose(B), pb)), cm.mul(cm.transpose(pb), A))
            new = cm.sub(cm.add(Q, cm.mul(cm.transpose(A), cm.mul(ref, A))), cm.mul(cm.transpose(A), cm.mul(pb, k)))
            done = maxabs(cm.sub(new, ref)) <= 1e-15 * maxabs(new)
            ref = new
            if done:
                break
        assert maxabs(cm.sub(P, ref)) <= 1e-8 * max(1.0, maxabs(ref))
        assert maxabs(dare_residual(A, B, Q, R, P)) <= 1e-9 * max(1.0, maxabs(P))
        assert schur_stable(cm.sub(A, cm.mul(B, K)))


def test_unstable_start_raises():
    with pytest.raises(ValueError):
        kleinman([[0, 1], [0, 0]], [[0], [1]], cm.eye(2), [[1]], [[0, 0]])
    with pytest.raises(ValueError):
        kleinman([[1]], [[1]], [[1]], [[1]], [[1]])
    with pytest.raises(ValueError):
        hewer([[2]], [[1]], [[1]], [[1]], [[0]])
