# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-congruential-generator/. The authors are listed in prov/GFMHDY.jsonl.

"""Linear congruential generator s_(i+1) = (a s_i + c) mod m, with exact integer arithmetic."""


def _is_power_of_two(m: int) -> bool:
    return m > 0 and m & (m - 1) == 0


class LinearCongruentialGenerator:
    """The generator with modulus m, multiplier a and increment c.

    next() returns the new state, an integer in [0, m). When m is a power of
    two the reduction is a mask, as in a w-bit machine word.
    """

    def __init__(self, m: int, a: int, c: int, seed: int) -> None:
        if m < 2 or not 0 < a < m or not 0 <= c < m:
            raise ValueError("need m >= 2, 0 < a < m and 0 <= c < m")
        self.m, self.a, self.c = m, a, c
        self.mask = m - 1 if _is_power_of_two(m) else None
        s = seed % m  # @line L1
        if c == 0 and s == 0:  # @line L2
            raise ValueError("seed 0 is a fixed point when c = 0")
        self.state = s

    def next(self) -> int:
        t = self.a * self.state + self.c  # @line L3
        self.state = t & self.mask if self.mask is not None else t % self.m
        return self.state  # @line L4

    def uniform(self) -> float:
        """A value in [0, 1). For m = 2^w with w > 53 the top 53 bits are used,
        because x / 2^w can round up to 1.0 in floating point."""
        x = self.next()  # @line L5
        w = self.m.bit_length() - 1
        if self.mask is not None and w > 53:
            return (x >> (w - 53)) * 2.0**-53
        return x / self.m


def schrage_mulmod(a: int, x: int, m: int) -> int:
    """a * x mod m with every intermediate value in (-m, m).

    Needs 0 <= x < m and r < q, where q = m // a and r = m % a.
    """
    q, r = divmod(m, a)
    if r >= q:
        raise ValueError("Schrage's method needs m mod a < m div a")
    t = a * (x % q) - r * (x // q)  # @line L6
    if t < 0:  # @line L7
        t += m
    return t  # @line L8


def minstd(seed: int, a: int = 16807) -> LinearCongruentialGenerator:
    """Park and Miller's minimal standard generator, m = 2^31 - 1."""
    return LinearCongruentialGenerator(2**31 - 1, a, 0, seed)


def prime_factors(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def hull_dobell(m: int, a: int, c: int) -> bool:
    """True when the Hull-Dobell conditions for period m hold."""
    from math import gcd

    b = a - 1
    return (
        gcd(c, m) == 1
        and all(b % p == 0 for p in prime_factors(m))
        and (m % 4 != 0 or b % 4 == 0)
    )


def period(m: int, a: int, c: int, seed: int) -> int:
    """The period rho of the state sequence from seed, by brute force (small m only)."""
    seen: dict[int, int] = {}
    s, i = seed % m, 0
    while s not in seen:
        seen[s] = i
        s = (a * s + c) % m
        i += 1
    return i - seen[s]
