# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeometric-collocation/. The authors are listed in prov/AE2H60.jsonl.
"""Isogeometric collocation for the 1D Poisson problem.

Solve -u'' = f on (a, b) with u(a) = ga and u(b) = gb in the B-spline space of
degree p on an open knot vector, by asking the strong form to hold at the
interior Greville abscissae.
"""

from __future__ import annotations

from typing import Callable, List, Sequence, Tuple

from ig2kit import all_basis, greville, open_uniform_knots, solve_dense


def collocate_poisson(
    knots: Sequence, p: int, f: Callable, ga, gb
) -> Tuple[List, List]:
    """Return (coefficients, collocation points) of the collocation solution.

    Precondition: p >= 2, an open knot vector (end multiplicity p + 1) and
    interior knots of multiplicity at most p - 1. Then the system is
    non-singular (Schoenberg-Whitney, see the proof on the page).
    Cost: O(n p) to build the banded rows and O(n^3) for the dense solve,
    with n = len(knots) - p - 1 unknowns.
    Works with float or with Fraction knots and data (then it is exact).
    """
    n = len(knots) - p - 1  # @line L1
    tau = greville(knots, p)  # @line L2
    a_, b_ = knots[0], knots[-1]
    rows, rhs = [], []
    rows.append(all_basis(knots, p, a_, 0)[0])  # @line L3
    rhs.append(ga)
    for i in range(1, n - 1):  # @line L4
        d2 = all_basis(knots, p, tau[i], 2)[2]
        rows.append([-v for v in d2])  # @line L5
        rhs.append(f(tau[i]))  # @line L6
    rows.append(all_basis(knots, p, b_, 0)[0])  # @line L7
    rhs.append(gb)
    c = solve_dense(rows, rhs)  # @line L8
    return c, tau


def evaluate(knots: Sequence, p: int, c: Sequence, x, nd: int = 0):
    """Value (nd = 0) or nd-th derivative of the spline with coefficients c at x."""
    row = all_basis(knots, p, x, nd)[nd]
    return sum(ci * ri for ci, ri in zip(c, row))


def max_error(knots: Sequence, p: int, c: Sequence, exact: Callable, samples: int = 400) -> float:
    """Largest |u_h - u| over equally spaced samples (a measure, not a proof)."""
    a_, b_ = float(knots[0]), float(knots[-1])
    worst = 0.0
    for k in range(samples + 1):
        x = a_ + (b_ - a_) * k / samples
        worst = max(worst, abs(float(evaluate(knots, p, c, x)) - exact(x)))
    return worst


def uniform_solve(p: int, ne: int, f: Callable, ga=0.0, gb=0.0) -> Tuple[List, List]:
    """Collocation on (0, 1) with ne equal elements; returns (knots, coefficients)."""
    knots = open_uniform_knots(p, ne)
    c, _ = collocate_poisson(knots, p, f, ga, gb)
    return knots, c
