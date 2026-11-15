# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schur-method-riccati/. The authors are listed in prov/TKPRJX.jsonl.

import cmath
import math
import random

import pytest

import ctlmat as cm
from schur_method_riccati import (
    care_residual, care_schur, dare_residual, dare_schur, hamiltonian, reorder, schur_form, swap, symplectic,
)

R3 = math.sqrt(3.0)


def ctrans(a):
    return [[v.conjugate() if isinstance(v, complex) else v for v in row] for row in cm.transpose(a)]


def maxabs(a):
    return max(abs(v) for row in a for v in row)


def fro(a):
    return math.sqrt(sum(abs(v) ** 2 for row in a for v in row))


def check_schur(M, T, Z, tol):
    n = len(M)
    scale = max(fro(M), 1.0)
    assert maxabs(cm.sub(cm.mul(ctrans(Z), Z), cm.eye(n))) <= tol
    assert maxabs(cm.sub(cm.mul(Z, cm.mul(T, ctrans(Z))), M)) <= tol * scale
    assert all(T[i][j] == 0 for i in range(n) for j in range(i))


def match(xs, ys, tol):
    """Return True if the two lists of complex numbers are equal as multisets, within tol."""
    rest = list(ys)
    for x in xs:
        y = min(rest, key=lambda v: abs(v - x))
        if abs(y - x) > tol * (1 + abs(x)):
            return False
        rest.remove(y)
    return not rest


def rand_mat(rng, n, m, lo=-2.0, hi=2.0):
    return [[rng.uniform(lo, hi) for _ in range(m)] for _ in range(n)]


def rand_pd(rng, n, shift):
    c = rand_mat(rng, n, n, -1.0, 1.0)
    return cm.add(cm.mul(cm.transpose(c), c), cm.scale(shift, cm.eye(n)))


def newton_care(A, B, Q, R):
    """Reference: Newton's method on the CARE from K = 0 (A must be Hurwitz).

    Each step solves the Lyapunov equation by its Kronecker form.
    """
    n, m = len(A), len(B[0])
    K = cm.zeros(m, n)
    P = cm.zeros(n)
    for _ in range(60):
        acl = cm.sub(A, cm.mul(B, K))
        w = cm.add(Q, cm.mul(cm.transpose(K), cm.mul(R, K)))
        act = cm.transpose(acl)
        big = cm.add(cm.kron(cm.eye(n), act), cm.kron(act, cm.eye(n)))
        new = cm.unvec(cm.solve(big, [-v for v in cm.vec(w)]), n)
        done = maxabs(cm.sub(new, P)) <= 1e-14 * max(1.0, maxabs(new))
        P = new
        K = cm.solve(R, cm.mul(cm.transpose(B), P))
        if done:
            break
    return P


def riccati_iteration(A, B, Q, R, steps):
    """Reference: the backward Riccati recursion of the DARE from P = 0."""
    n = len(A)
    P = cm.zeros(n)
    at = cm.transpose(A)
    for _ in range(steps):
        pb = cm.mul(P, B)
        k = cm.solve(cm.add(R, cm.mul(cm.transpose(B), pb)), cm.mul(cm.transpose(pb), A))
        new = cm.sub(cm.add(Q, cm.mul(at, cm.mul(P, A))), cm.mul(at, cm.mul(pb, k)))
        new = [[(new[i][j] + new[j][i]) / 2 for j in range(n)] for i in range(n)]
        if maxabs(cm.sub(new, P)) <= 1e-15 * maxabs(new):
            return new
        P = new
    return P


def test_double_integrator_and_scalar():
    P, K = care_schur([[0, 1], [0, 0]], [[0], [1]], cm.eye(2), [[1]])
    assert maxabs(cm.sub(P, [[R3, 1.0], [1.0, R3]])) <= 1e-12
    assert maxabs(cm.sub(K, [[1.0, R3]])) <= 1e-12
    P, K = care_schur([[1]], [[1]], [[1]], [[1]])
    assert abs(P[0][0] - (1 + math.sqrt(2))) <= 1e-12
    # (a, b) = (-1, 0) is stabilizable but not controllable: P solves -2 p + q = 0.
    P, K = care_schur([[-1]], [[0]], [[3]], [[1]])
    assert abs(P[0][0] - 1.5) <= 1e-12 and K[0][0] == 0


def test_dare_examples():
    P, K = dare_schur([[1]], [[1]], [[1]], [[1]])
    assert abs(P[0][0] - (1 + math.sqrt(5)) / 2) <= 1e-12
    P, K = dare_schur([[2]], [[1]], [[1]], [[1]])
    assert abs(P[0][0] - (2 + math.sqrt(5))) <= 1e-12
    A, B = [[1, 1], [0, 1]], [[0.5], [1]]
    P, K = dare_schur(A, B, cm.eye(2), [[1]])
    assert maxabs(cm.sub(P, [[2.367101490947877, math.sqrt(5) / 2], [math.sqrt(5) / 2, 2.587482927325332]])) <= 1e-11
    assert maxabs(dare_residual(A, B, cm.eye(2), [[1]], P)) <= 1e-12


def test_swap_and_reorder():
    T = [[1 + 0j, 2 + 0j], [0j, 3 + 0j]]
    Z = [[1 + 0j, 0j], [0j, 1 + 0j]]
    M = [[1.0, 2.0], [0.0, 3.0]]
    swap(T, Z, 0)
    assert T[0][0] == 3 and T[1][1] == 1
    check_schur(M, T, Z, 1e-14)
    rng = random.Random(11)
    for _ in range(50):
        n = rng.randint(2, 6)
        M = rand_mat(rng, n, n)
        T, Z = schur_form(M)
        diag = [T[i][i] for i in range(n)]
        count = reorder(T, Z, lambda d: d.real < 0)
        check_schur(M, T, Z, 1e-12)
        assert count == sum(1 for d in diag if d.real < 0)
        assert all(T[i][i].real < 0 for i in range(count))
        assert all(T[i][i].real >= 0 for i in range(count, n))
        assert match([T[i][i] for i in range(n)], diag, 1e-12)


def test_schur_form_special():
    for M in ([[0.0]], cm.zeros(3), cm.eye(3), [[0, 1], [0, 0]], [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
              [[0, -1], [1, 0]], [[2, 1, 0], [0, 2, 1], [0, 0, 2]]):
        T, Z = schur_form(M)
        check_schur(M, T, Z, 1e-13)
    T, _ = schur_form([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    roots = [cmath.exp(2j * math.pi * k / 3) for k in range(3)]
    assert match([T[i][i] for i in range(3)], roots, 1e-12)


def test_schur_form_random_against_charpoly():
    rng = random.Random(2024)
    for _ in range(100):
        n = rng.randint(1, 7)
        M = rand_mat(rng, n, n)
        if rng.random() < 0.3:
            M = [[complex(v, rng.uniform(-1, 1)) for v in row] for row in M]
        T, Z = schur_form(M)
        check_schur(M, T, Z, 1e-12)
        if all(not isinstance(v, complex) for row in M for v in row):
            assert match([T[i][i] for i in range(n)], cm.polyroots(cm.charpoly(M)), 1e-7)


def test_care_random_against_eigenvalues():
    rng = random.Random(7)
    for _ in range(250):
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A, B = rand_mat(rng, n, n), rand_mat(rng, n, m)
        Q, R = rand_pd(rng, n, 0.1), rand_pd(rng, m, 0.5)
        P0, _ = care_schur(A, B, Q, R, symmetrize=False)
        size = fro(Q) + 2 * fro(A) * fro(P0) + fro(hamiltonian(A, B, Q, R)) * fro(P0) ** 2
        assert maxabs(cm.sub(P0, cm.transpose(P0))) <= 1e-9 * max(1.0, fro(P0))
        P, K = care_schur(A, B, Q, R)
        assert maxabs(care_residual(A, B, Q, R, P)) <= 1e-9 * size
        assert cm.is_pos_def(P)
        acl = cm.sub(A, cm.mul(B, K))
        eigs = cm.polyroots(cm.charpoly(acl))
        assert all(e.real < 0 for e in eigs)
        hroots = cm.polyroots(cm.charpoly(hamiltonian(A, B, Q, R)))
        assert match(eigs, [r for r in hroots if r.real < 0], 1e-6)


def test_care_random_against_newton():
    rng = random.Random(99)
    for _ in range(250):
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A = rand_mat(rng, n, n)
        shift = max(sum(abs(v) for v in row) for row in A) + 0.2
        A = cm.sub(A, cm.scale(shift, cm.eye(n)))
        B = rand_mat(rng, n, m)
        Q, R = rand_pd(rng, n, 0.0), rand_pd(rng, m, 0.5)
        P, _ = care_schur(A, B, Q, R)
        ref = newton_care(A, B, Q, R)
        assert maxabs(cm.sub(P, ref)) <= 1e-9 * max(1.0, maxabs(ref))


def test_dare_random_against_recursion():
    rng = random.Random(5)
    done = 0
    while done < 100:
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A, B = rand_mat(rng, n, n, -1.2, 1.2), rand_mat(rng, n, m)
        if abs(cm.det(A)) < 0.05:
            continue
        Q, R = rand_pd(rng, n, 0.2), rand_pd(rng, m, 0.5)
        P, K = dare_schur(A, B, Q, R)
        ref = riccati_iteration(A, B, Q, R, 3000)
        assert maxabs(cm.sub(P, ref)) <= 1e-8 * max(1.0, maxabs(ref))
        assert maxabs(dare_residual(A, B, Q, R, P)) <= 1e-9 * max(1.0, maxabs(ref)) * (1 + maxabs(A)) ** 2
        acl = cm.sub(A, cm.mul(B, K))
        eigs = cm.polyroots(cm.charpoly(acl))
        assert all(abs(e) < 1 for e in eigs)
        sroots = cm.polyroots(cm.charpoly(symplectic(A, B, Q, R)))
        assert match(eigs, [r for r in sroots if abs(r) < 1], 1e-6)
        done += 1


def test_no_stabilizing_solution():
    # a = 0, q = 0: H = [[0, -1], [0, 0]] has the double eigenvalue 0 on the axis.
    with pytest.raises(ValueError):
        care_schur([[0]], [[1]], [[0]], [[1]])
    # b = 0 and a = 1: the unstable mode cannot be moved, U1 = 0.
    with pytest.raises(ValueError):
        care_schur([[1]], [[0]], [[1]], [[1]])
    # Undamped oscillator with q = 0: eigenvalues of H at +i and -i.
    with pytest.raises(ValueError):
        care_schur([[0, 1], [-1, 0]], [[0], [1]], cm.zeros(2), [[1]])
    # Discrete: a = 1, q = 0 puts both eigenvalues of S on the unit circle.
    with pytest.raises(ValueError):
        dare_schur([[1]], [[1]], [[0]], [[1]])
    with pytest.raises(ValueError):
        dare_schur([[0]], [[1]], [[1]], [[1]])
