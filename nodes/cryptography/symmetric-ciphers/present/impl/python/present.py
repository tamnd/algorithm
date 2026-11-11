# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/present/. The authors are listed in prov/ADV21B.jsonl.

"""The PRESENT block cipher with an 80-bit key (PRESENT-80), for study only.

Bogdanov et al., CHES 2007; also ISO/IEC 29192-2. This code is not constant
time as Python runs it and must not protect real data. Use a vetted cipher
from libsodium, OpenSSL or a FIPS 140 validated module.

A block is a 64-bit integer and a key an 80-bit integer, bit 0 being the
least significant bit, as in the paper.
"""

SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
SBOX_INV = [SBOX.index(x) for x in range(16)]
MASK64 = (1 << 64) - 1
MASK80 = (1 << 80) - 1


def p_position(i: int) -> int:
    """Return P(i), where bit i of the state moves: P(i) = 16 i mod 63, and P(63) = 63."""
    return 63 if i == 63 else (16 * i) % 63


def round_keys_80(key: int) -> list[int]:
    """Return the 32 round keys K_1 .. K_32 of PRESENT-80.

    Precondition: 0 <= key < 2^80. Cost: Theta(1), 31 updates of an 80-bit register.
    """
    keys = []
    k = key
    for i in range(1, 33):
        keys.append(k >> 16)  # the leftmost 64 bits
        if i == 32:
            break
        k = ((k << 61) | (k >> 19)) & MASK80  # rotate left by 61
        k = (SBOX[k >> 76] << 76) | (k & ((1 << 76) - 1))  # S-box on bits 79..76
        k ^= i << 15  # round counter into bits 19..15
    return keys


def s_layer(state: int, box: list[int]) -> int:
    """Apply a 4-bit S-box to each of the 16 nibbles of a 64-bit state."""
    out = 0
    for j in range(16):
        out |= box[(state >> (4 * j)) & 0xF] << (4 * j)
    return out


def p_layer(state: int) -> int:
    """Move bit i of the state to bit P(i)."""
    out = 0
    for i in range(64):
        out |= ((state >> i) & 1) << p_position(i)
    return out


def p_layer_inv(state: int) -> int:
    """Move bit P(i) of the state back to bit i."""
    out = 0
    for i in range(64):
        out |= ((state >> p_position(i)) & 1) << i
    return out


def present80_encrypt(block: int, key: int) -> int:
    """Encrypt a 64-bit block with an 80-bit key: 31 rounds and a final key addition.

    Precondition: 0 <= block < 2^64, 0 <= key < 2^80. Cost: Theta(1) (31 rounds of 64 bits).
    """
    rk = round_keys_80(key)  # @line L1
    state = block
    for i in range(31):  # @line L2
        state ^= rk[i]  # @line L3
        state = s_layer(state, SBOX)  # @line L4
        state = p_layer(state)  # @line L5
    return state ^ rk[31]  # @line L6


def present80_decrypt(block: int, key: int) -> int:
    """Invert present80_encrypt. Same preconditions and cost."""
    rk = round_keys_80(key)  # @line L7
    state = block ^ rk[31]  # @line L8
    for i in range(30, -1, -1):  # @line L9
        state = p_layer_inv(state)  # @line L10
        state = s_layer(state, SBOX_INV)  # @line L11
        state ^= rk[i]  # @line L12
    return state  # @line L13
