# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzw/. The authors are listed in prov/2BH6WA.jsonl.

"""LZW (Welch, 1984).

lzw_encode_codes and lzw_decode_codes are the plain method: the dictionary
starts with the 256 one-byte strings (codes 0 to 255), and the output is a
list of codes only.

lzw_compress and lzw_decompress add what file formats add: variable-width
codes packed into bytes (least significant bit first, as in GIF and Unix
compress), a CLEAR code 256 that resets the dictionary, and a maximum width.
The width starts at 9 bits. Each code is written with the bit length of the
largest code that the decoder can see at that point. When the dictionary is
full, the encoder writes CLEAR and starts again.
"""

CLEAR = 256
FIRST_FREE = 257


def lzw_encode_codes(data: bytes) -> list[int]:
    if not data:
        return []
    table = {bytes([b]): b for b in range(256)}  # @line L1
    nxt = 256
    out: list[int] = []
    w = data[:1]  # @line L2
    for i in range(1, len(data)):  # @line L3
        wk = w + data[i:i + 1]
        if wk in table:  # @line L4
            w = wk
        else:  # @line L5
            out.append(table[w])  # @line L6
            table[wk] = nxt  # @line L7
            nxt += 1
            w = data[i:i + 1]  # @line L8
    out.append(table[w])  # @line L9
    return out


def lzw_decode_codes(codes: list[int]) -> bytes:
    if not codes:
        return b""
    table = [bytes([b]) for b in range(256)]  # @line L10
    if codes[0] >= 256:
        raise ValueError("the first code must be a single symbol")
    prev = table[codes[0]]  # @line L11
    out = bytearray(prev)
    for c in codes[1:]:  # @line L12
        if c < len(table):  # @line L13
            cur = table[c]
        elif c == len(table):  # @line L14
            cur = prev + prev[:1]  # the KwKwK case: the code is the one being defined
        else:
            raise ValueError("code is not in the dictionary")
        out += cur  # @line L15
        table.append(prev + cur[:1])  # @line L16
        prev = cur  # @line L17
    return bytes(out)


def lzw_compress(data: bytes, max_bits: int = 12) -> bytes:
    if not 9 <= max_bits <= 16:
        raise ValueError("max_bits must be in 9..16")
    out = bytearray()
    acc = nacc = 0

    def put(code: int, width: int) -> None:
        nonlocal acc, nacc
        acc |= code << nacc
        nacc += width
        while nacc >= 8:
            out.append(acc & 0xFF)
            acc >>= 8
            nacc -= 8

    limit = 1 << max_bits
    table: dict[bytes, int] = {}
    nxt = FIRST_FREE
    w = b""
    for i in range(len(data)):
        k = data[i:i + 1]
        if not w:
            w = k
            continue
        wk = w + k
        if wk in table:
            w = wk
            continue
        put(table.get(w, w[0]), (nxt - 1).bit_length())
        table[wk] = nxt
        nxt += 1
        w = k
        if nxt == limit:  # the table is full: reset it
            put(CLEAR, (nxt - 1).bit_length())
            table.clear()
            nxt = FIRST_FREE
    if w:
        put(table.get(w, w[0]), (nxt - 1).bit_length())
    if nacc:
        out.append(acc & 0xFF)
    return bytes(out)


def lzw_decompress(blob: bytes, max_bits: int = 12) -> bytes:
    if not 9 <= max_bits <= 16:
        raise ValueError("max_bits must be in 9..16")
    total = 8 * len(blob)
    pos = 0
    out = bytearray()
    table: list[bytes] = [bytes([b]) for b in range(256)] + [b""]
    prev = b""
    while True:
        # The encoder has one more entry than we have, except before the first code.
        width = max(9, len(table).bit_length() if prev else (len(table) - 1).bit_length())
        if total - pos < width:
            break
        c = 0
        for t in range(width):
            c |= ((blob[(pos + t) >> 3] >> ((pos + t) & 7)) & 1) << t
        pos += width
        if c == CLEAR:
            del table[FIRST_FREE:]
            prev = b""
            continue
        if not prev:
            if c > 255:
                raise ValueError("the first code after a reset must be a single symbol")
            prev = table[c]
            out += prev
            continue
        if c < len(table) and c != CLEAR:
            cur = table[c]
        elif c == len(table):
            cur = prev + prev[:1]
        else:
            raise ValueError("code is not in the dictionary")
        out += cur
        if len(table) < (1 << max_bits):
            table.append(prev + cur[:1])
        prev = cur
    return bytes(out)
