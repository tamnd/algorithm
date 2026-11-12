# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-advantage-estimation/. The authors are listed in prov/25P3CM.jsonl.

import random
from fractions import Fraction as F

from generalized_advantage_estimation import gae, gae_direct, td_errors


def random_segment(rng, T, ended):
    rewards = [F(rng.randint(-4, 4)) for _ in range(T)]
    values = [F(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(T)]
    dones = [False] * T
    if ended:
        dones[-1] = True
    if T > 3 and rng.random() < 0.5:
        dones[rng.randrange(T - 1)] = True  # an episode end inside the segment
    return rewards, values, dones, F(rng.randint(-5, 5))


def n_step_return(rewards, values, dones, last_value, gamma, t, n):
    """G^(n)_t, stopped at an episode end."""
    T = len(rewards)
    G, w = F(0), F(1)
    for j in range(t, min(t + n, T)):
        G += w * rewards[j]
        if dones[j]:
            return G
        w *= gamma
    nxt = last_value if t + n >= T else values[t + n]
    return G + w * nxt


def test_example():
    adv, ret = gae([F(1), F(0), F(2)], [F(1), F(2), F(1)], [False, False, False], F(4), F(1, 2), F(1, 2))
    assert td_errors([F(1), F(0), F(2)], [F(1), F(2), F(1)], [False, False, False], F(4), F(1, 2)) == [F(1), F(-3, 2), F(3)]
    assert adv == [F(13, 16), F(-3, 4), F(3)]
    assert ret == [F(29, 16), F(5, 4), F(4)]


def test_recursion_equals_direct_sum():
    rng = random.Random(1)
    for _ in range(200):
        T = rng.randint(1, 7)
        seg = random_segment(rng, T, rng.random() < 0.5)
        gamma = F(rng.randint(0, 10), 10)
        lam = F(rng.randint(0, 10), 10)
        assert gae(*seg, gamma, lam)[0] == gae_direct(*seg, gamma, lam)


def test_limits():
    rng = random.Random(2)
    for _ in range(100):
        T = rng.randint(1, 7)
        rewards, values, dones, last = random_segment(rng, T, True)
        gamma = F(rng.randint(1, 10), 10)
        # lambda = 0: the one-step TD error
        assert gae(rewards, values, dones, last, gamma, F(0))[0] == td_errors(rewards, values, dones, last, gamma)
        # lambda = 1: the Monte Carlo return minus the value
        adv = gae(rewards, values, dones, last, gamma, F(1))[0]
        for t in range(T):
            G, w = F(0), F(1)
            for j in range(t, T):
                G += w * rewards[j]
                if dones[j]:
                    break
                w *= gamma
            assert adv[t] == G - values[t]


def test_lambda_return():
    rng = random.Random(3)
    for _ in range(100):
        T = rng.randint(1, 6)
        seg = random_segment(rng, T, rng.random() < 0.5)
        rewards, values, dones, last = seg
        gamma, lam = F(rng.randint(1, 10), 10), F(rng.randint(0, 9), 10)
        _, ret = gae(*seg, gamma, lam)
        for t in range(T):
            m = next((j for j in range(t, T) if dones[j]), T - 1) - t + 1  # steps until the end of the data
            direct = sum((1 - lam) * lam ** (n - 1) * n_step_return(*seg, gamma, t, n) for n in range(1, m))
            direct += lam ** (m - 1) * n_step_return(*seg, gamma, t, m)
            assert ret[t] == direct


# Exactness in expectation, on an acyclic MDP where every episode can be listed.

def solve_values(P, R, gamma, pi):
    n = len(P)
    V = [F(0)] * n
    for s in range(n - 1, -1, -1):  # states only move to larger indices
        V[s] = sum(pi[s][a] * (R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n))) for a in range(len(pi[s])))
    Q = [[R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n)) for a in range(len(pi[s]))] for s in range(n)]
    return V, Q


def episodes_from(P, R, pi, s, a):
    out, stack = [], [(F(1), s, a, [])]
    while stack:
        p, s, a, ep = stack.pop()
        ep = ep + [(s, R[s][a])]
        end = 1 - sum(P[s][a])
        if end > 0:
            out.append((p * end, ep))
        for t in range(len(P)):
            if P[s][a][t] > 0:
                for b in range(len(pi[t])):
                    stack.append((p * P[s][a][t] * pi[t][b], t, b, ep))
    return out


def mean_gae(P, R, pi, V, gamma, lam, s, a):
    tot = F(0)
    eps = episodes_from(P, R, pi, s, a)
    assert sum(p for p, _ in eps) == 1
    for p, ep in eps:
        rewards = [r for _, r in ep]
        values = [V[x] for x, _ in ep]
        dones = [False] * (len(ep) - 1) + [True]
        tot += p * gae(rewards, values, dones, F(0), gamma, lam)[0][0]
    return tot


def random_dag(rng, n, k):
    P = []
    for s in range(n):
        rows = []
        for _ in range(k):
            w = [0] * (s + 1) + [rng.randint(0, 3) for _ in range(n - s - 1)] + [rng.randint(1, 3)]
            rows.append([F(x, sum(w)) for x in w[:n]])
        P.append(rows)
    R = [[F(rng.randint(-3, 4)) for _ in range(k)] for _ in range(n)]
    pi = []
    for _ in range(n):
        w = [rng.randint(1, 4) for _ in range(k)]
        pi.append([F(x, sum(w)) for x in w])
    return P, R, pi


def test_exact_values_give_unbiased_advantages_for_every_lambda():
    rng = random.Random(5)
    for _ in range(10):
        P, R, pi = random_dag(rng, rng.randint(2, 4), 2)
        gamma = F(rng.randint(1, 10), 10)
        V, Q = solve_values(P, R, gamma, pi)
        for lam in (F(0), F(1, 3), F(9, 10), F(1)):
            for s in range(len(P)):
                for a in range(2):
                    assert mean_gae(P, R, pi, V, gamma, lam, s, a) == Q[s][a] - V[s]


def test_wrong_values_only_lambda_one_is_unbiased():
    rng = random.Random(8)
    P, R, pi = random_dag(rng, 4, 2)
    gamma = F(9, 10)
    V, Q = solve_values(P, R, gamma, pi)
    Vw = [v + F(rng.randint(1, 5), 2) for v in V]
    # lambda = 1: Q(s,a) - Vw(s); the error depends on s only, so it is a baseline
    for a in range(2):
        assert mean_gae(P, R, pi, Vw, gamma, F(1), 0, a) == Q[0][a] - Vw[0]
    # lambda < 1: the error of later values enters and depends on the action
    errs = [mean_gae(P, R, pi, Vw, gamma, F(1, 2), 0, a) - (Q[0][a] - V[0]) for a in range(2)]
    assert errs[0] != errs[1]
