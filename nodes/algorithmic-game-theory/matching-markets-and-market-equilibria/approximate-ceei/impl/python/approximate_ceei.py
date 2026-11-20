# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-ceei/. The authors are listed in prov/DWVSMG.jsonl.
"""A toy search for approximate competitive equilibrium from equal incomes (A-CEEI).

This is a toy for tiny inputs only: it tries every price vector on a grid, so its cost grows
exponentially with the number of goods. Practical solvers (Othman, Sandholm and Budish) use a
heuristic search over prices instead.

Agents are 0, ..., n - 1 and goods (course seats) are 0, ..., m - 1, with capacities q[j].
prefs[i] lists the bundles that agent i accepts, best first, each a tuple of goods; the empty
bundle is always acceptable and need not be listed. budgets[i] is the budget of agent i; A-CEEI
uses budgets that are close to equal but not equal. All numbers are Fractions or integers.
"""

from fractions import Fraction
from itertools import product
from math import sqrt


def demand(prefs_i, budget, p):
    """The agent's favorite affordable bundle: the first bundle on her list that she can pay for."""
    for bundle in prefs_i:
        if sum(p[j] for j in bundle) <= budget:
            return tuple(bundle)
    return ()


def clearing_error(bundles, q, p):
    """The vector z of Budish: demand minus capacity for each good, where a good of price 0 may
    have empty seats. The market clears exactly when z = 0."""
    z = []
    for j in range(len(q)):
        zj = sum(1 for bundle in bundles if j in bundle) - q[j]
        z.append(max(zj, 0) if p[j] == 0 else zj)
    return z


def approximate_ceei(prefs, q, budgets, step, cap):
    """Return (alpha, p, bundles) for a price vector on the grid {0, step, ..., cap}^m with the
    least clearing error alpha = ||z||_2 (ties go to the first vector in lexicographic order)."""
    m = len(q)
    grid = [step * k for k in range(int(cap / step) + 1)]
    best = None  # @line L1
    for p in product(grid, repeat=m):  # @line L2
        bundles = [demand(prefs[i], budgets[i], p) for i in range(len(prefs))]  # @line L3
        z = clearing_error(bundles, q, p)  # @line L4
        err = sum(v * v for v in z)
        if best is None or err < best[0]:  # @line L5
            best = (err, list(p), bundles)
    return sqrt(best[0]), best[1], best[2]  # @line L6


def perturbed_budgets(n, beta):
    """Budgets 1, 1 + beta / n, ..., 1 + (n - 1) beta / n: all distinct and within beta of 1."""
    return [1 + Fraction(beta) * i / n for i in range(n)]


def budish_bound(k, m):
    """The bound of Budish's existence theorem on the clearing error: sqrt(sigma m) / 2, with
    sigma = min(2k, m), where k is the largest number of goods in a bundle."""
    return sqrt(min(2 * k, m) * m) / 2
