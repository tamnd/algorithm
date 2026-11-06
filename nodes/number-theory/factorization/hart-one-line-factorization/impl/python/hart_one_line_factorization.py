# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hart-one-line-factorization/. The authors are listed in prov/D0TMW5.jsonl.

from math import gcd, isqrt


def hart_olf(n: int, multiplier: int = 1, iterations: int = 0) -> int:
    """Hart's one line factoring algorithm on n with a constant multiplier.

    Precondition: n >= 2 and multiplier >= 1. For each i = 1, 2, ...,
    s = ceil(sqrt(multiplier n i)) and m = s^2 - multiplier n i; a square m = t^2
    gives gcd(n, s - t). Only the i with 2 sqrt(multiplier n i) + 1 <= n are used,
    and for them every square gives a proper factor. Returns a proper factor of
    n, or 1. Cost: O(iterations) integer square roots of numbers of about
    2 log2 n bits."""
    if n < 2 or multiplier < 1:
        raise ValueError("need n >= 2 and multiplier >= 1")
    if iterations <= 0:
        iterations = 4 * iroot(n, 3) + 16
    mn = multiplier * n
    for i in range(1, iterations + 1):  # @line L1
        x = mn * i
        s = isqrt(x)  # @line L2
        if s * s < x:
            s += 1
        if 2 * s - 1 >= n:
            break
        m = s * s - x  # @line L3
        t = isqrt(m)  # @line L4
        if t * t == m:
            g = gcd(n, s - t)  # @line L5
            if 1 < g < n:
                return g
    return 1  # @line L6


def iroot(m: int, k: int) -> int:
    """The integer k-th root floor(m^(1/k)) of m >= 0, by Newton's method."""
    if m < 2:
        return m
    x = 1 << ((m.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + m // x ** (k - 1)) // k
        if y >= x:
            return x
        x = y


def primes_up_to(b: int) -> list[int]:
    """The primes p <= b, by the sieve of Eratosthenes in O(b log log b) time."""
    if b < 2:
        return []
    sieve = bytearray([1]) * (b + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, isqrt(b) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, b + 1, i)))
    return [i for i in range(b + 1) if sieve[i]]



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

    As in Hart's analysis, trial division runs up to n^(1/3) first. What is left
    has at most two prime factors, both above n^(1/3): it is 1, a prime, the
    square of a prime, or a product pq that OLF splits, with the multiplier 480
    and then 1. Trial division up to sqrt is the last resort, so it always ends."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    c = iroot(n, 3) + 1
    d = 2
    while d <= c and d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1 and is_probable_prime(n):
        out.append(n)
    elif n > 1:
        r = isqrt(n)
        if r * r == n:
            out += [r, r]
        else:
            g = 1
            for mult in (480, 1):
                g = hart_olf(n, mult, 8 * c + 64)
                if g > 1:
                    break
            if g == 1:
                g = d | 1
                while n % g:
                    g += 2
            out += [g, n // g]
    return sorted(out)
