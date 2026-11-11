# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brotli/. The authors are listed in prov/EH674F.jsonl.
"""Brotli (RFC 7932): a decoder and a simple encoder.

decompress() reads the full format of RFC 7932: compressed, uncompressed
and metadata meta-blocks, simple and complex prefix codes, block types
and block counts for the three categories, the four literal context
modes, context maps with run-length codes and the inverse move-to-front
transform, NPOSTFIX and NDIRECT, the distance ring buffer, and static
dictionary words with all 121 transforms. The static dictionary itself
(122,784 bytes, RFC 7932 Appendix A) is not bundled. Pass it in as
`dictionary`; a stream that uses a dictionary word without it raises
BrotliError.

compress() writes valid streams with a small subset of the tools: one
block type per category, one literal tree and one distance tree,
NPOSTFIX = 0, NDIRECT = 0, greedy LZ77 parsing with hash chains, and
uncompressed meta-blocks where they are smaller. It never uses the
static dictionary.
"""

# ---------------------------------------------------------------- tables

# RFC 7932 Section 5: insert length codes and copy length codes.
INSERT_BASE = [0, 1, 2, 3, 4, 5, 6, 8, 10, 14, 18, 26, 34, 50, 66, 98, 130,
               194, 322, 578, 1090, 2114, 6210, 22594]
INSERT_EXTRA = [0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9,
                10, 12, 14, 24]
COPY_BASE = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 18, 22, 30, 38, 54, 70, 102,
             134, 198, 326, 582, 1094, 2118]
COPY_EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8,
              9, 10, 24]

# The 64-code cells of the insert-and-copy alphabet: (insert code base,
# copy code base). Cells 0 and 1 also mean "distance code 0".
CELLS = [(0, 0), (0, 8), (0, 0), (0, 8), (8, 0), (8, 8), (0, 16), (16, 0),
         (8, 16), (16, 8), (16, 16)]

# RFC 7932 Section 6: block count codes.
BLOCK_BASE = [1, 5, 9, 13, 17, 25, 33, 41, 49, 65, 81, 97, 113, 145, 177,
              209, 241, 305, 369, 497, 753, 1265, 2289, 4337, 8433, 16625]
BLOCK_EXTRA = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 7, 8, 9,
               10, 11, 12, 13, 24]

# RFC 7932 Section 3.5: the order of the code length code lengths.
CL_ORDER = [1, 2, 3, 4, 0, 5, 17, 6, 16, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# RFC 7932 Section 7.1: context lookup tables.
LUT0 = bytes([
    0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    8, 12, 16, 12, 12, 20, 12, 16, 24, 28, 12, 12, 32, 12, 36, 12,
    44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 32, 32, 24, 40, 28, 12,
    12, 48, 52, 52, 52, 48, 52, 52, 52, 48, 52, 52, 52, 52, 52, 48,
    52, 52, 52, 52, 52, 48, 52, 52, 52, 52, 52, 24, 12, 28, 12, 12,
    12, 56, 60, 60, 60, 56, 60, 60, 60, 56, 60, 60, 60, 60, 60, 56,
    60, 60, 60, 60, 60, 56, 60, 60, 60, 60, 60, 24, 12, 28, 12, 0]
    + [0, 1] * 32 + [2, 3] * 32)
LUT1 = bytes(
    [0] * 32 + [0] + [1] * 15 + [2] * 10 + [1] * 6 + [1] + [2] * 26
    + [1] * 5 + [1] + [3] * 26 + [1] * 4 + [0] + [0] * 96 + [2] * 32)
LUT2 = bytes([0] + [1] * 15 + [2] * 48 + [3] * 64 + [4] * 64 + [5] * 48
             + [6] * 15 + [7])

# RFC 7932 Section 8 and Appendix A: the static dictionary layout.
NDBITS = [0, 0, 0, 0, 10, 10, 11, 11, 10, 10, 10, 10, 10, 9, 9, 8, 7, 7, 8,
          7, 7, 6, 6, 5, 5]
DOFFSET = [0] * 25
for _n in range(24):
    DOFFSET[_n + 1] = DOFFSET[_n] + (_n * (1 << NDBITS[_n]) if _n >= 4 else 0)
DICT_SIZE = DOFFSET[24] + 24 * (1 << NDBITS[24])        # 122784

# RFC 7932 Appendix B: (prefix, elementary transform, suffix). The
# elementary transforms are 0 Identity, 1 FermentFirst, 2 FermentAll,
# 3..11 OmitFirst1..9 and 12..20 OmitLast1..9.
_I, _FF, _FA = 0, 1, 2
_OF = [None] + list(range(3, 12))
_OL = [None] + list(range(12, 21))
TRANSFORMS = [
    (b"", _I, b""), (b"", _I, b" "), (b" ", _I, b" "), (b"", _OF[1], b""),
    (b"", _FF, b" "), (b"", _I, b" the "), (b" ", _I, b""), (b"s ", _I, b" "),
    (b"", _I, b" of "), (b"", _FF, b""), (b"", _I, b" and "), (b"", _OF[2], b""),
    (b"", _OL[1], b""), (b", ", _I, b" "), (b"", _I, b", "), (b" ", _FF, b" "),
    (b"", _I, b" in "), (b"", _I, b" to "), (b"e ", _I, b" "), (b"", _I, b"\""),
    (b"", _I, b"."), (b"", _I, b"\">"), (b"", _I, b"\n"), (b"", _OL[3], b""),
    (b"", _I, b"]"), (b"", _I, b" for "), (b"", _OF[3], b""), (b"", _OL[2], b""),
    (b"", _I, b" a "), (b"", _I, b" that "), (b" ", _FF, b""), (b"", _I, b". "),
    (b".", _I, b""), (b" ", _I, b", "), (b"", _OF[4], b""), (b"", _I, b" with "),
    (b"", _I, b"'"), (b"", _I, b" from "), (b"", _I, b" by "), (b"", _OF[5], b""),
    (b"", _OF[6], b""), (b" the ", _I, b""), (b"", _OL[4], b""), (b"", _I, b". The "),
    (b"", _FA, b""), (b"", _I, b" on "), (b"", _I, b" as "), (b"", _I, b" is "),
    (b"", _OL[7], b""), (b"", _OL[1], b"ing "), (b"", _I, b"\n\t"), (b"", _I, b":"),
    (b" ", _I, b". "), (b"", _I, b"ed "), (b"", _OF[9], b""), (b"", _OF[7], b""),
    (b"", _OL[6], b""), (b"", _I, b"("), (b"", _FF, b", "), (b"", _OL[8], b""),
    (b"", _I, b" at "), (b"", _I, b"ly "), (b" the ", _I, b" of "), (b"", _OL[5], b""),
    (b"", _OL[9], b""), (b" ", _FF, b", "), (b"", _FF, b"\""), (b".", _I, b"("),
    (b"", _FA, b" "), (b"", _FF, b"\">"), (b"", _I, b"=\""), (b" ", _I, b"."),
    (b".com/", _I, b""), (b" the ", _I, b" of the "), (b"", _FF, b"'"),
    (b"", _I, b". This "), (b"", _I, b","), (b".", _I, b" "), (b"", _FF, b"("),
    (b"", _FF, b"."), (b"", _I, b" not "), (b" ", _I, b"=\""), (b"", _I, b"er "),
    (b" ", _FA, b" "), (b"", _I, b"al "), (b" ", _FA, b""), (b"", _I, b"='"),
    (b"", _FA, b"\""), (b"", _FF, b". "), (b" ", _I, b"("), (b"", _I, b"ful "),
    (b" ", _FF, b". "), (b"", _I, b"ive "), (b"", _I, b"less "), (b"", _FA, b"'"),
    (b"", _I, b"est "), (b" ", _FF, b"."), (b"", _FA, b"\">"), (b" ", _I, b"='"),
    (b"", _FF, b","), (b"", _I, b"ize "), (b"", _FA, b"."), (b"\xc2\xa0", _I, b""),
    (b" ", _I, b","), (b"", _FF, b"=\""), (b"", _FA, b"=\""), (b"", _I, b"ous "),
    (b"", _FA, b", "), (b"", _FF, b"='"), (b" ", _FF, b","), (b" ", _FA, b"=\""),
    (b" ", _FA, b", "), (b"", _FA, b","), (b"", _FA, b"("), (b"", _FA, b". "),
    (b" ", _FA, b"."), (b"", _FA, b"='"), (b" ", _FA, b". "), (b" ", _FF, b"=\""),
    (b" ", _FA, b"='"), (b" ", _FF, b"='"),
]


class BrotliError(ValueError):
    pass


# ---------------------------------------------------------------- bit I/O

class _Reader:
    """Bits from bytes, least significant bit of each byte first."""

    def __init__(self, data):
        self.data, self.pos, self.buf, self.cnt = data, 0, 0, 0

    def _fill(self, n):
        while self.cnt < n and self.pos < len(self.data):
            self.buf |= self.data[self.pos] << self.cnt
            self.pos += 1
            self.cnt += 8

    def bits(self, n):
        if n == 0:
            return 0
        self._fill(n)
        if self.cnt < n:
            raise BrotliError("unexpected end of input")
        v = self.buf & ((1 << n) - 1)
        self.buf >>= n
        self.cnt -= n
        return v

    def symbol(self, code):
        table, maxlen = code
        if maxlen == 0:
            return table                     # a code with one symbol
        self._fill(maxlen)
        entry = table[self.buf & ((1 << maxlen) - 1)]
        ln = entry & 15
        if ln > self.cnt:
            raise BrotliError("unexpected end of input")
        self.buf >>= ln
        self.cnt -= ln
        return entry >> 4

    def align(self):
        """Skip to the next byte boundary; the skipped bits must be 0."""
        if self.bits(self.cnt & 7):
            raise BrotliError("nonzero padding bits")

    def take(self, n):
        """n whole bytes, after align()."""
        out = bytearray()
        while n and self.cnt:
            out.append(self.bits(8))
            n -= 1
        if self.pos + n > len(self.data):
            raise BrotliError("unexpected end of input")
        out += self.data[self.pos:self.pos + n]
        self.pos += n
        return out


class _Writer:
    def __init__(self):
        self.out, self.buf, self.cnt = bytearray(), 0, 0

    def write(self, value, n):
        self.buf |= value << self.cnt
        self.cnt += n
        while self.cnt >= 8:
            self.out.append(self.buf & 0xFF)
            self.buf >>= 8
            self.cnt -= 8

    def align(self):
        if self.cnt & 7:
            self.write(0, 8 - (self.cnt & 7))


# ---------------------------------------------------------------- prefix codes

def _canonical(lengths):
    """Canonical codes (RFC 7932 Section 3.2), MSB first."""
    maxlen = max(lengths, default=0)
    count = [0] * (maxlen + 2)
    for ln in lengths:
        count[ln] += 1
    count[0] = 0
    nxt, code = [0] * (maxlen + 2), 0
    for b in range(1, maxlen + 1):
        code = (code + count[b - 1]) << 1
        nxt[b] = code
    codes = [0] * len(lengths)
    for s, ln in enumerate(lengths):
        if ln:
            codes[s] = nxt[ln]
            nxt[ln] += 1
    return codes


def _reverse(code, n):
    r = 0
    for _ in range(n):
        r = (r << 1) | (code & 1)
        code >>= 1
    return r


def _table(lengths):
    """A lookup table indexed by the next maxlen input bits.

    The lengths must form a complete prefix code."""
    maxlen = max(lengths)
    if sum(1 << (maxlen - ln) for ln in lengths if ln) != 1 << maxlen:
        raise BrotliError("incomplete or over-full prefix code")
    codes = _canonical(lengths)
    table = [0] * (1 << maxlen)
    for s, ln in enumerate(lengths):
        if ln:
            r = _reverse(codes[s], ln)
            step = 1 << ln
            table[r::step] = [(s << 4) | ln] * len(range(r, 1 << maxlen, step))
    return table, maxlen


def _read_code(br, size):
    """Read one prefix code over an alphabet of `size` symbols (3.4, 3.5)."""
    hskip = br.bits(2)
    if hskip == 1:                                      # simple prefix code
        nsym = br.bits(2) + 1
        width = (size - 1).bit_length()
        syms = [br.bits(width) for _ in range(nsym)]
        if any(s >= size for s in syms) or len(set(syms)) != nsym:
            raise BrotliError("bad simple prefix code")
        if nsym == 1:
            return syms[0], 0
        if nsym == 4 and br.bits(1):
            shape = [1, 2, 3, 3]
        else:
            shape = {2: [1, 1], 3: [1, 2, 2], 4: [2, 2, 2, 2]}[nsym]
        lengths = [0] * size
        for s, ln in zip(syms, shape):
            lengths[s] = ln
        return _table(lengths)
    # Complex prefix code: first the code length code lengths.
    cl = [0] * 18
    space, used = 32, 0
    for i in range(hskip, 18):
        if space <= 0:
            break
        v = br.bits(2)                    # the fixed code of Section 3.5
        if v == 3:
            v = 2 if br.bits(1) == 0 else (1 if br.bits(1) == 0 else 5)
        elif v == 2:
            v = 3
        elif v == 1:
            v = 4
        cl[CL_ORDER[i]] = v
        if v:
            space -= 32 >> v
            used += 1
    if used != 1 and space != 0:
        raise BrotliError("bad code length code")
    if used == 1:
        clcode = (next(s for s in range(18) if cl[s]), 0)
    else:
        clcode = _table(cl)
    # Then the symbol code lengths, with the repeat codes 16 and 17.
    lengths = [0] * size
    sym, prev, space = 0, 8, 32768
    repeat, repeat_len = 0, 0
    while sym < size and space > 0:
        c = br.symbol(clcode)
        if c < 16:
            repeat = 0
            lengths[sym] = c
            sym += 1
            if c:
                prev = c
                space -= 32768 >> c
            continue
        nbits, value = (2, prev) if c == 16 else (3, 0)
        if repeat_len != value:
            repeat, repeat_len = 0, value
        old = repeat
        if repeat > 0:
            repeat = (repeat - 2) << nbits
        repeat += br.bits(nbits) + 3
        delta = repeat - old
        if sym + delta > size:
            raise BrotliError("code lengths run past the alphabet")
        for k in range(sym, sym + delta):
            lengths[k] = value
        sym += delta
        if value:
            space -= delta * (32768 >> value)
    if space != 0:
        raise BrotliError("incomplete or over-full prefix code")
    return _table(lengths)


def _read_count(br):
    """NBLTYPES or NTREES: 1..256 (Section 9.2)."""
    if br.bits(1) == 0:
        return 1
    n = br.bits(3)
    return (1 << n) + 1 + br.bits(n)


def _read_context_map(br, size, ntrees):
    if ntrees == 1:
        return bytearray(size)
    rlemax = br.bits(4) + 1 if br.bits(1) else 0
    code = _read_code(br, ntrees + rlemax)
    cmap, i = bytearray(size), 0
    while i < size:
        s = br.symbol(code)
        if s == 0:
            i += 1
        elif s <= rlemax:
            run = (1 << s) + br.bits(s)
            if i + run > size:
                raise BrotliError("context map run too long")
            i += run                                    # zeros already there
        else:
            cmap[i] = s - rlemax
            i += 1
    if br.bits(1):                                      # inverse move-to-front
        mtf = list(range(256))
        for i in range(size):
            k = cmap[i]
            v = mtf.pop(k)
            mtf.insert(0, v)
            cmap[i] = v
    return cmap


class _Blocks:
    """Block types and block counts of one category (Section 6)."""

    def __init__(self, br):
        self.n = _read_count(br)
        self.type, self.prev = 0, 1
        if self.n >= 2:
            self.tcode = _read_code(br, self.n + 2)
            self.ccode = _read_code(br, 26)
            self.left = self._count(br)
        else:
            self.left = 1 << 24

    def _count(self, br):
        c = br.symbol(self.ccode)
        return BLOCK_BASE[c] + br.bits(BLOCK_EXTRA[c])

    def step(self, br):
        """Switch the block type if the count is 0, then use one element."""
        if self.left == 0:
            t = br.symbol(self.tcode)
            t = self.prev if t == 0 else (self.type + 1) % self.n if t == 1 else t - 2
            if t >= self.n:
                raise BrotliError("block type out of range")
            self.prev, self.type = self.type, t
            self.left = self._count(br)
        self.left -= 1
        return self.type


# ---------------------------------------------------------------- decoder

def _window_bits(br):
    if br.bits(1) == 0:
        return 16
    n = br.bits(3)
    if n:
        return 17 + n
    m = br.bits(3)
    if m == 1:
        raise BrotliError("invalid window size")
    return 8 + m if m else 17


def _distance(code, rb, npostfix, ndirect, br):
    """The distance for distance code `code` (Section 4)."""
    if code < 16:
        if code < 4:
            d = rb[3 - code]
        else:
            d = rb[3 if code < 10 else 2] + (-1, 1, -2, 2, -3, 3)[(code - 4) % 6]
        if d <= 0:
            raise BrotliError("distance not positive")
        return d
    if code < 16 + ndirect:
        return code - 15
    c = code - ndirect - 16
    nbits = 1 + (c >> (npostfix + 1))
    hcode, lcode = c >> npostfix, c & ((1 << npostfix) - 1)
    offset = ((2 + (hcode & 1)) << nbits) - 4
    return ((offset + br.bits(nbits)) << npostfix) + lcode + ndirect + 1


def _ferment(w, i):
    if w[i] < 192:
        if 97 <= w[i] <= 122:
            w[i] ^= 32
        return 1
    if w[i] < 224:
        if i + 1 < len(w):
            w[i + 1] ^= 32
        return 2
    if i + 2 < len(w):
        w[i + 2] ^= 5
    return 3


def dictionary_word(dictionary, length, word_id):
    """The static dictionary word for a copy length and word id (Section 8)."""
    if not 4 <= length <= 24:
        raise BrotliError("bad dictionary word length")
    if dictionary is None:
        raise BrotliError("the stream uses the static dictionary; pass it in")
    nbits = NDBITS[length]
    index, t = word_id & ((1 << nbits) - 1), word_id >> nbits
    if t >= len(TRANSFORMS):
        raise BrotliError("bad transform id")
    start = DOFFSET[length] + index * length
    word = bytearray(dictionary[start:start + length])
    prefix, kind, suffix = TRANSFORMS[t]
    if kind == _FF:
        if word:
            _ferment(word, 0)
    elif kind == _FA:
        i = 0
        while i < len(word):
            i += _ferment(word, i)
    elif 3 <= kind <= 11:
        word = word[kind - 2:]
    elif kind >= 12:
        word = word[:max(0, len(word) - (kind - 11))]
    return prefix + bytes(word) + suffix


def _context(mode, p1, p2):
    if mode == 0:
        return p1 & 0x3F
    if mode == 1:
        return p1 >> 2
    if mode == 2:
        return LUT0[p1] | LUT1[p2]
    return (LUT2[p1] << 3) | LUT2[p2]


def _meta_block(br, out, mlen, rb, window, dictionary):
    lit_b, cmd_b, dst_b = _Blocks(br), _Blocks(br), _Blocks(br)
    npostfix = br.bits(2)
    ndirect = br.bits(4) << npostfix
    modes = [br.bits(2) for _ in range(lit_b.n)]
    ntreesl = _read_count(br)
    cmapl = _read_context_map(br, 64 * lit_b.n, ntreesl)
    ntreesd = _read_count(br)
    cmapd = _read_context_map(br, 4 * dst_b.n, ntreesd)
    lit_codes = [_read_code(br, 256) for _ in range(ntreesl)]
    cmd_codes = [_read_code(br, 704) for _ in range(cmd_b.n)]
    dsize = 16 + ndirect + (48 << npostfix)
    dst_codes = [_read_code(br, dsize) for _ in range(ntreesd)]
    _commands(br, out, mlen, rb, window, dictionary, npostfix, ndirect,
              lit_b, cmd_b, dst_b, modes, cmapl, cmapd,
              lit_codes, cmd_codes, dst_codes)


def _commands(br, out, mlen, rb, window, dictionary, npostfix, ndirect,
              lit_b, cmd_b, dst_b, modes, cmapl, cmapd,
              lit_codes, cmd_codes, dst_codes):
    end = len(out) + mlen                                    # @line L1
    while len(out) < end:                                    # @line L2
        code = br.symbol(cmd_codes[cmd_b.step(br)])          # @line L3
        ibase, cbase = CELLS[code >> 6]                      # @line L4
        ic, cc = ibase + ((code >> 3) & 7), cbase + (code & 7)
        ilen = INSERT_BASE[ic] + br.bits(INSERT_EXTRA[ic])
        clen = COPY_BASE[cc] + br.bits(COPY_EXTRA[cc])
        if len(out) + ilen > end:
            raise BrotliError("insert length runs past the meta-block")
        for _ in range(ilen):                                # @line L5
            t = lit_b.step(br)                               # @line L6
            n = len(out)
            p1 = out[n - 1] if n else 0
            p2 = out[n - 2] if n > 1 else 0
            ctx = _context(modes[t], p1, p2)
            out.append(br.symbol(lit_codes[cmapl[64 * t + ctx]]))   # @line L7
        if len(out) == end:                                  # @line L8
            break
        if code < 128:                                       # @line L9
            d = rb[3]
        else:                                                # @line L10
            t = dst_b.step(br)
            k = br.symbol(dst_codes[cmapd[4 * t + min(clen, 5) - 2]])
            d = _distance(k, rb, npostfix, ndirect, br)
        max_d = min(window, len(out))
        if d <= max_d:                                       # @line L11
            if code >= 128 and k != 0:
                rb[:] = rb[1:] + [d]
            if len(out) + clen > end:
                raise BrotliError("copy runs past the meta-block")
            start = len(out) - d
            if d >= clen:
                out += out[start:start + clen]
            else:
                for i in range(clen):
                    out.append(out[start + i])
        else:                                                # @line L12
            word = dictionary_word(dictionary, clen, d - max_d - 1)
            if len(out) + len(word) > end:
                raise BrotliError("dictionary word runs past the meta-block")
            out += word


def decompress(data, dictionary=None):
    """Decode one Brotli stream. `dictionary` is the 122,784-byte static
    dictionary of RFC 7932 Appendix A, needed only if the stream uses it."""
    if dictionary is not None and len(dictionary) != DICT_SIZE:
        raise ValueError("the static dictionary has 122784 bytes")
    br = _Reader(data)
    window = (1 << _window_bits(br)) - 16
    out = bytearray()
    rb = [16, 15, 11, 4]                     # fourth-to-last ... last distance
    while True:
        last = br.bits(1)
        if last and br.bits(1):                              # ISLASTEMPTY
            break
        nibbles = br.bits(2)
        if nibbles == 3:                                     # metadata
            if br.bits(1):
                raise BrotliError("reserved bit set")
            nbytes = br.bits(2)
            skip = 0
            if nbytes:
                skip = br.bits(8 * nbytes)
                if nbytes > 1 and skip >> (8 * nbytes - 8) == 0:
                    raise BrotliError("MSKIPLEN has a zero last byte")
                skip += 1
            br.align()
            br.take(skip)
            if last:
                break
            continue
        nibbles += 4
        mlen = br.bits(4 * nibbles)
        if nibbles > 4 and mlen >> (4 * nibbles - 4) == 0:
            raise BrotliError("MLEN has a zero last nibble")
        mlen += 1
        if not last and br.bits(1):                          # ISUNCOMPRESSED
            br.align()
            out += br.take(mlen)
            continue
        _meta_block(br, out, mlen, rb, window, dictionary)
        if last:
            break
    if br.buf != 0 or br.cnt >= 8 or br.pos != len(data):
        raise BrotliError("data after the end of the stream")
    return bytes(out)


# ---------------------------------------------------------------- encoder

MIN_MATCH = 4
META_MAX = 1 << 18


def limited_lengths(freqs, limit):
    """Optimal code lengths with no length above limit (package-merge)."""
    syms = sorted((f, s) for s, f in enumerate(freqs) if f > 0)
    lengths = [0] * len(freqs)
    if len(syms) == 1:
        lengths[syms[0][1]] = 1
        return lengths
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


class _Code:
    """An encoder's prefix code: lengths and LSB-first bit patterns."""

    def __init__(self, freqs, size):
        used = [s for s in range(size) if freqs[s]]
        if len(used) <= 1:
            self.single = used[0] if used else 0
            self.lengths = [0] * size
        else:
            self.single = None
            self.lengths = limited_lengths(freqs, 15)
        codes = _canonical(self.lengths)
        self.bits = [_reverse(codes[s], ln) for s, ln in enumerate(self.lengths)]
        self.size = size

    def put(self, ops, s):
        ln = self.lengths[s]
        if ln:
            ops.append((self.bits[s], ln))


def _repeat_extras(r, nbits):
    """Extra values for a run of r >= 3 repeats with code 16 or 17."""
    r -= 3
    out = []
    while True:
        out.append(r & ((1 << nbits) - 1))
        r >>= nbits
        if r == 0:
            return out[::-1]
        r -= 1


def _write_code(ops, code):
    size, lengths = code.size, code.lengths
    width = (size - 1).bit_length()
    used = sorted((lengths[s], s) for s in range(size) if lengths[s])
    if code.single is not None or len(used) <= 4:
        syms = [code.single] if code.single is not None else [s for _, s in used]
        ops.append((1, 2))
        ops.append((len(syms) - 1, 2))
        for s in syms:
            ops.append((s, width))
        if len(syms) == 4:
            ops.append((1 if used[-1][0] == 3 else 0, 1))
        return
    # Complex code: run-length tokens over the code lengths.
    last = max(s for _, s in used)
    tokens, prev, i = [], 8, 0
    while i <= last:
        v, j = lengths[i], i
        while j <= last and lengths[j] == v:
            j += 1
        r = j - i
        if v == 0:
            if r < 3:
                tokens += [(0, 0)] * r
            else:
                tokens += [(17, e) for e in _repeat_extras(r, 3)]
        else:
            if v != prev:
                tokens.append((v, 0))
                prev, r = v, r - 1
            if r < 3:
                tokens += [(v, 0)] * r
            else:
                tokens += [(16, e) for e in _repeat_extras(r, 2)]
        i = j
    freqs = [0] * 18
    for s, _ in tokens:
        freqs[s] += 1
    cl = limited_lengths(freqs, 5)
    nonzero = sum(1 for v in cl if v)
    hskip = 0
    if cl[1] == 0 and cl[2] == 0:
        hskip = 3 if cl[3] == 0 else 2
    order = CL_ORDER[hskip:]
    if nonzero >= 2:
        order = order[:max(i for i, s in enumerate(order) if cl[s]) + 1]
    ops.append((hskip, 2))
    fixed = {0: (0, 2), 1: (7, 4), 2: (3, 3), 3: (2, 2), 4: (1, 2), 5: (15, 4)}
    for s in order:
        ops.append(fixed[cl[s]])
    clc = [0] * 18 if nonzero == 1 else cl
    clbits = [_reverse(c, ln) for c, ln in zip(_canonical(clc), clc)]
    for s, e in tokens:
        if clc[s]:
            ops.append((clbits[s], clc[s]))
        if s == 16:
            ops.append((e, 2))
        elif s == 17:
            ops.append((e, 3))


def _code_of(base, value):
    c = 0
    while c + 1 < len(base) and base[c + 1] <= value:
        c += 1
    return c


def _dist_symbol(d):
    """Distance code and extra bits for NPOSTFIX = 0, NDIRECT = 0."""
    v = d + 3
    nbits = v.bit_length() - 2
    return 16 + 2 * (nbits - 1) + ((v >> nbits) & 1), nbits, v & ((1 << nbits) - 1)


def _match_len(data, a, b, limit):
    k = 0
    while k + 32 <= limit and data[a + k:a + k + 32] == data[b + k:b + k + 32]:
        k += 32
    while k < limit and data[a + k] == data[b + k]:
        k += 1
    return k


class _Finder:
    """Hash chains over 4-byte strings."""

    def __init__(self, data, depth, window):
        self.data, self.depth, self.window = data, depth, window
        self.head, self.prev = {}, [-1] * len(data)

    def insert(self, p):
        key = self.data[p:p + MIN_MATCH]
        if len(key) == MIN_MATCH:
            self.prev[p] = self.head.get(key, -1)
            self.head[key] = p

    def find(self, p, end):
        best, best_d = 0, 0
        c = self.head.get(self.data[p:p + MIN_MATCH], -1)
        for _ in range(self.depth):
            if c < 0 or p - c > self.window:
                break
            k = _match_len(self.data, c, p, end - p)
            if k > best:
                best, best_d = k, p - c
                if k == end - p:
                    break
            c = self.prev[c]
        return best, best_d


def _commands_for(data, start, end, finder, rb):
    """Greedy parse of data[start:end] into (insert, copy, distance)."""
    cmds, p, anchor = [], start, start
    while p + MIN_MATCH <= end:
        m, d = finder.find(p, end)
        finder.insert(p)
        if m < MIN_MATCH:
            p += 1
            continue
        cmds.append((anchor, p - anchor, m, d))
        for q in range(p + 1, p + m):
            finder.insert(q)
        p = anchor = p + m
    for q in range(p, end):
        finder.insert(q)
    if anchor < end:
        cmds.append((anchor, end - anchor, 0, 0))
    return cmds


def _compressed_body(data, cmds, rb):
    """The bits of one compressed meta-block after ISUNCOMPRESSED."""
    lit_f, cmd_f, dst_f = [0] * 256, [0] * 704, [0] * 64
    items = []
    for start, ilen, clen, d in cmds:
        ic = _code_of(INSERT_BASE, ilen)
        cc = _code_of(COPY_BASE, max(clen, 2))
        dist = None
        if clen:
            if d == rb[3]:
                dist = (0, 0, 0)
            elif d in rb[:3]:
                dist = (3 - rb.index(d), 0, 0)
            else:
                dist = _dist_symbol(d)
            if dist[0] != 0:
                rb[:] = rb[1:] + [d]
        if (dist is None or dist[0] == 0) and ic < 8 and cc < 16:
            code = 64 * (cc >> 3) + 8 * (ic & 7) + (cc & 7)    # implicit distance
            dist = None
        else:
            cell = CELLS.index((ic & ~7, cc & ~7), 2)
            code = 64 * cell + 8 * (ic & 7) + (cc & 7)
        cmd_f[code] += 1
        for b in data[start:start + ilen]:
            lit_f[b] += 1
        if dist:
            dst_f[dist[0]] += 1
        items.append((start, ilen, clen, ic, cc, code, dist))
    lit, cmd, dst = _Code(lit_f, 256), _Code(cmd_f, 704), _Code(dst_f, 64)
    ops = [(0, 1), (0, 1), (0, 1)]          # NBLTYPESL, NBLTYPESI, NBLTYPESD = 1
    ops += [(0, 2), (0, 4), (0, 2)]         # NPOSTFIX, NDIRECT, context mode LSB6
    ops += [(0, 1), (0, 1)]                 # NTREESL = 1, NTREESD = 1
    for code in (lit, cmd, dst):
        _write_code(ops, code)
    for start, ilen, clen, ic, cc, code, dist in items:
        cmd.put(ops, code)
        ops.append((ilen - INSERT_BASE[ic], INSERT_EXTRA[ic]))
        ops.append((max(clen, 2) - COPY_BASE[cc], COPY_EXTRA[cc]))
        for b in data[start:start + ilen]:
            lit.put(ops, b)
        if dist:
            dst.put(ops, dist[0])
            ops.append((dist[2], dist[1]))
    return ops


def _mlen_header(w, mlen, last):
    w.write(last, 1)
    if last:
        w.write(0, 1)                                       # ISLASTEMPTY = 0
    nibbles = max(4, ((mlen - 1).bit_length() + 3) // 4)
    w.write(nibbles - 4, 2)
    w.write(mlen - 1, 4 * nibbles)


def compress(data, depth=16):
    """Encode data as one Brotli stream (see the module docstring)."""
    data = bytes(data)
    n = len(data)
    wbits = 16
    while (1 << wbits) - 16 < n and wbits < 24:
        wbits += 1
    window = (1 << wbits) - 16
    w = _Writer()
    if wbits == 16:
        w.write(0, 1)
    elif wbits == 17:
        w.write(1, 1)
        w.write(0, 6)
    else:
        w.write(1, 1)
        w.write(wbits - 17, 3)
    finder = _Finder(data, depth, window)
    rb = [16, 15, 11, 4]
    for start in range(0, n, META_MAX):
        end = min(n, start + META_MAX)
        saved = rb[:]
        ops = _compressed_body(data, _commands_for(data, start, end, finder, rb), rb)
        _mlen_header(w, end - start, 0)
        if sum(k for _, k in ops) + 7 < 8 * (end - start):
            w.write(0, 1)                                   # ISUNCOMPRESSED = 0
            for value, k in ops:
                w.write(value, k)
        else:
            rb[:] = saved
            w.write(1, 1)                                   # ISUNCOMPRESSED = 1
            w.align()
            w.out += data[start:end]
    w.write(3, 2)                                           # ISLAST, ISLASTEMPTY
    w.align()
    return bytes(w.out)
