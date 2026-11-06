# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnorr-euchner-enumeration/. The authors are listed in prov/ARHDFM.jsonl.

from fractions import Fraction
from math import floor
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]


def _dot(u: Sequence[Number], v: Sequence[Number]) -> Number:
    return sum((a * b for a, b in zip(u, v)), 0)


def _nearest(x: Fraction) -> int:
    """The integer nearest to x; a half is rounded up."""
    return floor(x + Fraction(1, 2))


def _gram_schmidt(b: Sequence[Sequence[Number]]) -> tuple[list[list[Fraction]], list[Fraction], list[list[Fraction]]]:
    """Exact Gram-Schmidt: returns (mu, B, star) with B[i] = ||b_i*||^2."""
    n = len(b)
    mu = [[Fraction(0)] * n for _ in range(n)]
    big_b: list[Fraction] = []
    star: list[list[Fraction]] = []
    for i in range(n):
        v = [Fraction(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = Fraction(_dot(b[i], star[j])) / big_b[j]
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        norm = _dot(v, v)
        if norm == 0:
            raise ValueError("the rows are linearly dependent")
        star.append(v)
        big_b.append(norm)
    return mu, big_b, star


def _check(basis: Sequence[Sequence[Number]]) -> list[list[Number]]:
    b = [list(row) for row in basis]
    if not b or not b[0] or any(len(row) != len(b[0]) for row in b):
        raise ValueError("need n >= 1 rows of the same positive length")
    return b


def _search(
    mu: list[list[Fraction]],
    big_b: list[Fraction],
    tau: list[Fraction],
    r2: Fraction,
    best: list[int],
    svp: bool,
) -> tuple[list[int], Fraction]:
    """Depth-first search with zig-zag order and a shrinking radius.

    Finds integer x minimizing sum_k (x_k - c_k)^2 B_k with c_k = tau_k - sum_(j>k) x_j mu_jk,
    among x != 0 for SVP (tau = 0), and returns it with its value if it is below r2;
    otherwise returns the given best and r2. Levels are 0-based here.
    """
    n = len(big_b)
    x = [0] * n
    c = [Fraction(0)] * n
    ell = [Fraction(0)] * (n + 1)
    turn = [0] * n  # how many zig-zag steps were taken at each level
    side = [1] * n  # +1 if the second value tried is above the first, else -1
    k = n - 1  # @line L3
    c[k] = tau[k]
    x[k] = _nearest(c[k])
    side[k] = 1 if c[k] >= x[k] else -1
    while True:  # @line L4
        ell[k] = ell[k + 1] + (x[k] - c[k]) ** 2 * big_b[k]  # @line L5
        if ell[k] < r2 and k > 0:  # @line L6
            k -= 1  # @line L7
            c[k] = tau[k] - sum((x[j] * mu[j][k] for j in range(k + 1, n)), Fraction(0))
            x[k] = _nearest(c[k])
            side[k] = 1 if c[k] >= x[k] else -1
            turn[k] = 0
            continue
        if ell[k] < r2:  # @line L8
            if not svp or any(x):  # @line L9
                r2 = ell[0]
                best = list(x)
        else:
            k += 1  # @line L10
            if k == n:
                return best, r2  # @line L11
        # L12: next value of x_k, in order of non-decreasing distance from c_k.
        if svp and all(v == 0 for v in x[k + 1:]):  # @line L12
            x[k] += 1  # the top levels: only one of v and -v
        else:
            turn[k] += 1
            step = (turn[k] + 1) // 2
            x[k] = _nearest(c[k]) + (side[k] * step if turn[k] % 2 == 1 else -side[k] * step)


def schnorr_euchner_svp(basis: Sequence[Sequence[Number]]) -> tuple[list[Number], list[int], Fraction]:
    """Find a shortest nonzero vector of the lattice with basis rows `basis`.

    Input: n >= 1 linearly independent rows of length m, int or Fraction entries.
    Output: (v, x, s) with v = sum x_i b_i a shortest nonzero lattice vector,
    x its integer coefficients and s = ||v||^2, all exact.
    Cost: O(n^2 m) for Gram-Schmidt plus O(n) arithmetic operations per node of
    the enumeration tree; the tree size depends on the basis and is at most
    2^(O(n^2)) for an LLL-reduced basis. Space O(n^2 + n m).
    """
    b = _check(basis)
    n = len(b)
    mu, big_b, _ = _gram_schmidt(b)  # @line L1
    start = [1] + [0] * (n - 1)  # @line L2
    x, s = _search(mu, big_b, [Fraction(0)] * n, big_b[0], start, True)
    v = [sum((x[i] * b[i][t] for i in range(n)), 0) for t in range(len(b[0]))]
    return v, x, s


def schnorr_euchner_cvp(
    basis: Sequence[Sequence[Number]], target: Sequence[Number]
) -> tuple[list[Number], list[int], Fraction]:
    """Find a lattice vector closest to `target`.

    Output: (v, x, s) with v = sum x_i b_i closest to the target and s = ||target - v||^2.
    The search starts from Babai's nearest plane vector, so its radius is finite.
    Raises ValueError if the target has the wrong length.
    """
    b = _check(basis)
    n, m = len(b), len(b[0])
    if len(target) != m:
        raise ValueError("the target must have the length of the rows")
    mu, big_b, star = _gram_schmidt(b)
    tau = [Fraction(_dot(target, star[k])) / big_b[k] for k in range(n)]
    # the part of the target outside the span adds a constant to every distance
    proj = [sum((tau[k] * star[k][t] for k in range(n)), Fraction(0)) for t in range(m)]
    off = [Fraction(target[t]) - proj[t] for t in range(m)]
    # Babai's nearest plane gives the starting vector and radius.
    babai = [0] * n
    rest = list(tau)
    dist = Fraction(0)
    for k in range(n - 1, -1, -1):
        babai[k] = _nearest(rest[k])
        for j in range(k):
            rest[j] -= babai[k] * mu[k][j]
        dist += (rest[k] - babai[k]) ** 2 * big_b[k]
    # search for strictly better vectors; if there is none, Babai's vector is closest
    x, s = _search(mu, big_b, tau, dist, babai, False)
    v = [sum((x[i] * b[i][t] for i in range(n)), 0) for t in range(m)]
    return v, x, s + _dot(off, off)
