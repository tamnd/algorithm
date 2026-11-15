# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-pole-placement/. The authors are listed in prov/PCC8GC.jsonl.

import random

import pytest

import ctlmat as cm
from robust_pole_placement import eigenvectors, eigvec_condition, eigvec_subspace, input_qr, knv0

A4 = [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0], [-1.0, 2.0, 0.0, -1.0]]
B4 = [[0.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 1.0]]
POLES4 = [-1.0, -2.0, -3.0, -4.0]


def closed_loop(A, B, K):
    return cm.sub(A, cm.mul(B, K))


def residual(Acl, X, poles):
    """Return max over j of |Acl x_j - lambda_j x_j|."""
    worst = 0.0
    for x, lam in zip(X, poles):
        ax = cm.matvec(Acl, x)
        worst = max(worst, max(abs(a - lam * v) for a, v in zip(ax, x)))
    return worst


def ackermann_single(A, b, p):
    """Ackermann's formula, written out here as the reference gain."""
    n = len(A)
    cols = [list(b)]
    for _ in range(n - 1):
        cols.append(cm.matvec(A, cols[-1]))
    W = cm.transpose(cols)
    q = cm.solve(cm.transpose(W), [0.0] * (n - 1) + [1.0])
    K = [0.0] * n
    At = cm.transpose(A)
    for c in p:
        K = [x + c * y for x, y in zip(cm.matvec(At, K), q)]
    return K


def poly_from_roots(roots):
    p = [1.0]
    for r in roots:
        p = cm.polymul(p, [1.0, -r])
    return [complex(c).real for c in p]


def check_placement(A, B, poles, K, X, tol=1e-8):
    Acl = closed_loop(A, B, K)
    assert residual(Acl, X, poles) < tol * (1 + max(abs(v) for r in Acl for v in r))
    got = cm.charpoly(Acl)
    want = poly_from_roots(poles)
    for g, w in zip(got, want):
        assert abs(g - w) < 1e-7 * (1 + abs(w))


def test_stated_example_beats_rank_one_ackermann():
    K, X, cond = knv0(A4, B4, POLES4)
    check_placement(A4, B4, POLES4, K, X)
    roots = cm.polyroots(cm.charpoly(closed_loop(A4, B4, K)))
    for r, w in zip(roots, sorted(POLES4)):
        assert abs(r - w) < 1e-8
    # Rank-one design: u = -v k x with b = B v and k from Ackermann.
    for v in ([1.0, 1.0], [1.0, 0.0], [0.0, 1.0]):
        b = cm.matvec(B4, v)
        k = ackermann_single(A4, b, poly_from_roots(POLES4))
        Kr = [[vi * kj for kj in k] for vi in v]
        Acl = closed_loop(A4, B4, Kr)
        Xr = eigenvectors(Acl, POLES4)
        assert residual(Acl, Xr, POLES4) < 1e-6
        assert cond <= eigvec_condition(Xr)
        assert cm.norm2(K) <= cm.norm2(Kr)
    assert cond < 10.0


def test_identity_input_gives_orthonormal_eigenvectors():
    rng = random.Random(5)
    n = 4
    A = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(n)]
    B = cm.eye(n)
    poles = [-1.0, -2.0, -3.0, -5.0]
    K, X, cond = knv0(A, [[float(v) for v in r] for r in B], poles)
    check_placement(A, B, poles, K, X)
    assert cond < 1 + 1e-6


def test_random_systems_real_and_complex():
    rng = random.Random(7)
    for trial in range(8):
        n = rng.randint(3, 6)
        m = rng.randint(2, min(3, n))
        A = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(n)]
        B = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
        poles = [-(1.0 + i) for i in range(n)]
        if trial % 2 == 1:
            poles[0] = complex(-1.0, 1.5)
            poles[1] = complex(-1.0, -1.5)
        K, X, cond = knv0(A, B, poles, seed=trial)
        assert all(isinstance(v, float) for row in K for v in row)
        check_placement(A, B, poles, K, X, tol=1e-7)


def test_sweeps_do_not_increase_condition():
    rng = random.Random(11)
    A = [[rng.uniform(-2, 2) for _ in range(5)] for _ in range(5)]
    B = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(5)]
    poles = [-1.0, -2.0, -3.0, -4.0, -5.0]
    _, _, c0 = knv0(A, B, poles, sweeps=0)
    _, _, c1 = knv0(A, B, poles, sweeps=1)
    _, _, c9 = knv0(A, B, poles, sweeps=20)
    assert c9 <= c1 <= c0


def test_subspace_dimension_and_property():
    U0, U1, Z = input_qr(B4)
    assert len(U0) == 2 and len(U1) == 2
    Bq = cm.mul(cm.transpose(U0), Z)
    assert max(abs(x - y) for r, s in zip(Bq, B4) for x, y in zip(r, s)) < 1e-14
    for lam in (-1.0, complex(-2.0, 1.0)):
        S = eigvec_subspace(A4, U1, lam)
        assert len(S) == 2
        for s in S:
            v = [sum(A4[i][j] * s[j] for j in range(4)) - lam * s[i] for i in range(4)]
            for u in U1:
                assert abs(sum(a * b for a, b in zip(u, v))) < 1e-12


def test_rejections():
    with pytest.raises(ValueError):
        knv0(A4, B4, [-1.0, -1.0, -2.0, -3.0])
    with pytest.raises(ValueError):
        knv0(A4, B4, [complex(-1.0, 1.0), -2.0, -3.0, -4.0])
    with pytest.raises(ValueError):
        knv0(A4, [[1.0, 2.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], POLES4)
    # Uncontrollable: the last state is decoupled from both inputs.
    A = [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 2.0]]
    B = [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]
    with pytest.raises(ValueError):
        knv0(A, B, [-1.0, -2.0, -3.0])
