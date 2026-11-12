# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/value-iteration/. The authors are listed in prov/XRA79Y.jsonl.

"""Value iteration for a finite MDP with the discounted criterion.

An MDP is given by P and R: P[s][a] is a list of pairs (p, t), the
probability p of the next state t, and R[s][a] is the expected reward of
action a in state s. The numbers may be floats or fractions.Fraction.
"""

from typing import Sequence

Model = Sequence[Sequence[Sequence[tuple]]]


def q_value(P: Model, R, gamma, V, s: int, a: int):
    """Return R(s, a) + gamma * sum over t of P(t | s, a) V(t)."""
    return R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a])


def greedy_policy(P: Model, R, gamma, V) -> list[int]:
    """Return, for each state, the first action that maximizes q_value."""
    pi = []
    for s in range(len(P)):
        qs = [q_value(P, R, gamma, V, s, a) for a in range(len(P[s]))]
        pi.append(qs.index(max(qs)))
    return pi


def value_iteration(P: Model, R, gamma, eps, v0=None, max_iter: int | None = None):
    """Return (V, pi, k): the last iterate, a greedy policy and the number of sweeps.

    Precondition: 0 <= gamma < 1, eps > 0, each state has at least one action.
    The loop stops when two iterates differ by less than eps (1 - gamma) / (2 gamma)
    in the max norm; then pi is eps-optimal and V is within eps / 2 of V*.
    With max_iter set, it also stops after max_iter sweeps (eps = 0 then
    gives exactly max_iter sweeps). Each sweep costs O(sum of the sizes of P[s][a]).
    """
    n = len(P)
    V = [0 * gamma] * n if v0 is None else list(v0)  # @line L1
    stop = eps * (1 - gamma) / (2 * gamma) if gamma > 0 else None
    k = 0
    while True:  # @line L2
        W = list(V)
        for s in range(n):  # @line L3
            W[s] = max(q_value(P, R, gamma, V, s, a) for a in range(len(P[s])))  # @line L4
        delta = max(abs(W[s] - V[s]) for s in range(n)) if n else 0  # @line L5
        V = W  # @line L6
        k += 1
        if stop is None or delta < stop or (max_iter is not None and k >= max_iter):  # @line L7
            break
    pi = [0] * n
    for s in range(n):  # @line L8
        qs = [q_value(P, R, gamma, V, s, a) for a in range(len(P[s]))]
        pi[s] = qs.index(max(qs))  # @line L9
    return V, pi, k  # @line L10
