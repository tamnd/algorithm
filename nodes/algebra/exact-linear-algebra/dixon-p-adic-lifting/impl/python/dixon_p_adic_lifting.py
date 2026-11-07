# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dixon-p-adic-lifting/. The authors are listed in prov/YG36BM.jsonl.

from fractions import Fraction
from math import isqrt
from typing import Iterable, Iterator, Sequence


def _is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3 * 10^24."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _default_primes() -> Iterator[int]:
    """Primes below 2^31, largest first."""
    q = 2**31 - 1
    while q > 2:
        if _is_prime(q):
            yield q
        q -= 2


def inverse_mod_p(a: Sequence[Sequence[int]], p: int) -> list[list[int]] | None:
    """Inverse of a modulo the prime p by Gauss-Jordan elimination, or None if det a = 0 mod p."""
    n = len(a)
    m = [[x % p for x in row] + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        piv = next((i for i in range(c, n) if m[i][c]), None)
        if piv is None:
            return None
        m[c], m[piv] = m[piv], m[c]
        inv = pow(m[c][c], -1, p)
        m[c] = [x * inv % p for x in m[c]]
        for i in range(n):
            if i != c and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[c])]
    return [row[n:] for row in m]


def rational_reconstruction(u: int, m: int, bound_n: int, bound_d: int) -> Fraction | None:
    """Return the fraction s/t with s = t u (mod m), |s| <= bound_n and 0 < t <= bound_d.

    Requires 2 bound_n bound_d < m; then the fraction is unique if it exists.
    Runs the extended Euclidean algorithm on (m, u) until the remainder is at most bound_n.
    """
    r0, r1, t0, t1 = m, u % m, 0, 1
    while r1 > bound_n:
        q = r0 // r1
        r0, r1, t0, t1 = r1, r0 - q * r1, t1, t0 - q * t1
    if t1 == 0 or abs(t1) > bound_d:
        return None
    return Fraction(r1, t1)


def dixon_solve(a: Sequence[Sequence[int]], b: Sequence[int],
                primes: Iterable[int] | None = None) -> list[Fraction] | None:
    """Solve a x = b for a square integer matrix a; return the rational solution, or None if a is singular.

    Cost: O(n^3) operations modulo p for the inverse, then O(n^2) per p-adic digit for
    k = O(n (b + log n) / log p) digits, and n rational reconstructions:
    O(n^3 (b + log n)^2) bit operations with schoolbook arithmetic and a word-size p.
    """
    n = len(a)
    if n == 0:
        return []
    col2 = [sum(a[i][j] ** 2 for i in range(n)) for j in range(n)]
    prod = 1
    for c in col2:
        prod *= c
    had = isqrt(prod) + 1  # |det a| < had, by Hadamard on the columns
    p, inv, tried = 0, None, 1
    for q in primes if primes is not None else _default_primes():  # @line L1
        inv = inverse_mod_p(a, q)
        if inv is not None:
            p = q
            break
        tried *= q
        if tried > had:
            return None  # det a = 0 modulo a product larger than |det a|
    if inv is None:
        raise ValueError("ran out of primes")
    bound_d = had  # @line L2
    bound_n = isqrt(prod * sum(x * x for x in b)) + 1
    k, pk = 0, 1  # @line L3
    while pk <= 2 * bound_n * bound_d:
        k, pk = k + 1, pk * p
    r = list(b)  # @line L4
    xbar = [0] * n
    pi = 1
    for _ in range(k):  # @line L5
        y = [sum(inv[i][j] * r[j] for j in range(n)) % p for i in range(n)]  # @line L6
        xbar = [xbar[i] + y[i] * pi for i in range(n)]  # @line L7
        pi *= p
        new = []
        for i in range(n):  # @line L8
            t = r[i] - sum(a[i][j] * y[j] for j in range(n))
            assert t % p == 0
            new.append(t // p)
        r = new
    x = []
    for j in range(n):  # @line L9
        f = rational_reconstruction(xbar[j], pk, bound_n, bound_d)  # @line L10
        assert f is not None
        x.append(f)
    return x  # @line L11
