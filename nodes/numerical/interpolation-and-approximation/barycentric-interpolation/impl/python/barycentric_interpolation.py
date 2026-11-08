# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barycentric-interpolation/. The authors are listed in prov/6W7GGA.jsonl.

"""Evaluate the interpolating polynomial by the second barycentric formula."""

import math
from typing import Any, List, Sequence


def _check(xs: Sequence[Any], ys: Sequence[Any]) -> None:
    if len(xs) == 0 or len(xs) != len(ys):
        raise ValueError("need the same positive number of nodes and values")
    if len(set(xs)) != len(xs):
        raise ValueError("the nodes must be distinct")


def barycentric_weights(xs: Sequence[Any]) -> List[Any]:
    """Return w_j = 1 / prod over k != j of (x_j - x_k).

    Cost: 2n^2 + 2n operations for n + 1 nodes. Works with float or Fraction.
    """
    if len(set(xs)) != len(xs):
        raise ValueError("the nodes must be distinct")
    n1 = len(xs)
    w = []
    for j in range(n1):  # @line L1
        wj = 1  # @line L2
        for k in range(n1):  # @line L3
            if k != j:  # @line L4
                wj = wj / (xs[j] - xs[k])
        w.append(wj)
    return w


def barycentric_eval(xs: Sequence[Any], w: Sequence[Any], ys: Sequence[Any], t: Any) -> Any:
    """Return sum(w_j y_j / (t - x_j)) / sum(w_j / (t - x_j)), or y_j if t = x_j.

    Cost: 5n + 6 operations for n + 1 nodes. Any common factor of w cancels.
    """
    num = 0 * ys[0]  # @line L5
    den = 0 * w[0]
    for j in range(len(xs)):  # @line L6
        if t == xs[j]:  # @line L7
            return ys[j]
        q = w[j] / (t - xs[j])  # @line L8
        num = num + q * ys[j]  # @line L9
        den = den + q
    return num / den  # @line L10


def barycentric_interpolation(xs: Sequence[Any], ys: Sequence[Any], t: Any) -> Any:
    """Return p_n(t) for distinct nodes xs (any order) and values ys."""
    _check(xs, ys)
    return barycentric_eval(xs, barycentric_weights(xs), ys, t)


def add_node(xs: List[Any], w: List[Any], x_new: Any) -> None:
    """Append x_new to xs and update the weights w in place in O(n) operations."""
    if x_new in xs:
        raise ValueError("the nodes must be distinct")
    w_new = 1
    for j in range(len(xs)):
        w[j] = w[j] / (xs[j] - x_new)
        w_new = w_new / (x_new - xs[j])
    xs.append(x_new)
    w.append(w_new)


def chebyshev2_points_and_weights(n: int):
    """Chebyshev points cos(j pi / n), j = 0..n, and scaled weights (-1)^j delta_j.

    Uses the form sin(pi (n - 2j) / (2n)), which is exactly antisymmetric.
    """
    if n == 0:
        return [0.0], [1.0]
    xs = [math.sin(math.pi * (n - 2 * j) / (2 * n)) for j in range(n + 1)]
    w = [(-1.0) ** j * (0.5 if j in (0, n) else 1.0) for j in range(n + 1)]
    return xs, w


def chebyshev1_points_and_weights(n: int):
    """Chebyshev zeros cos((2j + 1) pi / (2n + 2)) and scaled weights."""
    xs = [math.cos((2 * j + 1) * math.pi / (2 * n + 2)) for j in range(n + 1)]
    w = [(-1.0) ** j * math.sin((2 * j + 1) * math.pi / (2 * n + 2)) for j in range(n + 1)]
    return xs, w
