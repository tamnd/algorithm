# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/park-miller-minimal-standard/. The authors are listed in prov/HR4MZ7.jsonl.

M = 2**31 - 1  # the modulus, a Mersenne prime
A = 16807  # the multiplier 7^5 of Park and Miller (1988)


def park_miller_seed(seed: int, m: int = M) -> int:
    """Return the start state for a seed. The state 0 is forbidden, so a multiple of m is rejected."""
    x = seed % m
    if x == 0:
        raise ValueError("the seed must not be a multiple of the modulus")
    return x


def park_miller_next(x: int, a: int = A, m: int = M) -> int:
    """Return (a * x) mod m by Schrage's method.

    Precondition: 1 <= x <= m - 1 and (m mod a) <= (m div a), which holds for
    a = 16807 and a = 48271 with m = 2^31 - 1. Every intermediate value lies in
    (-m, m), so it fits in a signed 32-bit word. Cost: O(1) word operations.
    """
    q, r = m // a, m % a  # @line L1
    t = a * (x % q) - r * (x // q)  # @line L2
    if t < 0:  # @line L3
        t += m
    return t  # @line L4


def park_miller_uniform(x: int, m: int = M) -> float:
    """Map a state in [1, m - 1] to a float in the open interval (0, 1)."""
    return x / m


def park_miller_stream(seed: int, n: int, a: int = A, m: int = M) -> list[int]:
    """Return the next n states after the seed."""
    x = park_miller_seed(seed, m)
    out: list[int] = []
    for _ in range(n):
        x = park_miller_next(x, a, m)
        out.append(x)
    return out
