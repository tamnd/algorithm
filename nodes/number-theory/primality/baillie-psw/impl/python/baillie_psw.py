# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baillie-psw/. The authors are listed in prov/33QWDT.jsonl.

"""Baillie-PSW primality test.

baillie_psw(n) returns False when n is certainly composite and True when n is
a probable prime. Every prime gets True. A composite that gets True would be a
counterexample to the test; none is known, and there is none below 2^64. No
bound on the error is proved. The test uses no randomness, so the answer
depends only on n.

The test is a strong probable prime test with the base 2 followed by a strong
Lucas probable prime test with P = 1 and Q = (1 - D)/4, where D is the first
of 5, -7, 9, -11, 13, ... with Jacobi symbol (D/n) = -1 (Selfridge's choice).

Cost: O(log n) products modulo n for each of the two tests, so
O((log n)^3) bit operations with schoolbook arithmetic, plus the Jacobi
symbols. Integers are of arbitrary precision (Python int).
"""

import math

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n >= 1, by quadratic reciprocity."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be odd and positive")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def is_strong_probable_prime(n: int, a: int) -> bool:
    """True when the odd n >= 3 passes the strong (Miller-Rabin) test with the base a."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def selfridge_parameters(n: int) -> tuple[int, int, int] | None:
    """Return (D, P, Q) by Selfridge's method A, or None if a D shares a factor with n.

    n must be odd, at least 3 and not a perfect square, or the search would not end.
    """
    d = 5  # @line L5
    while True:
        j = jacobi(d, n)  # @line L6
        if j == -1:
            break
        if j == 0 and abs(d) < n:  # @line L7
            return None
        d = -d - 2 if d > 0 else -d + 2  # @line L8
    return d, 1, (1 - d) // 4  # @line L9


def lucas_uvq(n: int, p: int, q: int, k: int) -> tuple[int, int, int]:
    """Return (U_k mod n, V_k mod n, Q^k mod n) for the Lucas sequences of (P, Q).

    n must be odd. The binary digits of k >= 1 are read from the top, with
    U_2m = U_m V_m, V_2m = V_m^2 - 2 Q^m, and the step m -> m + 1 given by
    U_(m+1) = (P U_m + V_m)/2, V_(m+1) = (D U_m + P V_m)/2 with D = P^2 - 4Q.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    dd = (p * p - 4 * q) % n
    half = (n + 1) // 2  # the inverse of 2 modulo the odd n
    u, v, qk = 1 % n, p % n, q % n
    for bit in bin(k)[3:]:
        u, v, qk = u * v % n, (v * v - 2 * qk) % n, qk * qk % n
        if bit == "1":
            u, v, qk = (p * u + v) * half % n, (dd * u + p * v) * half % n, qk * q % n
    return u, v, qk


def is_strong_lucas_probable_prime(n: int, p: int, q: int) -> bool:
    """The strong Lucas test of the odd n with parameters (P, Q)."""
    d, s = n + 1, 0  # @line L10
    while d % 2 == 0:
        d //= 2
        s += 1
    u, v, qk = lucas_uvq(n, p, q, d)  # @line L11
    if u == 0 or v == 0:  # @line L12
        return True
    for _ in range(s - 1):  # @line L13
        v, qk = (v * v - 2 * qk) % n, qk * qk % n  # @line L14
        if v == 0:  # @line L15
            return True
    return False  # @line L16


def baillie_psw(n: int) -> bool:
    """Return False if n is composite, True if n is a probable prime (Baillie-PSW)."""
    if n < 2:  # @line L1
        return False
    for p in SMALL_PRIMES:  # @line L2
        if n % p == 0:
            return n == p
    if not is_strong_probable_prime(n, 2):  # @line L3
        return False
    if math.isqrt(n) ** 2 == n:  # @line L4
        return False
    params = selfridge_parameters(n)
    if params is None:
        return False
    _, p, q = params
    return is_strong_lucas_probable_prime(n, p, q)
