# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reinforce/. The authors are listed in prov/QVNG1R.jsonl.

import random
from fractions import Fraction as F

from reinforce import episode_update, reinforce, sample_episode, softmax

P = [
    [[F(1, 2), F(1, 4)], [F(0), F(3, 4)]],
    [[F(1, 2), F(0)], [F(0), F(0)]],
]
R = [[F(1), F(0)], [F(0), F(3)]]
MU = [F(1), F(0)]
GAMMA = F(1, 2)
UNIFORM = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]


def all_episodes(P, R, pi, mu, horizon):
    """Oracle: every episode of at most horizon steps with its probability (explicit stack)."""
    n = len(P)
    out = []
    stack = [(s, mu[s], []) for s in range(n) if mu[s] > 0]
    while stack:
        s, p, ep = stack.pop()
        for a in range(len(pi[s])):
            q = p * pi[s][a]
            if q == 0:
                continue
            ep2 = ep + [(s, a, R[s][a])]
            end = 1 - sum(P[s][a])
            if len(ep2) == horizon:
                out.append((q, ep2))
                continue
            if end > 0:
                out.append((q * end, ep2))
            for t in range(n):
                if P[s][a][t] > 0:
                    stack.append((t, q * P[s][a][t], ep2))
    return out


def exact_gradient(P, R, gamma, pi, mu, horizon):
    """Oracle: differentiate the backward induction for J_H = E[sum_(t<H) gamma^t R_(t+1)]."""
    n, k = len(P), len(pi[0])
    V = [F(0)] * n
    dV = [[[F(0)] * k for _ in range(n)] for _ in range(n)]  # dV[s][x][b]
    for _ in range(horizon):
        V2 = [sum(pi[s][a] * (R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n))) for a in range(k)) for s in range(n)]
        dV2 = [[[F(0)] * k for _ in range(n)] for _ in range(n)]
        for s in range(n):
            for x in range(n):
                for b in range(k):
                    v = sum(pi[s][a] * gamma * sum(P[s][a][t] * dV[t][x][b] for t in range(n)) for a in range(k))
                    if x == s:
                        v += sum(pi[s][a] * ((1 if a == b else 0) - pi[s][b]) * (R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n))) for a in range(k))
                    dV2[s][x][b] = v
        V, dV = V2, dV2
    return [[sum(mu[s] * dV[s][x][b] for s in range(n)) for b in range(k)] for x in range(n)], sum(m * v for m, v in zip(mu, V))


def expected_update(pi, gamma, baseline, horizon):
    n, k = len(pi), len(pi[0])
    total = [[F(0)] * k for _ in range(n)]
    eps = all_episodes(P, R, pi, MU, horizon)
    assert sum(p for p, _ in eps) == 1
    for p, ep in eps:
        g = episode_update(pi, ep, gamma, baseline)
        for s in range(n):
            for j in range(k):
                total[s][j] += p * g[s][j]
    return total, eps


def test_worked_episode():
    ep = [(0, 0, F(1)), (1, 1, F(3))]
    assert episode_update(UNIFORM, ep, GAMMA) == [[F(5, 4), F(-5, 4)], [F(-3, 4), F(3, 4)]]
    b = [F(28, 27), F(44, 27)]
    assert episode_update(UNIFORM, ep, GAMMA, b) == [[F(79, 108), F(-79, 108)], [F(-37, 108), F(37, 108)]]


def test_expected_update_equals_gradient():
    for horizon in (1, 2, 3, 4):
        grad, _ = exact_gradient(P, R, GAMMA, UNIFORM, MU, horizon)
        assert expected_update(UNIFORM, GAMMA, None, horizon)[0] == grad
    grad3, j3 = exact_gradient(P, R, GAMMA, UNIFORM, MU, 3)
    assert j3 == F(129, 128)
    assert grad3 == [[F(63, 256), F(-63, 256)], [F(-13, 64), F(13, 64)]]


def test_baseline_keeps_mean_and_lowers_variance():
    rng = random.Random(5)
    pi = [[F(1, 3), F(2, 3)], [F(3, 4), F(1, 4)]]
    grad, _ = exact_gradient(P, R, GAMMA, pi, MU, 3)
    for _ in range(10):
        b = [F(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(2)]
        assert expected_update(pi, GAMMA, b, 3)[0] == grad

    def second_moment(baseline):
        _, eps = expected_update(UNIFORM, GAMMA, baseline, 3)
        tot = F(0)
        for p, ep in eps:
            g = episode_update(UNIFORM, ep, GAMMA, baseline)
            tot += p * sum(x * x for row in g for x in row)
        return tot

    assert second_moment([F(28, 27), F(44, 27)]) < second_moment(None)


def test_gamma_one_episodic():
    grad, _ = exact_gradient(P, R, F(1), UNIFORM, MU, 4)
    assert expected_update(UNIFORM, F(1), None, 4)[0] == grad


def test_sampled_mean_is_close():
    rng = random.Random(1)
    Pf = [[[float(x) for x in r] for r in rows] for rows in P]
    Rf = [[float(x) for x in r] for r in R]
    pi = softmax([[0.0, 0.0], [0.0, 0.0]])
    n = 40000
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for _ in range(n):
        g = episode_update(pi, sample_episode(Pf, Rf, pi, [1.0, 0.0], rng, 3), 0.5, [28 / 27, 44 / 27])
        for s in range(2):
            for j in range(2):
                acc[s][j] += g[s][j] / n
    assert abs(acc[0][0] - 63 / 256) < 0.02 and abs(acc[1][0] + 13 / 64) < 0.02


def test_learning_run():
    rng = random.Random(2)
    Pf = [[[float(x) for x in r] for r in rows] for rows in P]
    Rf = [[float(x) for x in r] for r in R]
    theta, b = reinforce(Pf, Rf, 0.5, [1.0, 0.0], [[0.0, 0.0], [0.0, 0.0]], 0.2, 3000, rng, baseline_rate=0.05)
    pi = softmax(theta)
    assert pi[1][1] > 0.9  # in state 1 the action that pays 3 is optimal
    assert b is not None and len(b) == 2
