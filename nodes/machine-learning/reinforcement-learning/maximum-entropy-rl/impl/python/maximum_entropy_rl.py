# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-entropy-rl/. The authors are listed in prov/X97YP9.jsonl.

"""Maximum entropy reinforcement learning in a finite discounted MDP.

The objective of a policy pi is the expected sum of gamma^t (r_t + alpha H(pi(.|s_t))),
where H is the Shannon entropy in nats and alpha > 0 is the temperature.
P[s][a][t] is the transition probability (rows may sum to less than 1; the
missing mass ends the episode), R[s][a] the expected reward.

Soft value iteration repeats the soft Bellman backup
    Q(s, a) = R(s, a) + gamma sum_t P(t | s, a) V(t),
    V(s)    = alpha log sum_a exp(Q(s, a) / alpha),
with the log-sum-exp evaluated stably. It is a gamma-contraction in the
maximum norm, so it has one fixed point, the soft optimal value. Each sweep
costs O(|S|^2 |A|); reaching accuracy eps needs O(log(1 / eps) / (1 - gamma)) sweeps.
"""

import math


def log_sum_exp(xs, alpha=1.0):
    """alpha log sum_i exp(x_i / alpha), computed as m + alpha log sum_i exp((x_i - m) / alpha) with m = max x_i."""
    m = max(xs)
    return m + alpha * math.log(sum(math.exp((x - m) / alpha) for x in xs))


def entropy(p):
    """Shannon entropy in nats; 0 log 0 = 0."""
    return -sum(x * math.log(x) for x in p if x > 0)


def q_from_v(P, R, V, gamma):
    return [[R[s][a] + gamma * sum(p * v for p, v in zip(P[s][a], V)) for a in range(len(R[s]))] for s in range(len(R))]


def soft_backup(P, R, V, gamma, alpha):
    """One soft Bellman backup V -> alpha log sum_a exp(Q_V(s, a) / alpha)."""
    return [log_sum_exp(row, alpha) for row in q_from_v(P, R, V, gamma)]


def soft_value_iteration(P, R, gamma, alpha, tol=1e-12, max_sweeps=100000):
    """Iterate the soft backup from V = 0 until the change is at most tol (1 - gamma) / gamma; returns (V, Q)."""
    V = [0.0] * len(R)
    for _ in range(max_sweeps):
        W = soft_backup(P, R, V, gamma, alpha)
        done = max(abs(x - y) for x, y in zip(W, V)) <= tol * (1 - gamma) / max(gamma, 1e-300)
        V = W
        if done:
            break
    return V, q_from_v(P, R, V, gamma)


def hard_value_iteration(P, R, gamma, tol=1e-12, max_sweeps=100000):
    """Ordinary value iteration, the limit alpha -> 0 of the soft backup."""
    V = [0.0] * len(R)
    for _ in range(max_sweeps):
        W = [max(row) for row in q_from_v(P, R, V, gamma)]
        done = max(abs(x - y) for x, y in zip(W, V)) <= tol * (1 - gamma) / max(gamma, 1e-300)
        V = W
        if done:
            break
    return V


def soft_greedy_policy(Q, V, alpha):
    """pi(a | s) = exp((Q(s, a) - V(s)) / alpha), a softmax of Q / alpha."""
    return [[math.exp((q - v) / alpha) for q in row] for row, v in zip(Q, V)]


def soft_policy_value(P, R, pi, gamma, alpha, sweeps=2000):
    """Entropy-augmented value of a fixed policy: V(s) = sum_a pi(a|s) (Q(s, a)) + alpha H(pi(.|s)), by repeated backups."""
    V = [0.0] * len(R)
    for _ in range(sweeps):
        Q = q_from_v(P, R, V, gamma)
        V = [sum(p * q for p, q in zip(pi[s], Q[s])) + alpha * entropy(pi[s]) for s in range(len(R))]
    return V
