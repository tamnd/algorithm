# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boehm-knot-insertion/. The authors are listed in prov/A1WEXZ.jsonl.

"""Boehm's algorithm: insert one knot into a B-spline curve without changing it.

A curve of degree p has control points P_0, ..., P_n (tuples of numbers) and a
non-decreasing knot vector t_0, ..., t_m with m = n + p + 1. Knots, parameters
and coordinates may be int or Fraction; with Fraction the result is exact.
"""

from bisect import bisect_right
from fractions import Fraction
from typing import List, Sequence, Tuple, Union

Number = Union[int, Fraction]
Point = Tuple[Number, ...]


def boehm_insert(
    knots: Sequence[Number], p: int, ctrl: Sequence[Point], u: Number
) -> Tuple[List[Number], List[Tuple[Fraction, ...]]]:
    """Insert the knot u once. Return the new knot vector and the n + 2 new control points.

    Precondition: len(knots) == len(ctrl) + p + 1, t_p <= u < t_(n+1), and u
    has multiplicity at most p in the knot vector. Cost: O(log m) to find the
    span, p convex combinations of points, and O(n + m) to copy the arrays.
    """
    n = len(ctrl) - 1
    if len(knots) != n + p + 2:
        raise ValueError("need len(knots) == len(ctrl) + p + 1")
    if not knots[p] <= u < knots[n + 1]:
        raise ValueError("u must lie in [t_p, t_(n+1))")
    if list(knots).count(u) > p:
        raise ValueError("u already has multiplicity p + 1")
    mu = bisect_right(knots, u) - 1  # @line L1
    new_ctrl: List[Tuple[Fraction, ...]] = []
    for i in range(0, mu - p + 1):  # @line L2
        new_ctrl.append(tuple(Fraction(c) for c in ctrl[i]))
    for i in range(mu - p + 1, mu + 1):  # @line L3
        a = Fraction(u - knots[i]) / (knots[i + p] - knots[i])  # @line L4
        new_ctrl.append(tuple((1 - a) * x + a * y for x, y in zip(ctrl[i - 1], ctrl[i])))  # @line L5
    for i in range(mu + 1, n + 2):  # @line L6
        new_ctrl.append(tuple(Fraction(c) for c in ctrl[i - 1]))
    new_knots = list(knots[: mu + 1]) + [u] + list(knots[mu + 1 :])  # @line L7
    return new_knots, new_ctrl  # @line L8


def refine_by_insertion(
    knots: Sequence[Number], p: int, ctrl: Sequence[Point], new: Sequence[Number]
) -> Tuple[List[Number], List[Tuple[Fraction, ...]]]:
    """Insert the knots in new one at a time with boehm_insert.

    Precondition: each knot of new lies in [t_p, t_(n+1)) and no knot reaches
    multiplicity p + 2. Cost: O(k (n + m + p)) for k new knots, because each
    insertion copies the arrays.
    """
    out_knots = list(knots)
    out_ctrl = [tuple(Fraction(c) for c in pt) for pt in ctrl]
    for u in new:
        out_knots, out_ctrl = boehm_insert(out_knots, p, out_ctrl, u)
    return out_knots, out_ctrl
