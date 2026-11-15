# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/super-twisting-algorithm/. The authors are listed in prov/QDH2NE.jsonl.

import math
import random
from fractions import Fraction

import ctlsim
from super_twisting_algorithm import SuperTwisting, certified, lyapunov_matrix, q_matrix, sgn, time_bound

# Simulations: the plant s' = u + d(t) is integrated with classical RK4
# (ctlsim) with step dt equal to the sampling period h of the controller, so
# u is held over each step. Tolerances are stated at each check.


def steps(T, h):
    n = round(T / h)
    assert abs(n * h - T) < 1e-12
    return n


def run(k1, k2, h, T, d=math.sin, s0=1.0):
    st = SuperTwisting(k1, k2, h)
    ws = []

    def control(t, x):
        ws.append(st.w)
        return st.step(x[0])

    ts, xs, us = ctlsim.simulate(lambda t, x, u: [u + d(t)], [s0], 0.0, T, h, control=control)
    ws.append(st.w)
    assert len(us) == steps(T, h)
    return ts, [x[0] for x in xs], ws


def rand_frac(rng, lo, hi, den=8):
    return Fraction(rng.randint(lo * den, hi * den), den)


def test_step_by_hand():
    st = SuperTwisting(2, 2, Fraction(1, 100))
    assert st.step(4.0) == -4.0
    assert st.w == Fraction(-2, 100)
    assert st.step(0.0) == -0.02
    assert st.w == Fraction(-2, 100)
    assert abs(st.step(-0.25) - (1.0 - 0.02)) < 1e-15


def test_q_matrix_is_minus_lyapunov_derivative():
    # Q(theta) = -(A^T P + P A) and det Q = k1^2 k2 / 2 - theta L k1^2 / 2 - theta^2 L^2, exactly.
    rng = random.Random(3)
    for _ in range(200):
        k1, k2, L = rand_frac(rng, 1, 5), rand_frac(rng, 1, 9), rand_frac(rng, 0, 3)
        theta = rand_frac(rng, -1, 1)
        P = lyapunov_matrix(k1, k2)
        A = [[-k1 / 2, Fraction(1, 2)], [-k2 + theta * L, 0]]
        M = [[sum(A[k][i] * P[k][j] + P[i][k] * A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        Q = q_matrix(k1, k2, L, theta)
        assert all(M[i][j] == -Q[i][j] for i in range(2) for j in range(2))
        det = Q[0][0] * Q[1][1] - Q[0][1] * Q[1][0]
        assert det == k1 * k1 * k2 / 2 - theta * L * k1 * k1 / 2 - theta * theta * L * L
        assert certified(k1, k2, L) == (k2 > L + 2 * L * L / (k1 * k1))


def test_lyapunov_rate_exact():
    # Along s' = -k1 |s|^(1/2) sgn s + v, v' = -k2 sgn s + rho, |rho| <= L, in
    # z = (|s|^(1/2) sgn s, v): V' = -z^T Q(theta) z / |z1| with theta = rho sgn(z1) / L.
    rng = random.Random(5)
    for _ in range(200):
        k1, k2, L = rand_frac(rng, 1, 4), rand_frac(rng, 1, 6), rand_frac(rng, 1, 2)
        z1 = rand_frac(rng, -3, 3)
        if z1 == 0:
            continue
        z2 = rand_frac(rng, -3, 3)
        rho = rand_frac(rng, -1, 1) * L
        dz1 = (-k1 * z1 + z2) / (2 * abs(z1))
        dz2 = -k2 * sgn(z1) + rho
        P = lyapunov_matrix(k1, k2)
        z, dz = [z1, z2], [dz1, dz2]
        vdot = 2 * sum(z[i] * P[i][j] * dz[j] for i in range(2) for j in range(2))
        theta = rho * sgn(z1) / L
        Q = q_matrix(k1, k2, L, theta)
        assert vdot == -sum(z[i] * Q[i][j] * z[j] for i in range(2) for j in range(2)) / abs(z1)
        if certified(k1, k2, L):
            assert vdot < 0


def test_page_example():
    # s' = u + sin t, L = 1, gains (2, 2): certified since 2 > 1 + 2 / 4.
    assert certified(2, 2, 1)
    assert abs(time_bound(2.0, 2.0, 1.0, 1.0, 0.0) - 132.984) < 1e-3
    h = 0.01
    ts, ss, ws = run(2.0, 2.0, h, 10.0)
    table = {0.5: (0.151849, -1.0), 1.0: (0.002585, -0.76), 2.0: (0.000023, -0.92), 4.0: (-0.000063, 0.76)}
    for t, (s, w) in table.items():
        i = steps(t, h)
        assert abs(ss[i] - s) < 5e-7 and abs(ws[i] - w) < 1e-9
    # |s| <= 0.05 for good from t = 0.59 (measured)
    i = steps(0.59, h)
    assert all(abs(s) <= 0.05 for s in ss[i:]) and abs(ss[i - 1]) > 0.05
    # w tracks -d: max |w + sin t| for t >= 6 is 0.045 (measured), about 2 h k2
    assert max(abs(w + math.sin(t)) for t, w in zip(ts, ws) if t >= 6) < 0.05


def test_accuracy_is_order_h_squared():
    # max |s| for t >= 6 is 4.35 h^2, 5.31 h^2, 4.75 h^2 for h = 0.01, 0.005, 0.0025 (measured).
    for h in (0.01, 0.005, 0.0025):
        ts, ss, ws = run(2.0, 2.0, h, 10.0)
        late = max(abs(s) for t, s in zip(ts, ss) if t >= 6)
        assert 3 * h * h < late < 6 * h * h


def test_first_order_comparison():
    # u = -1.5 sgn s with the same h: band 0.0235, about 50 times the super-twisting band.
    h = 0.01
    ts, xs, us = ctlsim.simulate(lambda t, x, u: [u + math.sin(t)], [1.0], 0.0, 10.0, h, control=lambda t, x: -1.5 * sgn(x[0]))
    assert len(us) == steps(10.0, h)
    band = max(abs(x[0]) for t, x in zip(ts, xs) if t >= 6)
    assert 0.02 < band <= 2.5 * h


def test_rule_of_thumb_gains():
    # k1 = 1.5 sqrt(L), k2 = 1.1 L is not certified by this P, but converges here.
    assert not certified(1.5, 1.1, 1.0)
    ts, ss, ws = run(1.5, 1.1, 0.01, 10.0)
    assert max(abs(s) for t, s in zip(ts, ss) if t >= 1) <= 0.05
    assert max(abs(s) for t, s in zip(ts, ss) if t >= 6) < 5e-4


def test_k2_below_L_fails():
    # d = t has d' = 1 = L. With k2 = 0.5 < L, v' >= 0.5 and s drifts away.
    ts, ss, ws = run(2.0, 0.5, 0.01, 10.0, d=lambda t: t)
    assert ss[-1] > 4.0
    ts, ss, ws = run(2.0, 1.5, 0.01, 10.0, d=lambda t: t)
    assert max(abs(s) for t, s in zip(ts, ss) if t >= 6) < 2e-4


def test_errors():
    for bad in [lambda: SuperTwisting(0, 1, 0.1), lambda: SuperTwisting(1, 1, 0), lambda: time_bound(1.0, 1.0, 1.0, 1.0, 0.0)]:
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("no error")
