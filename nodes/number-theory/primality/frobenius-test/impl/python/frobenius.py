# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frobenius-test/. The authors are listed in prov/3WFYQX.jsonl.

"""Grantham's random quadratic Frobenius test (RQFT).

frobenius_test(n, rng) returns False only when n is composite. For a
composite n that is not a square and has no prime factor up to 50000, one
call returns True for at most 1/7710 of the allowed polynomials, so with
probability at most 1/7710 (Grantham 1998). Below 50000^2 the answer is
exact, by trial division.

Cost, with lg n binary digits and arbitrary precision integers (Python int):
O(lg n) products in the ring Z_n[x]/(x^2 - a x + b), each a few products
modulo n, so about three times the cost of one Miller-Rabin round, plus a
fixed amount of trial division and an expected O(1) Jacobi symbols.
"""

import math
import random

TRIAL_BOUND = 50000


def primes_up_to(m: int) -> list[int]:
    """The primes p <= m, by the sieve of Eratosthenes."""
    if m < 2:
        return []
    sieve = bytearray([1]) * (m + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, math.isqrt(m) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, m + 1, i)))
    return [i for i in range(m + 1) if sieve[i]]


SMALL_PRIMES = primes_up_to(TRIAL_BOUND)


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n >= 1."""
    if n < 1 or n % 2 == 0:
        raise ValueError("n must be odd and positive")
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def _mul(f: tuple[int, int], g: tuple[int, int], n: int, a: int, b: int) -> tuple[int, int]:
    """(u1 + v1 x)(u2 + v2 x) modulo (x^2 - a x + b, n), using x^2 = a x - b."""
    u1, v1 = f
    u2, v2 = g
    vv = v1 * v2
    return (u1 * u2 - b * vv) % n, (u1 * v2 + u2 * v1 + a * vv) % n


def _square(f: tuple[int, int], n: int, a: int, b: int) -> tuple[int, int]:
    """(u + v x)^2 = u^2 - b v^2 + (2 u v + a v^2) x, with three products."""
    u, v = f
    vv = v * v
    return (u * u - b * vv) % n, (2 * u * v + a * vv) % n


def _times_x(f: tuple[int, int], n: int, a: int, b: int) -> tuple[int, int]:
    """(u + v x) x = -b v + (u + a v) x."""
    u, v = f
    return (-b * v) % n, (u + a * v) % n


def power_of_x(e: int, n: int, a: int, b: int) -> tuple[int, int]:
    """x^e modulo (x^2 - a x + b, n) as a pair (u, v) meaning u + v x.

    Left-to-right binary powering: a squaring for each binary digit of e
    and a cheap product by x for each digit 1.
    """
    result = (1 % n, 0)
    for bit in bin(e)[2:]:
        result = _square(result, n, a, b)
        if bit == "1":
            result = _times_x(result, n, a, b)
    return result


def quadratic_frobenius(n: int, a: int, b: int) -> bool:
    """The strong quadratic Frobenius test of n with respect to x^2 - a x + b.

    Needs n odd, n >= 3, gcd(n, b (a^2 - 4b)) = 1, ((a^2 - 4b)/n) = -1 and
    (b/n) = 1. Returns False only when n is composite.
    """
    u, v = power_of_x((n + 1) // 2, n, a, b)  # @line L7
    if v != 0:  # @line L8
        return False
    if u * u % n != b % n:  # @line L9
        return False
    s, r = n * n - 1, 0  # @line L10
    while s % 2 == 0:
        s //= 2
        r += 1
    z = power_of_x(s, n, a, b)
    if z == (1, 0):  # @line L11
        return True
    for _ in range(r - 1):  # @line L12
        if z == (n - 1, 0):
            return True
        z = _square(z, n, a, b)
    return False  # @line L13


def choose_parameters(n: int, rng: random.Random) -> tuple[int, int] | int:
    """Random a, b in [1, n) with ((a^2 - 4b)/n) = -1 and (b/n) = 1, for odd non-square n >= 3.

    Returns the pair, or a factor d with 1 < d < n if one turns up.
    """
    while True:
        a = rng.randrange(1, n)
        b = rng.randrange(1, n)
        delta = a * a - 4 * b
        d = math.gcd(delta * b, n)
        if 1 < d < n:
            return d
        if d == 1 and jacobi(delta, n) == -1 and jacobi(b, n) == 1:
            return a, b


def frobenius_test(n: int, rng: random.Random | None = None, bound: int = TRIAL_BOUND) -> bool:
    """One round of the random quadratic Frobenius test.

    Returns True if n is prime or a rare Frobenius liar, and False only when
    n is composite. The trial division bound can be lowered for experiments;
    the 1/7710 error bound needs bound >= 50000.
    """
    if bound < 2:
        raise ValueError("the trial division bound must be at least 2")
    if rng is None:
        rng = random.Random()
    if n < 2:  # @line L1
        return False
    primes = SMALL_PRIMES if bound == TRIAL_BOUND else primes_up_to(bound)
    for q in primes:  # @line L2
        if q * q > n:
            return True
        if n % q == 0:
            return n == q
    if n < (bound + 1) ** 2:  # @line L3
        return True  # every prime up to sqrt(n) was tried
    if math.isqrt(n) ** 2 == n:  # @line L4
        return False
    params = choose_parameters(n, rng)  # @line L5
    if isinstance(params, int):  # @line L6
        return False
    a, b = params
    return quadratic_frobenius(n, a, b)


def is_probable_prime(n: int, rounds: int = 1, rng: random.Random | None = None) -> bool:
    """rounds independent rounds; a composite passes with probability at most 7710^(-rounds)."""
    if rng is None:
        rng = random.Random()
    return all(frobenius_test(n, rng) for _ in range(max(1, rounds)))
