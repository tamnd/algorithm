# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/v-trace/. The authors are listed in prov/V75JCF.jsonl.

"""V-trace (Espeholt et al. 2018, IMPALA): off-policy n-step targets for a state value function.

A trajectory is a list of (x, a, r) steps from the behavior policy mu, then the last state x_n
(None if the episode ended). pi(a, x) and mu(a, x) give action probabilities; v is a dict on states.
rho_bar = None means no truncation. A model maps (x, a) to a list of (probability, reward, next state or None).
"""

from fractions import Fraction
from typing import Callable, Sequence


def clip(bar, ratio):
    return ratio if bar is None else min(bar, ratio)


def v_trace(trajectory: Sequence[tuple], x_last, v: dict, pi: Callable, mu: Callable, gamma, rho_bar, c_bar, alpha=0, lam=1):
    """Compute the V-trace targets v_s and the policy gradient advantages, then move v toward the targets."""
    value = lambda x: 0 if x is None else v.get(x, 0)
    n = len(trajectory)
    targets, advantages = [0] * (n + 1), [0] * n
    targets[n] = value(x_last)  # @line L1
    nxt = [x for x, _, _ in trajectory[1:]] + [x_last]
    for t in range(n - 1, -1, -1):  # @line L2
        x, a, r = trajectory[t]
        ratio = pi(a, x) / mu(a, x)
        rho, c = clip(rho_bar, ratio), lam * clip(c_bar, ratio)  # @line L3
        delta = rho * (r + gamma * value(nxt[t]) - value(x))  # @line L4
        targets[t] = value(x) + delta + gamma * c * (targets[t + 1] - value(nxt[t]))  # @line L5
        advantages[t] = rho * (r + gamma * targets[t + 1] - value(x))  # @line L6
    for t, (x, _, _) in enumerate(trajectory):
        v[x] = value(x) + alpha * (targets[t] - value(x))  # @line L7
    return targets[:n], advantages  # @line L8


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
                m[i] = [u - f * w for u, w in zip(m[i], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def states_of(model: dict) -> list:
    return sorted({x for x, _ in model}, key=str)


def truncated_target_policy(pi: Callable, mu: Callable, actions: Sequence, rho_bar) -> Callable:
    """pi_rho_bar(a|x), proportional to min(rho_bar mu(a|x), pi(a|x))."""

    def policy(a, x):
        w = {b: pi(b, x) if rho_bar is None else min(rho_bar * mu(b, x), pi(b, x)) for b in actions}
        return w[a] / sum(w.values())

    return policy


def state_values(model: dict, policy: Callable, actions: Sequence, gamma) -> dict:
    """V^policy by solving (I - gamma P^policy) V = r^policy."""
    xs = states_of(model)
    idx = {x: i for i, x in enumerate(xs)}
    a = [[Fraction(int(i == j)) for j in range(len(xs))] for i in range(len(xs))]
    b = [0] * len(xs)
    for x in xs:
        for act in actions:
            w = policy(act, x)
            for p, r, y in model[x, act]:
                b[idx[x]] += w * p * r
                if y is not None:
                    a[idx[x]][idx[y]] -= gamma * w * p
    return dict(zip(xs, solve(a, b)))


def v_trace_operator(v: dict, model: dict, pi: Callable, mu: Callable, actions: Sequence, gamma, rho_bar, c_bar) -> dict:
    """RV = V + (I - gamma C)^{-1} g with C(x, y) = sum_a mu c P and g(x) = sum_a mu rho (r + gamma P V - V(x))."""
    xs = states_of(model)
    idx = {x: i for i, x in enumerate(xs)}
    value = lambda x: 0 if x is None else v.get(x, 0)
    a = [[Fraction(int(i == j)) for j in range(len(xs))] for i in range(len(xs))]
    g = [0] * len(xs)
    for x in xs:
        for act in actions:
            m = mu(act, x)
            if m == 0:
                continue
            ratio = pi(act, x) / m
            rho, c = clip(rho_bar, ratio), clip(c_bar, ratio)
            for p, r, y in model[x, act]:
                g[idx[x]] += m * rho * p * (r + gamma * value(y) - value(x))
                if y is not None:
                    a[idx[x]][idx[y]] -= gamma * m * c * p
    z = solve(a, g)
    return {x: value(x) + z[idx[x]] for x in xs}
