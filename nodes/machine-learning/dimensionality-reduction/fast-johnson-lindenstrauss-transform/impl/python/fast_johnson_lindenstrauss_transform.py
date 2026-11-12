# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-johnson-lindenstrauss-transform/. The authors are listed in prov/E208HD.jsonl.
"""The fast Johnson-Lindenstrauss transform of Ailon and Chazelle (2009): Phi = P H D.

D is a diagonal matrix of random signs, H is the normalized Walsh-Hadamard
matrix (applied with the fast transform in O(d log d) additions), and P is a
sparse k x d matrix whose entries are 0 with probability 1 - q and N(0, 1/q)
with probability q. The map x -> P H D x / sqrt(k) keeps squared norms in
expectation. The subsampled randomized Hadamard transform (SRHT) is the
variant that replaces P by the sampling of k coordinates.
"""

import math


def fwht(a):
    """Unnormalized fast Walsh-Hadamard transform of a list whose length is a power of two.

    Returns a new list equal to H_d a, where H_d[i][j] = (-1)^popcount(i & j).
    It uses d log2 d additions and subtractions, and exact arithmetic on integers.
    """
    d = len(a)
    if d == 0 or d & (d - 1):
        raise ValueError("the length must be a power of two")
    y = list(a)
    h = 1  # @line L5
    while h < d:  # @line L6
        for start in range(0, d, 2 * h):
            for i in range(start, start + h):
                u, v = y[i], y[i + h]
                y[i], y[i + h] = u + v, u - v  # @line L7
        h *= 2  # @line L8
    return y


def hadamard_matrix(d):
    """The d x d Sylvester-Hadamard matrix with entries (-1)^popcount(i & j)."""
    return [[-1 if bin(i & j).count("1") % 2 else 1 for j in range(d)] for i in range(d)]


def next_power_of_two(d):
    p = 1
    while p < d:
        p *= 2
    return p


def pad(x, d):
    """Pad x with zeros to length d. Padding does not change any norm."""
    return list(x) + [0.0] * (d - len(x))


class FJLT:
    """One draw of Phi = P H D from R^d0 to R^k. Inputs are padded to a power of two d."""

    def __init__(self, d0, k, q, rng):
        if not 0 < q <= 1:
            raise ValueError("q must be in (0, 1]")
        self.d0 = d0
        self.d = next_power_of_two(d0)  # @line L1
        self.k = k
        self.q = q
        self.signs = [rng.choice((-1, 1)) for _ in range(self.d)]  # @line L2
        sd = 1.0 / math.sqrt(q)
        # P is stored by rows as lists of (column, value); each entry is nonzero with probability q.
        self.rows = []
        for _ in range(k):  # @line L3
            row = []
            for j in range(self.d):
                if rng.random() < q:
                    row.append((j, rng.gauss(0.0, sd)))
            self.rows.append(row)

    def precondition(self, x):
        """Return H D x with the normalized H; the Euclidean norm is unchanged."""
        y = [s * v for s, v in zip(self.signs, pad(x, self.d))]  # @line L4
        y = fwht(y)
        c = 1.0 / math.sqrt(self.d)
        return [c * v for v in y]  # @line L9

    def apply(self, x):
        """Return P H D x / sqrt(k), whose squared norm estimates the squared norm of x."""
        u = self.precondition(x)
        c = 1.0 / math.sqrt(self.k)
        return [c * sum(v * u[j] for j, v in row) for row in self.rows]  # @line L10

    def nonzeros(self):
        return sum(len(row) for row in self.rows)


def fjlt_sparsity(n, d):
    """The density q = min(1, (ln n)^2 / d) used here for the l2 case; the paper fixes q up to a constant."""
    return min(1.0, math.log(n) ** 2 / d)


class SRHT:
    """The subsampled randomized Hadamard transform: sqrt(d / k) S H D x with k sampled coordinates."""

    def __init__(self, d0, k, rng):
        self.d0 = d0
        self.d = next_power_of_two(d0)
        self.k = k
        self.signs = [rng.choice((-1, 1)) for _ in range(self.d)]
        self.coords = [rng.randrange(self.d) for _ in range(k)]  # with replacement

    def apply(self, x):
        y = fwht([s * v for s, v in zip(self.signs, pad(x, self.d))])
        c = 1.0 / math.sqrt(self.k)  # sqrt(d / k) times the 1 / sqrt(d) of the normalized H
        return [c * y[i] for i in self.coords]


def sq_norm(x):
    return sum(v * v for v in x)


def sq_dist(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))
