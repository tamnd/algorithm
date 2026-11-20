# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scarf-algorithm/. The authors are listed in prov/E57190.jsonl.
"""Scarf's algorithm in the ordinal form of primitive sets, on the grid of step 1/N in the simplex.

The vectors are the slack vectors s_0, ..., s_d and the grid points p = v / N of the simplex
Delta_d, where v is a tuple of d + 1 nonnegative integers with sum N. There is one strict order
for each coordinate i:

- s_i is the lowest vector in order i;
- the grid points follow, by the value of p_i, and ties go by the index of the point;
- the slacks s_j with j != i are above all the points, in the order of j.

A set S of d + 1 vectors is primitive if no vector is above the minimum of S in every order.
The slack s_j has label j, and a grid point gets its label from a labeling function. The
algorithm walks from the primitive set {s_1, ..., s_d, e_0} to a primitive set with all the
labels 0, ..., d. Every step keeps the labels 1, ..., d, so the walk is a path in an END OF THE
LINE graph, and it ends because it cannot repeat a set.

Vector v is the slack s_v if v <= d, and the grid point self.points[v - d - 1] otherwise.
"""

from fractions import Fraction
from itertools import combinations


def compositions(total, parts):
    """Return all tuples of `parts` nonnegative integers with sum `total`, in lexicographic order."""
    if parts == 1:
        return [(total,)]
    out = []
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            out.append((first,) + rest)
    return out


class ScarfGrid:
    """The vectors and the d + 1 orders of the ordinal Scarf algorithm."""

    def __init__(self, d, N):
        self.d, self.N = d, N
        self.points = compositions(N, d + 1)
        self.size = d + 1 + len(self.points)
        npts = len(self.points)
        self.rank = []
        for i in range(d + 1):
            r = [0] * self.size
            by_coord = sorted(range(npts), key=lambda q: (self.points[q][i], q))
            for pos, q in enumerate(by_coord):
                r[d + 1 + q] = 1 + pos
            for j in range(d + 1):
                r[j] = 0 if j == i else 1 + npts + j
            self.rank.append(r)

    def is_slack(self, v):
        return v <= self.d

    def point(self, v):
        """Return the grid point of vector v as a tuple of Fraction."""
        return tuple(Fraction(c, self.N) for c in self.points[v - self.d - 1])

    def vertex_e0(self):
        return self.d + 1 + self.points.index((self.N,) + (0,) * self.d)

    def minimum(self, S, i):
        return min(S, key=lambda v: self.rank[i][v])

    def holder(self, S, v):
        """Return the order in which v is the minimum of S (one order if S is primitive)."""
        return next(i for i in range(self.d + 1) if self.minimum(S, i) == v)

    def is_primitive(self, S):
        S = list(S)
        if len(S) != self.d + 1 or len(set(S)) != len(S):
            return False
        mins = [self.rank[i][self.minimum(S, i)] for i in range(self.d + 1)]
        return not any(all(self.rank[i][u] > mins[i] for i in range(self.d + 1)) for u in range(self.size))

    def highest_above(self, Q, b):
        """Return the highest vector in order b among those not in Q that are above min_i Q in every order i != b."""
        mins = [self.rank[i][self.minimum(Q, i)] for i in range(self.d + 1)]
        inQ = set(Q)
        cands = [u for u in range(self.size) if u not in inQ
                 and all(self.rank[i][u] > mins[i] for i in range(self.d + 1) if i != b)]
        return max(cands, key=lambda u: self.rank[b][u])

    def replace(self, S, y):
        """Return the vector z != y such that (S minus y) plus z is primitive (the ordinal pivot)."""
        Q = [v for v in S if v != y]
        w = self.minimum(Q, self.holder(S, y))
        return self.highest_above(Q, self.holder(S, w))


def scarf(grid, point_label, trace=None):
    """Return (P, pivots): a completely labeled primitive set and the number of pivots.

    point_label maps a grid point (a tuple of Fraction) to a label in 0, ..., d. If trace is a
    list, each primitive set of the path is appended to it.
    """
    d = grid.d

    def label(v):
        return v if grid.is_slack(v) else point_label(grid.point(v))

    z = grid.vertex_e0()
    P = list(range(1, d + 1)) + [z]  # @line L1
    pivots = 0
    if trace is not None:
        trace.append(list(P))
    while label(z) != 0:  # @line L2
        y = next(v for v in P if v != z and label(v) == label(z))  # @line L3
        Q, a = [v for v in P if v != y], grid.holder(P, y)  # @line L4
        w = grid.minimum(Q, a)  # @line L5
        b = grid.holder(P, w)
        z = grid.highest_above(Q, b)  # @line L6
        P = Q + [z]  # @line L7
        pivots += 1
        if trace is not None:
            trace.append(list(P))
    return P, pivots  # @line L8


def brouwer_label(f):
    """The label of a point p is the least i with f_i(p) >= p_i."""
    def label(p):
        fp = f(p)
        return next(i for i in range(len(p)) if fp[i] >= p[i])
    return label


def approximate_fixed_point(f, d, N):
    """Return a grid point p with |f(p) - p|_inf <= d (1 + lam) (d + 1) / N, for f lam-Lipschitz in sup norm."""
    grid = ScarfGrid(d, N)
    P, _ = scarf(grid, brouwer_label(f))
    return next(grid.point(v) for v in P if not grid.is_slack(v))


def best_response_label(C):
    """For a symmetric game with payoff matrix C, label q by the least pure best response to q."""
    def label(q):
        pay = [sum((Fraction(C[r][c]) * q[c] for c in range(len(q))), Fraction(0)) for r in range(len(q))]
        best = max(pay)
        return pay.index(best)
    return label


def approximate_symmetric_equilibrium(C, N):
    """Return q such that (q, q) is a (2 k^2 / N)-Nash equilibrium of the symmetric game (C, C^T).

    C is k by k with payoffs in [0, 1]; the row player gets C[r][c] and the column player C[c][r].
    """
    k = len(C)
    grid = ScarfGrid(k - 1, N)
    P, _ = scarf(grid, best_response_label(C))
    return list(next(grid.point(v) for v in P if not grid.is_slack(v)))


def primitive_sets(grid):
    """Return all primitive sets, by brute force (small grids only)."""
    return [S for S in combinations(range(grid.size), grid.d + 1) if grid.is_primitive(S)]
