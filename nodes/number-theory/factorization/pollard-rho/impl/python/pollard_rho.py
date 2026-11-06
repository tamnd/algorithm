# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-rho/. The authors are listed in prov/ZGK3CY.jsonl.

from math import gcd


def pollard_rho(n: int, c: int = 1, s: int = 2) -> int:
    """Pollard's rho method with f(x) = x^2 + c mod n and Floyd's cycle finding.

    Return a divisor g > 1 of n. The method succeeds when g < n; g == n means
    that this choice of c and s failed, and another c should be tried.
    Precondition: n >= 2, 0 <= s < n. Raises ValueError otherwise.
    Cost: heuristically O(p^(1/2)) steps, p the smallest prime factor of n, each
    with 3 multiplications modulo n and one gcd. Never more than n steps.
    """
    if n < 2 or not 0 <= s < n:
        raise ValueError("need n >= 2 and 0 <= s < n")
    x, y, g = s, s, 1  # @line L1
    while g == 1:  # @line L2
        x = (x * x + c) % n  # @line L3
        y = (y * y + c) % n  # @line L4
        y = (y * y + c) % n
        g = gcd(abs(x - y), n)  # @line L5
    return g  # @line L6


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
    """A proper factor of an odd composite m: rho with c = 1, 2, ... (c = m - 2
    is skipped, since x^2 - 2 is a poor map). Trial division is a last resort."""
    for c in range(1, 100):
        if c == m - 2:
            continue
        g = pollard_rho(m, c, 2 % m)
        if g < m:
            return g
    d = 3
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    The factors 2 are removed first; every odd composite part is split by
    Pollard's rho. A loop with an explicit stack replaces recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    while n % 2 == 0:
        out.append(2)
        n //= 2
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
