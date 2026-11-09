# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypervolume-indicator/. The authors are listed in prov/X557ES.jsonl.

"""The hypervolume indicator of a finite set of images (minimization).

HV(A, r) is the Lebesgue measure of the union of the boxes [a, r] over the
points a of A with a < r in every coordinate. Points that do not strictly
dominate r add nothing. The functions work with int, Fraction or float input;
with int or Fraction input the result is exact.
"""

from typing import Iterable, Sequence

Vector = Sequence


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    return all(u <= v for u, v in zip(a, b)) and any(u < v for u, v in zip(a, b))


def weakly_dominates_set(a: Iterable[Vector], b: Iterable[Vector]) -> bool:
    """Return True when every point of b is weakly dominated by some point of a."""
    a = list(a)
    return all(any(all(u <= v for u, v in zip(x, y)) for x in a) for y in b)


def _inside(points: Iterable[Vector], ref: Vector) -> list:
    return [tuple(x) for x in points if all(u < v for u, v in zip(x, ref))]


def hypervolume_2d(points: Iterable[Vector], ref: Vector):
    """Sweep in the first objective: O(N log N) for N points."""
    pts = sorted(_inside(points, ref))
    total, low = 0, ref[1]
    for x, y in pts:
        if y < low:
            total += (ref[0] - x) * (low - y)
            low = y
    return total


def hypervolume(points: Iterable[Vector], ref: Vector):
    """Exact hypervolume in any dimension by slicing along the last objective.

    The slices between consecutive values of the last coordinate are boxes
    over the (p - 1)-dimensional hypervolume of the points below the slice.
    The cost is exponential in p; see the hypervolume computation page for
    faster methods.
    """
    pts = _inside(points, ref)
    if not pts:
        return 0
    p = len(ref)
    if p == 1:
        return ref[0] - min(x[0] for x in pts)
    if p == 2:
        return hypervolume_2d(pts, ref)
    pts.sort(key=lambda x: x[-1])
    total = 0
    for i, x in enumerate(pts):
        top = pts[i + 1][-1] if i + 1 < len(pts) else ref[-1]
        if top > x[-1]:
            total += (top - x[-1]) * hypervolume([y[:-1] for y in pts[: i + 1]], ref[:-1])
    return total


def contributions(points: Sequence[Vector], ref: Vector) -> list:
    """The exclusive contribution HV(A) - HV(A without a) of each point."""
    pts = [tuple(x) for x in points]
    whole = hypervolume(pts, ref)
    return [whole - hypervolume(pts[:i] + pts[i + 1 :], ref) for i in range(len(pts))]
