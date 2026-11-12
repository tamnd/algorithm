# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temporal-difference-learning/. The authors are listed in prov/WDFA4D.jsonl.

"""Tabular TD(0) prediction, online and batch.

An episode is a list of pairs (S_t, R_(t+1)) for t = 0, ..., T - 1. The state
after the last pair is terminal, with value 0. Because the policy is fixed,
running TD(0) over a recorded episode makes the same updates, in the same
order, as running it while the episode is generated.
"""

from typing import Callable, Hashable, Iterable, Sequence

Episode = Sequence[tuple[Hashable, object]]


def td0(episodes: Iterable[Episode], alpha, gamma, V: dict | None = None, v0=0):
    """Run online TD(0) over the episodes and return the value table V.

    alpha is a number, or a function of the visit count n = 1, 2, ... of the
    updated state (for example lambda n: 1 / n). States not in V start at v0.
    Cost: O(1) arithmetic operations per step, O(number of states) memory.
    """
    V = {} if V is None else V
    n: dict = {}
    step: Callable = alpha if callable(alpha) else (lambda k: alpha)
    for ep in episodes:  # @line L1
        T = len(ep)
        for t in range(T):  # @line L2
            s, r = ep[t]
            if t + 1 < T:  # @line L3
                target = r + gamma * V.get(ep[t + 1][0], v0)
            else:
                target = r  # @line L4
            vs = V.get(s, v0)
            delta = target - vs  # @line L5
            n[s] = n.get(s, 0) + 1
            V[s] = vs + step(n[s]) * delta  # @line L6
    return V  # @line L7


def batch_td0(episodes: Sequence[Episode], alpha, gamma, v0=0, tol=1e-12, max_sweeps=10**6):
    """Batch TD(0): sum the TD(0) increments over the whole batch with V fixed,
    apply them, and repeat until the largest increment is below tol.

    For a small enough alpha this converges to the certainty-equivalence
    estimate: the value function of the maximum likelihood Markov model of the batch.
    """
    states = {s for ep in episodes for s, _ in ep}
    V = {s: v0 for s in states}
    for _ in range(max_sweeps):
        inc = {s: 0 * alpha for s in states}
        for ep in episodes:
            T = len(ep)
            for t in range(T):
                s, r = ep[t]
                nxt = gamma * V[ep[t + 1][0]] if t + 1 < T else 0
                inc[s] += alpha * (r + nxt - V[s])
        for s in states:
            V[s] += inc[s]
        if max(abs(x) for x in inc.values()) < tol:
            return V
    raise RuntimeError("batch TD(0) did not converge; use a smaller alpha")
