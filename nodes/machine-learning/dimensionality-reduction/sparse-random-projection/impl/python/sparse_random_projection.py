# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-random-projection/. The authors are listed in prov/J2JFH9.jsonl.
"""Sparse random projection (Achlioptas 2003; Li, Hastie and Church 2006) and the
block sparse Johnson-Lindenstrauss transform (Kane and Nelson 2014).

With the parameter s >= 1, each entry of the d x k matrix R is
    +sqrt(s) with probability 1/(2s),  0 with probability 1 - 1/s,  -sqrt(s) with probability 1/(2s).
s = 1 is the Rademacher matrix, s = 3 is the sparse matrix of Achlioptas, and
s = sqrt(d) is the very sparse projection of Li, Hastie and Church.
A row vector x maps to x R / sqrt(k). The matrix is stored by columns of R
(one list per output coordinate) with only the nonzero entries, as integer signs.
"""

import math
from fractions import Fraction


def draw_sign(s, rng):
    """One entry divided by sqrt(s): +1 or -1 with probability 1/(2s) each, else 0."""
    u = rng.random() * s
    if u < 0.5:
        return 1
    if u < 1.0:
        return -1
    return 0


class SparseRandomProjection:
    """A d -> k sparse random projection with density 1/s."""

    def __init__(self, d, k, s, rng):
        if s < 1:
            raise ValueError("s must be at least 1")
        self.d, self.k, self.s = d, k, s
        # entries[j] lists (i, sign) for the nonzero R[i][j] = sign * sqrt(s).
        self.entries = []
        for _ in range(k):  # @line L1
            col = []  # @line L2
            for i in range(d):  # @line L3
                u = rng.random() * s  # @line L4
                if u < 0.5:  # @line L5
                    col.append((i, 1))
                elif u < 1.0:  # @line L6
                    col.append((i, -1))
            self.entries.append(col)
        self.scale = math.sqrt(s / k)

    def transform(self, points):
        """Return x R / sqrt(k) for each point x, in O(nnz(R)) time per dense point."""
        out = []
        for x in points:  # @line L7
            y = []
            for col in self.entries:  # @line L8
                y.append(self.scale * sum(g * x[i] for i, g in col))  # @line L9
            out.append(y)  # @line L10
        return out

    def apply(self, x):
        """Return x R / sqrt(k) for one point."""
        return self.transform([x])[0]

    def nonzeros(self):
        return sum(len(col) for col in self.entries)


class SparseJL:
    """Block construction of Kane and Nelson: k = s * b rows in s blocks of b rows.

    Each input coordinate j gets, in each block, one row chosen uniformly and one
    random sign, with value sign / sqrt(s). So each column has exactly s nonzeros.
    """

    def __init__(self, d, b, s, rng):
        self.d, self.b, self.s, self.k = d, b, s, b * s
        self.cols = []
        for _ in range(d):
            self.cols.append([(blk * b + rng.randrange(b), rng.choice((-1, 1))) for blk in range(s)])
        self.scale = 1.0 / math.sqrt(s)

    def apply(self, x):
        """Return S x in O(s * nnz(x)) time."""
        y = [0.0] * self.k
        for j, v in enumerate(x):
            if v:
                for r, g in self.cols[j]:
                    y[r] += g * v
        return [self.scale * t for t in y]


def entry_moments(s):
    """Exact E[r^2] and E[r^4] of one entry for an integer s (the values are +-sqrt(s), 0)."""
    s = Fraction(s)
    p = 1 / s  # probability that the entry is nonzero
    return p * s, p * s * s


def estimator_variance(x, s, k=1):
    """Exact Var of ||x R||^2 / k: (2 ||x||^4 + (s - 3) sum x_i^4) / k."""
    n2 = sum(Fraction(v) ** 2 for v in x)
    n4 = sum(Fraction(v) ** 4 for v in x)
    return (2 * n2 * n2 + (Fraction(s) - 3) * n4) / k


def sq_norm(x):
    return sum(v * v for v in x)


def sq_dist(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))
