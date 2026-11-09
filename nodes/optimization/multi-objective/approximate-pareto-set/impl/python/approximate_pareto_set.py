# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-pareto-set/. The authors are listed in prov/ERC7WZ.jsonl.

"""An epsilon-Pareto set of a stream of points, kept by the box archive of
Laumanns, Thiele, Deb and Zitzler (2002), in its additive form.

All objectives are minimized. Each objective value is at least `lower[i]`.
The box of y is b(y)_i = floor((y_i - lower_i) / eps). The archive keeps at
most one point per box, and its boxes are mutually non-dominated. Then:

- each point seen so far is eps-dominated by an archive point: a_i < y_i + eps;
- the archive points are mutually non-dominated;
- if each value is at most upper_i, the archive has at most K^(p-1) points,
  K = floor((upper - lower) / eps) + 1, for an equal range in each objective.

Use integers or fractions.Fraction for exact boxes.
"""

from math import floor
from typing import Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for x, y in zip(a, b):
        if x > y:
            return False
        if x < y:
            strict = True
    return strict


def eps_dominates(a: Vector, b: Vector, eps: float) -> bool:
    """Additive epsilon-dominance: a_i - eps <= b_i for each i."""
    return all(x - eps <= y for x, y in zip(a, b))


def is_eps_pareto_set(archive: Sequence[Vector], seen: Sequence[Vector], eps: float) -> bool:
    """True when each point of `seen` is eps-dominated by a point of `archive`."""
    return all(any(eps_dominates(a, y, eps) for a in archive) for y in seen)


class EpsilonArchive:
    """The box archive. Points are stored as tuples."""

    def __init__(self, eps: float, lower: Sequence[float]):
        if eps <= 0:
            raise ValueError("eps must be positive")
        self.eps = eps
        self.lower = tuple(lower)
        self.points: list[tuple] = []

    def box(self, y: Vector) -> tuple[int, ...]:
        return tuple(floor((v - lo) / self.eps) for v, lo in zip(y, self.lower))

    def _corner_dist2(self, y: Vector, b: tuple[int, ...]):
        return sum((v - (lo + k * self.eps)) ** 2 for v, lo, k in zip(y, self.lower, b))

    def add(self, y: Vector) -> bool:
        """Offer y to the archive. Return True when y is stored."""
        y = tuple(y)
        b = self.box(y)  # @line L1
        boxes = [self.box(a) for a in self.points]
        if any(dominates(ba, b) for ba in boxes):  # @line L2
            return False  # @line L3
        for k, ba in enumerate(boxes):  # @line L4
            if ba == b:
                a = self.points[k]
                if dominates(y, a) or (  # @line L5
                    not dominates(a, y) and self._corner_dist2(y, b) < self._corner_dist2(a, b)
                ):
                    self.points[k] = y  # @line L6
                    return True
                return False  # @line L7
        self.points = [a for a, ba in zip(self.points, boxes) if not dominates(b, ba)]  # @line L8
        self.points.append(y)  # @line L9
        return True
