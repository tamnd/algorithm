# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retrace/. The authors are listed in prov/Y7PV00.jsonl.

"""Retrace(lambda) (Munos, Stepleton, Harutyunyan and Bellemare 2016), with Tree Backup and Q^pi(lambda) traces for contrast.

A trajectory is a list of (x, a, r) steps from the behavior policy mu, followed by the last state x_T
(None if the episode ended). pi(a, x) and mu(a, x) are action probabilities; q is a dict on (x, a).
A model maps (x, a) to a list of (probability, reward, next state or None).
"""

from fractions import Fraction
from typing import Callable, Hashable, Sequence


def trace_coefficient(kind: str, lam, p, m):
    """c(x, a) from p = pi(a|x) and m = mu(a|x)."""
    if kind == "retrace":
        return lam * min(1, p / m)
    if kind == "tree-backup":
        return lam * p
    if kind == "q-pi-lambda":
        return lam
    if kind == "importance-sampling":
        return lam * p / m
    raise ValueError(kind)


def expected_q(q: dict, x, pi: Callable, actions: Sequence):
    return 0 if x is None else sum(pi(b, x) * q.get((x, b), 0) for b in actions)


def retrace(trajectory: Sequence[tuple], x_last, q: dict, pi: Callable, mu: Callable, actions: Sequence, gamma, lam, alpha, kind: str = "retrace"):
    """One offline Retrace update of q in place along the trajectory. Returns the targets Q^ret_t."""
    g = expected_q(q, x_last, pi, actions)  # @line L1
    targets = [0] * len(trajectory)
    for t in range(len(trajectory) - 1, -1, -1):  # @line L2
        x, a, r = trajectory[t]
        targets[t] = r + gamma * g  # @line L3
        c = trace_coefficient(kind, lam, pi(a, x), mu(a, x))  # @line L4
        g = expected_q(q, x, pi, actions) + c * (targets[t] - q.get((x, a), 0))  # @line L5
    for t, (x, a, _) in enumerate(trajectory):  # @line L6
        q[x, a] = q.get((x, a), 0) + alpha * (targets[t] - q.get((x, a), 0))  # @line L7
    return targets  # @line L8


def solve(a: list, b: list) -> list:
    """Gaussian elimination with partial pivoting; exact for Fractions."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda i: abs(m[i][col]))
        if m[piv][col] == 0:
            raise ValueError("singular matrix")
        m[col], m[piv] = m[piv], m[col]
        for i in range(n):
            if i != col and m[i][col] != 0:
                f = m[i][col] / m[col][col]
                m[i] = [u - f * v for u, v in zip(m[i], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def q_pi(model: dict, pi: Callable, actions: Sequence, gamma) -> dict:
    """Q^pi by solving (I - gamma P^pi) Q = r_bar."""
    pairs = list(model)
    idx = {p: i for i, p in enumerate(pairs)}
    a = [[Fraction(int(i == j)) for j in range(len(pairs))] for i in range(len(pairs))]
    b = [0] * len(pairs)
    for i, x_a in enumerate(pairs):
        for prob, r, y in model[x_a]:
            b[i] += prob * r
            if y is not None:
                for c in actions:
                    a[i][idx[y, c]] -= gamma * prob * pi(c, y)
    return dict(zip(pairs, solve(a, b)))


def expected_operator(q: dict, model: dict, pi: Callable, mu: Callable, actions: Sequence, gamma, lam, kind: str = "retrace") -> dict:
    """RQ = Q + (I - gamma P^{c mu})^{-1} (T^pi Q - Q), the mean of the Retrace target over trajectories of mu."""
    pairs = list(model)
    idx = {p: i for i, p in enumerate(pairs)}
    a = [[Fraction(int(i == j)) for j in range(len(pairs))] for i in range(len(pairs))]
    b = []
    for i, x_a in enumerate(pairs):
        t_pi = 0
        for prob, r, y in model[x_a]:
            t_pi += prob * (r + gamma * expected_q(q, y, pi, actions))
            if y is not None:
                for c in actions:
                    m = mu(c, y)
                    if m != 0:
                        a[i][idx[y, c]] -= gamma * prob * m * trace_coefficient(kind, lam, pi(c, y), m)
        b.append(t_pi - q.get(x_a, 0))
    z = solve(a, b)
    return {x_a: q.get(x_a, 0) + z[i] for i, x_a in enumerate(pairs)}
