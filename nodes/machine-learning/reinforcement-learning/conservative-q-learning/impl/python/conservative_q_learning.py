# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-q-learning/. The authors are listed in prov/QCDBQ4.jsonl.

"""Conservative Q-learning (CQL), tabular.

cql_h is the CQL(H) variant (Kumar et al. 2020, eq. 4) with the max backup:
each outer iteration freezes the target, then takes G full-batch gradient
steps on

  alpha * (1/N) sum_i [ logsumexp_a Q(s_i, a) - Q(s_i, a_i) ]
  + (1/N) sum_i 1/2 (Q(s_i, a_i) - y_i)^2,   y_i = r_i + gamma max_a' Qk(s'_i, a').

fqi is tabular fitted Q-iteration on the same data, for comparison.
cql_evaluate is the tabular policy evaluation update of eq. 2 with mu = pi.

A transition is (s, a, r, s2, done). Cost of cql_h: O(K * (N + G * S * A)).
"""

import math


def counts(data, n_states: int, n_actions: int):
    """n(s, a) and the sum of rewards and next states per pair."""
    n = [[0] * n_actions for _ in range(n_states)]
    for s, a, _, _, _ in data:
        n[s][a] += 1
    return n


def mean_targets(data, q, n_states: int, n_actions: int, gamma: float):
    """ybar(s, a) = mean over the data at (s, a) of r + gamma (1 - done) max_a' q(s', a')."""
    tot = [[0.0] * n_actions for _ in range(n_states)]
    n = counts(data, n_states, n_actions)
    for s, a, r, s2, done in data:
        tot[s][a] += r if done else r + gamma * max(q[s2])
    return [[tot[s][a] / n[s][a] if n[s][a] else 0.0 for a in range(n_actions)]
            for s in range(n_states)]


def softmax(row):
    m = max(row)
    e = [math.exp(x - m) for x in row]
    z = sum(e)
    return [x / z for x in e]


def cql_h(data, n_states: int, n_actions: int, gamma: float, alpha: float,
          iters: int, grad_steps: int, lr: float):
    """Tabular CQL(H) with the max backup; returns the Q table."""
    big_n = len(data)
    n = counts(data, n_states, n_actions)
    ns = [sum(row) for row in n]
    q = [[0.0] * n_actions for _ in range(n_states)]  # @line L1
    for _ in range(iters):  # @line L2
        ybar = mean_targets(data, q, n_states, n_actions, gamma)  # @line L3
        for _ in range(grad_steps):  # @line L4
            new = []
            for s in range(n_states):
                sig = softmax(q[s])  # @line L5
                row = []
                for a in range(n_actions):
                    g = alpha * ns[s] * sig[a] - alpha * n[s][a]  # @line L6
                    g += n[s][a] * (q[s][a] - ybar[s][a])  # @line L6
                    row.append(q[s][a] - lr * g / big_n)  # @line L7
                new.append(row)
            q = new
    return q  # @line L8


def fqi(data, n_states: int, n_actions: int, gamma: float, iters: int):
    """Tabular fitted Q-iteration: each pair gets the mean of its targets.

    Pairs with no data keep their initial value 0."""
    n = counts(data, n_states, n_actions)
    q = [[0.0] * n_actions for _ in range(n_states)]
    for _ in range(iters):
        ybar = mean_targets(data, q, n_states, n_actions, gamma)
        q = [[ybar[s][a] if n[s][a] else q[s][a] for a in range(n_actions)]
             for s in range(n_states)]
    return q


def cql_evaluate(data, pi, n_states: int, n_actions: int, gamma: float, alpha: float,
                 iters: int):
    """Tabular CQL policy evaluation (eq. 2, mu = pi): the update

        Q(s, a) <- (B^pi Q)(s, a) - alpha * (pi(a|s) - pihat_b(a|s)) / pihat_b(a|s),

    with the empirical Bellman operator and pihat_b(a|s) = n(s, a) / n(s).
    Every pair must be in the data."""
    n = counts(data, n_states, n_actions)
    ns = [sum(row) for row in n]
    q = [[0.0] * n_actions for _ in range(n_states)]
    for _ in range(iters):
        tot = [[0.0] * n_actions for _ in range(n_states)]
        for s, a, r, s2, done in data:
            v2 = sum(p * x for p, x in zip(pi[s2], q[s2]))
            tot[s][a] += r if done else r + gamma * v2
        q = [[tot[s][a] / n[s][a] - alpha * (pi[s][a] - n[s][a] / ns[s]) / (n[s][a] / ns[s])
              for a in range(n_actions)] for s in range(n_states)]
    return q


def greedy(q):
    """The first maximizing action in each state."""
    return [max(range(len(row)), key=lambda a: (row[a], -a)) for row in q]


def solve(mat, rhs):
    """Solve mat x = rhs by Gauss-Jordan elimination (exact with Fractions)."""
    k = len(rhs)
    m = [list(mat[i]) + [rhs[i]] for i in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda i: abs(m[i][c]))
        m[c], m[p] = m[p], m[c]
        for i in range(k):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def policy_q(step, pi, n_states: int, n_actions: int, gamma):
    """Exact Q^pi of a deterministic MDP step(s, a) -> (r, s2, done) and a
    stochastic policy pi[s][a], by one linear solve over the state values."""
    mat = [[0] * n_states for _ in range(n_states)]
    rhs = [0] * n_states
    for s in range(n_states):
        mat[s][s] += 1
        for a in range(n_actions):
            r, s2, done = step(s, a)
            rhs[s] += pi[s][a] * r
            if not done:
                mat[s][s2] -= gamma * pi[s][a]
    v = solve(mat, rhs)
    out = []
    for s in range(n_states):
        row = []
        for a in range(n_actions):
            r, s2, done = step(s, a)
            row.append(r if done else r + gamma * v[s2])
        out.append(row)
    return out
