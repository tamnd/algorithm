# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranking-function-synthesis/. The authors are listed in prov/HA12CT.jsonl.
"""Linear ranking functions for single-path linear loops (Podelski and
Rybalchenko).

A loop over n rational variables is one relation between the state x
before and the state x' after one turn, given as rows (a, b) with
len(a) = 2n, each meaning a[:n] . x + a[n:] . x' <= b. Write A and A' for
the two halves of the rows. The loop is "while the rows can be satisfied,
move to some x' that satisfies them".

linear_ranking(n, rows) solves one linear program in the multipliers
lambda1, lambda2 >= 0 and returns (rho, bound, decrease) with Fraction
entries, or None. When it returns, every rational (x, x') of the relation
satisfies rho . x >= bound and rho . x - rho . x' >= decrease >= 1. It
returns None exactly when no linear ranking function exists over the
rationals. Cost: one linear program with 2m unknowns and 3n + 1 rows for m
rows of the loop; polynomial in theory, the simplex method in practice.
"""

from fractions import Fraction

from fraclp import lp_solve


def loop_rows(n, guard, update):
    """The rows of 'while guard do x := U x + u'. guard is a list of rows
    (a, b) over x; update is a list of n pairs (U_k, u_k) and sets
    x'_k = U_k . x + u_k."""
    rows = [(list(a) + [0] * n, b) for a, b in guard]
    for k, (uk, ck) in enumerate(update):
        e = [0] * n
        e[k] = 1
        lhs = [-v for v in uk] + e
        rows.append((lhs, ck))
        rows.append(([-v for v in lhs], -ck))
    return rows


def linear_ranking(n, rows):
    """A linear ranking function (rho, bound, decrease) or None."""
    m = len(rows)
    a_eq, b_eq = [], []
    # Unknowns: lambda1 (m entries), then lambda2 (m entries).
    # @line L1 the multipliers lambda1, lambda2 >= 0
    for k in range(n):
        # @line L2 lambda1 A' = 0
        a_eq.append([a[n + k] for a, _ in rows] + [0] * m)
        b_eq.append(0)
        # @line L3 (lambda1 - lambda2) A = 0
        a_eq.append([a[k] for a, _ in rows] + [-a[k] for a, _ in rows])
        b_eq.append(0)
        # @line L4 lambda2 (A + A') = 0
        a_eq.append([0] * m + [a[k] + a[n + k] for a, _ in rows])
        b_eq.append(0)
    # @line L5 lambda2 b <= -1
    a_ub = [[0] * m + [b for _, b in rows]]
    b_ub = [-1]
    # Minimizing the sum of the multipliers keeps the numbers small.
    status, lam, _ = lp_solve([1] * (2 * m), a_eq, b_eq, a_ub, b_ub)
    if status != "optimal":
        # @line L6 no multipliers: no linear ranking function
        return None
    lam1, lam2 = lam[:m], lam[m:]
    # @line L7 rho = lambda2 A'
    rho = tuple(sum(l * a[n + k] for l, (a, _) in zip(lam2, rows)) for k in range(n))
    # @line L8 the bound -lambda1 b and the decrease -lambda2 b
    bound = -sum(l * b for l, (_, b) in zip(lam1, rows))
    decrease = -sum(l * b for l, (_, b) in zip(lam2, rows))
    return rho, bound, decrease


def value(rho, x):
    """rho . x as an exact rational."""
    return sum(Fraction(r) * v for r, v in zip(rho, x))
