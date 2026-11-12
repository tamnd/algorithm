# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a2c/. The authors are listed in prov/S26G9H.jsonl.

import math
import random
from fractions import Fraction as F

from a2c import a2c, gradients, n_step_returns, softmax

P = [
    [[F(1, 2), F(1, 4)], [F(0), F(3, 4)]],
    [[F(1, 2), F(0)], [F(0), F(0)]],
]
R = [[F(1), F(0)], [F(0), F(3)]]
GAMMA = F(1, 2)
UNIFORM = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
V_TRUE = [F(28, 27), F(44, 27)]
Q_TRUE = [[F(79, 54), F(11, 18)], [F(7, 27), F(3)]]
PHI = [[1, 0], [0, 1]]


def segments(s, a, n):
    """Every n-step segment that starts with (s, a): (probability, rewards, dones, last state)."""
    out = []
    stack = [(F(1), s, a, [], [])]
    while stack:
        p, s, a, rs, ds = stack.pop()
        rs = rs + [R[s][a]]
        end = 1 - sum(P[s][a])
        if end > 0:
            out.append((p * end, rs, ds + [True], None))
        for t in range(2):
            q = p * P[s][a][t]
            if q == 0:
                continue
            if len(rs) == n:
                out.append((q, rs, ds + [False], t))
            else:
                for b in range(2):
                    stack.append((q * UNIFORM[t][b], t, b, rs, ds + [False]))
    return out


def expected_return(s, a, n, V):
    tot = F(0)
    for p, rs, ds, last in segments(s, a, n):
        boot = V[last] if last is not None else F(0)
        tot += p * n_step_returns(rs, ds, boot, GAMMA)[0]
    return tot


def test_n_step_returns():
    assert n_step_returns([F(1), F(2), F(3)], [False, False, False], F(10), F(1, 2)) == [
        F(1) + F(1, 2) * 2 + F(1, 4) * 3 + F(1, 8) * 10,
        F(2) + F(1, 2) * 3 + F(1, 4) * 10,
        F(3) + F(1, 2) * 10,
    ]
    # the episode ends after the second reward: no bootstrap there, and the third reward starts a new episode
    assert n_step_returns([F(1), F(2), F(3)], [False, True, False], F(10), F(1, 2)) == [F(2), F(2), F(8)]


def test_exact_critic_gives_q_for_every_n():
    for n in (1, 2, 3, 4):
        for s in range(2):
            for a in range(2):
                assert expected_return(s, a, n, V_TRUE) == Q_TRUE[s][a]


def test_critic_error_bias_decays_like_gamma_n():
    for n in (1, 2, 3, 4):
        bias = [expected_return(0, a, n, [F(0), F(0)]) - Q_TRUE[0][a] for a in range(2)]
        # bias = -gamma^n E[V(S_n); still running]
        alive = [F(0)] * 2
        for p, rs, ds, last in segments(0, 0, n):
            if last is not None:
                alive[last] += p
        assert bias[0] == -GAMMA ** n * sum(alive[t] * V_TRUE[t] for t in range(2))
        assert abs(bias[0]) <= GAMMA ** n * max(V_TRUE)


def test_gradients_match_finite_differences():
    theta = [[0.3, -0.1], [0.2, 0.5]]
    w = [0.4, -0.2]
    batch = [(0, 0, 1.5), (1, 1, 2.0), (0, 1, -0.5), (1, 0, 0.7)]
    beta = 0.1
    g_theta, g_w = gradients(theta, w, PHI, softmax(theta), batch, beta)
    adv = [G - w[s] for s, _, G in batch]

    def surrogate(th):
        pi = softmax(th)
        tot = 0.0
        for (s, a, _), A in zip(batch, adv):
            tot += A * math.log(pi[s][a]) - beta * sum(p * math.log(p) for p in pi[s])
        return tot / len(batch)

    def value_loss(ww):
        return -sum((G - ww[s]) ** 2 for s, _, G in batch) / (2 * len(batch))

    h = 1e-6
    for s in range(2):
        for b in range(2):
            tp = [r[:] for r in theta]
            tm = [r[:] for r in theta]
            tp[s][b] += h
            tm[s][b] -= h
            assert abs((surrogate(tp) - surrogate(tm)) / (2 * h) - g_theta[s][b]) < 1e-7
        wp, wm = w[:], w[:]
        wp[s] += h
        wm[s] -= h
        assert abs((value_loss(wp) - value_loss(wm)) / (2 * h) - g_w[s]) < 1e-7


def test_exact_mean_actor_direction():
    # with the exact critic and states drawn from a weighting rho, the mean actor direction is
    # sum_s rho(s) sum_a pi(a|s) A(s,a) grad log pi(a|s)
    batch = []
    for s in range(2):
        for a in range(2):
            batch.append((s, a, Q_TRUE[s][a]))
    g_theta, _ = gradients([[F(0)] * 2] * 2, V_TRUE, PHI, UNIFORM, batch, 0)
    # weights 1/4 each: g[s][b] = (1/4) sum_a A(s,a) (1[a=b] - 1/2) = (1/4) A(s,b) because sum_a A(s,a) = 0 here
    for s in range(2):
        for b in range(2):
            assert g_theta[s][b] == (Q_TRUE[s][b] - V_TRUE[s]) / 4


def test_learning_run():
    Pf = [[[float(x) for x in r] for r in rows] for rows in P]
    Rf = [[float(x) for x in r] for r in R]
    theta, w = a2c(Pf, Rf, [1.0, 0.0], 0.5, [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], PHI, 4, 5, 400, 0.5, random.Random(0), beta=0.01)
    pi = softmax(theta)
    assert pi[0][0] > 0.9 and pi[1][1] > 0.9
    assert abs(w[1] - 3.0) < 0.5
