# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranlux/. The authors are listed in prov/WG0HW1.jsonl.


class SubtractWithBorrow:
    """Marsaglia-Zaman subtract-with-borrow: x_n = (x_(n-s) - x_(n-r) - c) mod 2^w, as std::subtract_with_carry_engine."""

    def __init__(self, w: int, s: int, r: int, seed: int = 19780503) -> None:
        if not 0 < s < r:
            raise ValueError("need 0 < s < r")
        self.w, self.s, self.r = w, s, r
        self.b = 1 << w
        # The C++ seeding: an LCG with multiplier 40014 and modulus 2147483563 gives
        # ceil(w / 32) values per word, combined little-endian and reduced mod 2^w.
        z = seed % 2147483563 or 19780503
        n = (w + 31) // 32
        buf = []
        for _ in range(r):
            v = 0
            for j in range(n):
                z = 40014 * z % 2147483563
                v |= z << (32 * j)
            buf.append(v & (self.b - 1))
        self.x = buf  # circular buffer, x[i] is the oldest value x_(n-r)
        self.i = 0
        self.c = 1 if buf[-1] == 0 else 0

    def step(self) -> int:
        r, s, i = self.r, self.s, self.i
        d = self.x[(i + r - s) % r] - self.x[i] - self.c  # @line L6
        if d < 0:  # @line L7
            d, self.c = d + self.b, 1
        else:
            self.c = 0
        self.x[i] = d  # the new value overwrites the oldest one
        self.i = (i + 1) % r
        return d  # @line L8


class Ranlux:
    """Luescher's RANLUX: use q consecutive values of the SWB, then discard p - q of them."""

    def __init__(self, base: SubtractWithBorrow, p: int, q: int) -> None:
        if not 0 < q <= p:
            raise ValueError("need 0 < q <= p")
        self.base, self.p, self.q, self.k = base, p, q, 0

    def next(self) -> int:
        if self.k == self.q:  # @line L1
            for _ in range(self.p - self.q):  # @line L2
                self.base.step()
            self.k = 0  # @line L3
        self.k += 1  # @line L4
        return self.base.step()  # @line L5


def ranlux24_base(seed: int = 19780503) -> SubtractWithBorrow:
    return SubtractWithBorrow(24, 10, 24, seed)


def ranlux48_base(seed: int = 19780503) -> SubtractWithBorrow:
    return SubtractWithBorrow(48, 5, 12, seed)


def ranlux24(seed: int = 19780503) -> Ranlux:
    """std::ranlux24: blocks of 223, of which 23 are used (Luescher's luxury level 3 is p = 223)."""
    return Ranlux(ranlux24_base(seed), 223, 23)


def ranlux48(seed: int = 19780503) -> Ranlux:
    """std::ranlux48: blocks of 389, of which 11 are used."""
    return Ranlux(ranlux48_base(seed), 389, 11)


def to_uniform(v: int, w: int = 24) -> float:
    """Map a w-bit output to (0, 1)-style float v / 2^w in [0, 1)."""
    return v / (1 << w)
