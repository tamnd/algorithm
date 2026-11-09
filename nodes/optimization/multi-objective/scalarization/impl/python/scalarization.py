# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scalarization/. The authors are listed in prov/YDZF9D.jsonl.

"""Scalarization methods on a finite multi-objective problem.

All objectives are minimized. The input Y is a list of N vectors of length p,
the images y = f(x) of a finite feasible set X. Each method returns the indices
of all minimizers of its scalarizing function, so that a caller can check each
optimum. One method call costs O(N p) arithmetic operations. Use int or
fractions.Fraction entries to get exact results.
"""

import math
from typing import Callable, List, Optional, Sequence

Vector = Sequence


def argmin_all(values: Sequence) -> List[int]:
    """Return the indices of all minimal values. The list must not be empty."""
    best = min(values)
    return [i for i, v in enumerate(values) if v == best]


def weighted_sum(Y: Sequence[Vector], lam: Vector) -> List[int]:
    """Minimizers of sum_i lam_i y_i. Requires lam >= 0, lam != 0."""
    return argmin_all([sum(l * v for l, v in zip(lam, y)) for y in Y])


def tchebycheff_value(y: Vector, w: Vector, z: Vector, rho=0):
    """max_i w_i (y_i - z_i) + rho sum_i (y_i - z_i)."""
    return max(wi * (yi - zi) for wi, yi, zi in zip(w, y, z)) + rho * sum(
        yi - zi for yi, zi in zip(y, z)
    )


def tchebycheff(Y: Sequence[Vector], w: Vector, z: Vector, rho=0) -> List[int]:
    """Minimizers of the weighted (augmented if rho > 0) Tchebycheff function.

    Requires w > 0 and z < y for every y in Y (a utopia point)."""
    return argmin_all([tchebycheff_value(y, w, z, rho) for y in Y])


def epsilon_constraint(Y: Sequence[Vector], k: int, eps: Vector) -> List[int]:
    """Minimizers of y_k subject to y_j <= eps_j for all j != k.

    eps[k] is ignored. Returns [] when no vector meets the bounds."""
    feas = [
        i
        for i, y in enumerate(Y)
        if all(y[j] <= eps[j] for j in range(len(y)) if j != k)
    ]
    if not feas:
        return []
    best = min(Y[i][k] for i in feas)
    return [i for i in feas if Y[i][k] == best]


def achievement(Y: Sequence[Vector], zbar: Vector, w: Vector, rho=0) -> List[int]:
    """Minimizers of max_i w_i (y_i - zbar_i) + rho sum_i w_i (y_i - zbar_i).

    The reference point zbar may be attainable or not. Requires w > 0."""
    vals = []
    for y in Y:
        t = [wi * (yi - zi) for wi, yi, zi in zip(w, y, zbar)]
        vals.append(max(t) + rho * sum(t))
    return argmin_all(vals)


def goal_programming(Y: Sequence[Vector], goals: Vector, w: Vector) -> List[int]:
    """Minimizers of sum_i w_i max(0, y_i - g_i), the weighted overachievement
    of the goals. Requires w > 0."""
    return argmin_all(
        [sum(wi * max(0, yi - gi) for wi, yi, gi in zip(w, y, goals)) for y in Y]
    )


def lexicographic(Y: Sequence[Vector], order: Sequence[int]) -> List[int]:
    """Minimizers of the objectives in the priority order given by `order`."""
    return argmin_all([tuple(y[i] for i in order) for y in Y])


def weakly_dominates(a: Vector, b: Vector) -> bool:
    """a <= b componentwise."""
    return all(x <= y for x, y in zip(a, b))


def cleanup(Y: Sequence[Vector], i: int) -> int:
    """Return a Pareto optimal index j with Y[j] <= Y[i] componentwise.

    It minimizes the sum of the objectives over the vectors that weakly
    dominate Y[i]. A vector that dominated the result would also be a candidate
    with a smaller sum, so the result is Pareto optimal. O(N p) time."""
    cand = [j for j, y in enumerate(Y) if weakly_dominates(y, Y[i])]
    return min(cand, key=lambda j: (sum(Y[j]), j))


def sweep(
    Y: Sequence[Vector],
    s: Callable[[Vector, object], object],
    thetas: Sequence,
    weak: bool,
) -> List[int]:
    """The scalarization sweep of the template.

    s(y, theta) is the scalarizing function with parameter theta. Set weak to
    True when s is only weakly decreasing, so that each optimum gets the
    cleanup solve. Precondition: each s(., theta) has a finite minimum on Y.
    Time O(|thetas| N p)."""
    S: List[int] = []  # @line L1
    for theta in thetas:  # @line L2
        i = argmin_all([s(y, theta) for y in Y])[0]  # @line L3
        if weak:  # @line L4
            i = cleanup(Y, i)  # @line L5
        if i not in S:  # @line L6
            S.append(i)  # @line L6
    return S  # @line L7


def epsilon_constraint_front(Y: Sequence[Vector]) -> List[int]:
    """The nondominated vectors of a two-objective list, by the epsilon-
    constraint loop: minimize (y_1, y_2) lexicographically subject to
    y_2 < the last value found. One index is returned for each nondominated
    vector, in the order of rising y_1. It makes |Y_N| + 1 solves of O(N) each."""
    out: List[int] = []
    bound: Optional[object] = math.inf
    while True:
        feas = [i for i, y in enumerate(Y) if y[1] < bound]
        if not feas:
            return out
        i = min(feas, key=lambda j: (Y[j][0], Y[j][1], j))
        out.append(i)
        bound = Y[i][1]
