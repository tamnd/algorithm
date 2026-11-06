# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-pollard-rho/. The authors are listed in prov/ES28TA.jsonl.

from math import gcd


def brent_pollard_rho(n: int, c: int = 1, s: int = 2, m: int = 128) -> int:
    """Brent's variant of Pollard's rho with f(x) = x^2 + c mod n.

    It compares x_{2r-2} with x_j for 3r - 1 <= j <= 4r - 2, r = 1, 2, 4, ...
    (Brent's cycle detection), and multiplies m differences before each gcd.
    Return a divisor g > 1 of n; g == n means failure for this c and s.
    Precondition: n >= 2, 0 <= s < n, m >= 1. Raises ValueError otherwise.
    Cost: heuristically O(p^(1/2)) multiplications modulo n, p the smallest prime
    factor of n, with one gcd per m steps. Never more than O(n) steps.
    """
    if n < 2 or not 0 <= s < n or m < 1:
        raise ValueError("need n >= 2, 0 <= s < n and m >= 1")
    y, r, q, g = s, 1, 1, 1  # @line L1
    x = ys = s
    while g == 1:  # @line L2
        x = y  # @line L3
        for _ in range(r):
            y = (y * y + c) % n
        k = 0  # @line L4
        while k < r and g == 1:  # @line L5
            ys = y  # @line L6
            for _ in range(min(m, r - k)):  # @line L7
                y = (y * y + c) % n
                q = q * abs(x - y) % n
            g = gcd(q, n)  # @line L8
            k += m
        r *= 2  # @line L9
    if g == n:  # @line L10
        while True:  # @line L11
            ys = (ys * ys + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break
    return g  # @line L12


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


def _split(m: int) -> int:
    """A proper factor of an odd composite m, by Brent's rho with c = 1, 2, ...
    (skipping c = m - 2). Trial division is a last resort."""
    for c in range(1, 100):
        if c == m - 2:
            continue
        g = brent_pollard_rho(m, c, 2 % m)
        if g < m:
            return g
    d = 3
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    The factors 2 are removed first; every odd composite part is split by Brent's
    rho. A loop with an explicit stack replaces recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    while n % 2 == 0:
        out.append(2)
        n //= 2
    stack = [n]
    while stack:
        v = stack.pop()
        if v == 1:
            continue
        if is_probable_prime(v):
            out.append(v)
            continue
        g = _split(v)
        stack.extend((g, v // g))
    return sorted(out)
