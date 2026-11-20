# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hylland-zeckhauser-mechanism/. The authors are listed in prov/NMFNPQ.jsonl.
"""A toy Hylland-Zeckhauser solver: exact checks, and a search over a grid of prices.

This is a toy. It is not an efficient algorithm, and none is known: finding an approximate
HZ equilibrium is PPAD-complete. The search tries every price vector on a grid, so its
running time is exponential in the number of objects, and it can miss an equilibrium whose
prices are not on the grid (HZ equilibria can even be irrational). Use it on 2 or 3 objects.

The market has n agents and n objects, one unit of each. Agent i has utility u[i][j] for
object j and a budget of 1. An allocation x is an n by n matrix with x[i][j] the
probability share of object j given to agent i. All arithmetic is exact (Fraction).
"""

from fractions import Fraction
from itertools import product
from typing import Optional, Sequence

from agtlp import lp_max, lp_min

Matrix = list[list[Fraction]]


def demand_values(ui: Sequence[int], p: Sequence[Fraction]) -> tuple[Fraction, Fraction]:
    """Return (U, C): the best utility of a unit bundle with cost at most 1, and the least
    cost of a bundle with that utility. Two LPs with m variables."""
    m = len(p)
    ones = [[1] * m]
    st, x, U, _ = lp_max(list(ui), [list(p)], [1], ones, [1])  # @line L3
    if st != "optimal":
        raise ValueError("no unit bundle is affordable: some price must be at most 1")
    st, x, C, _ = lp_min(list(p), [list(p)], [1], ones + [list(ui)], [1, U])  # @line L4
    return U, C


def clearing_allocation(u: Sequence[Sequence[int]], p: Sequence[Fraction], vals) -> Optional[Matrix]:
    """Find x with x_i in the demand set of each agent and every object fully assigned, or None.

    The demand set of agent i is {x_i >= 0 : sum_j x_ij = 1, u_i x_i = U_i, p x_i = C_i}."""
    n = len(u)
    nv = n * n
    A_eq, b_eq = [], []

    def row():
        return [0] * nv

    for i in range(n):
        r = row()
        for j in range(n):
            r[i * n + j] = 1
        A_eq.append(r)
        b_eq.append(1)
        r = row()
        for j in range(n):
            r[i * n + j] = u[i][j]
        A_eq.append(r)
        b_eq.append(vals[i][0])
        r = row()
        for j in range(n):
            r[i * n + j] = p[j]
        A_eq.append(r)
        b_eq.append(vals[i][1])
    for j in range(n):
        r = row()
        for i in range(n):
            r[i * n + j] = 1
        A_eq.append(r)
        b_eq.append(1)
    st, x, _, _ = lp_max([0] * nv, [], [], A_eq, b_eq)
    if st != "optimal":
        return None
    return [[x[i * n + j] for j in range(n)] for i in range(n)]


def hz_grid_search(
    u: Sequence[Sequence[int]], k: int = 5, pmax: int = 2
) -> Optional[tuple[list[Fraction], Matrix]]:
    """Try the price vectors with entries in {0, 1/k, ..., pmax} and smallest entry 0, in
    lexicographic order, and return the first (p, x) that is an HZ equilibrium, or None.

    (k * pmax + 1)^n price vectors, each costing 2n + 1 small LPs: exponential in n."""
    n = len(u)
    if any(len(row) != n for row in u):
        raise ValueError("the toy needs n agents and n objects")
    grid = [Fraction(t, k) for t in range(k * pmax + 1)]
    for p in product(grid, repeat=n):  # @line L1
        if min(p) != 0:
            continue
        vals = []
        for i in range(n):  # @line L2
            vals.append(demand_values(u[i], p))
        x = clearing_allocation(u, p, vals)  # @line L5
        if x is not None:  # @line L6
            return list(p), x
    return None  # @line L7


def is_equilibrium(u: Sequence[Sequence[int]], p: Sequence[Fraction], x: Matrix) -> bool:
    """Exact check that (p, x) is an HZ equilibrium with budgets 1."""
    n = len(u)
    p = [Fraction(v) for v in p]
    if any(v < 0 for v in p) or min(p) > 1:
        return False
    for j in range(n):
        if sum(x[i][j] for i in range(n)) != 1:
            return False
    for i in range(n):
        if any(v < 0 for v in x[i]) or sum(x[i]) != 1:
            return False
        U, C = demand_values(u[i], p)
        util = sum(a * b for a, b in zip(u[i], x[i]))
        cost = sum(a * b for a, b in zip(p, x[i]))
        if util != U or cost != C:
            return False
    return True
