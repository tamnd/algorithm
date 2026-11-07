# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-irreducibility-test/. The authors are listed in prov/6CAYMS.jsonl.
"""Rabin's irreducibility test over the prime field F_p.

Polynomials are lists of ints, lowest degree first, read modulo p; the zero
polynomial is []. The prime p is not checked.
"""

from __future__ import annotations

from typing import Sequence

Poly = list[int]


def _strip(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def _rem(a: Sequence[int], f: Sequence[int], p: int) -> Poly:
    """a rem f for a monic f of degree at least 1."""
    r = [c % p for c in a]
    n = len(f) - 1
    for k in range(len(r) - 1, n - 1, -1):
        t = r[k]
        if t:
            for j in range(n):
                r[k - n + j] = (r[k - n + j] - t * f[j]) % p
        r[k] = 0
    return _strip(r[:n])


def _mulmod(a: Poly, b: Poly, f: Poly, p: int) -> Poly:
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return _rem(c, f, p)


def _powmod(a: Poly, e: int, f: Poly, p: int) -> Poly:
    """a^e rem f by binary powering, with O(log e) products modulo f."""
    result = _rem([1], f, p)
    base = _rem(a, f, p)
    while e:
        if e & 1:
            result = _mulmod(result, base, f, p)
        base = _mulmod(base, base, f, p)
        e >>= 1
    return result


def _gcd_is_one(a: Poly, b: Poly, p: int) -> bool:
    a, b = _strip([c % p for c in a]), _strip([c % p for c in b])
    while b:
        inv = pow(b[-1], -1, p)
        a, b = b, _rem(a, [c * inv % p for c in b], p)
    return len(a) == 1


def _prime_divisors(n: int) -> set[int]:
    out, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def is_irreducible(f: Sequence[int], p: int) -> bool:
    """True when f is irreducible in F_p[x].

    Precondition: p is prime. Constants (including 0) are not irreducible.
    Cost: n powerings by p modulo f, each O(log p) products of degree < n,
    so O(n log p) multiplications modulo f, plus one gcd for each prime
    divisor of n; with the schoolbook products here, O(n^3 log p).
    """
    f = _strip([c % p for c in f])
    if len(f) < 2:
        return False
    inv = pow(f[-1], -1, p)
    f = [c * inv % p for c in f]  # @line L1
    n = len(f) - 1
    primes = _prime_divisors(n)  # @line L2
    x = _rem([0, 1], f, p)
    h = x  # @line L3
    for j in range(1, n + 1):  # @line L4
        h = _powmod(h, p, f, p)  # @line L5
        if j < n and n % j == 0 and n // j in primes:  # @line L6
            diff = _strip([(h[i] if i < len(h) else 0) - (x[i] if i < len(x) else 0)
                           for i in range(max(len(h), len(x)))])
            if not _gcd_is_one(diff, f, p):  # @line L7
                return False
    return h == x  # @line L8
