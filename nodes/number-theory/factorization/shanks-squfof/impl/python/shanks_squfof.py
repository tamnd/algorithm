# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shanks-squfof/. The authors are listed in prov/QBJ183.jsonl.

from math import gcd, isqrt

MULTIPLIERS = (1, 3, 5, 7, 11, 15, 21, 33, 35, 55, 77, 105, 165, 231, 385, 1155)


def squfof(n: int, k: int = 1, limit: int = 0) -> int:
    """Shanks' square forms factorization of n with the multiplier k.

    Precondition: n >= 3 odd, not a perfect square, k >= 1 squarefree, and k * n
    not a perfect square. The forward and backward cycles each make at most
    `limit` steps; the default is 4 * ceil(sqrt(2 * sqrt(k * n))) + 8.
    Returns a proper factor of n, or 1 if this multiplier fails.
    Cost: O(limit) steps, each one division and a few products of numbers below
    2 sqrt(k n); heuristically O(n^(1/4)) steps.
    """
    if n < 3 or n % 2 == 0 or k < 1:
        raise ValueError("need odd n >= 3 and k >= 1")
    d = k * n  # @line L1
    a0 = isqrt(d)
    if a0 * a0 == d:
        raise ValueError("k * n must not be a perfect square")
    if limit <= 0:
        limit = 4 * (isqrt(2 * a0) + 1) + 8
    p, q_prev, q = a0, 1, d - a0 * a0  # @line L2
    i = 1
    while i < limit:
        b = (a0 + p) // q  # @line L3
        p_new = b * q - p
        q_prev, q = q, q_prev + b * (p - p_new)
        p = p_new
        i += 1
        if i % 2 == 1:  # @line L4
            continue
        r = isqrt(q)
        if r * r != q:
            continue
        b = (a0 - p) // r  # @line L5
        s_p = b * r + p
        s_prev, s = r, (d - s_p * s_p) // r
        for _ in range(limit):  # @line L6
            b = (a0 + s_p) // s  # @line L7
            s_new = b * s - s_p
            if s_new == s_p:  # @line L8
                break
            s_prev, s = s, s_prev + b * (s_p - s_new)
            s_p = s_new
        else:
            continue
        g = gcd(n, s_p)  # @line L9
        if 1 < g < n:
            return g  # @line L10
    return 1  # @line L11


_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_probable_prime(n: int) -> bool:
    """Strong probable-prime test to the 13 prime bases up to 41.

    It is a proof of primality for n < 3317044064679887385961981 (about 3.3 * 10^24)."""
    if n < 2:
        return False
    for p in _BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in _BASES:
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


_SMALL_PRIMES = [d for d in range(2, 1 << 16) if all(d % e for e in range(2, isqrt(d) + 1))]


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 2^16.

    A perfect square is split by its square root. Otherwise SQUFOF runs with
    the multipliers 1, 3, 5, ..., 1155 in turn, skipping those that share a
    factor with m or make k * m a square. Trial division is the last resort."""
    r = isqrt(m)
    if r * r == m:
        return r
    for k in MULTIPLIERS:
        if gcd(k, m) > 1:
            continue
        s = isqrt(k * m)
        if s * s == k * m:
            continue
        g = squfof(m, k)
        if g > 1:
            return g
    d = 65537
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 2^16, then each composite part is
    split by SQUFOF. A loop with an explicit stack replaces recursion. SQUFOF
    costs about m^(1/4) steps for a part m, so this is meant for n up to about
    2^80 once the small factors are gone."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    for d in _SMALL_PRIMES:
        if d * d > n:
            break
        while n % d == 0:
            out.append(d)
            n //= d
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_probable_prime(m):
            out.append(m)
            continue
        g = _split(m)
        stack.extend((g, m // g))
    return sorted(out)
