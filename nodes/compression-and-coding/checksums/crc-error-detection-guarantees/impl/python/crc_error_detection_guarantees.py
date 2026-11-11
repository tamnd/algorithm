# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crc-error-detection-guarantees/. The authors are listed in prov/Y8VC6W.jsonl.

"""Exhaustive checks of the error-detection guarantees of a CRC.

A generator G is an int with bit i the coefficient of x^i. An error pattern
E on a codeword is missed exactly when G divides E, that is, when the XOR of
the syndromes s_i = x^i mod G over the error positions is 0.
"""


def deg(a: int) -> int:
    return a.bit_length() - 1


def pmod(a: int, g: int) -> int:
    dg = deg(g)
    while a and deg(a) >= dg:
        a ^= g << (deg(a) - dg)
    return a


def syndromes(g: int, n: int) -> list[int]:
    """s_i = x^i mod G for i < n."""
    r = deg(g)
    out, s = [], 1
    for _ in range(n):
        out.append(s)
        s <<= 1
        if s >> r:
            s ^= g
    return out


def is_missed(error: int, g: int) -> bool:
    return error != 0 and pmod(error, g) == 0


def period(g: int, limit: int) -> int | None:
    """Least e >= 1 with x^e = 1 mod G, searched up to limit; None if none."""
    r = deg(g)
    s = 1
    for e in range(1, limit + 1):
        s <<= 1
        if s >> r:
            s ^= g
        if s == 1:
            return e
    return None


def missed_patterns_all(g: int, n: int) -> list[int]:
    """Every nonzero pattern of length n that G divides, by a Gray-code walk
    over all 2^n patterns (each step flips one bit and one syndrome)."""
    s = syndromes(g, n)
    out = []
    pattern, syn = 0, 0
    for k in range(1, 1 << n):
        bit = (k & -k).bit_length() - 1
        pattern ^= 1 << bit
        syn ^= s[bit]
        if syn == 0:
            out.append(pattern)
    return out


def burst_miss_count(g: int, b: int) -> tuple[int, int]:
    """For bursts of length exactly b (first and last error bit set, any bits
    between), return (missed, total). The position does not matter, because
    G(0) = 1 makes x invertible modulo G; Theorem 4 of the proof."""
    if b == 1:
        return (0, 1)
    s = syndromes(g, b)
    base = s[0] ^ s[b - 1]
    missed, total = 0, 0
    syn = base
    inner = b - 2
    for k in range(1 << inner):
        if k:
            bit = (k & -k).bit_length() - 1
            syn ^= s[1 + bit]
        total += 1
        if syn == 0:
            missed += 1
    return missed, total


def bursts_missed_at_positions(g: int, n: int, b: int) -> int:
    """Number of missed bursts of length exactly b at all positions in a
    codeword of n bits, by direct division of each pattern."""
    missed = 0
    for start in range(n - b + 1):
        for mid in range(1 << max(b - 2, 0)):
            if b == 1:
                e = 1
            else:
                e = 1 | (mid << 1) | (1 << (b - 1))
            if is_missed(e << start, g):
                missed += 1
    return missed


# Bit-by-bit CRC with init 0 and no reflection; the codeword is the message
# followed by the r check bits.
def codeword(message_bits: int, k: int, g: int) -> int:
    r = deg(g)
    return (message_bits << r) | pmod(message_bits << r, g)


def receiver_accepts(word: int, g: int) -> bool:
    return pmod(word, g) == 0
