# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-factorization/. The authors are listed in prov/GZCF2N.jsonl.

from math import isqrt


def fermat_factorization(n: int) -> tuple[int, int]:
    """Return (a, b) with a * b == n and a <= b, where a is the largest divisor of n
    that is at most sqrt(n). So a == 1 exactly when n is prime (or n == 1).

    Precondition: n is odd and n >= 1. Raises ValueError otherwise.
    Cost: (a + b) / 2 - ceil(sqrt(n)) + 1 loop steps, each with one perfect-square
    test. This is fast when the two factors are close and Theta(n) when n = 3p.
    """
    if n < 1 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    x = isqrt(n)  # @line L1
    if x * x < n:
        x += 1
    r = x * x - n  # @line L2
    y = isqrt(r)
    while y * y != r:  # @line L3
        r += 2 * x + 1  # @line L4
        x += 1
        y = isqrt(r)
    # @line L5: y is the square root of r = x^2 - n
    return x - y, x + y  # @line L6


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


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division first removes every prime factor up to min(n^(1/3), 2^16),
    including all factors 2 (an n that is 2 mod 4 is not a difference of two
    squares). For n < 2^48 the rest is then 1, a prime, or a product of two primes
    above n^(1/3), and Fermat's method splits it in O(n^(2/3)) steps. A loop with an
    explicit stack replaces recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    while n % 2 == 0:
        out.append(2)
        n //= 2
    limit = _icbrt(n) if n < 1 << 48 else 1 << 16
    d = 3
    while d <= limit:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 2
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_probable_prime(m):
            out.append(m)
            continue
        a, b = fermat_factorization(m)
        stack.extend((a, b))
    return sorted(out)


def _icbrt(n: int) -> int:
    """The largest integer c with c^3 <= n, for 0 <= n < 2^48."""
    c = int(round(n ** (1 / 3)))
    while c * c * c > n:
        c -= 1
    while (c + 1) ** 3 <= n:
        c += 1
    return c
