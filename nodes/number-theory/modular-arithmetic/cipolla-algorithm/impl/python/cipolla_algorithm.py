# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cipolla-algorithm/. The authors are listed in prov/W39G65.jsonl.

"""Cipolla's algorithm: a square root modulo an odd prime p.

For a quadratic residue n modulo p, choose a at random until d = a^2 - n is a
quadratic nonresidue. In the field F_p(w) with w^2 = d, the element
(a + w)^((p+1)/2) lies in F_p and is a square root of n. Elements x + y w are
stored as pairs (x, y) of residues in [0, p).

The modulus must be prime. The function does not test primality, but it never
returns a wrong root: for a composite modulus it raises ValueError when it
notices, or returns None, or returns a value whose square is n.
"""

import random
from typing import Optional

MAX_TRIALS = 200  # for a prime p, all trials fail with probability below 10^(-35)


def power_mod(base: int, exponent: int, p: int) -> int:
    """base^exponent mod p by binary exponentiation with a loop."""
    result = 1 % p
    base %= p
    while exponent > 0:
        if exponent & 1:
            result = result * base % p
        base = base * base % p
        exponent >>= 1
    return result


def cipolla_sqrt(n: int, p: int, rng: Optional[random.Random] = None) -> Optional[int]:
    """Return x in [0, p) with x^2 = n (mod p), or None if n is not a square."""
    if p < 2:
        raise ValueError("the modulus must be a prime")
    if p == 2:
        return n % 2  # every residue modulo 2 is its own square root
    if rng is None:
        rng = random.Random()
    n %= p  # @line L1
    if n == 0:
        return 0
    euler = power_mod(n, (p - 1) // 2, p)  # @line L2
    if euler == p - 1:
        return None  # Euler's criterion: n is a nonresidue
    if euler != 1:
        raise ValueError("the modulus is not prime")
    for _ in range(MAX_TRIALS):
        a = rng.randrange(p)  # @line L3
        d = (a * a - n) % p
        if power_mod(d, (p - 1) // 2, p) == p - 1:  # @line L4
            break
    else:
        raise ValueError("no nonresidue found; the modulus is probably not prime")
    x, y = 1, 0  # @line L5
    b, c = a, 1
    e = (p + 1) // 2  # @line L6
    while e > 0:  # @line L7
        if e & 1:  # @line L8
            x, y = (x * b + y * c % p * d) % p, (x * c + y * b) % p
        b, c = (b * b + c * c % p * d) % p, 2 * b * c % p  # @line L9
        e >>= 1  # @line L10
    if y != 0 or x * x % p != n:
        raise ValueError("the modulus is not prime")
    return x  # @line L11
