# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzss/. The authors are listed in prov/M0JP2V.jsonl.

"""LZSS: an LZ77 coder whose tokens are a literal or a (distance, length) pair.

Each token starts with one flag bit: 0 for a literal byte (8 more bits), 1 for
a pair (offset_bits for d - 1, then length_bits for length - m). A pair is
used only when it costs fewer bits than the literals it replaces, which gives
the shortest useful length m = floor(pair_bits / 9) + 1.
"""

Token = int | tuple[int, int]  # a literal byte, or (distance, length)


def min_match(offset_bits: int, length_bits: int) -> int:
    """The least length L with 1 + offset_bits + length_bits < 9 * L."""
    return (1 + offset_bits + length_bits) // 9 + 1


def lzss_tokens(data: bytes, offset_bits: int = 12, length_bits: int = 4) -> list[Token]:
    """Greedy LZSS parse with an exhaustive search of the window."""
    window = 1 << offset_bits
    m = min_match(offset_bits, length_bits)
    max_len = m + (1 << length_bits) - 1
    n = len(data)
    out: list[Token] = []
    where: list[list[int]] = [[] for _ in range(256)]
    i = 0  # @line L1
    while i < n:  # @line L2
        cap = min(max_len, n - i)
        best_d, best_len = 0, 0
        cands = where[data[i]]
        for idx in range(len(cands) - 1, -1, -1):  # @line L3
            j = cands[idx]
            if j < i - window or best_len == cap:
                break
            k = 0
            while k < cap and data[j + k] == data[i + k]:
                k += 1
            if k > best_len:
                best_d, best_len = i - j, k
        if best_len >= m:  # @line L4
            out.append((best_d, best_len))  # @line L5
            step = best_len  # @line L6
        else:  # @line L7
            out.append(data[i])  # @line L8
            step = 1  # @line L9
        for p in range(i, i + step):
            where[data[p]].append(p)
        i += step
    return out


def lzss_untokens(tokens: list[Token]) -> bytes:
    """Rebuild the data from tokens, copying one byte at a time."""
    s = bytearray()
    for t in tokens:
        if isinstance(t, tuple):
            d, length = t
            if not 1 <= d <= len(s):
                raise ValueError("distance points before the start of the output")
            for _ in range(length):
                s.append(s[len(s) - d])
        else:
            s.append(t)
    return bytes(s)


def lzss_encode(data: bytes, offset_bits: int = 12, length_bits: int = 4) -> bytes:
    """Pack the tokens into bytes, most significant bit first, zero padded."""
    m = min_match(offset_bits, length_bits)
    acc, nacc, out = 0, 0, bytearray()

    def put(value: int, width: int) -> None:
        nonlocal acc, nacc
        acc = (acc << width) | value
        nacc += width
        while nacc >= 8:
            nacc -= 8
            out.append((acc >> nacc) & 0xFF)
        acc &= (1 << nacc) - 1

    for t in lzss_tokens(data, offset_bits, length_bits):
        if isinstance(t, tuple):
            put(1, 1)
            put(t[0] - 1, offset_bits)
            put(t[1] - m, length_bits)
        else:
            put(0, 1)
            put(t, 8)
    if nacc:
        put(0, 8 - nacc)
    return bytes(out)


def lzss_decode(blob: bytes, offset_bits: int = 12, length_bits: int = 4) -> bytes:
    """Invert lzss_encode. The padding is under 8 bits of 0, so it never forms a
    token: its first bit reads as a literal flag, and a literal needs 8 more bits."""
    m = min_match(offset_bits, length_bits)
    total = 8 * len(blob)
    pos = 0

    def get(width: int) -> int:
        nonlocal pos
        v = 0
        for _ in range(width):
            v = (v << 1) | ((blob[pos >> 3] >> (7 - (pos & 7))) & 1)
            pos += 1
        return v

    s = bytearray()  # @line L10
    while pos < total:  # @line L11
        flag = get(1)  # @line L12
        if total - pos < (offset_bits + length_bits if flag else 8):
            break  # the rest is padding, which is all 0 bits and shorter than a token
        if flag == 1:  # @line L13
            d = get(offset_bits) + 1
            length = get(length_bits) + m
            if d > len(s):
                raise ValueError("distance points before the start of the output")
            for _ in range(length):
                s.append(s[len(s) - d])
        else:
            s.append(get(8))  # @line L14
    return bytes(s)  # @line L15
