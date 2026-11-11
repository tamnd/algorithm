# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-cryptanalysis/. The authors are listed in prov/X8G9S4.jsonl.
"""Linear cryptanalysis (Matsui 1993) on the Heys toy SPN.

For study only: a teaching attack on a 16-bit toy cipher. Nothing here is
constant time or fit for real use; for real data use AES from a validated
library (for example the Python package "cryptography").

The approximation is the one of Heys's tutorial. Four S-box approximations,
each with bias +-1/4, chain through three rounds:

    P5 ^ P7 ^ P8 ^ U4,6 ^ U4,8 ^ U4,14 ^ U4,16 ^ (key bits) = 0

where U4 is the input of the round-4 S-boxes. The piling-up lemma gives the
bias 2^3 * (1/4) * (-1/4)^3 = -1/32. In masks (bit 1 is the leftmost bit):
plaintext mask 0x0B00 and U4 mask 0x0505.

Algorithm 1 reads one key parity bit from a 3-round cipher. Algorithm 2 runs
over the full 4-round cipher: it guesses the 8 bits of K5 on nibbles 2 and 4,
decrypts those nibbles of each ciphertext through the last S-boxes and keeps
the guess whose count is furthest from N/2.
"""

from heys_spn import PERM, SUB, SBOX_INV, lat, parity

P_MASK = 0x0B00
U4_MASK = 0x0505
# Key masks of the trail: the input mask of each round's S-box layer.
KEY_MASKS = [0x0B00, 0x0400, 0x0404, 0x0505]
# (round, S-box, input mask, output mask)
TRAIL = [(1, 2, 0xB, 0x4), (2, 2, 0x4, 0x5), (3, 2, 0x4, 0x5), (3, 4, 0x4, 0x5)]


def piling_up(biases: list[float]) -> float:
    """Bias of X1 ^ ... ^ Xn for independent bits with the given biases."""
    eps = 2 ** (len(biases) - 1)
    for e in biases:
        eps *= e
    return eps


def trail_bias() -> float:
    t = lat()
    return piling_up([t[a][b] / 16 for _, _, a, b in TRAIL])


def three_round_cipher(p: int, keys: list[int]) -> int:
    """Rounds 1 to 3 of the toy SPN, then XOR K4: the output is U4."""
    x = p
    for r in range(3):
        x = PERM[SUB[x ^ keys[r]]]
    return x ^ keys[3]


def key_parity(keys: list[int]) -> int:
    return parity(keys[0] & KEY_MASKS[0]) ^ parity(keys[1] & KEY_MASKS[1]) ^ parity(keys[2] & KEY_MASKS[2]) ^ parity(keys[3] & KEY_MASKS[3])


def algorithm_1(pairs: list[tuple[int, int]], bias: float) -> int:
    """Matsui's Algorithm 1: guess the key parity bit from N (P, C) pairs."""
    t = sum(1 for p, c in pairs if parity(p & P_MASK) ^ parity(c & U4_MASK) == 0)
    more_zeros = 2 * t > len(pairs)
    # lhs ^ key = 0 holds with probability 1/2 + bias.
    return 0 if more_zeros == (bias > 0) else 1


def algorithm_2(pairs: list[tuple[int, int]]) -> tuple[int, list[float]]:
    """Matsui's Algorithm 2 on the last round: return (k2 << 4 | k4, biases)."""
    # Count the texts by the two ciphertext nibbles and the plaintext parity.
    # A pair with the same table index gives the same answer for every guess,
    # so the loop of line L4 runs over the 512 cells instead of the N pairs.
    hist = [0] * 512
    for p, c in pairs:  # @line L1
        hist[(((c >> 8) & 0xF) << 5) | ((c & 0xF) << 1) | parity(p & P_MASK)] += 1
    n = len(pairs)
    biases = []
    for g in range(256):  # @line L2
        k2, k4 = g >> 4, g & 0xF
        zeros = 0  # @line L3
        for idx in range(512):  # @line L4
            if hist[idx]:
                c2, c4, pb = idx >> 5, (idx >> 1) & 0xF, idx & 1
                u2, u4 = SBOX_INV[c2 ^ k2], SBOX_INV[c4 ^ k4]  # @line L5
                if parity(u2 & 0x5) ^ parity(u4 & 0x5) ^ pb == 0:  # @line L6
                    zeros += hist[idx]
        biases.append(zeros / n - 0.5)  # @line L7
    best = max(range(256), key=lambda g: abs(biases[g]))  # @line L8
    return best, biases


def known_plaintexts_needed(c: float = 8.0) -> int:
    """N = c / eps^2 known plaintexts."""
    return int(round(c / trail_bias() ** 2))
