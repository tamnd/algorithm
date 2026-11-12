# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-muller-code/. The authors are listed in prov/CWKBQ3.jsonl.

"""Binary Reed-Muller codes RM(r, m).

RM(r, m) is the set of value tables of Boolean polynomials of degree at most r in m
variables, evaluated at all 2^m points. A word is an int with bit p = value at the point
whose binary digits are p (bit i of p is the variable x_i).

* generator(r, m): one row per monomial x_S with |S| <= r.
* encode(coeffs, r, m): the table of sum_S coeffs[S] x_S.
* uuv(r, m): the same code built by the (u | u + v) recursion.
* anf(word, m): the inverse map (the binary Moebius transform), word -> polynomial.
"""

from itertools import combinations
from math import comb


def monomials(r: int, m: int) -> list[tuple[int, ...]]:
    """Subsets S of {0, ..., m-1} with |S| <= r, by degree then lexicographically."""
    return [s for d in range(r + 1) for s in combinations(range(m), d)]


def monomial_table(s: tuple[int, ...], m: int) -> int:
    """Value table of x_S = prod_{i in S} x_i: bit p is 1 exactly when p contains S."""
    mask = sum(1 << i for i in s)
    return sum(1 << p for p in range(1 << m) if p & mask == mask)


def generator(r: int, m: int) -> list[int]:
    return [monomial_table(s, m) for s in monomials(r, m)]


def dimension(r: int, m: int) -> int:
    return sum(comb(m, i) for i in range(r + 1))


def encode(msg: int, r: int, m: int) -> int:
    """Bit j of msg is the coefficient of the j-th monomial of monomials(r, m)."""
    out = 0
    for j, row in enumerate(generator(r, m)):
        if (msg >> j) & 1:
            out ^= row
    return out


def span(rows: list[int]) -> set[int]:
    words = {0}
    for row in rows:
        words |= {w ^ row for w in words}
    return words


def code(r: int, m: int) -> set[int]:
    if r < 0:
        return {0}
    return span(generator(min(r, m), m))


def uuv(r: int, m: int) -> set[int]:
    """RM(r, m) = {(u | u + v) : u in RM(r, m - 1), v in RM(r - 1, m - 1)},
    with RM(0, m) = {0, 1...1}, RM(m, m) = all words, RM(-1, m) = {0}.
    The left half is the points with x_{m-1} = 0, the right half those with x_{m-1} = 1."""
    if r < 0:
        return {0}
    if r >= m:
        return set(range(1 << (1 << m)))
    if r == 0:
        return {0, (1 << (1 << m)) - 1}
    half = 1 << (m - 1)
    return {u | ((u ^ v) << half) for u in uuv(r, m - 1) for v in uuv(r - 1, m - 1)}


def anf(word: int, m: int) -> dict[tuple[int, ...], int]:
    """Algebraic normal form by the binary Moebius transform: the coefficient of x_S is the
    sum of the word over the points p contained in S."""
    n = 1 << m
    a = [(word >> p) & 1 for p in range(n)]
    for i in range(m):
        for p in range(n):
            if p >> i & 1:
                a[p] ^= a[p ^ (1 << i)]
    return {tuple(i for i in range(m) if p >> i & 1): a[p] for p in range(n) if a[p]}


def degree(word: int, m: int) -> int:
    """Degree of the Boolean function with this table; -1 for the zero function."""
    return max((len(s) for s in anf(word, m)), default=-1)


def min_weight_count(r: int, m: int) -> int:
    """Number of words of weight 2^(m - r) in RM(r, m): the indicator vectors of the
    (m - r)-dimensional affine subspaces (flats) of GF(2)^m."""
    num, den = 1, 1
    for i in range(m - r):
        num *= (1 << (m - i)) - 1
        den *= (1 << (m - r - i)) - 1
    return (1 << r) * num // den


def weight_distribution(words, n: int) -> list[int]:
    out = [0] * (n + 1)
    for w in words:
        out[w.bit_count()] += 1
    return out


def inner(u: int, v: int) -> int:
    return (u & v).bit_count() & 1
