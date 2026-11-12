# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prioritized-experience-replay/. The authors are listed in prov/T8RE4E.jsonl.

"""Prioritized experience replay with a sum tree (proportional variant).

Transition i has priority p_i = |delta_i| + eps and is sampled with
probability P(i) = p_i^alpha / sum_k p_k^alpha. The importance weight is
w_i = (N P(i))^(-beta), divided by the largest weight of the minibatch.

SumTree keeps the leaf values v_0 .. v_{n-1} in an array tree of size 2m,
where m is the capacity rounded up to a power of two; tree[1] is the total
and tree[j] = tree[2j] + tree[2j+1]. update and find cost O(log m).
Values may be ints, floats or fractions.Fraction.
"""

import random
from typing import Any


class SumTree:
    """A complete binary tree whose internal nodes hold the sums of their leaves."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        m = 1
        while m < capacity:
            m *= 2
        self.capacity = capacity
        self.size = m
        self.tree: list[Any] = [0] * (2 * m)

    def total(self):
        return self.tree[1]

    def leaf(self, i: int):
        return self.tree[self.size + i]

    def update(self, i: int, value) -> None:
        """Set leaf i to value and fix the sums on the path to the root."""
        if not 0 <= i < self.capacity:
            raise IndexError("leaf index out of range")
        j = self.size + i
        self.tree[j] = value
        j //= 2
        while j >= 1:
            self.tree[j] = self.tree[2 * j] + self.tree[2 * j + 1]
            j //= 2

    def find(self, u) -> int:
        """Return the leaf i with v_0 + .. + v_{i-1} <= u < v_0 + .. + v_i.

        Precondition: 0 <= u < total(). For floats, a u that rounding pushes
        past the last positive leaf is moved back to that leaf.
        """
        j = 1
        while j < self.size:
            left = 2 * j
            if u < self.tree[left] or self.tree[left + 1] == 0:
                j = left
            else:
                u -= self.tree[left]
                j = left + 1
        return j - self.size


class PrioritizedReplay:
    """A circular buffer of transitions with proportional prioritized sampling."""

    def __init__(self, capacity: int, alpha: float, eps: float = 1e-6) -> None:
        self.tree = SumTree(capacity)  # @line L1
        self.capacity = capacity
        self.alpha = alpha
        self.eps = eps
        self.data: list[Any] = []
        self.next = 0
        self.p_max = 1.0  # @line L1

    def __len__(self) -> int:
        return len(self.data)

    def add(self, transition: Any) -> None:
        """Store a transition with the largest priority seen so far."""
        if len(self.data) < self.capacity:
            self.data.append(transition)
        else:
            self.data[self.next] = transition
        self.tree.update(self.next, self.p_max ** self.alpha)  # @line L2
        self.next = (self.next + 1) % self.capacity

    def probability(self, i: int) -> float:
        return self.tree.leaf(i) / self.tree.total()

    def sample(self, batch_size: int, beta: float, rng: random.Random):
        """Return (indices, transitions, weights) of a stratified prioritized minibatch."""
        n = len(self.data)
        if n == 0:
            raise ValueError("cannot sample from an empty buffer")
        total = self.tree.total()
        seg = total / batch_size  # @line L3
        idx, weights = [], []
        for j in range(batch_size):
            u = (j + rng.random()) * seg  # @line L4
            i = self.tree.find(min(u, total * (1 - 1e-12)))  # @line L4
            idx.append(i)
            weights.append((n * self.probability(i)) ** (-beta))  # @line L5
        w_max = max(weights)
        weights = [w / w_max for w in weights]  # @line L6
        return idx, [self.data[i] for i in idx], weights

    def update_priorities(self, idx: list[int], td_errors: list[float]) -> None:
        """Set p_i = |delta_i| + eps for each sampled index."""
        for i, d in zip(idx, td_errors):
            p = abs(d) + self.eps  # @line L7
            self.tree.update(i, p ** self.alpha)  # @line L7
            self.p_max = max(self.p_max, p)  # @line L7


def rank_based_probabilities(td_errors: list[float], alpha: float) -> list[float]:
    """P(i) proportional to (1 / rank(i))^alpha, rank 1 for the largest |delta|."""
    order = sorted(range(len(td_errors)), key=lambda i: -abs(td_errors[i]))
    p = [0.0] * len(td_errors)
    for r, i in enumerate(order, start=1):
        p[i] = (1.0 / r) ** alpha
    z = sum(p)
    return [x / z for x in p]
