# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-bruijn-bit-scan/. The authors are listed in prov/3BENJ1.jsonl.

# For each word size w = 2^n: the de Bruijn constant D (a binary de Bruijn
# sequence of order n whose top n bits are zero) and n.
_CONSTANTS: dict[int, tuple[int, int]] = {
    8: (0x1D, 3),
    16: (0x09AF, 4),
    32: (0x077CB531, 5),
    64: (0x03F79D71B4CB0A89, 6),
}


def build_table(d: int, w: int, n: int) -> tuple[int, ...]:
    """Return T with T[((2^k * d) mod 2^w) >> (w - n)] = k for 0 <= k < w.

    Raises ValueError if two values of k give the same index, that is, if d
    is not a valid multiplier for this word size. Cost: Theta(w).
    """
    mask = (1 << w) - 1
    table = [-1] * w
    for k in range(w):
        i = (((1 << k) * d) & mask) >> (w - n)
        if table[i] != -1:
            raise ValueError("d is not a de Bruijn multiplier for this w")
        table[i] = k
    return tuple(table)


_TABLES: dict[int, tuple[int, ...]] = {
    w: build_table(d, w, n) for w, (d, n) in _CONSTANTS.items()
}


def de_bruijn_bit_scan(x: int, w: int = 64) -> int:
    """Return the index of the lowest 1-bit of x (the trailing-zero count).

    Precondition: w is 8, 16, 32 or 64, and x is an unsigned w-bit word with
    x != 0. Raises ValueError otherwise. Cost: one negation, one AND, one
    multiplication, one shift and one table read, so O(1) word operations.
    """
    if w not in _CONSTANTS:
        raise ValueError("w must be 8, 16, 32 or 64")
    if not 0 < x < (1 << w):
        raise ValueError("x must satisfy 0 < x < 2^w")
    d, n = _CONSTANTS[w]
    table = _TABLES[w]
    mask = (1 << w) - 1
    b = x & (-x & mask)  # @line L1
    p = (b * d) & mask  # @line L2
    i = p >> (w - n)  # @line L3
    return table[i]  # @line L4
