# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xorshift/. The authors are listed in prov/ZZ9CEX.jsonl.

MASK32 = (1 << 32) - 1
MASK64 = (1 << 64) - 1


def xorshift_next(x: int, a: int, b: int, c: int, w: int) -> int:
    """One step of Marsaglia's xorshift generator on a w-bit word.

    The state x must be non-zero and below 2^w. The step is the linear map
    T = (I + L^a)(I + R^b)(I + L^c) over GF(2)^w, applied right to left as in
    Marsaglia (2003): first the left shift by a, then the right shift by b,
    then the left shift by c. Every left shift is masked to w bits.
    The returned word is both the new state and the output.
    Cost: 3 shifts, 3 XORs and 2 masks.
    """
    mask = (1 << w) - 1
    x ^= (x << a) & mask  # @line L1
    x ^= x >> b  # @line L2
    x ^= (x << c) & mask  # @line L3
    return x  # @line L4


def xorshift32_next(x: int) -> int:
    """Marsaglia's xor32 with the triple (13, 17, 5); period 2^32 - 1."""
    return xorshift_next(x, 13, 17, 5, 32)


def xorshift64_next(x: int) -> int:
    """Marsaglia's xor64 with the triple (13, 7, 17); period 2^64 - 1."""
    return xorshift_next(x, 13, 7, 17, 64)


def xorshift_stream(seed: int, n: int, a: int = 13, b: int = 17, c: int = 5, w: int = 32) -> list[int]:
    """Return the next n outputs from a non-zero w-bit seed."""
    x = seed & ((1 << w) - 1)
    if x == 0:
        raise ValueError("the seed must be non-zero modulo 2^w")
    out: list[int] = []
    for _ in range(n):
        x = xorshift_next(x, a, b, c, w)
        out.append(x)
    return out


def xorshift128_next(state: tuple[int, int, int, int]) -> tuple[tuple[int, int, int, int], int]:
    """Marsaglia's xor128 on four 32-bit words; period 2^128 - 1.

    Returns the new state and the output, which is the new last word.
    """
    x, y, z, w = state
    t = (x ^ (x << 11)) & MASK32
    w_new = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return (y, z, w, w_new), w_new


def xorshift64star_next(x: int) -> tuple[int, int]:
    """Vigna's xorshift64* (shifts 12, 25, 27, then a multiplication).

    Returns the new state and the output. The state step is a plain xorshift
    with the shifts right 12, left 25, right 27; only the output is scrambled.
    """
    x ^= x >> 12
    x ^= (x << 25) & MASK64
    x ^= x >> 27
    return x, (x * 2685821657736338717) & MASK64
