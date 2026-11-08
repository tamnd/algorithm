# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcg-random/. The authors are listed in prov/0VZS5V.jsonl.

MASK32 = (1 << 32) - 1
MASK64 = (1 << 64) - 1
MULT = 6364136223846793005  # the 64-bit LCG multiplier of pcg32, congruent to 5 mod 8


def rotr32(x: int, r: int) -> int:
    """Rotate a 32-bit word right by r places, 0 <= r < 32."""
    return ((x >> r) | (x << ((-r) & 31))) & MASK32


def pcg32_next(state: int, inc: int) -> tuple[int, int]:
    """pcg32 (XSH RR 64/32): return (new state, 32-bit output).

    inc must be odd. The LCG step uses the old state's successor; the output
    is a function of the old state only. Cost: one 64-bit multiply-add,
    two shifts, one XOR and one rotation.
    """
    old = state  # @line L1
    state = (old * MULT + inc) & MASK64  # @line L2
    x = (((old >> 18) ^ old) >> 27) & MASK32  # @line L3
    r = old >> 59  # @line L4
    return state, rotr32(x, r)  # @line L5


def pcg32_seed(initstate: int, initseq: int) -> tuple[int, int]:
    """The seeding of pcg32_srandom_r: return (state, inc) for a seed and a stream number."""
    inc = ((initseq << 1) | 1) & MASK64
    state, _ = pcg32_next(0, inc)
    state = (state + initstate) & MASK64
    state, _ = pcg32_next(state, inc)
    return state, inc


def pcg32_stream(initstate: int, initseq: int, n: int) -> list[int]:
    """The first n outputs for a seed and a stream number."""
    state, inc = pcg32_seed(initstate, initseq)
    out: list[int] = []
    for _ in range(n):
        state, v = pcg32_next(state, inc)
        out.append(v)
    return out


def pcg32_bounded(state: int, inc: int, bound: int) -> tuple[int, int]:
    """pcg32_boundedrand_r: an unbiased value in [0, bound) by rejection."""
    if not 1 <= bound <= MASK32:
        raise ValueError("bound must be in [1, 2^32 - 1]")
    threshold = (-bound) % bound  # (2^32 - bound) mod bound, as in the reference code
    while True:
        state, r = pcg32_next(state, inc)
        if r >= threshold:
            return state, r % bound


def lcg_advance(state: int, delta: int, mult: int, inc: int, bits: int = 64) -> int:
    """Jump the LCG x -> mult * x + inc mod 2^bits ahead by delta steps in O(log delta).

    Brown's method: square the affine map (mult, inc) and compose the factors
    for the set bits of delta. delta is taken modulo 2^bits, so a negative
    delta goes backwards (the period divides 2^bits).
    """
    mask = (1 << bits) - 1
    delta &= mask
    acc_mult, acc_plus = 1, 0
    cur_mult, cur_plus = mult & mask, inc & mask
    while delta > 0:
        if delta & 1:
            acc_mult = (acc_mult * cur_mult) & mask
            acc_plus = (acc_plus * cur_mult + cur_plus) & mask
        cur_plus = ((cur_mult + 1) * cur_plus) & mask
        cur_mult = (cur_mult * cur_mult) & mask
        delta >>= 1
    return (acc_mult * state + acc_plus) & mask


def xsh_rr(state: int, bits: int, out_bits: int) -> int:
    """The general XSH RR output function of PCG for a state of `bits` bits and output of `out_bits` bits.

    out_bits must be a power of 2 with bits - out_bits >= log2(out_bits).
    """
    opbits = out_bits.bit_length() - 1
    bottom = bits - out_bits - opbits
    xshift = (opbits + out_bits) // 2
    rot = state >> (bits - opbits)
    x = ((state ^ (state >> xshift)) >> bottom) & ((1 << out_bits) - 1)
    return ((x >> rot) | (x << ((-rot) % out_bits))) & ((1 << out_bits) - 1)
