# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-kangaroo/. The authors are listed in prov/VXD7T2.jsonl.

import random
from math import isqrt


def _bsgs(g: int, h: int, n: int, p: int) -> int | None:
    """Least x in [0, n) with g^x = h (mod p), or None; O(n^(1/2)) steps."""
    m = isqrt(max(n - 1, 0)) + 1
    table: dict[int, int] = {}
    e = 1 % p
    for j in range(m):
        if e not in table:
            table[e] = j
        e = e * g % p
    u = pow(g, -m, p)
    gamma = h
    for i in range(m):
        if gamma in table:
            x = i * m + table[gamma]
            return x if x < n else None
        gamma = gamma * u % p
    return None


def pollard_kangaroo(g: int, h: int, a: int, b: int, p: int, seed: int = 0, attempts: int = 3) -> int | None:
    """Pollard's kangaroo method with distinguished points, modulo p.

    Return some x in [a, b] with g^x = h (mod p), or None if there is none.
    The group is the cyclic subgroup <g> of (Z/pZ)^*.
    Precondition: p >= 2, gcd(g, p) = 1 and 0 <= a <= b. Raises ValueError
    otherwise.
    Cost: heuristically about 2 w^(1/2) + 2/theta multiplications modulo p
    per attempt, with w = b - a, jumps 2^j of mean about w^(1/2)/2 and a
    table of O(theta w^(1/2)) distinguished points. A kangaroo run cannot
    prove that no solution exists, so after `attempts` failed runs the
    answer is certified by baby-step giant-step on the interval, at a cost
    of O(w^(1/2)) steps and memory.
    """
    if p < 2 or a < 0 or b < a:
        raise ValueError("need p >= 2 and 0 <= a <= b")
    g %= p
    h %= p
    w = b - a  # @line L1
    target = h * pow(g, -a, p) % p
    half = isqrt(w)
    k = 1  # @line L2
    while (2**k - 1) < k * max(1, half // 2):
        k += 1
    jumps = [pow(g, 2**j, p) for j in range(k)]
    spacing = max(1, half // 8)
    budget = 4 * half + 4 * spacing + 16
    rng = random.Random(seed)
    key = 1
    for _ in range(attempts):  # @line L3
        tame, d_tame = pow(g, w // 2, p), w // 2  # @line L4
        wild, d_wild = target, 0
        traps: dict[int, tuple[int, int]] = {}  # @line L5
        for _ in range(budget):  # @line L6
            for kind in (0, 1):  # @line L7
                y, d = (tame, d_tame) if kind == 0 else (wild, d_wild)
                v = y * key % p
                if (v // k) % spacing == 0:  # @line L8
                    other = traps.get(y)
                    if other is not None and other[0] != kind:  # @line L9
                        t_dist, w_dist = (d, other[1]) if kind == 0 else (other[1], d)
                        z = t_dist - w_dist  # @line L10
                        if 0 <= z <= w and pow(g, z, p) == target:  # @line L11
                            return a + z
                    traps[y] = (kind, d)  # @line L12
                j = v % k  # @line L13
                if kind == 0:
                    tame, d_tame = tame * jumps[j] % p, d_tame + 2**j
                else:
                    wild, d_wild = wild * jumps[j] % p, d_wild + 2**j
        key = rng.randrange(1, p) if p > 2 else 1  # @line L14
    x = _bsgs(g, target, w + 1, p)  # @line L15
    return None if x is None else a + x
