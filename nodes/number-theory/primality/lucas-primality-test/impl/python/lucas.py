# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-primality-test/. The authors are listed in prov/12XYK5.jsonl.

"""The Lucas primality test (n - 1 test), in the form of Brillhart, Lehmer and Selfridge.

lucas_primality_test(n, primes) decides whether n is prime, given the distinct
prime factors of n - 1. For each such prime q it looks for a base a with
a^(n-1) = 1 (mod n) and a^((n-1)/q) != 1 (mod n). The answer is always right:
true is a proof of primality, false comes with a Fermat witness.

Cost, with l binary digits in n and m distinct primes q: each base tried costs
two modular exponentiations, O(l) products modulo n, so O(l^3) bit operations
with schoolbook arithmetic. For a prime n the number of bases tried for q is
the least a that is not a q-th power residue, usually 2 or 3. For a composite
n each search stops at the latest at the smallest prime factor of n. Integers
are of arbitrary precision (Python int).
"""


def distinct_prime_factors(m: int) -> list[int]:
    """The distinct prime factors of m >= 1, by trial division (for small m only)."""
    if m < 1:
        raise ValueError("m must be at least 1")
    primes = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            primes.append(d)
            while m % d == 0:
                m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        primes.append(m)
    return primes


def _check_factors(n: int, primes: list[int] | tuple[int, ...]) -> None:
    """Raise ValueError unless primes are distinct and n - 1 is a product of their powers."""
    m = n - 1
    if len(set(primes)) != len(primes):
        raise ValueError("the primes must be distinct")
    for q in primes:
        if q < 2 or m % q != 0:
            raise ValueError("each q must be at least 2 and divide n - 1")
        while m % q == 0:
            m //= q
    if m != 1:
        raise ValueError("the primes must include every prime factor of n - 1")


def lucas_witnesses(n: int, primes: list[int] | tuple[int, ...]) -> dict[int, int] | None:
    """For a prime n, a dict q -> a with a^(n-1) = 1 and a^((n-1)/q) != 1 (mod n).

    Return None if n is composite. primes must be the distinct prime factors of
    n - 1; this is checked, except that the primality of each q is the caller's
    responsibility.
    """
    if n < 3:  # @line L1
        return {} if n == 2 else None
    _check_factors(n, primes)
    found: dict[int, int] = {}
    for q in primes:  # @line L2
        a = 2  # @line L3
        while True:  # @line L4
            if pow(a, n - 1, n) != 1:  # @line L5
                return None
            if pow(a, (n - 1) // q, n) != 1:  # @line L6
                found[q] = a
                break
            a += 1  # @line L7
    return found  # @line L8


def lucas_primality_test(n: int, primes: list[int] | tuple[int, ...]) -> bool:
    """True if n is prime, given the distinct prime factors of n - 1 (n >= 2)."""
    return lucas_witnesses(n, primes) is not None


def is_prime_lucas(n: int) -> bool:
    """Primality of n by the Lucas test, factoring n - 1 by trial division (small n only)."""
    if n < 3:
        return n == 2
    return lucas_primality_test(n, distinct_prime_factors(n - 1))


def verify_lucas_witnesses(n: int, primes: list[int] | tuple[int, ...], witnesses: dict[int, int]) -> bool:
    """Check a certificate from lucas_witnesses: one exponentiation pair per prime q."""
    if n == 2:
        return True
    if n < 3:
        return False
    _check_factors(n, primes)
    for q in primes:
        a = witnesses.get(q)
        if a is None or pow(a, n - 1, n) != 1 or pow(a, (n - 1) // q, n) == 1:
            return False
    return True
