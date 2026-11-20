# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nucleolus-sequential-lp/. The authors are listed in prov/F1V2JQ.jsonl.
"""The nucleolus of a TU game by a sequence of linear programs (Kopelowitz 1967).

A game with n players 0, ..., n - 1 is a sequence v of 2^n numbers indexed by bitmask:
v[S] is the value of the coalition whose members are the set bits of S, and v[0] = 0.
The excess of a coalition S at a payoff vector x is e(S, x) = v[S] - x(S).

nucleolus(v) returns the nucleolus: the imputation (x(N) = v(N) and x_i >= v({i}))
whose vector of excesses over the coalitions S with 0 < S < N, sorted in nonincreasing
order, is lexicographically smallest. nucleolus(v, imputations=False) returns the
prenucleolus, the same minimum over all x with x(N) = v(N).

Each round solves one LP for the smallest maximum excess t* of the free coalitions, then
fixes every free coalition whose excess equals t* at every optimal point. A coalition with
a nonzero dual value is fixed at once (complementary slackness); for the others one more
LP decides. A free coalition whose indicator vector is a linear combination of the fixed
ones has a constant excess from then on, so it is dropped. Every round raises the rank of
the fixed system by at least 1, so there are at most n - 1 rounds, each with at most
2^n - 1 LPs on n + 1 free variables. All arithmetic is exact, in Fraction, through the
simplex method of agtlp.
"""

from fractions import Fraction

from agtlp import lp_max, lp_min


def members(S, n):
    """Return the list of the players in the coalition with bitmask S."""
    return [i for i in range(n) if S >> i & 1]


def num_players(v):
    """Return n for a game given as a sequence of 2^n values."""
    n = len(v).bit_length() - 1
    if len(v) != 1 << n or n < 1:
        raise ValueError("v must have 2^n entries for some n >= 1")
    if v[0] != 0:
        raise ValueError("v of the empty coalition must be 0")
    return n


def excess(v, S, x):
    """Return e(S, x) = v[S] - x(S)."""
    n = len(x)
    return Fraction(v[S]) - sum((x[i] for i in members(S, n)), Fraction(0))


def excess_vector(v, x):
    """Return the excesses of all coalitions 0 < S < N, sorted in nonincreasing order."""
    full = (1 << len(x)) - 1
    return sorted((excess(v, S, x) for S in range(1, full)), reverse=True)


class _Span:
    """Rows in reduced echelon form over Fraction, for rank and span tests."""

    def __init__(self, n):
        self.n = n
        self.rows = []  # (pivot column, row), each row with a 1 at its pivot

    def reduce(self, vec):
        vec = [Fraction(a) for a in vec]
        for p, row in self.rows:
            f = vec[p]
            if f != 0:
                vec = [a - f * b for a, b in zip(vec, row)]
        return vec

    def contains(self, vec):
        return all(a == 0 for a in self.reduce(vec))

    def add(self, vec):
        vec = self.reduce(vec)
        p = next((j for j, a in enumerate(vec) if a != 0), None)
        if p is None:
            return False
        vec = [a / vec[p] for a in vec]
        self.rows = [(q, [a - r[p] * b for a, b in zip(r, vec)]) for q, r in self.rows]
        self.rows.append((p, vec))
        return True

    def rank(self):
        return len(self.rows)


def _indicator(S, n):
    return [1 if S >> i & 1 else 0 for i in range(n)]


def _build(v, n, free, fixed, imputations):
    """Constraint rows of the round LP in agtlp form.

    The variables are y_0, ..., y_{n-1} and then t+ and t-. In imputation mode,
    x_i = v({i}) + y_i with y_i >= 0; in the other mode, x_i = y_i - z_i with two
    nonnegative parts, and the z columns come after the y columns. Returns
    (A_ub, b_ub, A_eq, b_eq, nx, base), where nx is the number of x columns and base[i]
    is the constant part of x_i.
    """
    if imputations:
        nx = n
        base = [Fraction(v[1 << i]) for i in range(n)]
    else:
        nx = 2 * n
        base = [Fraction(0)] * n

    def xrow(S):
        row = [Fraction(0)] * (nx + 2)
        for i in members(S, n):
            row[i] = Fraction(1)
            if not imputations:
                row[n + i] = Fraction(-1)
        const = sum((base[i] for i in members(S, n)), Fraction(0))
        return row, const

    A_ub, b_ub = [], []
    for S in free:  # v(S) - x(S) <= t, written as -x(S) - t <= -v(S)
        row, const = xrow(S)
        row = [-a for a in row]
        row[nx], row[nx + 1] = Fraction(-1), Fraction(1)
        A_ub.append(row)
        b_ub.append(const - Fraction(v[S]))
    full = (1 << n) - 1
    A_eq, b_eq = [], []
    row, const = xrow(full)
    A_eq.append(row)
    b_eq.append(Fraction(v[full]) - const)
    for S, tS in fixed:  # x(S) = v(S) - t_S
        row, const = xrow(S)
        A_eq.append(row)
        b_eq.append(Fraction(v[S]) - tS - const)
    return A_ub, b_ub, A_eq, b_eq, nx, base


def _x_of(sol, n, nx, base, imputations):
    if imputations:
        return [base[i] + sol[i] for i in range(n)]
    return [sol[i] - sol[n + i] for i in range(n)]


def nucleolus(v, imputations=True):
    """Return the nucleolus of the game v as a list of n Fractions.

    v is a sequence of 2^n numbers indexed by bitmask, with v[0] = 0. With
    imputations=False the result is the prenucleolus. Raises ValueError if the set of
    imputations is empty (v(N) < sum of v({i})).
    Cost: at most n - 1 rounds; each round solves at most 2^n - 1 LPs with O(n)
    variables and O(2^n) constraints.
    """
    return nucleolus_trace(v, imputations)[0]


def nucleolus_trace(v, imputations=True):
    """Return (x, rounds): the nucleolus and, for each round, the triple
    (t*, the coalitions fixed at t*, the coalitions dropped as dependent)."""
    n = num_players(v)
    full = (1 << n) - 1
    if imputations and Fraction(v[full]) < sum(Fraction(v[1 << i]) for i in range(n)):
        raise ValueError("the game has no imputation")  # @line L1
    free = list(range(1, full))  # @line L2
    fixed = []
    span = _Span(n)
    span.add(_indicator(full, n))
    rounds = []
    while span.rank() < n:  # @line L3
        A_ub, b_ub, A_eq, b_eq, nx, base = _build(v, n, free, fixed, imputations)
        c = [Fraction(0)] * nx + [Fraction(1), Fraction(-1)]
        status, _, tstar, dual = lp_min(c, A_ub, b_ub, A_eq, b_eq)  # @line L4
        if status != "optimal":
            raise ArithmeticError("round LP is " + status)
        # The optimal face: t+ - t- = t* as one more equation.
        face_eq = A_eq + [[Fraction(0)] * nx + [Fraction(1), Fraction(-1)]]
        face_b = b_eq + [tstar]
        moved = []
        for k, S in enumerate(free):  # @line L5
            tight = dual[k] != 0
            if not tight:
                row, const = [Fraction(0)] * (nx + 2), Fraction(0)
                for i in members(S, n):
                    row[i] = Fraction(1)
                    if not imputations:
                        row[n + i] = Fraction(-1)
                    const += base[i]
                st, _, best, _ = lp_max(row, A_ub, b_ub, face_eq, face_b)
                tight = st == "optimal" and best + const == Fraction(v[S]) - tstar
            if tight:  # @line L6
                moved.append(S)
                fixed.append((S, tstar))  # @line L7
        if not moved:
            raise ArithmeticError("no coalition is tight at every optimal point")
        for S in moved:
            span.add(_indicator(S, n))
        rest, dropped = [], []
        for S in free:  # @line L8
            if S in moved:
                continue
            if span.contains(_indicator(S, n)):
                dropped.append(S)  # @line L9
            else:
                rest.append(S)
        free = rest
        rounds.append((tstar, moved, dropped))
    rows = [_indicator(full, n)] + [_indicator(S, n) for S, _ in fixed]
    rhs = [Fraction(v[full])] + [Fraction(v[S]) - tS for S, tS in fixed]
    return _solve(rows, rhs, n), rounds  # @line L10


def _solve(rows, rhs, n):
    """Solve a consistent linear system of rank n exactly, by Gauss-Jordan elimination."""
    M = [[Fraction(a) for a in r] + [Fraction(b)] for r, b in zip(rows, rhs)]
    r = 0
    piv = []
    for col in range(n):
        p = next((k for k in range(r, len(M)) if M[k][col] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        M[r] = [a / M[r][col] for a in M[r]]
        for k in range(len(M)):
            if k != r and M[k][col] != 0:
                f = M[k][col]
                M[k] = [a - f * b for a, b in zip(M[k], M[r])]
        piv.append(col)
        r += 1
    if len(piv) != n:
        raise ArithmeticError("the fixed system does not determine x")
    x = [Fraction(0)] * n
    for k, col in enumerate(piv):
        x[col] = M[k][-1]
    return x
