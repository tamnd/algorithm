# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deflate/. The authors are listed in prov/TDJAX5.jsonl.
"""DEFLATE (RFC 1951) with the zlib (RFC 1950) and gzip (RFC 1952) wrappers.

The inflater reads all three block types: stored, fixed Huffman and dynamic
Huffman. The deflater finds matches with hash chains (greedy or lazy) and
writes, for each block, the cheapest of a stored, a fixed Huffman and a
dynamic Huffman block. Dynamic codes are length limited by package-merge.
"""

from bisect import bisect_right

LEN_BASE = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31,
            35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258]
LEN_EXTRA = [0] * 8 + [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4 + [0]
DIST_BASE = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193,
             257, 385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145,
             8193, 12289, 16385, 24577]
DIST_EXTRA = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6,
              7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13]
CL_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
WINDOW = 32768
MAX_MATCH = 258
MIN_MATCH = 3


class DeflateError(ValueError):
    """The input is not a valid DEFLATE, zlib or gzip stream."""


# ---------------------------------------------------------------- checksums

def _crc_table():
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
        table.append(c)
    return table


_CRC = _crc_table()


def crc32(data, value=0):
    """CRC-32 of gzip (reflected polynomial 0xEDB88320, init and xorout 0xFFFFFFFF)."""
    c = value ^ 0xFFFFFFFF
    for b in data:
        c = _CRC[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


def adler32(data, value=1):
    """Adler-32 of zlib: two sums modulo 65521, the first one started at 1."""
    s1, s2 = value & 0xFFFF, value >> 16
    for i in range(0, len(data), 5552):
        for b in data[i:i + 5552]:
            s1 += b
            s2 += s1
        s1 %= 65521
        s2 %= 65521
    return (s2 << 16) | s1


# ---------------------------------------------------------------- bit I/O

class BitReader:
    """Reads bits from bytes, least significant bit of each byte first."""

    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos
        self.buf = 0
        self.cnt = 0

    def _fill(self, n, strict):
        while self.cnt < n:
            if self.pos >= len(self.data):
                if strict:
                    raise DeflateError("unexpected end of input")
                return
            self.buf |= self.data[self.pos] << self.cnt
            self.pos += 1
            self.cnt += 8

    def bits(self, n):
        if n == 0:
            return 0
        self._fill(n, True)
        v = self.buf & ((1 << n) - 1)
        self.buf >>= n
        self.cnt -= n
        return v

    def decode(self, code):
        """Decode one symbol with a table made by huffman_table."""
        table, maxlen = code
        if self.cnt < maxlen:
            self._fill(maxlen, False)
        entry = table[self.buf & ((1 << maxlen) - 1)]
        if entry < 0:
            raise DeflateError("invalid Huffman code")
        ln = entry & 15
        if ln > self.cnt:
            raise DeflateError("unexpected end of input")
        self.buf >>= ln
        self.cnt -= ln
        return entry >> 4

    def align(self):
        """Drop the bits up to the next byte boundary."""
        k = self.cnt & 7
        self.buf >>= k
        self.cnt -= k

    def byte_pos(self):
        """Position of the first byte not consumed, after align()."""
        return self.pos - self.cnt // 8


class BitWriter:
    """Writes bits into bytes, least significant bit of each byte first."""

    def __init__(self):
        self.out = bytearray()
        self.buf = 0
        self.cnt = 0

    def write(self, value, n):
        self.buf |= value << self.cnt
        self.cnt += n
        while self.cnt >= 8:
            self.out.append(self.buf & 0xFF)
            self.buf >>= 8
            self.cnt -= 8

    def align(self):
        if self.cnt:
            self.write(0, 8 - self.cnt)

    def bit_length(self):
        return 8 * len(self.out) + self.cnt

    def finish(self):
        self.align()
        return bytes(self.out)


# ---------------------------------------------------------------- prefix codes

def _reverse(code, n):
    r = 0
    for _ in range(n):
        r = (r << 1) | (code & 1)
        code >>= 1
    return r


def canonical_codes(lengths):
    """RFC 1951 Section 3.2.2: the canonical code of each symbol, MSB first."""
    maxlen = max(lengths, default=0)
    bl_count = [0] * (maxlen + 1)
    for ln in lengths:
        if ln:
            bl_count[ln] += 1
    next_code = [0] * (maxlen + 2)
    code = 0
    for bits in range(1, maxlen + 1):
        code = (code + bl_count[bits - 1]) << 1
        next_code[bits] = code
    codes = [0] * len(lengths)
    for sym, ln in enumerate(lengths):
        if ln:
            codes[sym] = next_code[ln]
            next_code[ln] += 1
    return codes


def huffman_table(lengths, allow_single=True):
    """A decoding table indexed by the next maxlen input bits.

    An over-subscribed code is an error. An incomplete code is an error,
    except a code with one symbol of length 1 when allow_single is true.
    """
    maxlen = max(lengths, default=0)
    if maxlen == 0:
        return None
    kraft = sum(1 << (maxlen - ln) for ln in lengths if ln)
    if kraft > (1 << maxlen):
        raise DeflateError("over-subscribed code lengths")
    if kraft < (1 << maxlen):
        used = [ln for ln in lengths if ln]
        if not (allow_single and used == [1]):
            raise DeflateError("incomplete code lengths")
    codes = canonical_codes(lengths)
    table = [-1] * (1 << maxlen)
    for sym, ln in enumerate(lengths):
        if ln:
            r = _reverse(codes[sym], ln)
            entry = (sym << 4) | ln
            for k in range(r, 1 << maxlen, 1 << ln):
                table[k] = entry
    return table, maxlen


FIXED_LIT_LENGTHS = [8] * 144 + [9] * 112 + [7] * 24 + [8] * 8
FIXED_DIST_LENGTHS = [5] * 30
_FIXED_LIT = huffman_table(FIXED_LIT_LENGTHS)
_FIXED_DIST = huffman_table([5] * 32)


# ---------------------------------------------------------------- inflate

def _read_dynamic(br):
    hlit = br.bits(5) + 257
    hdist = br.bits(5) + 1
    hclen = br.bits(4) + 4
    if hlit > 286 or hdist > 30:
        raise DeflateError("too many length or distance codes")
    cl_lengths = [0] * 19
    for i in range(hclen):
        cl_lengths[CL_ORDER[i]] = br.bits(3)
    cl_code = huffman_table(cl_lengths, allow_single=False)
    if cl_code is None:
        raise DeflateError("empty code length code")
    lengths = []
    while len(lengths) < hlit + hdist:
        sym = br.decode(cl_code)
        if sym < 16:
            lengths.append(sym)
            continue
        if sym == 16:
            if not lengths:
                raise DeflateError("repeat with no previous length")
            value, count = lengths[-1], 3 + br.bits(2)
        elif sym == 17:
            value, count = 0, 3 + br.bits(3)
        else:
            value, count = 0, 11 + br.bits(7)
        if len(lengths) + count > hlit + hdist:
            raise DeflateError("code lengths overflow")
        lengths.extend([value] * count)
    lit_lengths, dist_lengths = lengths[:hlit], lengths[hlit:]
    if lit_lengths[256] == 0:
        raise DeflateError("no end-of-block code")
    lit = huffman_table(lit_lengths)
    dist = huffman_table(dist_lengths)
    return lit, dist


def _inflate_block(br, out, lit, dist):
    while True:  # @line L13
        sym = br.decode(lit)  # @line L14
        if sym < 256:  # @line L15
            out.append(sym)
        elif sym == 256:  # @line L16
            return
        else:  # @line L17
            sym -= 257
            if sym >= 29:
                raise DeflateError("invalid length symbol")
            length = LEN_BASE[sym] + br.bits(LEN_EXTRA[sym])  # @line L18
            if dist is None:
                raise DeflateError("distance code used but none defined")
            dsym = br.decode(dist)
            if dsym >= 30:
                raise DeflateError("invalid distance symbol")
            d = DIST_BASE[dsym] + br.bits(DIST_EXTRA[dsym])  # @line L19
            if d > len(out):  # @line L20
                raise DeflateError("distance too far back")
            start = len(out) - d  # @line L21
            if d >= length:
                out += out[start:start + length]
            else:  # the copy overlaps itself: repeat the last d bytes
                chunk = out[start:]
                out += (chunk * (length // d + 1))[:length]


def inflate_raw(data, pos=0, history=b""):
    """Decode a raw DEFLATE stream that starts at byte pos.

    history is a preset dictionary (the zlib FDICT case). Returns the output
    and the position of the first byte after the stream.
    """
    br = BitReader(data, pos)
    out = bytearray(history)  # @line L1
    start = len(history)
    while True:  # @line L2
        final, btype = br.bits(1), br.bits(2)  # @line L3
        if btype == 0:  # @line L4
            br.align()  # @line L5
            n, nlen = br.bits(16), br.bits(16)  # @line L6
            if nlen != n ^ 0xFFFF:  # @line L7
                raise DeflateError("stored block length check failed")
            p = br.byte_pos()
            if p + n > len(data):
                raise DeflateError("unexpected end of input")
            out += data[p:p + n]  # @line L8
            br = BitReader(data, p + n)
        else:  # @line L9
            if btype == 1:  # @line L10
                lit, dist = _FIXED_LIT, _FIXED_DIST
            elif btype == 2:  # @line L11
                lit, dist = _read_dynamic(br)
            else:  # @line L12
                raise DeflateError("invalid block type 3")
            _inflate_block(br, out, lit, dist)
        if final:  # @line L22
            break
    br.align()
    return bytes(out[start:]), br.byte_pos()  # @line L23


def inflate(data):
    """Decode a raw DEFLATE stream (no wrapper)."""
    return inflate_raw(data)[0]


# ---------------------------------------------------------------- matching

_LEVELS = {  # level: (max chain length, lazy matching, nice length)
    1: (4, False, 8), 2: (8, False, 16), 3: (32, False, 32),
    4: (16, True, 16), 5: (32, True, 32), 6: (128, True, 128),
    7: (256, True, 258), 8: (1024, True, 258), 9: (4096, True, 258),
}


def _match_length(buf, a, b, limit):
    """Length of the longest common prefix of buf[a:] and buf[b:], at most limit."""
    if buf[a:a + limit] == buf[b:b + limit]:
        return limit
    lo, hi = 0, limit - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if buf[a:a + mid] == buf[b:b + mid]:
            lo = mid
        else:
            hi = mid - 1
    return lo


def tokenize(data, level=6, history=b""):
    """LZ77 parse of data into literals (int) and matches (length, distance)."""
    chain_max, lazy, nice = _LEVELS[level]
    buf = bytes(history) + bytes(data)
    n = len(buf)
    head = {}
    prev = [-1] * n

    def insert(p):
        if p + 2 < n:
            key = buf[p:p + 3]
            prev[p] = head.get(key, -1)
            head[key] = p

    def longest(p):
        limit = min(MAX_MATCH, n - p)
        if limit < MIN_MATCH:
            return 0, 0
        best_len, best_dist = 0, 0
        c = head.get(buf[p:p + 3], -1)
        chain = chain_max
        while c >= 0 and p - c <= WINDOW and chain > 0:
            if buf[c + best_len] == buf[p + best_len]:
                ln = _match_length(buf, c, p, limit)
                if ln > best_len:
                    best_len, best_dist = ln, p - c
                    if ln >= nice or ln == limit:
                        break
            c = prev[c]
            chain -= 1
        if best_len < MIN_MATCH:
            return 0, 0
        return best_len, best_dist

    for p in range(max(0, len(history) - WINDOW), len(history)):
        insert(p)
    tokens = []
    p = len(history)
    while p < n:
        ln, d = longest(p)
        insert(p)
        if lazy and MIN_MATCH <= ln < nice and p + 1 < n:
            # Lazy matching: if the match at p + 1 is longer, emit a literal.
            if longest(p + 1)[0] > ln:
                tokens.append(buf[p])
                p += 1
                continue
        if ln >= MIN_MATCH:
            tokens.append((ln, d))
            for q in range(p + 1, p + ln):
                insert(q)
            p += ln
        else:
            tokens.append(buf[p])
            p += 1
    return tokens


# ---------------------------------------------------------------- encoder

def limited_lengths(freqs, limit):
    """Optimal code lengths with no length above limit (package-merge)."""
    syms = sorted((f, s) for s, f in enumerate(freqs) if f > 0)
    lengths = [0] * len(freqs)
    if not syms:
        return lengths
    if len(syms) == 1:
        lengths[syms[0][1]] = 1
        return lengths
    if len(syms) > (1 << limit):
        raise ValueError("too many symbols for the length limit")
    leaves = [(f, (s,)) for f, s in syms]
    current = leaves
    for _ in range(limit - 1):
        packages = [(current[i][0] + current[i + 1][0], current[i][1] + current[i + 1][1])
                    for i in range(0, len(current) - 1, 2)]
        current = sorted(leaves + packages, key=lambda item: item[0])
    for _, group in current[:2 * len(syms) - 2]:
        for s in group:
            lengths[s] += 1
    return lengths


def _len_code(length):
    i = bisect_right(LEN_BASE, length) - 1
    if length == 258:
        i = 28
    return i, LEN_EXTRA[i], length - LEN_BASE[i]


def _dist_code(d):
    i = bisect_right(DIST_BASE, d) - 1
    return i, DIST_EXTRA[i], d - DIST_BASE[i]


_LEN_TAB = [None] * 3 + [_len_code(k) for k in range(3, 259)]


def _encoder(lengths):
    codes = canonical_codes(lengths)
    return [(_reverse(c, ln), ln) for c, ln in zip(codes, lengths)]


_FIXED_LIT_ENC = _encoder(FIXED_LIT_LENGTHS)
_FIXED_DIST_ENC = _encoder(FIXED_DIST_LENGTHS)


def _symbols(tokens):
    """Turn tokens into (lit/len symbol, extra) and (dist symbol, extra) entries."""
    out = []
    for t in tokens:
        if isinstance(t, int):
            out.append((t, 0, 0, -1, 0, 0))
        else:
            ln, d = t
            ls, le, lv = _LEN_TAB[ln]
            ds, de, dv = _dist_code(d)
            out.append((257 + ls, le, lv, ds, de, dv))
    out.append((256, 0, 0, -1, 0, 0))
    return out


def _rle_lengths(lengths):
    """Code length sequence with the repeat codes 16, 17 and 18."""
    out = []
    i, n = 0, len(lengths)
    while i < n:
        v = lengths[i]
        run = 1
        while i + run < n and lengths[i + run] == v:
            run += 1
        if v == 0 and run >= 3:
            k = run
            while k >= 11:
                m = min(k, 138)
                out.append((18, 7, m - 11))
                k -= m
            if k >= 3:
                out.append((17, 3, k - 3))
                k = 0
            out.extend([(0, 0, 0)] * k)
        elif v != 0 and run >= 4:
            out.append((v, 0, 0))
            k = run - 1
            while k >= 3:
                m = min(k, 6)
                out.append((16, 2, m - 3))
                k -= m
            out.extend([(v, 0, 0)] * k)
        else:
            out.extend([(v, 0, 0)] * run)
        i += run
    return out


def _write_symbols(bw, syms, lit_enc, dist_enc):
    for ls, le, lv, ds, de, dv in syms:
        code, ln = lit_enc[ls]
        bw.write(code, ln)
        if ds >= 0:
            if le:
                bw.write(lv, le)
            code, ln = dist_enc[ds]
            bw.write(code, ln)
            if de:
                bw.write(dv, de)


def _dynamic_header(lit_lengths, dist_lengths):
    """The bits of a dynamic block header, after BFINAL and BTYPE."""
    hlit = max(257, max(i for i, ln in enumerate(lit_lengths) if ln) + 1)
    used = [i for i, ln in enumerate(dist_lengths) if ln]
    hdist = max(1, used[-1] + 1) if used else 1
    seq = _rle_lengths(lit_lengths[:hlit] + dist_lengths[:hdist])
    cl_freq = [0] * 19
    for s, _, _ in seq:
        cl_freq[s] += 1
    cl_lengths = limited_lengths(cl_freq, 7)
    if sum(1 for ln in cl_lengths if ln) == 1:  # keep the code complete
        other = 0 if cl_lengths[0] == 0 else 1
        cl_lengths[other] = 1
    cl_enc = _encoder(cl_lengths)
    hclen = 19
    while hclen > 4 and cl_lengths[CL_ORDER[hclen - 1]] == 0:
        hclen -= 1
    bw = BitWriter()
    bw.write(hlit - 257, 5)
    bw.write(hdist - 1, 5)
    bw.write(hclen - 4, 4)
    for i in range(hclen):
        bw.write(cl_lengths[CL_ORDER[i]], 3)
    for s, eb, ev in seq:
        code, ln = cl_enc[s]
        bw.write(code, ln)
        if eb:
            bw.write(ev, eb)
    return bw


def _cost(syms, lit_lengths, dist_lengths):
    bits = 0
    for ls, le, _, ds, de, _ in syms:
        bits += lit_lengths[ls] + le
        if ds >= 0:
            bits += dist_lengths[ds] + de
    return bits


def _write_stored(bw, chunk, final):
    pieces = [chunk[i:i + 65535] for i in range(0, len(chunk), 65535)] or [b""]
    for k, piece in enumerate(pieces):
        bw.write(1 if final and k == len(pieces) - 1 else 0, 1)
        bw.write(0, 2)
        bw.align()
        bw.write(len(piece), 16)
        bw.write(len(piece) ^ 0xFFFF, 16)
        bw.out += piece
    return bw


def deflate(data, level=6, history=b"", block_tokens=16384):
    """Compress data into a raw DEFLATE stream.

    Level 0 writes stored blocks only. Levels 1 to 9 choose the match finder
    effort; each block is then written as the cheapest of stored, fixed
    Huffman and dynamic Huffman.
    """
    data = bytes(data)
    bw = BitWriter()
    if level == 0:
        return _write_stored(bw, data, True).finish()
    tokens = tokenize(data, level, history)
    blocks = [tokens[i:i + block_tokens] for i in range(0, len(tokens), block_tokens)] or [[]]
    pos = 0
    for b, block in enumerate(blocks):
        final = b == len(blocks) - 1
        size = sum(1 if isinstance(t, int) else t[0] for t in block)
        chunk = data[pos:pos + size]
        pos += size
        syms = _symbols(block)
        lit_freq = [0] * 286
        dist_freq = [0] * 30
        for ls, _, _, ds, _, _ in syms:
            lit_freq[ls] += 1
            if ds >= 0:
                dist_freq[ds] += 1
        if sum(1 for f in lit_freq if f) < 2:
            lit_freq[0 if lit_freq[0] == 0 else 1] += 1
        while sum(1 for f in dist_freq if f) < 2:
            dist_freq[dist_freq.index(0)] += 1
        lit_lengths = limited_lengths(lit_freq, 15)
        dist_lengths = limited_lengths(dist_freq, 15)
        header = _dynamic_header(lit_lengths, dist_lengths)
        dyn_bits = 3 + header.bit_length() + _cost(syms, lit_lengths, dist_lengths)
        fix_bits = 3 + _cost(syms, FIXED_LIT_LENGTHS, FIXED_DIST_LENGTHS)
        npieces = max(1, -(-len(chunk) // 65535))
        stored_bits = npieces * 40 + 7 + 8 * len(chunk)
        best = min(stored_bits, fix_bits, dyn_bits)
        if best == stored_bits:
            _write_stored(bw, chunk, final)
        elif best == fix_bits:
            bw.write(1 if final else 0, 1)
            bw.write(1, 2)
            _write_symbols(bw, syms, _FIXED_LIT_ENC, _FIXED_DIST_ENC)
        else:
            bw.write(1 if final else 0, 1)
            bw.write(2, 2)
            for byte in header.out:
                bw.write(byte, 8)
            if header.cnt:
                bw.write(header.buf, header.cnt)
            _write_symbols(bw, syms, _encoder(lit_lengths), _encoder(dist_lengths))
    return bw.finish()


# ---------------------------------------------------------------- wrappers

def zlib_compress(data, level=6, zdict=None):
    """RFC 1950: CMF, FLG, optional DICTID, DEFLATE data, Adler-32 (big endian)."""
    cmf = 0x78  # CM = 8 (deflate), CINFO = 7 (32 KiB window)
    flevel = 0 if level < 2 else 1 if level < 6 else 2 if level == 6 else 3
    flg = flevel << 6
    if zdict is not None:
        flg |= 0x20
    flg += 31 - ((cmf << 8) | flg) % 31
    out = bytearray([cmf, flg])
    if zdict is not None:
        out += adler32(zdict).to_bytes(4, "big")
    out += deflate(data, level, history=zdict or b"")
    out += adler32(data).to_bytes(4, "big")
    return bytes(out)


def zlib_decompress(data, zdict=None):
    if len(data) < 6:
        raise DeflateError("zlib stream too short")
    cmf, flg = data[0], data[1]
    if cmf & 15 != 8 or cmf >> 4 > 7:
        raise DeflateError("not a deflate zlib stream")
    if ((cmf << 8) | flg) % 31:
        raise DeflateError("FCHECK failed")
    pos = 2
    history = b""
    if flg & 0x20:
        if zdict is None:
            raise DeflateError("a preset dictionary is needed")
        if int.from_bytes(data[2:6], "big") != adler32(zdict):
            raise DeflateError("wrong preset dictionary")
        history, pos = bytes(zdict), 6
    out, end = inflate_raw(data, pos, history)
    if end + 4 > len(data):
        raise DeflateError("missing Adler-32")
    if int.from_bytes(data[end:end + 4], "big") != adler32(out):
        raise DeflateError("Adler-32 mismatch")
    return out


def gzip_compress(data, level=6, mtime=0, name=None):
    """RFC 1952: a single gzip member with CRC-32 and ISIZE (little endian)."""
    flg = 0x08 if name else 0
    xfl = 2 if level == 9 else 4 if level == 1 else 0
    out = bytearray([0x1F, 0x8B, 8, flg]) + mtime.to_bytes(4, "little") + bytes([xfl, 255])
    if name:
        out += name + b"\x00"
    out += deflate(data, level)
    out += crc32(data).to_bytes(4, "little")
    out += (len(data) & 0xFFFFFFFF).to_bytes(4, "little")
    return bytes(out)


def gzip_decompress(data):
    """Decode one or more concatenated gzip members."""
    out = bytearray()
    pos = 0
    while pos < len(data):
        if data[pos:pos + 3] != b"\x1f\x8b\x08":
            raise DeflateError("not a gzip member")
        if len(data) < pos + 10:
            raise DeflateError("gzip header too short")
        flg = data[pos + 3]
        if flg & 0xE0:
            raise DeflateError("reserved FLG bits set")
        p = pos + 10
        if flg & 0x04:  # FEXTRA
            xlen = int.from_bytes(data[p:p + 2], "little")
            p += 2 + xlen
        for bit in (0x08, 0x10):  # FNAME, FCOMMENT: zero-terminated
            if flg & bit:
                z = data.index(0, p)
                p = z + 1
        if flg & 0x02:  # FHCRC: low 16 bits of the CRC-32 of the header
            if int.from_bytes(data[p:p + 2], "little") != crc32(data[pos:p]) & 0xFFFF:
                raise DeflateError("header CRC mismatch")
            p += 2
        member, end = inflate_raw(data, p)
        if end + 8 > len(data):
            raise DeflateError("missing gzip trailer")
        if int.from_bytes(data[end:end + 4], "little") != crc32(member):
            raise DeflateError("CRC-32 mismatch")
        if int.from_bytes(data[end + 4:end + 8], "little") != len(member) & 0xFFFFFFFF:
            raise DeflateError("ISIZE mismatch")
        out += member
        pos = end + 8
    return bytes(out)
