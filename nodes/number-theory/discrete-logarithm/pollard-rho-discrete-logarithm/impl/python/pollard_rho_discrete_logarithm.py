# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-rho-discrete-logarithm/. The authors are listed in prov/8WE1PE.jsonl.

import random
from math import gcd, isqrt


def _step(x: int, a: int, b: int, g: int, h: int, n: int, p: int, key: int) -> tuple[int, int, int]:
    """One step of Pollard's walk; the invariant x = g^a h^b is kept."""
    s = x * key % p % 3
    if s == 1:  # @line L17
        return x * h % p, a, (b + 1) % n
    if s == 0:  # @line L18
        return x * x % p, 2 * a % n, 2 * b % n
    return x * g % p, (a + 1) % n, b  # @line L19


def pollard_rho_log(g: int, h: int, n: int, p: int, seed: int = 0) -> int | None:
    """Pollard's rho method for discrete logarithms modulo a prime p.

    Return the x in [0, n) with g^x = h (mod p), or None if h is not a power
    of g. The group is the cyclic subgroup <g> of (Z/pZ)^*.
    Precondition: p is prime, gcd(g, p) = 1 and n = ord(g) exactly.
    Raises ValueError if p < 2 or n < 1.
    Cost: heuristically about 3 * 1.03 * (pi n / 2)^(1/2) multiplications
    modulo p per attempt (Floyd's cycle finding), O(1) stored residues; the
    first attempt is Pollard's walk from x0 = 1 and later attempts use a
    random start and a random partition. The number of attempts is small in
    expectation but not bounded in the worst case.
    """
    if p < 2 or n < 1:
        raise ValueError("need p >= 2 and n >= 1")
    g %= p
    h %= p
    if pow(h, n, p) != 1:  # @line L1
        return None
    if h == 1:  # @line L2
        return 0
    rng = random.Random(seed)
    a0, b0, key = 0, 0, 1  # @line L3
    while True:  # @line L4
        x = pow(g, a0, p) * pow(h, b0, p) % p  # @line L5
        a, b = a0, b0
        big_x, big_a, big_b = x, a, b  # @line L6
        while True:  # @line L7
            x, a, b = _step(x, a, b, g, h, n, p, key)  # @line L8
            big_x, big_a, big_b = _step(big_x, big_a, big_b, g, h, n, p, key)  # @line L9
            big_x, big_a, big_b = _step(big_x, big_a, big_b, g, h, n, p, key)
            if x == big_x:  # @line L10
                break
        s = (b - big_b) % n  # @line L11
        d = gcd(s, n)
        if s != 0 and d <= isqrt(n) + 1:  # @line L12
            m = n // d
            y = (big_a - a) // d * pow(s // d, -1, m) % m  # @line L13
            for k in range(d):  # @line L14
                if pow(g, y + k * m, p) == h:  # @line L15
                    return y + k * m
        a0, b0, key = rng.randrange(n), rng.randrange(n), rng.randrange(1, p)  # @line L16
