# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fitted-q-iteration/. The authors are listed in prov/BSTS37.jsonl.

"""Fitted Q-iteration (Ernst, Geurts and Wehenkel 2005) with pluggable regressors.

A transition is (s, a, r, s_next), with s_next = None when the episode ends there.
A regressor maps a list of ((s, a), y) pairs to a function q(s, a).
"""

import heapq
from collections import defaultdict
from fractions import Fraction
from typing import Callable, Hashable, Sequence

Q = Callable[[Hashable, Hashable], float]


def zero_q(s, a):
    return 0


def _mean(total, n: int):
    """total / n, exact unless total is a float."""
    return total / n if isinstance(total, float) else Fraction(total) / n


def fitted_q_iteration(transitions: Sequence[tuple], actions: Sequence, gamma, iterations: int, regress: Callable, history: bool = False):
    """Return Q_K after K = iterations rounds, or the list [Q_0, ..., Q_K] if history is true."""
    q = zero_q  # @line L1
    qs = [q]
    for _ in range(iterations):  # @line L2
        training_set = []  # @line L3
        for s, a, r, s_next in transitions:  # @line L4
            y = r if s_next is None else r + gamma * max(q(s_next, b) for b in actions)  # @line L5
            training_set.append(((s, a), y))  # @line L6
        q = regress(training_set)  # @line L7
        qs.append(q)
    return qs if history else q  # @line L8


def greedy(q: Q, actions: Sequence) -> Callable:
    """The greedy policy of q; ties go to the first action in the list."""
    return lambda s: max(actions, key=lambda a: q(s, a))


def tabular_regressor(training_set):
    """Least squares over all functions of (s, a): the mean target of each pair, 0 for unseen pairs."""
    total, count = defaultdict(int), defaultdict(int)
    for x, y in training_set:
        total[x] += y
        count[x] += 1
    table = {x: _mean(total[x], count[x]) for x in total}
    return lambda s, a: table.get((s, a), 0)


def knn_regressor(k: int, distance: Callable = lambda u, v: abs(u - v)):
    """k-nearest-neighbor averaging per action. It is an averager, so FQI with it is a gamma-contraction."""

    def regress(training_set):
        by_action = defaultdict(list)
        for (s, a), y in training_set:
            by_action[a].append((s, y))

        def q(s, a):
            points = by_action.get(a)
            if not points:
                return 0
            nearest = heapq.nsmallest(k, points, key=lambda p: distance(p[0], s))
            return sum(y for _, y in nearest) / len(nearest)

        return q

    return regress


def empirical_mdp(transitions: Sequence[tuple]):
    """Counts-based model: P_hat[(s, a)] maps s_next (or None for the end) to its frequency, R_hat is the mean reward."""
    nexts, rewards, count = defaultdict(lambda: defaultdict(int)), defaultdict(int), defaultdict(int)
    for s, a, r, s_next in transitions:
        nexts[s, a][s_next] += 1
        rewards[s, a] += r
        count[s, a] += 1
    p_hat = {x: {t: Fraction(c, count[x]) for t, c in nxt.items()} for x, nxt in nexts.items()}
    r_hat = {x: _mean(rewards[x], count[x]) for x in count}
    return p_hat, r_hat


def q_value_iteration(p_hat, r_hat, actions: Sequence, gamma, iterations: int):
    """Value iteration on Q for the model, with Q = 0 on pairs the model does not contain. Returns [Q_0, ..., Q_K] as dicts."""
    q = {}
    out = [dict(q)]
    for _ in range(iterations):
        q = {
            x: r_hat[x] + gamma * sum(p * max(q.get((t, b), 0) for b in actions) for t, p in nxt.items() if t is not None)
            for x, nxt in p_hat.items()
        }
        out.append(q)
    return out
