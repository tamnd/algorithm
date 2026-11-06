# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lehman-factorization/. The authors are listed in prov/DT65XZ.jsonl.

from math import gcd, isqrt


def icbrt(n: int) -> int:
    """The largest integer c with c^3 <= n, for n >= 0, by Newton's method."""
    if n < 8:
        return 1 if n > 0 else 0
    c = 1 << ((n.bit_length() + 2) // 3)
    while True:
        d = (2 * c + n // (c * c)) // 3
        if d >= c:
            break
        c = d
    while c * c * c > n:
        c -= 1
    while (c + 1) ** 3 <= n:
        c += 1
    return c


def lehman_factorization(n: int) -> int:
    """Lehman's method. Return a divisor d of n with 1 < d < n, or n if n is prime.

    Precondition: n >= 22. Raises ValueError otherwise.
    Cost: O(n^(1/3)) arithmetic operations on numbers of the size of n: trial
    division to n^(1/3), then about n^(1/3) perfect-square tests.
    """
    if n < 22:
        raise ValueError("n must be at least 22")
    c = icbrt(n)  # @line L1
    for d in range(2, c + 1):
        if n % d == 0:
            return d
    for k in range(1, c + 2):  # @line L2
        a = isqrt(4 * k * n)  # @line L3
        if a * a < 4 * k * n:
            a += 1
        while True:
            r = a * a - 4 * k * n  # @line L4
            if r * r * r >= n * n:
                break
            b = isqrt(r)  # @line L5
            if b * b == r:
                return gcd(a + b, n)
            a += 1  # @line L6
    return n  # @line L7


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

    Parts below 22 are factored by trial division. Larger parts are tested with
    Miller-Rabin and, when composite, split by Lehman's method. A loop with an
    explicit stack replaces recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if m < 22:
            d = 2
            while m % d:
                d += 1
            out.append(d)
            stack.append(m // d)
            continue
        if is_probable_prime(m):
            out.append(m)
            continue
        d = lehman_factorization(m)
        stack.extend((d, m // d))
    return sorted(out)
