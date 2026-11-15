# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kalman-bucy-filter/. The authors are listed in prov/HYX6WP.jsonl.

import math
import random

import ctlmat as cm
from ctlsim import rk4_step
from kalman_bucy_filter import KalmanBucy, gain, riccati_rhs, riccati_solution, steady_state

R2 = math.sqrt(2.0)
R3 = math.sqrt(3.0)

# Double integrator, position measured, W = I, V = 1.
A = [[0.0, 1.0], [0.0, 0.0]]
B = [[0.0], [1.0]]
C = [[1.0, 0.0]]
W = [[1.0, 0.0], [0.0, 1.0]]
V = [[1.0]]


def test_scalar_riccati_closed_forms():
    # a = 0, c = w = v = 1, S(0) = 0: S(t) = tanh(t).  RK4 with h = 0.01, error below 1e-8.
    for t in [0.5, 1.0, 2.0]:
        S = riccati_solution([[0.0]], [[1.0]], [[1.0]], [[1.0]], [[0.0]], t, 0.01)
        assert abs(S[0][0] - math.tanh(t)) < 1e-8
    # a = 1: S(t) = 1 + sqrt2 tanh(sqrt2 t + atanh(-1/sqrt2)).
    c0 = math.atanh(-1.0 / R2)
    for t in [0.5, 1.0, 3.0]:
        S = riccati_solution([[1.0]], [[1.0]], [[1.0]], [[1.0]], [[0.0]], t, 0.01)
        assert abs(S[0][0] - (1.0 + R2 * math.tanh(R2 * t + c0))) < 1e-8


def test_steady_state_values():
    S, L = steady_state([[1.0]], [[1.0]], [[1.0]], [[1.0]])
    assert abs(S[0][0] - (1.0 + R2)) < 1e-9
    S, L = steady_state([[-1.0]], [[1.0]], [[1.0]], [[1.0]])
    assert abs(S[0][0] - (R2 - 1.0)) < 1e-9
    S, L = steady_state(A, C, W, V)
    want = [[R3, 1.0], [1.0, R3]]
    assert all(abs(S[i][j] - want[i][j]) < 1e-9 for i in range(2) for j in range(2))
    assert abs(L[0][0] - R3) < 1e-9 and abs(L[1][0] - 1.0) < 1e-9
    # Error polynomial s^2 + sqrt3 s + 1.
    p = cm.charpoly(cm.sub(A, cm.mul(L, C)))
    assert abs(p[1] - R3) < 1e-9 and abs(p[2] - 1.0) < 1e-9


def test_steady_state_solves_the_filter_are_on_random_plants():
    rng = random.Random(7)
    for _ in range(5):
        n = rng.choice([2, 3])
        A_ = [[rng.uniform(-1.0, 1.0) - (1.5 if i == j else 0.0) for j in range(n)] for i in range(n)]
        C_ = [[rng.uniform(-1, 1) for _ in range(n)]]
        W_ = cm.eye(n)
        S, L = steady_state(A_, C_, W_, [[0.5]], h=0.02)
        res = riccati_rhs(A_, C_, W_, [[0.5]])(0.0, [v for row in S for v in row], None)
        assert max(abs(v) for v in res) < 1e-9
        assert cm.is_pos_def(S)
        assert max(z.real for z in cm.polyroots(cm.charpoly(cm.sub(A_, cm.mul(L, C_))))) < 0


def test_riccati_solution_beats_every_constant_gain():
    # For a fixed gain G the error covariance obeys P' = (A - G C) P + P (A - G C)^T + W + G V G^T.
    # P(t) - S(t) stays positive semidefinite for every G when both start at S0.
    rng = random.Random(1)
    S0 = [[2.0, 0.0], [0.0, 2.0]]
    h = 0.02
    f = riccati_rhs(A, C, W, V)
    for _ in range(4):
        G = [[rng.uniform(0.5, 3.0)], [rng.uniform(0.3, 2.0)]]
        F = cm.sub(A, cm.mul(G, C))
        Ft = cm.transpose(F)
        N = cm.add(W, cm.mul(cm.mul(G, V), cm.transpose(G)))

        def g(t, s, u, F=F, Ft=Ft, N=N):
            P = [s[0:2], s[2:4]]
            dP = cm.add(cm.add(cm.mul(F, P), cm.mul(P, Ft)), N)
            return [v for row in dP for v in row]
        s = [v for row in S0 for v in row]
        p = list(s)
        for k in range(150):
            s = rk4_step(f, k * h, s, None, h)
            p = rk4_step(g, k * h, p, None, h)
            if k % 10 == 9:
                D = [[p[0] - s[0], p[1] - s[1]], [p[2] - s[2], p[3] - s[3]]]
                ev = [(D[0][0] + D[1][1]) / 2 + sg * math.sqrt(((D[0][0] - D[1][1]) / 2) ** 2 + D[0][1] * D[1][0]) for sg in (-1, 1)]
                assert min(ev) >= -1e-9


def test_noise_free_error_decays():
    S, L = steady_state(A, C, W, V)
    h = 0.01
    kb = KalmanBucy(A, B, C, W, V, [0.0, 0.0], S)
    x = [1.0, -1.0]
    e0 = math.hypot(x[0], x[1])
    rate = R3 / 2 - 0.05
    for k in range(1, 801):
        u = [math.sin(0.3 * k * h)]
        dz = [h * cm.dot(C[0], x)]
        kb.step(u, dz, h)
        x = [x[0] + h * x[1], x[1] + h * u[0]]  # Euler step of the plant, the same scheme as the filter
        e = math.hypot(x[0] - kb.xhat[0], x[1] - kb.xhat[1])
        assert e <= 4.0 * math.exp(-rate * k * h) * e0  # max over t of |e^((A - L C) t)| e^(rate t) is about 3.2
    assert e < 1e-2


def test_monte_carlo_error_matches_the_riccati_variance():
    # Scalar plant a = -1, c = 1, W = V = 1, x0 ~ N(0, 1), xhat0 = 0, S0 = 1, Euler-Maruyama with h = 0.04 to T = 2.
    # The event |e(T)| <= sqrt(S(T)) has probability erf(1/sqrt2) = 0.6827 for e ~ N(0, S(T)).
    # Hoeffding with M = 400 paths and delta = 1e-6 gives the tolerance sqrt(ln(2/delta) / (2 M)) = 0.135;
    # 0.02 more covers the O(h) bias of the Euler-Maruyama scheme.
    rng = random.Random(2024)
    h, steps, M = 0.04, 50, 400
    a = -1.0
    S_T = riccati_solution([[a]], [[1.0]], [[1.0]], [[1.0]], [[1.0]], h * steps, h)[0][0]
    hit = 0
    below = 0
    sq = math.sqrt(h)
    for _ in range(M):
        x = rng.gauss(0.0, 1.0)
        kb = KalmanBucy([[a]], None, [[1.0]], [[1.0]], [[1.0]], [0.0], [[1.0]])
        for _ in range(steps):
            dz = [x * h + sq * rng.gauss(0.0, 1.0)]
            kb.step(None, dz, h)
            x = x + a * x * h + sq * rng.gauss(0.0, 1.0)
        e = x - kb.xhat[0]
        hit += abs(e) <= math.sqrt(S_T)
        below += e <= 0.0
    tol = math.sqrt(math.log(2 / 1e-6) / (2 * M)) + 0.02
    assert abs(hit / M - math.erf(1 / R2)) <= tol
    assert abs(below / M - 0.5) <= tol


def test_gain_formula():
    S = [[2.0, 0.5], [0.5, 1.0]]
    assert gain(S, C, [[4.0]]) == [[0.5], [0.125]]
