# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-blum-shub/. The authors are listed in prov/QDNJTG.jsonl.

"""Blum Blum Shub: x_(i+1) = x_i^2 mod n for a Blum integer n = p q, output the low bits of x_i."""

import math
import random
from typing import List, Optional, Tuple

_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n: int) -> bool:
    """Miller-Rabin with the first 12 prime bases, deterministic for n < 3.3 * 10^24."""
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_blum_prime(p: int) -> bool:
    return p % 4 == 3 and is_prime(p)


def random_blum_prime(bits: int, rng: random.Random) -> int:
    if bits < 3:
        raise ValueError("need at least 3 binary digits")
    while True:
        p = rng.getrandbits(bits) | (1 << (bits - 1)) | 3
        if is_blum_prime(p):
            return p


class BBS:
    """The Blum Blum Shub generator with modulus n = p q and j output bits per squaring."""

    def __init__(self, n: int, seed: int, j: int = 1) -> None:
        if n < 21 or n % 2 == 0:
            raise ValueError("n must be an odd Blum integer")
        if math.gcd(seed, n) != 1:
            raise ValueError("the seed must be coprime to n")
        if j < 1:
            raise ValueError("need j >= 1 output bits per step")
        self.n = n
        self.j = j
        self.x = seed * seed % n  # x_0 = s^2 mod n, a quadratic residue  # @line L1

    def next_word(self) -> int:
        self.x = self.x * self.x % self.n  # @line L3
        return self.x & ((1 << self.j) - 1)  # @line L4

    def bits(self, k: int) -> List[int]:
        out: List[int] = []
        while len(out) < k:  # @line L2
            v = self.next_word()
            for t in range(self.j):
                out.append((v >> t) & 1)
        return out[:k]  # @line L5


def states(n: int, x0: int, k: int) -> List[int]:
    """x_0, x_1, ..., x_k with x_(i+1) = x_i^2 mod n."""
    xs = [x0 % n]
    for _ in range(k):
        xs.append(xs[-1] * xs[-1] % n)
    return xs


def carmichael_lambda_pq(p: int, q: int) -> int:
    return (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)


def carmichael_lambda(m: int) -> int:
    """Carmichael's function by trial factorization (small m only)."""
    if m == 1:
        return 1
    result, d, n = 1, 2, m
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            if d == 2:
                lam = 1 if e == 1 else 2 if e == 2 else 2 ** (e - 2)
            else:
                lam = (d - 1) * d ** (e - 1)
            result = result * lam // math.gcd(result, lam)
        d += 1
    if n > 1:
        result = result * (n - 1) // math.gcd(result, n - 1)
    return result


def multiplicative_order(a: int, m: int) -> int:
    if m == 1:
        return 1
    if math.gcd(a, m) != 1:
        raise ValueError("a must be coprime to m")
    k, x = 1, a % m
    while x != 1:
        x = x * a % m
        k += 1
    return k


def predicted_period(p: int, q: int, x0: int) -> int:
    """Period of x_0, x_1, ... for a quadratic residue x0: ord_t(2) with t = ord_n(x0)."""
    t = multiplicative_order(x0, p * q)
    return multiplicative_order(2, t)


def brute_period(n: int, x0: int) -> int:
    """Least i >= 1 with x_i = x_0 (the sequence from a quadratic residue is purely periodic)."""
    x, i = x0 * x0 % n, 1
    while x != x0:
        x = x * x % n
        i += 1
    return i


def direct_state(p: int, q: int, x0: int, i: int) -> int:
    """x_i = x_0^(2^i mod lambda(n)) mod n, computed from the factorization."""
    lam = carmichael_lambda_pq(p, q)
    return pow(x0, pow(2, i, lam), p * q)


def previous_state(p: int, q: int, x: int) -> int:
    """The unique quadratic residue y with y^2 = x mod n, for x a quadratic residue (needs the factors)."""
    n = p * q
    rp = pow(x, (p + 1) // 4, p)  # the square root mod p that is itself a residue mod p
    rq = pow(x, (q + 1) // 4, q)
    return (rp * q * pow(q, -1, p) + rq * p * pow(p, -1, q)) % n


def quadratic_residues(n: int) -> List[int]:
    return sorted({x * x % n for x in range(1, n) if math.gcd(x, n) == 1})
