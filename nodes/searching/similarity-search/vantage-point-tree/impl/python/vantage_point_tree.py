# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vantage-point-tree/. The authors are listed in prov/ET45HH.jsonl.

import math
import random
from dataclasses import dataclass
from typing import Callable, Generic, Optional, Sequence, TypeVar

T = TypeVar("T")
Metric = Callable[[T, T], float]


@dataclass
class Node(Generic[T]):
    vp: T
    mu: float
    inside: Optional["Node[T]"]
    outside: Optional["Node[T]"]


class VPTree(Generic[T]):
    """A vantage-point tree over a finite set of objects of a metric space.

    choose(S) picks the vantage point of a nonempty list S; the default is a random element.
    The counter evaluations counts calls of the metric.
    """

    def __init__(self, points: Sequence[T], d: Metric, choose: Optional[Callable[[list[T]], int]] = None, seed: int = 0) -> None:
        self._d = d
        self.evaluations = 0
        rng = random.Random(seed)
        self._choose = choose or (lambda s: rng.randrange(len(s)))
        self.root = self._build(list(points))

    def dist(self, a: T, b: T) -> float:
        self.evaluations += 1
        return self._d(a, b)

    def _build(self, s: list[T]) -> Optional[Node[T]]:
        if not s:  # @line L1
            return None
        i = self._choose(s)  # @line L2
        vp = s[i]
        rest = s[:i] + s[i + 1 :]
        keyed = sorted(((self.dist(vp, x), j) for j, x in enumerate(rest)))  # @line L3
        m = (len(keyed) + 1) // 2
        if not keyed:  # @line L4
            return Node(vp, 0.0, None, None)
        mu = keyed[m - 1][0]  # @line L5
        inside = [rest[j] for _, j in keyed[:m]]
        outside = [rest[j] for _, j in keyed[m:]]
        return Node(vp, mu, self._build(inside), self._build(outside))  # @line L6

    def range(self, q: T, r: float) -> list[T]:
        """All stored objects x with d(q, x) <= r."""
        out: list[T] = []
        self._range(self.root, q, r, out)
        return out

    def _range(self, node: Optional[Node[T]], q: T, r: float, out: list[T]) -> None:
        if node is None:  # @line L7
            return
        t = self.dist(q, node.vp)  # @line L8
        if t <= r:
            out.append(node.vp)
        if t - r <= node.mu:  # @line L9
            self._range(node.inside, q, r, out)
        if t + r >= node.mu:  # @line L10
            self._range(node.outside, q, r, out)

    def nearest(self, q: T) -> Optional[tuple[T, float]]:
        """A stored object at the least distance from q, with that distance; None if empty."""
        best: list = [None, math.inf]
        self._nearest(self.root, q, best)
        return None if self.root is None else (best[0], best[1])

    def _nearest(self, node: Optional[Node[T]], q: T, best: list) -> None:
        if node is None:  # @line L11
            return
        t = self.dist(q, node.vp)  # @line L12
        if t < best[1]:
            best[0], best[1] = node.vp, t
        if t <= node.mu:  # @line L13
            order = [(node.inside, True), (node.outside, False)]
        else:
            order = [(node.outside, False), (node.inside, True)]
        for child, is_inside in order:  # @line L14
            if (t - best[1] <= node.mu) if is_inside else (t + best[1] >= node.mu):  # @line L15
                self._nearest(child, q, best)
