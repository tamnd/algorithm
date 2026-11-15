# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lqg-control/. The authors are listed in prov/WY53ER.jsonl.

import math
import random

import ctlmat as cm
from lqg_control import care, closed_loop, filter_are, lqg, lqg_cost, lyap, optimal_cost

R3 = math.sqrt(3.0)

# Double integrator, position measured, Q = I, R = 1, W = I, V = 1.
A = [[0, 1], [0, 0]]
B = [[0], [1]]
C = [[1, 0]]
Q = cm.eye(2)
R = [[1]]
W = cm.eye(2)
V = [[1]]


def close(X, Y, tol):
    return all(abs(a - b) <= tol for ra, rb in zip(X, Y) for a, b in zip(ra, rb))


def max_real(M):
    return max(z.real for z in cm.polyroots(cm.charpoly(M)))


def care_residual(A, B, Q, R, P):
    G = cm.mul(cm.mul(B, cm.inv(R)), cm.transpose(B))
    res = cm.add(cm.add(cm.mul(cm.transpose(A), P), cm.mul(P, A)), cm.sub(Q, cm.mul(cm.mul(P, G), P)))
    return max(abs(v) for row in res for v in row)


def test_double_integrator_closed_form():
    K, L, P, S = lqg(A, B, C, Q, R, W, V)
    want = [[R3, 1.0], [1.0, R3]]
    assert close(P, want, 1e-9) and close(S, want, 1e-9)
    assert close(K, [[1.0, R3]], 1e-9)
    assert close(L, [[R3], [1.0]], 1e-9)


def test_scalar_closed_form():
    # x' = a x + u + w, y = x + v: P = a + sqrt(a^2 + q) with r = 1, S = a + sqrt(a^2 + w) with v = 1.
    for a, q, w in [(1.0, 1.0, 1.0), (-2.0, 3.0, 0.5), (0.0, 4.0, 9.0)]:
        K, L, P, S = lqg([[a]], [[1.0]], [[1.0]], [[q]], [[1.0]], [[w]], [[1.0]])
        assert abs(P[0][0] - (a + math.sqrt(a * a + q))) < 1e-9
        assert abs(S[0][0] - (a + math.sqrt(a * a + w))) < 1e-9


def test_riccati_residuals_on_random_plants():
    rng = random.Random(11)
    for _ in range(6):
        n = rng.choice([2, 3])
        A_ = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(n)]
        B_ = [[rng.uniform(-1, 1)] for _ in range(n)]
        C_ = [[rng.uniform(-1, 1) for _ in range(n)]]
        Q_ = cm.eye(n)
        W_ = cm.eye(n)
        K, L, P, S = lqg(A_, B_, C_, Q_, [[1.0]], W_, [[0.5]])
        scale = 1.0 + max(abs(v) for row in P for v in row) ** 2
        assert care_residual(A_, B_, Q_, [[1.0]], P) <= 1e-9 * scale
        At, Ct = cm.transpose(A_), cm.transpose(C_)
        scale = 1.0 + max(abs(v) for row in S for v in row) ** 2
        assert care_residual(At, Ct, W_, [[0.5]], S) <= 1e-9 * scale
        assert cm.is_symmetric(P, 1e-12) and cm.is_pos_def(P)
        assert max_real(cm.sub(A_, cm.mul(B_, K))) < 0
        assert max_real(cm.sub(A_, cm.mul(L, C_))) < 0


def test_separation_of_eigenvalues():
    rng = random.Random(5)
    for _ in range(4):
        n = 3
        A_ = [[rng.uniform(-1.5, 1.5) for _ in range(n)] for _ in range(n)]
        B_ = [[rng.uniform(-1, 1)] for _ in range(n)]
        C_ = [[rng.uniform(-1, 1) for _ in range(n)]]
        K, L, P, S = lqg(A_, B_, C_, cm.eye(n), [[1.0]], cm.eye(n), [[1.0]])
        got = cm.charpoly(closed_loop(A_, B_, C_, K, L))
        want = cm.polymul(cm.charpoly(cm.sub(A_, cm.mul(B_, K))), cm.charpoly(cm.sub(A_, cm.mul(L, C_))))
        assert all(abs(g - w) <= 1e-8 * (1 + abs(w)) for g, w in zip(got, want))


def test_optimal_cost_and_perturbed_gains():
    K, L, P, S = lqg(A, B, C, Q, R, W, V)
    j_opt = optimal_cost(B, R, W, K, P, S)
    assert abs(j_opt - 8 * R3) < 1e-9
    assert abs(lqg_cost(A, B, C, Q, R, W, V, K, L) - j_opt) < 1e-8
    rng = random.Random(3)
    tried = 0
    while tried < 15:
        Kp = [[k + rng.uniform(-0.3, 0.3) for k in K[0]]]
        Lp = [[l[0] + rng.uniform(-0.3, 0.3)] for l in L]
        if max_real(closed_loop(A, B, C, Kp, Lp)) >= -1e-3:
            continue
        tried += 1
        assert lqg_cost(A, B, C, Q, R, W, V, Kp, Lp) > j_opt - 1e-9


def test_gain_margin_of_the_lqg_loop_is_finite():
    # Closed loop with input gain k: s^4 + 2 sqrt3 s^3 + 5 s^2 + 2 sqrt3 k s + k, Hurwitz iff 0 < k < 4.
    K, L, P, S = lqg(A, B, C, Q, R, W, V)
    for k, ok in [(0.05, True), (1.0, True), (3.9, True), (4.1, False), (6.0, False)]:
        assert (max_real(closed_loop(A, B, C, K, L, gain=[[k]])) < 0) == ok
    # The LQR loop alone keeps every gain k >= 1/2 (here every k > 0).
    for k in [0.5, 4.1, 100.0]:
        assert max_real(cm.sub(A, cm.scale(k, cm.mul(B, K)))) < 0


def test_doyle_example_has_a_tiny_gain_margin():
    q = sig = 60
    A_ = [[1, 1], [0, 1]]
    Q_ = [[q, q], [q, q]]
    W_ = [[sig, sig], [sig, sig]]
    K, L, P, S = lqg(A_, B, C, Q_, R, W_, V)
    assert close(K, [[10.0, 10.0]], 1e-8) and close(L, [[10.0], [10.0]], 1e-8)
    m_low = (97 - 8 * math.sqrt(85)) / 25
    for m, ok in [(1.0, True), (1.009, True), (1.011, False), (m_low + 1e-4, True), (m_low - 1e-4, False)]:
        assert (max_real(closed_loop(A_, B, C, K, L, gain=[[m]])) < 0) == ok


def test_noise_free_closed_loop_goes_to_zero():
    K, L, P, S = lqg(A, B, C, Q, R, W, V)
    Acl = closed_loop(A, B, C, K, L)
    E = cm.expm(cm.scale(30.0, Acl))
    z = cm.matvec(E, [1.0, -1.0, 0.0, 0.0])
    assert cm.norm2(z) < 1e-6


def test_lyap_solves_its_equation():
    F = [[-1.0, 2.0], [0.0, -3.0]]
    M = [[1.0, 0.5], [0.5, 2.0]]
    X = lyap(F, M)
    res = cm.add(cm.add(cm.mul(F, X), cm.mul(X, cm.transpose(F))), M)
    assert max(abs(v) for row in res for v in row) < 1e-12


def test_filter_are_is_the_dual_care():
    S = filter_are(A, C, W, V)
    P = care(cm.transpose(A), cm.transpose(C), W, V)
    assert close(S, P, 0.0)
