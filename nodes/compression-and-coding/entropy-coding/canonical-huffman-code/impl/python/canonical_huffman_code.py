# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canonical-huffman-code/. The authors are listed in prov/ZVDKR0.jsonl.

"""Canonical prefix codes: codewords from the code lengths alone.

The rule is the one of RFC 1951, Section 3.2.2: shorter codewords come
first, and codewords of the same length are consecutive integers in the
order of the symbols. A length of 0 means that the symbol is not used.
"""

from typing import Sequence


def assign_codes(lengths: Sequence[int]) -> list[int | None]:
    """Return the codeword of each symbol as an integer (None if unused).

    The codeword of a symbol of length l is the l low bits of the integer,
    most significant bit first. Raises ValueError if the lengths break the
    Kraft inequality.
    """
    max_len = max(lengths, default=0)
    bl_count = [0] * (max_len + 1)
    for l in lengths:
        if l:
            bl_count[l] += 1
    # Step 2 of RFC 1951: the smallest code of each length.
    next_code = [0] * (max_len + 2)
    code = 0
    for bits in range(1, max_len + 1):
        code = (code + bl_count[bits - 1]) << 1 if bits > 1 else 0
        next_code[bits] = code
        if code + bl_count[bits] > (1 << bits):
            raise ValueError("the lengths break the Kraft inequality")
    # Step 3: consecutive values for the symbols of each length.
    codes: list[int | None] = []
    for l in lengths:
        if l:
            codes.append(next_code[l])
            next_code[l] += 1
        else:
            codes.append(None)
    return codes


def code_strings(lengths: Sequence[int]) -> list[str | None]:
    return [None if c is None else format(c, "0%db" % l) for c, l in zip(assign_codes(lengths), lengths)]


class Decoder:
    """Decoding tables in the style of Moffat and Turpin (1997).

    For each length l: count[l] is the number of codewords of length l,
    first[l] is the smallest codeword of length l, and offset[l] is the
    index in `symbols` of the first symbol of length l. `symbols` lists
    the used symbols sorted by (length, symbol). These tables have
    O(maximum length) entries plus one entry per symbol; no tree is built.
    """

    def __init__(self, lengths: Sequence[int]):
        assign_codes(lengths)  # checks the Kraft inequality
        self.max_len = max(lengths, default=0)
        m = self.max_len
        self.count = [0] * (m + 2)
        for l in lengths:
            if l:
                self.count[l] += 1
        self.symbols = sorted((i for i, l in enumerate(lengths) if l), key=lambda i: (lengths[i], i))
        self.first = [0] * (m + 2)
        self.offset = [0] * (m + 2)
        code = idx = 0
        for l in range(1, m + 1):
            self.first[l] = code
            self.offset[l] = idx
            code = (code + self.count[l]) << 1
            idx += self.count[l]
        # Left-justified limits for the search decoder: every codeword of
        # length l, read as an m-bit number, is below limit[l].
        self.limit = [0] * (m + 2)
        for l in range(1, m + 1):
            self.limit[l] = (self.first[l] + self.count[l]) << (m - l)

    def decode_bits(self, bits: str) -> list[int]:
        """Bit-serial decoding: one shift, one subtraction, one compare per bit."""
        out = []
        code = length = 0
        for b in bits:
            code = (code << 1) | (b == "1")
            length += 1
            if length > self.max_len:
                raise ValueError("invalid codeword")
            k = code - self.first[length]
            if k < self.count[length]:
                out.append(self.symbols[self.offset[length] + k])
                code = length = 0
        if length:
            raise ValueError("the bit string ends inside a codeword")
        return out

    def decode_buffer(self, bits: str) -> list[int]:
        """Search decoding: look at the next max_len bits as one integer.

        The length l of the next codeword is the smallest l with
        buffer < limit[l]; a short loop finds it, as in the linear search
        of Moffat and Turpin.
        """
        m = self.max_len
        out = []
        pos = 0
        n = len(bits)
        while pos < n:
            window = bits[pos : pos + m].ljust(m, "0")
            buf = int(window, 2)
            l = 1
            while l <= m and buf >= self.limit[l]:
                l += 1
            if l > m or pos + l > n:
                raise ValueError("invalid codeword")
            k = (buf >> (m - l)) - self.first[l]
            out.append(self.symbols[self.offset[l] + k])
            pos += l
        return out


def encode(message: Sequence[int], lengths: Sequence[int]) -> str:
    words = code_strings(lengths)
    return "".join(words[s] for s in message)  # type: ignore[misc]
