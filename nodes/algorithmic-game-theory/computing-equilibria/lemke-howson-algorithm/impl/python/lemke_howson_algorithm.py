# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lemke-howson-algorithm/. The authors are listed in prov/W47DAN.jsonl.
"""The Lemke-Howson algorithm for bimatrix games, with exact tableaux in Fraction.

The row player gets A[i][j] and the column player gets B[i][j]; both maximize. The labels
are 0, ..., m - 1 for the rows and m, ..., m + n - 1 for the columns. The minimum ratio test
is lexicographic, so the method also ends on degenerate games.
"""

from fractions import Fraction


def _positive(P):
    k = 1 - min(min(row) for row in P)
    return [[Fraction(v) + max(k, 0) for v in row] for row in P]


class _Tableau:
    """Rows of the system  coefficients . z = 1, with a basis. Column index = label."""

    def __init__(self, rows, basis, slack_cols):
        self.rows = rows  # each row: [coefficients for the m + n labels] + [rhs]
        self.basis = basis
        self.slack_cols = slack_cols  # the columns of the first basis, for the lexicographic rule

    def pivot_in(self, col):
        """Enter column col; return the label of the leaving variable."""
        best, best_r = None, None
        for r, row in enumerate(self.rows):
            a = row[col]
            if a > 0:
                key = tuple(row[c] / a for c in [-1] + self.slack_cols)
                if best is None or key < best:
                    best, best_r = key, r
        if best_r is None:
            raise AssertionError("the polytope is bounded, so a pivot row exists")
        row = self.rows[best_r]
        p = row[col]
        row = [v / p for v in row]
        self.rows[best_r] = row
        for r in range(len(self.rows)):
            f = self.rows[r][col]
            if r != best_r and f != 0:
                self.rows[r] = [a - f * b for a, b in zip(self.rows[r], row)]
        leaving = self.basis[best_r]
        self.basis[best_r] = col
        return leaving

    def values(self, size):
        z = [Fraction(0)] * size
        for r, c in enumerate(self.basis):
            z[c] = self.rows[r][-1]
        return z


def lemke_howson(A, B, k=0, trace=None):
    """Return a Nash equilibrium (x, y) of the bimatrix game (A, B), from the missing label k.

    If trace is a list, the pair (entering label, leaving label) of each pivot is appended to it.
    """
    m, n = len(A), len(A[0])
    if not 0 <= k < m + n:
        raise ValueError("the missing label must be in 0 .. m + n - 1")
    Ap, Bp = _positive(A), _positive(B)
    one = Fraction(1)
    # T1: B'^T x + s = 1, columns x_0..x_(m-1) (labels 0..m-1), s_0..s_(n-1) (labels m..).
    t1 = _Tableau([[Bp[i][j] for i in range(m)] + [Fraction(int(c == j)) for c in range(n)] + [one]
                   for j in range(n)], list(range(m, m + n)), list(range(m, m + n)))  # @line L1
    # T2: r + A' y = 1, columns r_0..r_(m-1) (labels 0..m-1), y_0..y_(n-1) (labels m..).
    t2 = _Tableau([[Fraction(int(c == i)) for c in range(m)] + Ap[i] + [one] for i in range(m)],
                  list(range(m)), list(range(m)))
    label = k  # @line L2
    tab = t1 if k < m else t2
    while True:  # @line L3
        leaving = tab.pivot_in(label)  # @line L4
        if trace is not None:
            trace.append((label, leaving))
        label = leaving  # @line L5
        if label == k:  # @line L6
            break
        tab = t2 if tab is t1 else t1  # @line L7
    x = t1.values(m + n)[:m]  # @line L8
    y = t2.values(m + n)[m:]
    sx, sy = sum(x), sum(y)
    return [v / sx for v in x], [v / sy for v in y]


def all_lemke_howson(A, B):
    """Return the distinct equilibria reached from the artificial equilibrium by each label."""
    out = []
    for k in range(len(A) + len(A[0])):
        eq = lemke_howson(A, B, k)
        if eq not in out:
            out.append(eq)
    return out
