# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-cryptanalysis/. The authors are listed in prov/7PQPMV.jsonl.
"""Differential cryptanalysis (Biham and Shamir 1991) on the Heys toy SPN.

For study only: a teaching attack on a 16-bit toy cipher. Nothing here is
constant time or fit for real use; for real data use AES from a validated
library (for example the Python package "cryptography").

The attack follows Heys's tutorial. A 3-round characteristic with input
difference 0x0B00 reaches the input of the last S-box layer with difference
0x0606 with probability 27/1024. Right pairs then have ciphertext difference
zero in nibbles 1 and 3. For each guess of the 8 key bits of K5 that sit on
nibbles 2 and 4, decrypt those two nibbles through the last S-boxes and count
the pairs that show difference 6 in both. The right guess gets about N * p
counts; a wrong guess gets far fewer.
"""

from collections.abc import Callable

from heys_spn import PERM, SBOX_INV, ddt, nibble

ALPHA = 0x0B00  # plaintext difference
BETA = 0x0606   # difference at the input of the round-4 S-boxes

# The characteristic, one S-box at a time: (round, S-box, input diff, output diff).
TRAIL = [(1, 2, 0xB, 0x2), (2, 3, 0x4, 0x6), (3, 2, 0x2, 0x5), (3, 3, 0x2, 0x5)]


def characteristic_probability() -> float:
    """Product of the DDT entries over the active S-boxes (Markov assumption)."""
    t = ddt()
    p = 1.0
    for _, _, a, b in TRAIL:
        p *= t[a][b] / 16
    return p


def check_trail() -> bool:
    """The trail is consistent: each S-box output, after the permutation, feeds the next round."""
    diff = ALPHA
    for rnd in (1, 2, 3):
        out = 0
        for r, s, a, b in TRAIL:
            if r == rnd:
                if nibble(diff, s) != a:
                    return False
                out |= b << (4 * (4 - s))
        diff = PERM[out]
    return diff == BETA


def pairs_needed(c: float = 8.0) -> int:
    """N = c / p chosen pairs: about c right pairs are expected."""
    return int(round(c / characteristic_probability()))


def recover_last_round_bits(oracle: Callable[[int], int], n_pairs: int, plaintexts: list[int]) -> tuple[int, list[int]]:
    """Return the best guess (k2, k4) packed as k2 << 4 | k4, and all 256 counts.

    oracle encrypts one 16-bit plaintext; plaintexts gives the first member of
    each pair (the second is p ^ ALPHA).
    """
    counts = [0] * 256  # @line L1
    for p in plaintexts[:n_pairs]:  # @line L2
        c1, c2 = oracle(p), oracle(p ^ ALPHA)  # @line L3
        d = c1 ^ c2
        if nibble(d, 1) or nibble(d, 3):  # @line L4
            continue  # filter: a right pair has no difference there
        a2, b2, a4, b4 = nibble(c1, 2), nibble(c2, 2), nibble(c1, 4), nibble(c2, 4)
        ok2 = [k for k in range(16) if SBOX_INV[a2 ^ k] ^ SBOX_INV[b2 ^ k] == nibble(BETA, 2)]
        ok4 = [k for k in range(16) if SBOX_INV[a4 ^ k] ^ SBOX_INV[b4 ^ k] == nibble(BETA, 4)]
        for k2 in ok2:  # @line L5
            for k4 in ok4:
                counts[(k2 << 4) | k4] += 1  # @line L6
    best = max(range(256), key=lambda g: counts[g])  # @line L7
    return best, counts
