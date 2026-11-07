# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kulisch-accumulator/. The authors are listed in prov/CV0X1C.jsonl.

"""A Kulisch long accumulator for binary64 sums and dot products.

The register holds an integer V in two's complement over LIMBS 64-bit limbs,
and represents V * 2^-OFFSET. OFFSET = 2148 covers the smallest product of two
subnormals (2^-1074 * 2^-1074); the top covers products below 2^2048, plus
91 guard bits so that up to 2^91 products of any size cannot overflow. Every addition is
exact; rounding happens once, in round().
"""

import math

LIMB = 64
LIMBS = 67  # 4288 bits
OFFSET = 2148
MASK = (1 << LIMB) - 1
WIDTH = LIMB * LIMBS


def decompose(x: float) -> tuple[int, int]:
    """Return (m, e) with x = m * 2^e exactly, m a signed integer of at most 53 bits."""
    if x == 0.0:
        return 0, 0
    f, e = math.frexp(x)  # x = f * 2^e, 0.5 <= |f| < 1
    m = int(f * 2**53)
    return m, e - 53


class KulischAccumulator:
    def __init__(self) -> None:
        self.limbs = [0] * LIMBS
        self.nan = False
        self.pos_inf = False
        self.neg_inf = False

    def _special(self, v: float) -> bool:
        if math.isnan(v):
            self.nan = True
        elif math.isinf(v):
            if v > 0:
                self.pos_inf = True
            else:
                self.neg_inf = True
        else:
            return False
        return True

    def add_product(self, a: float, b: float) -> None:
        """R <- R + a*b, exactly."""
        if not (math.isfinite(a) and math.isfinite(b)):
            self._special(a * b)  # IEEE semantics: inf * 0 is NaN
            return
        ma, ea = decompose(a)
        mb, eb = decompose(b)
        m, e = ma * mb, ea + eb  # @line L1
        if m == 0:
            return
        s = e + OFFSET  # @line L2
        i, chunk = s // LIMB, abs(m) << (s % LIMB)  # @line L3
        limbs = self.limbs
        if m > 0:
            carry = 0
            while chunk or carry:  # @line L4
                if i >= LIMBS:
                    break  # wraps modulo 2^WIDTH (only after about 2^91 additions)
                t = limbs[i] + (chunk & MASK) + carry  # @line L5
                limbs[i], carry = t & MASK, t >> LIMB
                chunk >>= LIMB
                i += 1
        else:
            borrow = 0
            while chunk or borrow:  # @line L4
                if i >= LIMBS:
                    break
                t = limbs[i] - (chunk & MASK) - borrow  # @line L5
                limbs[i], borrow = t & MASK, 1 if t < 0 else 0
                chunk >>= LIMB
                i += 1

    def add(self, x: float) -> None:
        """R <- R + x, exactly."""
        self.add_product(x, 1.0)

    def value(self) -> int:
        """The signed integer V; the exact value is V * 2^-OFFSET."""
        v = 0
        for limb in reversed(self.limbs):
            v = (v << LIMB) | limb
        return v - (1 << WIDTH) if v >> (WIDTH - 1) else v

    def round(self) -> float:
        """The exact contents rounded to nearest binary64, ties to even."""
        if self.nan or (self.pos_inf and self.neg_inf):
            return math.nan
        if self.pos_inf or self.neg_inf:
            return math.inf if self.pos_inf else -math.inf
        v = self.value()  # @line L6
        if v == 0:
            return 0.0
        sign, a = (-1 if v < 0 else 1), abs(v)
        k = a.bit_length()  # @line L7
        # exponent of the leading bit is k - 1 - OFFSET; keep 53 bits, but not below 2^-1074
        drop = max(k - 53, OFFSET - 1074)
        if drop <= 0:
            return sign * math.ldexp(a, -OFFSET)
        q, r = a >> drop, a & ((1 << drop) - 1)
        half = 1 << (drop - 1)
        if r > half or (r == half and q & 1):  # @line L8
            q += 1
        e = drop - OFFSET
        if q.bit_length() + e > 1024:
            return sign * math.inf
        return sign * math.ldexp(q, e)  # @line L9


def exact_sum(xs) -> float:
    acc = KulischAccumulator()
    for x in xs:
        acc.add(x)
    return acc.round()


def exact_dot(xs, ys) -> float:
    acc = KulischAccumulator()
    for x, y in zip(xs, ys):
        acc.add_product(x, y)
    return acc.round()
