# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiply-with-carry/. The authors are listed in prov/D46KH3.jsonl.

B32 = 1 << 32
MASK32 = B32 - 1
A64 = 4294957665  # a * 2^32 - 1 is a safe prime: period (a * 2^32 - 2) / 2, about 2^63


def mwc_next(x: int, c: int, a: int, b: int) -> tuple[int, int]:
    """One step of the lag-1 multiply-with-carry generator in base b.

    Requires 0 <= x < b and 0 <= c < a. Returns the new (x, c); the output is the new x.
    """
    t = a * x + c  # @line L1
    x = t % b  # @line L2
    c = t // b  # @line L3
    return x, c  # @line L4


def mwc_stream(n: int, x: int, c: int, a: int, b: int) -> list[int]:
    out = []
    for _ in range(n):
        x, c = mwc_next(x, c, a, b)
        out.append(x)
    return out


def mwc64_next(s: int, a: int = A64) -> int:
    """The usual 64-bit form: the state word holds c in the high half and x in the low half."""
    return (a * (s & MASK32) + (s >> 32)) & ((1 << 64) - 1)


def to_lcg(x: int, c: int, a: int) -> int:
    """The equivalent LCG state z = a x + c, which evolves as z <- a z mod (a b - 1)."""
    return a * x + c


def from_lcg(z: int, a: int) -> tuple[int, int]:
    """Inverse of to_lcg: x = floor(z / a), c = z mod a."""
    return z // a, z % a


def mwc_jump(x: int, c: int, a: int, b: int, k: int) -> tuple[int, int]:
    """The state k steps ahead, in O(log k) multiplications modulo m = a b - 1."""
    m = a * b - 1
    z = to_lcg(x, c, a)
    if z in (0, m):  # the two fixed points
        return x, c
    return from_lcg(pow(a, k, m) * z % m, a)


def mwc_lag_next(xs: tuple[int, ...], c: int, a: int, b: int) -> tuple[tuple[int, ...], int]:
    """Lag-r MWC: x_n = (a x_(n-r) + c_(n-1)) mod b, c_n = floor((a x_(n-r) + c_(n-1)) / b).

    xs holds x_(n-r), ..., x_(n-1), oldest first. The period divides the order of b modulo a b^r - 1.
    """
    t = a * xs[0] + c
    return xs[1:] + (t % b,), t // b


def kiss99_mwc_pair(z: int, w: int) -> tuple[int, int, int]:
    """The two 16-bit MWC components of Marsaglia's 1999 KISS, and their combination."""
    z = 36969 * (z & 0xFFFF) + (z >> 16)
    w = 18000 * (w & 0xFFFF) + (w >> 16)
    return z, w, ((z << 16) + w) & MASK32
