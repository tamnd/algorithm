# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-micali/. The authors are listed in prov/01DETK.jsonl.

"""The Blum-Micali generator x_(i+1) = g^(x_i) mod p with the half predicate as output,
and the reduction from a perfect predictor of that predicate to the discrete logarithm."""

from typing import Callable, Dict, List


def prime_factors(n: int) -> List[int]:
    fs, d = [], 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fs.append(n)
    return fs


def is_primitive_root(g: int, p: int) -> bool:
    if not 1 <= g < p:
        return False
    return all(pow(g, (p - 1) // f, p) != 1 for f in prime_factors(p - 1))


def half_predicate(x: int, p: int) -> int:
    """B(x) = 1 if 1 <= x <= (p - 1)/2, else 0, for x in {1, ..., p - 1}."""
    return 1 if x <= (p - 1) // 2 else 0


class BlumMicali:
    def __init__(self, p: int, g: int, seed: int) -> None:
        if p < 5 or p % 2 == 0:
            raise ValueError("p must be an odd prime >= 5")
        if not is_primitive_root(g, p):
            raise ValueError("g must be a primitive root modulo p")
        if not 1 <= seed <= p - 1:
            raise ValueError("the seed must lie in {1, ..., p - 1}")
        self.p, self.g = p, g
        self.x = seed  # @line L1

    def next_bit(self) -> int:
        b = half_predicate(self.x, self.p)  # @line L3
        self.x = pow(self.g, self.x, self.p)  # @line L4
        return b

    def bits(self, k: int) -> List[int]:
        return [self.next_bit() for _ in range(k)]  # @line L2 @line L5


def cycle_lengths(p: int, g: int) -> List[int]:
    """Cycle lengths of the permutation x -> g^x mod p of {1, ..., p - 1}."""
    seen = [False] * p
    out = []
    for s in range(1, p):
        if seen[s]:
            continue
        n, x = 0, s
        while not seen[x]:
            seen[x] = True
            x = pow(g, x, p)
            n += 1
        out.append(n)
    return sorted(out)


def sqrt_mod(a: int, p: int) -> int:
    """A square root of the quadratic residue a modulo the odd prime p (Tonelli-Shanks)."""
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        raise ValueError("a is not a quadratic residue")
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def dlog_with_oracle(y: int, p: int, g: int, oracle: Callable[[int], int]) -> int:
    """Return x in {1, ..., p - 1} with g^x = y mod p, given oracle(z) = B(log_g z) for every z.

    Each round reads one binary digit of the exponent: the Legendre symbol gives its parity,
    and the oracle picks which square root halves the exponent.
    """
    if not 1 <= y < p:
        raise ValueError("y must be a unit modulo p")
    g_inv = pow(g, -1, p)
    e, place = 0, 1
    while y != 1:
        if pow(y, (p - 1) // 2, p) == p - 1:  # odd exponent
            e += place
            y = y * g_inv % p
            if y == 1:
                break
        r = sqrt_mod(y, p)
        if oracle(r) == 0:
            r = p - r  # the other root, r * g^((p-1)/2)
        y = r
        place *= 2
    return e if e != 0 else p - 1


def dlog_table(p: int, g: int) -> Dict[int, int]:
    """log_g z in {1, ..., p - 1} for every unit z, by exhaustive powering."""
    table, z = {}, 1
    for x in range(1, p):
        z = z * g % p
        table[z] = x
    return table
