# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nash-equilibrium-computation/. The authors are listed in prov/EYAA2N.jsonl.

"""Nash equilibria of a bimatrix game by support enumeration, in exact arithmetic.

The row player gets A[i][j] and the column player gets B[i][j]. For each pair
of supports (I, J) of the same size, the indifference equations are solved
exactly, and the solution is kept if it is a probability vector that is
positive on its support and no pure strategy outside the support does better.
"""

from fractions import Fraction
from itertools import combinations
from typing import Optional, Sequence

Number = int | Fraction
Matrix = Sequence[Sequence[Number]]
Profile = tuple[tuple[Fraction, ...], tuple[Fraction, ...]]


def _solve(rows: list[list[Fraction]]) -> Optional[list[Fraction]]:
    """Solve a square system given as an augmented matrix, or return None if it is singular."""
    a = [r[:] for r in rows]
    k = len(a)
    for c in range(k):
        p = next((r for r in range(c, k) if a[r][c] != 0), -1)
        if p < 0:
            return None
        a[c], a[p] = a[p], a[c]
        inv = 1 / a[c][c]
        a[c] = [t * inv for t in a[c]]
        for r in range(k):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [s - f * t for s, t in zip(a[r], a[c])]
    return [a[r][k] for r in range(k)]


def _mix_for(pay: list[list[Fraction]], own: tuple[int, ...], other: tuple[int, ...]) -> Optional[tuple[list[Fraction], Fraction]]:
    """Find a mix on `other` that makes every strategy in `own` earn the same payoff.

    pay[a][b] is the payoff of the indifferent player for own strategy a against b.
    Unknowns: the probabilities on `other` and the common payoff.
    """
    k = len(own)
    system = []
    for a in own:
        system.append([pay[a][b] for b in other] + [Fraction(-1), Fraction(0)])
    system.append([Fraction(1)] * k + [Fraction(0), Fraction(1)])
    sol = _solve(system)
    if sol is None:
        return None
    return sol[:k], sol[k]


def support_enumeration(a: Matrix, b: Matrix) -> list[Profile]:
    """Return the Nash equilibria (x, y) found from square supports, in a fixed order.

    Precondition: a and b are m by n matrices of int or Fraction, m, n >= 1.
    Postcondition: every returned profile is an exact Nash equilibrium. If the
    game is nondegenerate (no mixed strategy with support size k has more than
    k pure best responses), the list contains every equilibrium exactly once.
    Cost: sum over k of C(m, k) C(n, k) = C(m + n, m) support pairs, each
    O(k^3 + m n) exact operations.
    """
    m, n = len(a), len(a[0])
    if any(len(r) != n for r in a) or len(b) != m or any(len(r) != n for r in b):
        raise ValueError("a and b must be m by n matrices")
    A = [[Fraction(v) for v in r] for r in a]
    B = [[Fraction(v) for v in r] for r in b]
    BT = [[B[i][j] for i in range(m)] for j in range(n)]
    found: list[Profile] = []
    for k in range(1, min(m, n) + 1):
        for rows in combinations(range(m), k):
            for cols in combinations(range(n), k):
                # The column mix y makes the rows in I indifferent for the row player.
                ry = _mix_for(A, rows, cols)
                # The row mix x makes the columns in J indifferent for the column player.
                rx = _mix_for(BT, cols, rows)
                if ry is None or rx is None:
                    continue
                (py, u), (px, w) = ry, rx
                if any(p <= 0 for p in py) or any(p <= 0 for p in px):
                    continue
                y = [Fraction(0)] * n
                for j, p in zip(cols, py):
                    y[j] = p
                x = [Fraction(0)] * m
                for i, p in zip(rows, px):
                    x[i] = p
                if is_equilibrium(A, B, x, y):
                    found.append((tuple(x), tuple(y)))
    return found


def payoffs(a: Matrix, b: Matrix, x: Sequence[Number], y: Sequence[Number]) -> tuple[Fraction, Fraction]:
    """Return the expected payoffs (x^T A y, x^T B y). Cost O(m n)."""
    ua = sum((Fraction(a[i][j]) * x[i] * y[j] for i in range(len(x)) for j in range(len(y))), Fraction(0))
    ub = sum((Fraction(b[i][j]) * x[i] * y[j] for i in range(len(x)) for j in range(len(y))), Fraction(0))
    return ua, ub


def is_equilibrium(a: Matrix, b: Matrix, x: Sequence[Number], y: Sequence[Number]) -> bool:
    """Check that no pure deviation gains for either player, exactly. Cost O(m n)."""
    m, n = len(a), len(a[0])
    if any(p < 0 for p in x) or any(q < 0 for q in y) or sum(x) != 1 or sum(y) != 1:
        return False
    ua, ub = payoffs(a, b, x, y)
    for i in range(m):
        if sum((Fraction(a[i][j]) * y[j] for j in range(n)), Fraction(0)) > ua:
            return False
    for j in range(n):
        if sum((Fraction(b[i][j]) * x[i] for i in range(m)), Fraction(0)) > ub:
            return False
    return True
