# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xoshiro-xoroshiro/. The authors are listed in prov/XXBA1W.jsonl.

MASK64 = (1 << 64) - 1

# Jump polynomials of the reference code: x^(2^128) and x^(2^192) modulo the
# characteristic polynomial for xoshiro256, x^(2^64) and x^(2^96) for xoroshiro128.
JUMP256 = (0x180EC6D33CFD0ABA, 0xD5A61266F0C9392C, 0xA9582618E03FC9AA, 0x39ABDC4529B1661C)
LONG_JUMP256 = (0x76E15D3EFEFDCBBF, 0xC5004E441C522FB3, 0x77710069854EE241, 0x39109BB02ACBE635)
JUMP128 = (0xDF900294D8F554A5, 0x170865DF4B3201FC)
LONG_JUMP128 = (0xD2A98B26625EEE7B, 0xDDDF9B1090AA7AC1)


def rotl(x: int, k: int) -> int:
    """Rotate a 64-bit word left by k places, 0 < k < 64."""
    return ((x << k) | (x >> (64 - k))) & MASK64


def xoshiro256_step(s: list[int]) -> None:
    """The linear engine of xoshiro256 (shift 17, rotation 45), in place."""
    t = (s[1] << 17) & MASK64  # @line L2
    s[2] ^= s[0]  # @line L3
    s[3] ^= s[1]
    s[1] ^= s[2]  # @line L4
    s[0] ^= s[3]
    s[2] ^= t  # @line L5
    s[3] = rotl(s[3], 45)  # @line L6


def xoshiro256ss_next(s: list[int]) -> int:
    """xoshiro256**: return the next output and update the 4-word state s in place.

    The state must not be all zero. Cost: about 11 word operations.
    """
    r = (rotl((s[1] * 5) & MASK64, 7) * 9) & MASK64  # @line L1
    xoshiro256_step(s)
    return r  # @line L7


def xoshiro256pp_next(s: list[int]) -> int:
    """xoshiro256++: the same engine with the scrambler rotl(s0 + s3, 23) + s0."""
    r = (rotl((s[0] + s[3]) & MASK64, 23) + s[0]) & MASK64
    xoshiro256_step(s)
    return r


def xoroshiro128_step(s: list[int]) -> None:
    """The linear engine of xoroshiro128 with (a, b, c) = (24, 16, 37), in place."""
    s0, s1 = s
    s1 ^= s0
    s[0] = rotl(s0, 24) ^ s1 ^ ((s1 << 16) & MASK64)
    s[1] = rotl(s1, 37)


def xoroshiro128p_next(s: list[int]) -> int:
    """xoroshiro128+: output s0 + s1."""
    r = (s[0] + s[1]) & MASK64
    xoroshiro128_step(s)
    return r


def xoroshiro128ss_next(s: list[int]) -> int:
    """xoroshiro128**: output rotl(s0 * 5, 7) * 9."""
    r = (rotl((s[0] * 5) & MASK64, 7) * 9) & MASK64
    xoroshiro128_step(s)
    return r


def jump_by_polynomial(s: list[int], poly: int, step) -> None:
    """Replace s by T^J s, where poly = x^J mod the characteristic polynomial.

    poly is an int whose bit i is the coefficient of x^i. This is Horner's
    rule run from the low coefficient up: accumulate s when the bit is set,
    then step. Cost: deg steps of the engine.
    """
    acc = [0] * len(s)
    deg = 64 * len(s)
    for i in range(deg):
        if (poly >> i) & 1:
            for k in range(len(s)):
                acc[k] ^= s[k]
        step(s)
    s[:] = acc


def words_to_int(words: tuple[int, ...]) -> int:
    """Pack words, the first word lowest, as the reference code stores polynomials."""
    v = 0
    for i, w in enumerate(words):
        v |= w << (64 * i)
    return v


def xoshiro256_jump(s: list[int]) -> None:
    """Advance a xoshiro256 state by 2^128 steps."""
    jump_by_polynomial(s, words_to_int(JUMP256), xoshiro256_step)


def xoshiro256_long_jump(s: list[int]) -> None:
    """Advance a xoshiro256 state by 2^192 steps."""
    jump_by_polynomial(s, words_to_int(LONG_JUMP256), xoshiro256_step)


def xoroshiro128_jump(s: list[int]) -> None:
    """Advance a xoroshiro128 state by 2^64 steps."""
    jump_by_polynomial(s, words_to_int(JUMP128), xoroshiro128_step)


def seed_xoshiro256(seed: int) -> list[int]:
    """Fill the 4-word state with SplitMix64 outputs, as the reference code recommends."""
    x, out = seed & MASK64, []
    for _ in range(4):
        x = (x + 0x9E3779B97F4A7C15) & MASK64
        z = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        out.append(z ^ (z >> 31))
    return out
