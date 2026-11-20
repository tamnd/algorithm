# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/support-enumeration/. The authors are listed in prov/GHTYAP.jsonl.
"""Support enumeration for bimatrix games, in exact rational arithmetic.

The row player gets A[i][j] and the column player gets B[i][j]; both maximize. For a
nondegenerate game the function returns every Nash equilibrium. For a degenerate game
every pair it returns is still a Nash equilibrium, but it can miss equilibria.
"""

from fractions import Fraction
from itertools import combinations


def solve_square(K, b):
    """Return the unique solution z of K z = b, or None if K is singular."""
    r = len(K)
    rows = [[Fraction(v) for v in K[k]] + [Fraction(b[k])] for k in range(r)]
    for col in range(r):
        p = next((k for k in range(col, r) if rows[k][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for k in range(r):
            f = rows[k][col]
            if k != col and f != 0:
                rows[k] = [a - f * c for a, c in zip(rows[k], rows[col])]
    return [rows[k][-1] for k in range(r)]


def _indifferent_mix(P, rows, cols):
    """Solve sum_{c in cols} P[r][c] z_c = u for r in rows and sum z_c = 1. Return (z, u) or None."""
    k = len(cols)
    K = [[P[r][c] for c in cols] + [-1] for r in rows] + [[1] * k + [0]]
    sol = solve_square(K, [0] * k + [1])
    if sol is None:
        return None
    return sol[:k], sol[k]


def support_enumeration(A, B):
    """Return the list of the Nash equilibria (x, y) found from supports of equal size."""
    A = [[Fraction(v) for v in row] for row in A]
    B = [[Fraction(v) for v in row] for row in B]
    m, n = len(A), len(A[0])
    Bt = [[B[i][j] for i in range(m)] for j in range(n)]  # Bt[j][i] = B[i][j]
    found = []
    for k in range(1, min(m, n) + 1):  # @line L1
        for I in combinations(range(m), k):  # @line L2
            for J in combinations(range(n), k):
                ys = _indifferent_mix(A, I, J)  # @line L3
                xs = _indifferent_mix(Bt, J, I)  # @line L4
                if ys is None or xs is None:  # @line L5
                    continue
                (yJ, u), (xI, v) = ys, xs
                if min(yJ) <= 0 or min(xI) <= 0:
                    continue
                x, y = [Fraction(0)] * m, [Fraction(0)] * n  # @line L6
                for i, p in zip(I, xI):
                    x[i] = p
                for j, q in zip(J, yJ):
                    y[j] = q
                row_pay = [sum((A[i][j] * y[j] for j in J), Fraction(0)) for i in range(m)]  # @line L7
                col_pay = [sum((x[i] * B[i][j] for i in I), Fraction(0)) for j in range(n)]
                if max(row_pay) <= u and max(col_pay) <= v:
                    found.append((x, y))  # @line L8
    return found


def is_nondegenerate(A, B):
    """Return True if no mixed strategy with support size s has more than s pure best responses.

    It checks the equivalent condition of von Stengel: for every set I of rows and every set J of
    columns with |J| > |I|, no x with support exactly I makes all columns of J best responses,
    and the same with the players swapped. It drops one tie at a time and needs the rest of the
    system to be nonsingular, so it can miss a degeneracy whose systems are all singular. It is
    exponential; use it on small games.
    """
    A = [[Fraction(v) for v in row] for row in A]
    B = [[Fraction(v) for v in row] for row in B]
    m, n = len(A), len(A[0])
    Bt = [[B[i][j] for i in range(m)] for j in range(n)]
    for P, r, c in ((Bt, m, n), (A, n, m)):
        # P[c'][r'] is the payoff of the responding player; r is the number of mixing strategies.
        for s in range(1, r + 1):
            for I in combinations(range(r), s):
                for J in combinations(range(c), s + 1):
                    if _has_mix_with_ties(P, I, J):
                        return False
    return True


def _has_mix_with_ties(P, I, J):
    """Is there a z > 0 on I (sum 1) that gives every response in J the same payoff, which is the best?"""
    # The s + 1 ties and the sum give s + 2 equations in s + 1 unknowns. Drop each tie in turn.
    for drop in J:
        J2 = tuple(j for j in J if j != drop)
        sol = _indifferent_mix(P, J2, I)
        if sol is None:
            continue
        z, u = sol
        if min(z) <= 0:
            continue
        pay = [sum((P[j][i] * zi for i, zi in zip(I, z)), Fraction(0)) for j in range(len(P))]
        if pay[drop] == u and max(pay) == u:
            return True
    return False
