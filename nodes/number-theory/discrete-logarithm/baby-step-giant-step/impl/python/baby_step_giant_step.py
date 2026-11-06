# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baby-step-giant-step/. The authors are listed in prov/KW87TP.jsonl.

from math import isqrt


def baby_step_giant_step(g: int, h: int, n: int, p: int) -> int | None:
    """Shanks' baby-step giant-step in the group of units modulo p.

    Return the least x >= 0 with g^x = h (mod p), or None if h is not a power
    of g. The group is (Z/pZ)^*; p need not be prime.
    Precondition: p >= 2, gcd(g, p) = 1, n >= 1 and n >= ord(g) (for example
    n = p - 1 for a prime p). Raises ValueError if p < 2 or n < 1.
    Cost: at most 2m + O(log m) multiplications modulo p and m hash table
    insertions and lookups, where m = ceil(n^(1/2)); m stored residues.
    """
    if p < 2 or n < 1:
        raise ValueError("need p >= 2 and n >= 1")
    g %= p
    h %= p
    m = isqrt(n - 1) + 1  # @line L1
    table: dict[int, int] = {}  # @line L2
    e = 1 % p  # @line L3
    for j in range(m):  # @line L4
        if e not in table:  # @line L5
            table[e] = j
        e = e * g % p  # @line L6
    u = pow(g, -m, p)  # @line L7
    gamma = h  # @line L8
    for i in range(m):  # @line L9
        if gamma in table:  # @line L10
            return i * m + table[gamma]
        gamma = gamma * u % p  # @line L11
    return None  # @line L12
