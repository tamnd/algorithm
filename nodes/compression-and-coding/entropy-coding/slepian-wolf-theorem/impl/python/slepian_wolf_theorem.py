# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slepian-wolf-theorem/. The authors are listed in prov/VX919M.jsonl.
"""Syndrome coding at a corner of the Slepian-Wolf region, with the [7, 4, 3] Hamming code.

X is a uniform 7-bit word. Y is X with at most one bit flipped. The encoder of X
sees only X and sends its 3-bit syndrome. The encoder of Y sends Y in 7 bits.
The decoder finds X from the syndrome and Y. The total rate is 3 + 7 = 10 bits,
which equals H(X, Y) = H(Y) + H(X | Y) = 7 + 3.
"""

from math import log2

N = 7  # block length
R_BITS = 3  # syndrome length


def syndrome(x: int) -> int:
    """H x over GF(2), where column j (1-based) of H is j in binary. Bit j - 1 of x is position j.

    The syndrome is the XOR of the positions j whose bit is 1.
    """
    if not 0 <= x < 1 << N:
        raise ValueError("x must be a 7-bit word")
    s = 0
    for j in range(1, N + 1):
        if x >> (j - 1) & 1:
            s ^= j
    return s


def encode_x(x: int) -> int:
    """The message of the encoder of X: 3 bits."""
    return syndrome(x)


def decode(s: int, y: int) -> int:
    """Recover x from its syndrome s and the side information y = x XOR e with weight(e) <= 1.

    H y XOR s = H e, and for a single error at position j that is j, so the
    error is located and removed. For e = 0 it is 0.
    """
    d = syndrome(y) ^ s
    if d == 0:
        return y
    return y ^ (1 << (d - 1))


def coset(s: int) -> list[int]:
    """The bin of syndrome s: the 16 words that share it."""
    return [x for x in range(1 << N) if syndrome(x) == s]


def joint_entropy_bits() -> float:
    """H(X, Y) for X uniform on 7 bits and E uniform on the 8 patterns of weight at most 1."""
    pairs = {}
    for x in range(1 << N):
        for e in [0] + [1 << i for i in range(N)]:
            pairs[(x, x ^ e)] = pairs.get((x, x ^ e), 0) + 1
    total = sum(pairs.values())
    return -sum(c / total * log2(c / total) for c in pairs.values())
