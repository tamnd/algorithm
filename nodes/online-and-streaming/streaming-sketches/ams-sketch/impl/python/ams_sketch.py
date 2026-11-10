# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ams-sketch/. The authors are listed in prov/ATY7TN.jsonl.

import math
import random

# GF(2^64) with the reduction polynomial x^64 + x^4 + x^3 + x + 1.
GF64 = (64, (1 << 64) | 0b11011)


def gf_mul(a: int, b: int, field: tuple[int, int] = GF64) -> int:
    """Carry-less product of a and b reduced modulo the field polynomial."""
    bits, mod = field
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a >> bits:
            a ^= mod
    return r


def low_bit_mask(a: int, field: tuple[int, int] = GF64) -> int:
    """The mask L with bit0(a * y) = parity(L & y) for every field element y.

    bit0(a * y) is linear in the bits of y, and bit k of L is bit0(a * x^k).
    """
    bits, mod = field
    mask, v = 0, a
    for k in range(bits):
        mask |= (v & 1) << k
        v <<= 1
        if v >> bits:
            v ^= mod
    return mask


class FourWiseSign:
    """s(x) = (-1)^bit0(a3 x^3 + a2 x^2 + a1 x + a0) over GF(2^bits).

    The values of a random polynomial of degree at most 3 at four distinct
    points are independent and uniform, so the signs are 4-wise independent
    and fair. Each sign costs three AND-and-parity steps, given x^2 and x^3.
    """

    def __init__(self, coeffs: tuple[int, int, int, int], field: tuple[int, int] = GF64) -> None:
        a0, a1, a2, a3 = coeffs
        self.coeffs, self.field = coeffs, field
        self.b0 = a0 & 1
        self.m1, self.m2, self.m3 = (low_bit_mask(a, field) for a in (a1, a2, a3))

    @classmethod
    def random(cls, rng: random.Random, field: tuple[int, int] = GF64) -> "FourWiseSign":
        return cls(tuple(rng.getrandbits(field[0]) for _ in range(4)), field)

    def sign_from_powers(self, x1: int, x2: int, x3: int) -> int:
        bit = self.b0 ^ ((self.m1 & x1).bit_count() + (self.m2 & x2).bit_count() + (self.m3 & x3).bit_count()) & 1
        return -1 if bit else 1

    def __call__(self, x: int) -> int:
        x2 = gf_mul(x, x, self.field)
        return self.sign_from_powers(x, x2, gf_mul(x2, x, self.field))

    def direct(self, x: int) -> int:
        """The same sign by Horner's rule, for checking."""
        v = 0
        for a in reversed(self.coeffs):
            v = gf_mul(v, x, self.field) ^ a
        return -1 if v & 1 else 1


class AMSSketch:
    """The tug-of-war sketch of Alon, Matias and Szegedy for F_2 = sum of f_x^2.

    r groups of t counters Z = sum_x s(x) f_x, each with its own 4-wise
    independent sign. Each Z^2 is an unbiased estimate of F_2 with variance at
    most 2 F_2^2. The estimate is the median over the groups of the mean of Z^2
    in the group. With t = ceil(6/eps^2) and r = ceil(18 ln(1/delta)), it is
    within a factor 1 +- eps of F_2 with probability at least 1 - delta.
    """

    def __init__(self, t: int, r: int, rng: random.Random, field: tuple[int, int] = GF64) -> None:
        if t < 1 or r < 1:
            raise ValueError("t and r must be at least 1")
        self.t, self.r, self.field = t, r, field
        self.signs = [[FourWiseSign.random(rng, field) for _ in range(t)] for _ in range(r)]
        self.z = [[0] * t for _ in range(r)]

    @classmethod
    def from_error(cls, eps: float, delta: float, rng: random.Random) -> "AMSSketch":
        if not (0 < eps and 0 < delta < 1):
            raise ValueError("need eps > 0 and 0 < delta < 1")
        return cls(math.ceil(6 / eps**2), math.ceil(18 * math.log(1 / delta)), rng)

    def empty_like(self) -> "AMSSketch":
        out = AMSSketch.__new__(AMSSketch)
        out.t, out.r, out.field, out.signs = self.t, self.r, self.field, self.signs
        out.z = [[0] * self.t for _ in range(self.r)]
        return out

    def update(self, x: int, c: int = 1) -> None:
        """Add c to f_x; c may be negative."""
        if not 0 <= x < (1 << self.field[0]):
            raise ValueError("items must be field elements")
        x2 = gf_mul(x, x, self.field)
        x3 = gf_mul(x2, x, self.field)
        for g in range(self.r):  # @line L1
            zg, sg = self.z[g], self.signs[g]
            for i in range(self.t):  # @line L1
                zg[i] += sg[i].sign_from_powers(x, x2, x3) * c  # @line L2

    def group_means(self) -> list[float]:
        return [sum(v * v for v in zg) / self.t for zg in self.z]  # @line L3

    def estimate(self) -> float:
        """The lower median of the group means."""
        y = sorted(self.group_means())
        return y[(self.r + 1) // 2 - 1]  # @line L4

    def merge(self, other: "AMSSketch") -> "AMSSketch":
        """The sketch of f + g; the signs must be shared."""
        if other.signs is not self.signs:
            raise ValueError("the sketches must share the sign functions")
        out = self.empty_like()
        out.z = [[u + v for u, v in zip(a, b)] for a, b in zip(self.z, other.z)]  # @line L5
        return out

    def subtract(self, other: "AMSSketch") -> "AMSSketch":
        """The sketch of f - g; its estimate approximates ||f - g||_2^2."""
        if other.signs is not self.signs:
            raise ValueError("the sketches must share the sign functions")
        out = self.empty_like()
        out.z = [[u - v for u, v in zip(a, b)] for a, b in zip(self.z, other.z)]
        return out
