# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/advantage-function/. The authors are listed in prov/H7XRK4.jsonl.
"""The advantage function A^pi = Q^pi - V^pi of a finite discounted MDP.

P[s][a][t] is the transition probability, R[s][a] the expected reward and
pi[s][a] the probability of action a in state s. Use Fractions for exact values.
"""

from typing import List


def solve_linear(a, b):
    """Solve a x = b by Gaussian elimination with row pivoting. Cost O(n^3)."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def induced_chain(P, pi):
    n, m = len(P), len(P[0])
    return [[sum(pi[s][a] * P[s][a][t] for a in range(m)) for t in range(n)] for s in range(n)]


def state_value(P, R, pi, gamma) -> List:
    """V^pi = (I - gamma P^pi)^(-1) R^pi."""
    n, m = len(P), len(P[0])
    pp = induced_chain(P, pi)
    a = [[(1 if s == t else 0) - gamma * pp[s][t] for t in range(n)] for s in range(n)]
    return solve_linear(a, [sum(pi[s][b] * R[s][b] for b in range(m)) for s in range(n)])


def advantage(P, R, pi, gamma):
    """Return (A, Q, V) with Q(s, a) = R(s, a) + gamma sum_t P(t|s, a) V(t) and A = Q - V."""
    n, m = len(P), len(P[0])
    v = state_value(P, R, pi, gamma)
    q = [[R[s][a] + gamma * sum(P[s][a][t] * v[t] for t in range(n)) for a in range(m)] for s in range(n)]
    adv = [[q[s][a] - v[s] for a in range(m)] for s in range(n)]
    return adv, q, v


def discounted_occupancy(P, pi, gamma, mu) -> List:
    """d(s) = (1 - gamma) sum_k gamma^k Pr(S_k = s), the row vector (1 - gamma) mu (I - gamma P^pi)^(-1)."""
    n = len(P)
    pp = induced_chain(P, pi)
    # solve x (I - gamma P^pi) = (1 - gamma) mu, the transposed system
    a = [[(1 if s == t else 0) - gamma * pp[t][s] for t in range(n)] for s in range(n)]
    return solve_linear(a, [(1 - gamma) * x for x in mu])


def performance_difference(P, R, pi_new, pi_old, gamma, mu):
    """The right side of the performance difference lemma:
    (1 / (1 - gamma)) sum_s d^(pi_new)_mu(s) sum_a pi_new(a|s) A^(pi_old)(s, a)."""
    adv, _, _ = advantage(P, R, pi_old, gamma)
    d = discounted_occupancy(P, pi_new, gamma, mu)
    m = len(P[0])
    return sum(d[s] * sum(pi_new[s][a] * adv[s][a] for a in range(m)) for s in range(len(P))) / (1 - gamma)


def expected_td_error(P, R, gamma, v, s, a):
    """E[delta | S = s, A = a] for delta = R + gamma v(S') - v(S), summed over the next states."""
    return sum(P[s][a][t] * (R[s][a] + gamma * v[t] - v[s]) for t in range(len(P)))


def gae(rewards, values, gamma, lam):
    """Generalized advantage estimates on one trajectory.
    values has one more entry than rewards (the last one bootstraps).
    A_t = sum_l (gamma lam)^l delta_(t+l). Computed backward in O(T)."""
    out = [0] * len(rewards)
    acc = 0
    for t in range(len(rewards) - 1, -1, -1):
        delta = rewards[t] + gamma * values[t + 1] - values[t]
        acc = delta + gamma * lam * acc
        out[t] = acc
    return out
