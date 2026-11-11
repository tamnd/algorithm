# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snappy/. The authors are listed in prov/A8ZRG6.jsonl.
"""Snappy: the raw format of format_description.txt and the framing format.

A raw stream is the uncompressed length as a varint, then elements. The low
two bits of each tag byte give the element: 00 literal, 01 copy with a
1-byte offset, 10 copy with a 2-byte offset, 11 copy with a 4-byte offset.
"""

BLOCK = 1 << 16          # the encoder matches only inside 64 KiB blocks
MIN_MATCH = 4


class SnappyError(ValueError):
    """The input is not a valid Snappy stream."""


# ---------------------------------------------------------------- varint

def put_varint(n):
    if not 0 <= n < 1 << 32:
        raise ValueError("Snappy lengths are below 2^32")
    out = bytearray()
    while n >= 0x80:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def get_varint(data, pos=0):
    """Read a little-endian base-128 varint of at most 5 bytes, below 2^32."""
    value, shift = 0, 0
    for i in range(5):
        if pos + i >= len(data):
            raise SnappyError("truncated varint")
        b = data[pos + i]
        value |= (b & 0x7F) << shift
        if not b & 0x80:
            if value >= 1 << 32:
                raise SnappyError("varint overflows 32 bits")
            return value, pos + i + 1
        shift += 7
    raise SnappyError("varint longer than 5 bytes")


# ---------------------------------------------------------------- decoder

def decompress(data):
    """Decode a raw Snappy stream."""
    n, pos = get_varint(data)                      # @line L1
    out = bytearray()                              # @line L2
    end = len(data)
    while pos < end:                               # @line L3
        tag = data[pos]                            # @line L4
        pos += 1
        kind = tag & 3
        if kind == 0:                              # @line L5
            ln = tag >> 2                          # @line L6
            if ln >= 60:                           # @line L7
                k = ln - 59
                if pos + k > end:
                    raise SnappyError("truncated literal length")
                ln = int.from_bytes(data[pos:pos + k], "little")
                pos += k
            ln += 1                                # @line L8
            if pos + ln > end or len(out) + ln > n:
                raise SnappyError("literal runs past the end")
            out += data[pos:pos + ln]              # @line L9
            pos += ln
            continue
        if kind == 1:                              # @line L10
            if pos + 1 > end:
                raise SnappyError("truncated copy")
            ln = 4 + ((tag >> 2) & 7)
            off = ((tag >> 5) << 8) | data[pos]
            pos += 1
        else:                                      # @line L11
            k = 2 if kind == 2 else 4
            if pos + k > end:
                raise SnappyError("truncated copy")
            ln = 1 + (tag >> 2)
            off = int.from_bytes(data[pos:pos + k], "little")
            pos += k
        if off == 0 or off > len(out):             # @line L12
            raise SnappyError("bad copy offset")
        if len(out) + ln > n:
            raise SnappyError("copy runs past the end")
        start = len(out) - off                     # @line L13
        if off >= ln:
            out += out[start:start + ln]
        else:
            out += (out[start:] * (ln // off + 1))[:ln]
    if len(out) != n:                              # @line L14
        raise SnappyError("length does not match the preamble")
    return bytes(out)                              # @line L15


# ---------------------------------------------------------------- encoder

def _emit_literal(out, lit):
    n = len(lit) - 1
    if n < 60:
        out.append(n << 2)
    else:
        k = (n.bit_length() + 7) // 8
        out.append((59 + k) << 2)
        out += n.to_bytes(k, "little")
    out += lit


def _emit_copy_upto64(out, off, ln):
    if 4 <= ln <= 11 and off < 2048:
        out.append(1 | ((ln - 4) << 2) | ((off >> 8) << 5))
        out.append(off & 0xFF)
    elif off < 65536:
        out.append(2 | ((ln - 1) << 2))
        out += off.to_bytes(2, "little")
    else:
        out.append(3 | ((ln - 1) << 2))
        out += off.to_bytes(4, "little")


def _emit_copy(out, off, ln):
    # Long matches: pieces of 64, and keep the last piece at 4 or more bytes.
    while ln >= 68:
        _emit_copy_upto64(out, off, 64)
        ln -= 64
    if ln > 64:
        _emit_copy_upto64(out, off, 60)
        ln -= 60
    _emit_copy_upto64(out, off, ln)


def _match_length(buf, a, b, limit):
    """Longest common prefix of buf[a:] and buf[b:], at most limit.

    Galloping on slice comparisons: O(l log l) byte work for a result l.
    """
    k = 8
    while k < limit and buf[a:a + k] == buf[b:b + k]:
        k *= 2
    lo = k // 2 if k > 8 else 0          # a length known to match
    if k >= limit:
        if buf[a:a + limit] == buf[b:b + limit]:
            return limit
        k = limit
    hi = k - 1                           # the first k bytes do not all match
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if buf[a:a + mid] == buf[b:b + mid]:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _compress_block(out, buf, base, end):
    """Greedy parse of buf[base:end]; matches stay inside the block."""
    table = {}
    lit_start = base
    p = base
    skip = 32
    while p + MIN_MATCH <= end:
        key = buf[p:p + 4]
        cand = table.get(key, -1)
        table[key] = p
        if cand < 0:
            # Search faster through data with no matches, as the reference
            # does: the step is (bytes scanned since the last match) / 32.
            step = skip >> 5
            p += step
            skip += step
            continue
        skip = 32
        ln = _match_length(buf, cand, p, end - p)
        if lit_start < p:
            _emit_literal(out, buf[lit_start:p])
        _emit_copy(out, p - cand, ln)
        for q in range(p + 1, min(p + ln, end - 3)):
            table[buf[q:q + 4]] = q
        p += ln
        lit_start = p
    if lit_start < end:
        _emit_literal(out, buf[lit_start:end])


def compress(data):
    """Encode data as a raw Snappy stream."""
    data = bytes(data)
    out = bytearray(put_varint(len(data)))
    for base in range(0, len(data), BLOCK):
        _compress_block(out, data, base, min(base + BLOCK, len(data)))
    return bytes(out)


# ---------------------------------------------------------------- framing

def _crc32c_table():
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ 0x82F63B78 if c & 1 else c >> 1
        table.append(c)
    return table


_CRC32C = _crc32c_table()


def crc32c(data):
    c = 0xFFFFFFFF
    for b in data:
        c = _CRC32C[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


def masked_crc(data):
    c = crc32c(data)
    return (((c >> 15) | (c << 17)) + 0xA282EAD8) & 0xFFFFFFFF


STREAM_ID = b"\xff\x06\x00\x00sNaPpY"


def frame_compress(data):
    """The framing format: a stream identifier, then chunks of at most 64 KiB."""
    data = bytes(data)
    out = bytearray(STREAM_ID)
    for i in range(0, len(data), BLOCK):
        piece = data[i:i + BLOCK]
        crc = masked_crc(piece).to_bytes(4, "little")
        comp = compress(piece)
        if len(comp) < len(piece):
            kind, body = 0x00, crc + comp
        else:
            kind, body = 0x01, crc + piece
        out.append(kind)
        out += len(body).to_bytes(3, "little")
        out += body
    return bytes(out)


def frame_decompress(data):
    if not data.startswith(STREAM_ID):
        raise SnappyError("missing stream identifier")
    out = bytearray()
    pos = 0
    while pos < len(data):
        if pos + 4 > len(data):
            raise SnappyError("truncated chunk header")
        kind = data[pos]
        ln = int.from_bytes(data[pos + 1:pos + 4], "little")
        body = data[pos + 4:pos + 4 + ln]
        if len(body) != ln:
            raise SnappyError("truncated chunk")
        pos += 4 + ln
        if kind == 0xFF:
            if body != b"sNaPpY":
                raise SnappyError("bad stream identifier")
        elif kind in (0x00, 0x01):
            if ln < 4:
                raise SnappyError("chunk too short")
            piece = decompress(body[4:]) if kind == 0 else body[4:]
            if len(piece) > BLOCK:
                raise SnappyError("chunk holds more than 65536 bytes")
            if masked_crc(piece) != int.from_bytes(body[:4], "little"):
                raise SnappyError("CRC-32C mismatch")
            out += piece
        elif kind <= 0x7F:
            raise SnappyError("reserved unskippable chunk")
        # 0x80 to 0xFE: padding or reserved skippable chunks are skipped.
    return bytes(out)
