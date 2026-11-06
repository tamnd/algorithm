# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pocklington-primality-test/. The authors are listed in prov/1J28JY.jsonl.

"""Pocklington primality test.

pocklington(n, f_factors) proves n prime from a factored part F of n - 1 with
F * F > n. f_factors maps each prime q dividing F to its exponent. The
primes q must already be known to be prime; the test does not check them.

The result is a pair (verdict, evidence):
  ("prime", {q: a_q})       a base a_q for each q; the certificate.
  ("composite", {...})       a Fermat witness or a proper factor.
  ("unknown", {})            no good base found in the allowed tries.
"prime" and "composite" are always right. For a prime n, "unknown" has
probability at most t * 2^-tries, where t is the number of primes q.

Cost: integers of arbitrary precision with bit length l = len(n). Each try
costs two modular exponentiations, O(l^3) bit operations with schoolbook
arithmetic, and one gcd, O(l^2). Factoring n - 1 is not included.
"""

import math
import random

PRIME = "prime"
COMPOSITE = "composite"
UNKNOWN = "unknown"


def factored_part(f_factors: dict[int, int]) -> int:
    f = 1
    for q, e in f_factors.items():
        f *= q**e
    return f


def pocklington(
    n: int, f_factors: dict[int, int], tries: int = 40, rng: random.Random | None = None
) -> tuple[str, dict]:
    if n < 5:  # @line L1
        return (PRIME, {}) if n in (2, 3) else (COMPOSITE, {})
    if n % 2 == 0:  # @line L2
        return COMPOSITE, {"factor": 2}
    big_f = factored_part(f_factors)
    if (n - 1) % big_f != 0 or big_f * big_f <= n:  # @line L3
        raise ValueError("need F | n - 1 and F * F > n")
    rng = rng if rng is not None else random.Random()
    bases: dict[int, int] = {}
    for q in f_factors:  # @line L4
        for _ in range(tries):  # @line L5
            a = rng.randint(2, n - 2)  # @line L6
            if pow(a, n - 1, n) != 1:  # @line L7
                return COMPOSITE, {"witness": a}
            g = math.gcd(pow(a, (n - 1) // q, n) - 1, n)  # @line L8
            if 1 < g < n:  # @line L9
                return COMPOSITE, {"factor": g}
            if g == 1:  # @line L10
                bases[q] = a
                break
        else:
            return UNKNOWN, {}  # @line L11
    return PRIME, bases  # @line L12


def verify_certificate(n: int, f_factors: dict[int, int], bases: dict[int, int]) -> bool:
    """Check a Pocklington certificate: F | n - 1, F * F > n, and for each
    prime q of F, a_q^(n-1) = 1 and gcd(a_q^((n-1)/q) - 1, n) = 1. The primes
    q themselves are trusted."""
    if n in (2, 3):
        return True
    if n < 2 or n % 2 == 0:
        return False
    big_f = factored_part(f_factors)
    if (n - 1) % big_f != 0 or big_f * big_f <= n or set(bases) != set(f_factors):
        return False
    for q, a in bases.items():
        if pow(a, n - 1, n) != 1 or math.gcd(pow(a, (n - 1) // q, n) - 1, n) != 1:
            return False
    return True


def bls_cube_root_test(
    n: int, f_factors: dict[int, int], tries: int = 40, rng: random.Random | None = None
) -> tuple[str, dict]:
    """Brillhart, Lehmer and Selfridge: the same base search, but F only needs
    F^3 >= n. When F^2 <= n, write n = c2 F^2 + c1 F + 1; n is prime exactly
    when c1^2 - 4 c2 is not a square."""
    if n < 5 or n % 2 == 0:
        return pocklington(n, {}, tries, rng) if n < 5 else (COMPOSITE, {"factor": 2})
    big_f = factored_part(f_factors)
    if (n - 1) % big_f != 0 or big_f**3 < n:
        raise ValueError("need F | n - 1 and F^3 >= n")
    rng = rng if rng is not None else random.Random()
    bases: dict[int, int] = {}
    for q in f_factors:
        for _ in range(tries):
            a = rng.randint(2, n - 2)
            if pow(a, n - 1, n) != 1:
                return COMPOSITE, {"witness": a}
            g = math.gcd(pow(a, (n - 1) // q, n) - 1, n)
            if 1 < g < n:
                return COMPOSITE, {"factor": g}
            if g == 1:
                bases[q] = a
                break
        else:
            return UNKNOWN, {}
    if big_f * big_f > n:
        return PRIME, bases
    c1 = (n // big_f) % big_f
    c2 = n // (big_f * big_f)
    d = c1 * c1 - 4 * c2
    if d >= 0 and math.isqrt(d) ** 2 == d:
        u = math.isqrt(d)
        return COMPOSITE, {"factor": (c1 - u) // 2 * big_f + 1}
    return PRIME, bases
