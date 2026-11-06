# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wheel-factorization/. The authors are listed in prov/SXCYK3.jsonl.

from math import gcd, prod


def wheel(basis: tuple[int, ...]) -> tuple[int, list[int]]:
    """The wheel of the basis primes p_1, ..., p_k with W = p_1 * ... * p_k.

    Return (s, gaps): s is the least integer above 1 coprime to W (so s = p_{k+1}
    when the basis is the first k primes), and gaps lists the differences between
    the phi(W) consecutive integers coprime to W, starting at s, around one turn.
    Cost: O(W log W) time, O(phi(W)) space."""
    w = prod(basis)
    s = 2
    while gcd(s, w) != 1:
        s += 1
    res = [r for r in range(s, s + w) if gcd(r, w) == 1]
    gaps = [b - a for a, b in zip(res, res[1:])] + [res[0] + w - res[-1]]
    return s, gaps


def wheel_factorization(n: int, basis: tuple[int, ...] = (2, 3, 5)) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division by the basis primes, then by the integers coprime to their
    product W, which the wheel lists. Precondition: basis is a tuple of the first
    k primes, k >= 0. Cost: O(n^(1/2) * phi(W)/W + k) divisions after the
    O(W log W) wheel set-up.
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    s, gaps = wheel(basis)
    factors: list[int] = []
    m = n  # @line L1
    for p in basis:  # @line L2
        while m % p == 0:  # @line L3
            factors.append(p)
            m //= p
    d, i = s, 0  # @line L4
    while d * d <= m:  # @line L5
        while m % d == 0:  # @line L6
            factors.append(d)
            m //= d
        d += gaps[i]  # @line L7
        i = (i + 1) % len(gaps)
    if m > 1:  # @line L8
        factors.append(m)
    return factors  # @line L9
