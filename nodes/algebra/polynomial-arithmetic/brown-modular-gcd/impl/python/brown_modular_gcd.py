# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brown-modular-gcd/. The authors are listed in prov/02TR5G.jsonl.

"""Brown's modular gcd of two polynomials in Z[x], with the small primes method.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n] of
Python ints, lowest degree first; the zero polynomial is []. The gcd is
returned with a positive leading coefficient, and gcd(0, 0) = [].

For each prime p that does not divide b = gcd(lc f, lc g), the algorithm
computes the monic gcd v of f and g modulo p and the cofactors f / v and
g / v modulo p. Images of the smallest degree are combined by the Chinese
remainder theorem. A norm test, not a trial division, proves that the
combined polynomial is the gcd. All loops are iterative.
"""

from __future__ import annotations

from math import gcd
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

Poly = List[int]


def trim(a: Sequence[int]) -> Poly:
    """Return a copy of a without trailing zero coefficients."""
    out = list(a)
    while out and out[-1] == 0:
        out.pop()
    return out


def content(a: Sequence[int]) -> int:
    """The gcd of the coefficients, 0 for the zero polynomial."""
    c = 0
    for x in a:
        c = gcd(c, x)
    return c


def primitive_part(a: Sequence[int]) -> Poly:
    """a divided by its content, with a positive leading coefficient."""
    a = trim(a)
    if not a:
        return []
    c = content(a)
    if a[-1] < 0:
        c = -c
    return [x // c for x in a]


def _mod_p(a: Sequence[int], p: int) -> Poly:
    return trim([x % p for x in a])


def _divmod_p(a: Sequence[int], b: Sequence[int], p: int) -> Tuple[Poly, Poly]:
    """Quotient and remainder of a by the nonzero b in (Z/pZ)[x]."""
    r = _mod_p(a, p)
    inv = pow(b[-1], -1, p)
    db = len(b) - 1
    if len(r) <= db:
        return [], r
    q = [0] * (len(r) - db)
    for i in range(len(r) - 1, db - 1, -1):
        c = r[i] * inv % p
        if c:
            q[i - db] = c
            for j in range(db + 1):
                r[i - db + j] = (r[i - db + j] - c * b[j]) % p
    return trim(q), trim(r[:db])


def gcd_mod_p(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    """The monic gcd of a and b in (Z/pZ)[x], by the Euclidean algorithm."""
    a, b = _mod_p(a, p), _mod_p(b, p)
    while b:
        a, b = b, _divmod_p(a, b, p)[1]
    if not a:
        return []
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]


def _symmetric(a: Sequence[int], m: int) -> Poly:
    return trim([x - m if 2 * x > m else x for x in a])


def _norm1(a: Sequence[int]) -> int:
    return sum(abs(x) for x in a)


def _crt(old: Sequence[int], m: int, new: Sequence[int], p: int) -> Poly:
    """Combine residues modulo m and modulo p into residues modulo m p (0 .. m p - 1)."""
    n = max(len(old), len(new))
    minv = pow(m, -1, p)
    out = []
    for i in range(n):
        x = old[i] if i < len(old) else 0
        y = new[i] if i < len(new) else 0
        out.append(x + m * ((y - x) * minv % p))
    return out


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
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


def word_primes(start: int = 2 ** 31) -> Iterator[int]:
    """Primes below start, in decreasing order."""
    n = start - 1
    while n > 2:
        if _is_prime(n):
            yield n
        n -= 1


def brown_gcd(f: Sequence[int], g: Sequence[int], primes: Optional[Iterable[int]] = None,
              log: Optional[list] = None) -> Poly:
    """Return gcd(f, g) in Z[x] with a positive leading coefficient.

    primes is an iterable of distinct primes to use (default: primes below
    2^31). If log is a list, one entry (p, degree, action) is appended for
    every prime tried.
    """
    f, g = trim(f), trim(g)
    if not f or not g:
        h = f or g
        return [-x for x in h] if h and h[-1] < 0 else h
    c = gcd(content(f), content(g))  # @line L1
    f, g = primitive_part(f), primitive_part(g)  # @line L1
    if len(f) == 1 or len(g) == 1:
        return [c]
    b = gcd(f[-1], g[-1])  # @line L2
    d = min(len(f), len(g)) - 1  # @line L2
    m = 1  # @line L2
    bf = [b * x for x in f]
    bg = [b * x for x in g]
    big = 2 * max(max(abs(x) for x in bf), max(abs(x) for x in bg))
    H: Poly = []
    U: Poly = []
    W: Poly = []
    for p in (primes if primes is not None else word_primes()):  # @line L3
        if b % p == 0:  # @line L3
            continue
        v = gcd_mod_p(f, g, p)  # @line L4
        u = _divmod_p(f, v, p)[0]  # @line L4
        w = _divmod_p(g, v, p)[0]  # @line L4
        v = [b * x % p for x in v]  # @line L4
        if len(v) - 1 > d:  # @line L5
            if log is not None:
                log.append((p, len(v) - 1, "skipped"))
            continue
        if len(v) - 1 < d or m == 1:  # @line L6
            H, U, W, m, d = v, u, w, p, len(v) - 1  # @line L6
            step = "restarted"
        else:
            step = "combined"
            H, U, W = _crt(H, m, v, p), _crt(U, m, u, p), _crt(W, m, w, p)  # @line L7
            m = m * p  # @line L7
        hs, us, ws = _symmetric(H, m), _symmetric(U, m), _symmetric(W, m)  # @line L8
        n1 = _norm1(hs)
        ok = 2 * n1 * _norm1(us) < m and 2 * n1 * _norm1(ws) < m and big < m  # @line L9
        if log is not None:
            log.append((p, d, "accepted" if ok else step))
        if ok:
            return [c * x for x in primitive_part(hs)]  # @line L10
    raise ValueError("ran out of primes")
