# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-interleaving/. The authors are listed in prov/5WYWSE.jsonl.

import random
from typing import Collection, Hashable, Sequence


def softmax_weights(ranking: Sequence[Hashable], tau: float) -> dict[Hashable, float]:
    """Return the weight 1 / r**tau of each document at rank r (from 1)."""
    return {d: 1.0 / (r + 1) ** tau for r, d in enumerate(ranking)}


def interleave(
    a: Sequence[Hashable], b: Sequence[Hashable], rng: random.Random, tau: float = 3.0
) -> tuple[list[Hashable], list[int]]:
    """Return the shown list and the assignment (1 for a, 2 for b) of each position.

    Precondition: a and b are orderings of the same set of n documents. At each
    position a fair coin picks a softmax, and a document is drawn from it among the
    documents not yet shown. Each draw scans the remaining documents, so the time is
    O(n^2) and the extra space is O(n).
    """
    w = {1: softmax_weights(a, tau), 2: softmax_weights(b, tau)}  # @line L1
    shown: list[Hashable] = []
    assign: list[int] = []
    left = list(a)  # @line L2
    while left:  # @line L3
        x = 1 if rng.random() < 0.5 else 2  # @line L4
        total = sum(w[x][d] for d in left)
        u = rng.random() * total
        k = 0
        acc = w[x][left[0]]
        while acc <= u and k + 1 < len(left):
            k += 1
            acc += w[x][left[k]]
        d = left.pop(k)  # @line L5
        shown.append(d)  # @line L6
        assign.append(x)
    return shown, assign  # @line L7


def outcome(assign: Sequence[int], clicked: Collection[int]) -> int:
    """Return 1 if the clicked positions (from 0) credit a more often, -1 if b, else 0."""
    c1 = sum(1 for r in clicked if assign[r] == 1)  # @line L8
    c2 = sum(1 for r in clicked if assign[r] == 2)
    return (c1 > c2) - (c1 < c2)  # @line L9


def posterior(a: Sequence[Hashable], b: Sequence[Hashable], shown: Sequence[Hashable], tau: float = 3.0) -> list[float]:
    """Return q[r] = P(position r was drawn from a's softmax | shown list).

    Precondition: shown is an ordering of the documents of a and b. Given the shown
    list, the assignments of the positions are independent, so two passes with
    suffix sums suffice: O(n) time.
    """
    w1 = softmax_weights(a, tau)
    w2 = softmax_weights(b, tau)
    n = len(shown)
    z1 = [0.0] * (n + 1)
    z2 = [0.0] * (n + 1)
    for r in range(n - 1, -1, -1):  # suffix sums: the weight left before position r
        z1[r] = z1[r + 1] + w1[shown[r]]
        z2[r] = z2[r + 1] + w2[shown[r]]
    q: list[float] = []
    for r, d in enumerate(shown):  # @line L10
        f1 = w1[d] / z1[r]
        f2 = w2[d] / z2[r]
        q.append(f1 / (f1 + f2))
    return q


def marginal_outcome(
    a: Sequence[Hashable], b: Sequence[Hashable], shown: Sequence[Hashable], clicked: Collection[int], tau: float = 3.0
) -> float:
    """Return the sum over assignments x of P(x | shown) * outcome(x, clicked).

    Precondition: as for posterior; clicked holds positions from 0. A dynamic
    program over the clicked positions tracks the distribution of c1 - c2, so the
    time is O(n + c^2) for c clicks, against 2^n terms for the plain sum.
    """
    q = posterior(a, b, shown, tau)  # @line L11
    dist = {0: 1.0}
    for r in sorted(clicked):  # @line L12
        nxt: dict[int, float] = {}
        for diff, p in dist.items():
            nxt[diff + 1] = nxt.get(diff + 1, 0.0) + p * q[r]
            nxt[diff - 1] = nxt.get(diff - 1, 0.0) + p * (1.0 - q[r])
        dist = nxt
    return sum(p for diff, p in dist.items() if diff > 0) - sum(p for diff, p in dist.items() if diff < 0)  # @line L13
