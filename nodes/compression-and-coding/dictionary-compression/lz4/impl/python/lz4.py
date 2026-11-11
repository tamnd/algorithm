# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz4/. The authors are listed in prov/2E3NAH.jsonl.
"""LZ4: the block format and the frame format (lz4_Block_format.md and
lz4_Frame_format.md of the reference repository).

A block is a list of sequences. Each sequence is a token (literal length in
the high 4 bits, match length minus 4 in the low 4 bits), extra length
bytes, the literals, a 2-byte little-endian offset, and extra match length
bytes. The last sequence has literals only.
"""

MIN_MATCH = 4
LAST_LITERALS = 5      # the last 5 bytes of a block are literals
MF_LIMIT = 12          # the last match starts at least 12 bytes before the end
MAX_OFFSET = 65535
MAGIC = 0x184D2204
BLOCK_SIZES = {4: 1 << 16, 5: 1 << 18, 6: 1 << 20, 7: 1 << 22}


class LZ4Error(ValueError):
    """The input is not a valid LZ4 block or frame."""


# ---------------------------------------------------------------- xxHash32

P1, P2, P3, P4, P5 = 2654435761, 2246822519, 3266489917, 668265263, 374761393
M32 = 0xFFFFFFFF


def _rotl(x, r):
    return ((x << r) | (x >> (32 - r))) & M32


def _round(acc, lane):
    acc = (acc + lane * P2) & M32
    return (_rotl(acc, 13) * P1) & M32


def xxh32(data, seed=0):
    """xxHash32, as the frame format uses for its checksums."""
    n = len(data)
    p = 0
    if n >= 16:
        v1 = (seed + P1 + P2) & M32
        v2 = (seed + P2) & M32
        v3 = seed & M32
        v4 = (seed - P1) & M32
        while p + 16 <= n:
            v1 = _round(v1, int.from_bytes(data[p:p + 4], "little"))
            v2 = _round(v2, int.from_bytes(data[p + 4:p + 8], "little"))
            v3 = _round(v3, int.from_bytes(data[p + 8:p + 12], "little"))
            v4 = _round(v4, int.from_bytes(data[p + 12:p + 16], "little"))
            p += 16
        h = (_rotl(v1, 1) + _rotl(v2, 7) + _rotl(v3, 12) + _rotl(v4, 18)) & M32
    else:
        h = (seed + P5) & M32
    h = (h + n) & M32
    while p + 4 <= n:
        h = (h + int.from_bytes(data[p:p + 4], "little") * P3) & M32
        h = (_rotl(h, 17) * P4) & M32
        p += 4
    while p < n:
        h = (h + data[p] * P5) & M32
        h = (_rotl(h, 11) * P1) & M32
        p += 1
    h ^= h >> 15
    h = (h * P2) & M32
    h ^= h >> 13
    h = (h * P3) & M32
    h ^= h >> 16
    return h


# ---------------------------------------------------------------- block decoder

def _read_length(src, pos, base):
    """Add the bytes 255, 255, ..., k to base (k < 255 ends the length)."""
    ln = base
    while True:
        if pos >= len(src):
            raise LZ4Error("truncated length")
        b = src[pos]
        pos += 1
        ln += b
        if b != 255:
            return ln, pos


def decompress_block(src, history=b"", max_size=None):
    """Decode one LZ4 block. history is earlier output that matches may use."""
    out = bytearray(history)                          # @line L1
    start = len(history)
    pos, end = 0, len(src)
    while True:                                       # @line L2
        if pos >= end:
            raise LZ4Error("truncated block")
        token = src[pos]                              # @line L3
        pos += 1
        lit = token >> 4                              # @line L4
        if lit == 15:
            lit, pos = _read_length(src, pos, 15)
        if pos + lit > end:
            raise LZ4Error("literals run past the end")
        out += src[pos:pos + lit]                     # @line L5
        pos += lit
        if pos == end:                                # @line L6
            break                                     # the last sequence
        if pos + 2 > end:
            raise LZ4Error("truncated offset")
        off = src[pos] | (src[pos + 1] << 8)          # @line L7
        pos += 2
        if off == 0 or off > len(out):                # @line L8
            raise LZ4Error("bad offset")
        ml = token & 15                               # @line L9
        if ml == 15:
            ml, pos = _read_length(src, pos, 15)
        ml += MIN_MATCH                               # @line L10
        if max_size is not None and len(out) - start + ml > max_size:
            raise LZ4Error("output larger than allowed")
        s = len(out) - off                            # @line L11
        if off >= ml:
            out += out[s:s + ml]
        else:
            out += (out[s:] * (ml // off + 1))[:ml]
    return bytes(out[start:])                         # @line L12


# ---------------------------------------------------------------- block encoder

def _match_length(buf, a, b, limit):
    k = 8
    while k < limit and buf[a:a + k] == buf[b:b + k]:
        k *= 2
    lo = k // 2 if k > 8 else 0
    if k >= limit:
        if buf[a:a + limit] == buf[b:b + limit]:
            return limit
        k = limit
    hi = k - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if buf[a:a + mid] == buf[b:b + mid]:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _put_length(out, n):
    while n >= 255:
        out.append(255)
        n -= 255
    out.append(n)


def _sequence(out, literals, ml, off):
    lit = len(literals)
    token = (min(lit, 15) << 4) | (min(ml - MIN_MATCH, 15) if ml else 0)
    out.append(token)
    if lit >= 15:
        _put_length(out, lit - 15)
    out += literals
    if ml:
        out += off.to_bytes(2, "little")
        if ml - MIN_MATCH >= 15:
            _put_length(out, ml - MIN_MATCH - 15)


def compress_block(data, history=b""):
    """Greedy LZ4 block. Matches may reach into history (dependent blocks)."""
    hist = bytes(history[-MAX_OFFSET:])
    buf = hist + bytes(data)
    base, n = len(hist), len(buf)
    out = bytearray()
    table = {}
    for q in range(max(0, base - MAX_OFFSET), base - 3):
        table[buf[q:q + 4]] = q
    anchor = p = base
    match_limit = n - MF_LIMIT + 1   # a match may start at p <= n - 12
    end_limit = n - LAST_LITERALS    # and must end at or before end_limit
    while p < match_limit:
        key = buf[p:p + 4]
        c = table.get(key, -1)
        table[key] = p
        if c < 0 or p - c > MAX_OFFSET:
            p += 1
            continue
        ml = _match_length(buf, c, p, end_limit - p)
        if ml < MIN_MATCH:
            p += 1
            continue
        _sequence(out, buf[anchor:p], ml, p - c)
        for q in range(p + 1, min(p + ml, n - 3)):
            table[buf[q:q + 4]] = q
        p += ml
        anchor = p
    _sequence(out, buf[anchor:n], 0, 0)
    return bytes(out)


# ---------------------------------------------------------------- frame

def compress_frame(data, block_max=4, independent=True, block_checksum=False,
                   content_checksum=True, content_size=False):
    """An LZ4 frame (version 01) with blocks of at most BLOCK_SIZES[block_max]."""
    data = bytes(data)
    flg = 0x40 | (independent << 5) | (block_checksum << 4) | (content_size << 3) | (content_checksum << 2)
    desc = bytes([flg, block_max << 4])
    if content_size:
        desc += len(data).to_bytes(8, "little")
    out = bytearray(MAGIC.to_bytes(4, "little")) + desc
    out.append((xxh32(desc) >> 8) & 0xFF)
    size = BLOCK_SIZES[block_max]
    for i in range(0, len(data), size):
        raw = data[i:i + size]
        history = b"" if independent else data[max(0, i - MAX_OFFSET):i]
        comp = compress_block(raw, history)
        if len(comp) < len(raw):
            body, word = comp, len(comp)
        else:
            body, word = raw, len(raw) | 0x80000000
        out += word.to_bytes(4, "little") + body
        if block_checksum:
            out += xxh32(body).to_bytes(4, "little")
    out += bytes(4)
    if content_checksum:
        out += xxh32(data).to_bytes(4, "little")
    return bytes(out)


def decompress_frame(src):
    """Decode concatenated LZ4 frames and skip skippable frames."""
    out = bytearray()
    pos = 0
    while pos < len(src):
        if pos + 4 > len(src):
            raise LZ4Error("truncated magic number")
        magic = int.from_bytes(src[pos:pos + 4], "little")
        pos += 4
        if magic & 0xFFFFFFF0 == 0x184D2A50:      # skippable frame
            size = int.from_bytes(src[pos:pos + 4], "little")
            pos += 4 + size
            if pos > len(src):
                raise LZ4Error("truncated skippable frame")
            continue
        if magic != MAGIC:
            raise LZ4Error("bad magic number")
        flg, bd = src[pos], src[pos + 1]
        if flg >> 6 != 1:
            raise LZ4Error("unsupported version")
        if flg & 2 or bd & 0x8F:
            raise LZ4Error("reserved bits set")
        if (bd >> 4) & 7 not in BLOCK_SIZES:
            raise LZ4Error("bad block maximum size")
        dlen = 2 + 8 * ((flg >> 3) & 1) + 4 * (flg & 1)
        desc = src[pos:pos + dlen]
        if len(desc) < dlen or pos + dlen >= len(src):
            raise LZ4Error("truncated frame descriptor")
        if src[pos + dlen] != (xxh32(desc) >> 8) & 0xFF:
            raise LZ4Error("header checksum mismatch")
        # A DictID (flg & 1) names a dictionary that both sides agree on. We
        # have no dictionary, so a match that reaches before the start of the
        # frame fails as a bad offset.
        pos += dlen + 1
        independent = (flg >> 5) & 1
        block_sum = (flg >> 4) & 1
        max_size = BLOCK_SIZES[(bd >> 4) & 7]
        frame = bytearray()
        while True:
            if pos + 4 > len(src):
                raise LZ4Error("truncated block size")
            word = int.from_bytes(src[pos:pos + 4], "little")
            pos += 4
            if word == 0:                       # EndMark
                break
            size = word & 0x7FFFFFFF
            body = src[pos:pos + size]
            if len(body) != size:
                raise LZ4Error("truncated block")
            pos += size
            if block_sum:
                if int.from_bytes(src[pos:pos + 4], "little") != xxh32(body):
                    raise LZ4Error("block checksum mismatch")
                pos += 4
            if word & 0x80000000:
                piece = bytes(body)
            else:
                history = b"" if independent else bytes(frame[-MAX_OFFSET:])
                piece = decompress_block(body, history, max_size)
            if len(piece) > max_size:
                raise LZ4Error("block larger than the maximum size")
            frame += piece
        if (flg >> 3) & 1 and int.from_bytes(desc[2:10], "little") != len(frame):
            raise LZ4Error("content size mismatch")
        if (flg >> 2) & 1:
            if int.from_bytes(src[pos:pos + 4], "little") != xxh32(frame):
                raise LZ4Error("content checksum mismatch")
            pos += 4
        out += frame
    return bytes(out)
