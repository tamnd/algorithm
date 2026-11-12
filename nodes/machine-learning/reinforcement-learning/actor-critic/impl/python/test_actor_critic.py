# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/actor-critic/. The authors are listed in prov/2ZBR0P.jsonl.

import random
from fractions import Fraction as F

from actor_critic import actor_critic, softmax, step


def solve(M, b):
    n = len(M)
    A = [list(M[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def bellman(P, R, gamma, pi):
    n, k = len(P), len(pi[0])
    M = [[(1 if s == t else 0) - gamma * sum(pi[s][a] * P[s][a][t] for a in range(k)) for t in range(n)] for s in range(n)]
    return M, solve(M, [sum(pi[s][a] * R[s][a] for a in range(k)) for s in range(n)])


def exact_gradient(P, R, gamma, pi, mu):
    """Oracle: differentiate (I - gamma P_pi) V = r_pi with respect to theta[x][b]."""
    n, k = len(P), len(pi[0])
    M, V = bellman(P, R, gamma, pi)
    out = []
    for x in range(n):
        row = []
        for b in range(k):
            rhs = [F(0)] * n
            for a in range(k):
                rhs[x] += pi[x][a] * ((1 if a == b else 0) - pi[x][b]) * (R[x][a] + gamma * sum(P[x][a][t] * V[t] for t in range(n)))
            row.append(sum(m * v for m, v in zip(mu, solve(M, rhs))))
        out.append(row)
    return out


def all_episodes(P, pi, mu):
    """Every episode of an acyclic MDP with its probability: lists of (s, a, s_next)."""
    n = len(P)
    out, stack = [], [(s, mu[s], []) for s in range(n) if mu[s] > 0]
    while stack:
        s, p, ep = stack.pop()
        for a in range(len(pi[s])):
            q = p * pi[s][a]
            end = 1 - sum(P[s][a])
            if end > 0:
                out.append((q * end, ep + [(s, a, None)]))
            for t in range(n):
                if P[s][a][t] > 0:
                    stack.append((t, q * P[s][a][t], ep + [(s, a, t)]))
    return out


def expected_actor_update(P, R, gamma, pi, mu, V):
    """Mean over all episodes of sum_t gamma^t delta_t grad log pi, with the critic V frozen."""
    n, k = len(P), len(pi[0])
    phi = [[1 if i == s else 0 for i in range(n)] for s in range(n)]
    total = [[F(0)] * k for _ in range(n)]
    eps = all_episodes(P, pi, mu)
    assert sum(p for p, _ in eps) == 1
    for p, ep in eps:
        th = [[F(0)] * k for _ in range(n)]
        I = F(1)
        for s, a, t in ep:
            step(th, list(V), phi, pi, s, a, R[s][a], t, gamma, I, F(1), F(0))
            I *= gamma
        for s in range(n):
            for b in range(k):
                total[s][b] += p * th[s][b]
    return total


def random_dag(rng, n, k):
    P = []
    for s in range(n):
        rows = []
        for _ in range(k):
            w = [0] * (s + 1) + [rng.randint(0, 3) for _ in range(n - s - 1)] + [rng.randint(1, 3)]
            rows.append([F(x, sum(w)) for x in w[:n]])
        P.append(rows)
    R = [[F(rng.randint(-3, 4)) for _ in range(k)] for _ in range(n)]
    return P, R


def random_policy(rng, n, k):
    out = []
    for _ in range(n):
        w = [rng.randint(1, 4) for _ in range(k)]
        out.append([F(x, sum(w)) for x in w])
    return out


def test_worked_steps():
    pi = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
    phi = [[1, 0], [0, 1]]
    theta = [[F(0), F(0)], [F(0), F(0)]]
    w = [F(28, 27), F(44, 27)]
    d0 = step(theta, w, phi, pi, 0, 0, F(1), 1, F(1, 2), F(1), F(1), F(0))
    d1 = step(theta, w, phi, pi, 1, 1, F(3), None, F(1, 2), F(1, 2), F(1), F(0))
    assert (d0, d1) == (F(7, 9), F(37, 27))
    assert theta == [[F(7, 18), F(-7, 18)], [F(-37, 108), F(37, 108)]]
    w2 = [F(0), F(0)]
    step([[F(0), F(0)], [F(0), F(0)]], w2, phi, pi, 0, 0, F(1), 1, F(1, 2), F(1), F(0), F(1, 10))
    assert w2 == [F(1, 10), F(0)]


def test_exact_critic_gives_exact_gradient():
    rng = random.Random(4)
    for _ in range(25):
        n, k = rng.randint(1, 4), rng.randint(2, 3)
        P, R = random_dag(rng, n, k)
        pi = random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        gamma = F(rng.randint(1, 10), 10)
        _, V = bellman(P, R, gamma, pi)
        assert expected_actor_update(P, R, gamma, pi, mu, V) == exact_gradient(P, R, gamma, pi, mu)


def test_wrong_critic_is_biased():
    rng = random.Random(9)
    P, R = random_dag(rng, 3, 2)
    pi = random_policy(rng, 3, 2)
    mu = [F(1), F(0), F(0)]
    gamma = F(9, 10)
    _, V = bellman(P, R, gamma, pi)
    true = exact_gradient(P, R, gamma, pi, mu)
    assert expected_actor_update(P, R, gamma, pi, mu, V) == true
    assert expected_actor_update(P, R, gamma, pi, mu, [F(0)] * 3) != true
    shifted = [V[0], V[1] + 1, V[2]]
    assert expected_actor_update(P, R, gamma, pi, mu, shifted) != true


def test_critic_learns_values_for_a_fixed_policy():
    P = [[[0.5, 0.25], [0.0, 0.75]], [[0.5, 0.0], [0.0, 0.0]]]
    R = [[1.0, 0.0], [0.0, 3.0]]
    phi = [[1.0, 0.0], [0.0, 1.0]]
    theta, w = actor_critic(P, R, 0.5, [0.5, 0.5], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], phi, 0.0, 0.02, 6000, random.Random(3))
    assert theta == [[0.0, 0.0], [0.0, 0.0]]
    assert abs(w[0] - 28 / 27) < 0.1 and abs(w[1] - 44 / 27) < 0.1


def test_learning_run():
    P = [[[0.5, 0.25], [0.0, 0.75]], [[0.5, 0.0], [0.0, 0.0]]]
    R = [[1.0, 0.0], [0.0, 3.0]]
    phi = [[1.0, 0.0], [0.0, 1.0]]
    theta, w = actor_critic(P, R, 0.5, [1.0, 0.0], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], phi, 0.5, 0.1, 3000, random.Random(1))
    pi = softmax(theta)
    assert pi[1][1] > 0.9 and pi[0][0] > 0.9  # the optimal policy: V* = (11/6, 3)
    assert abs(w[1] - 3.0) < 0.5
