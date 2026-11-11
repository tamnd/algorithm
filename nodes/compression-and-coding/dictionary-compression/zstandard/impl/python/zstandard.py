# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zstandard/. The authors are listed in prov/E9Q3EG.jsonl.
"""Zstandard (RFC 8878): a frame decoder and a simple frame encoder.

The decoder reads the whole format of RFC 8878 except dictionaries: raw,
RLE and compressed blocks; raw, RLE, Huffman and treeless literals with 1
or 4 streams; Huffman weights in direct or FSE form; predefined, RLE, FSE
and repeat modes for the three sequence tables; repeat offsets; the
XXH64 content checksum; skippable frames and concatenated frames. A frame
with a nonzero Dictionary_ID raises ZstdError.

The encoder writes valid frames from a subset of the format: one frame
with Single_Segment_Flag, Frame_Content_Size and the checksum; blocks of
at most 128 KiB that are RLE, raw, or compressed with raw literals and
the predefined FSE tables. Its matches come from a greedy hash chain
search and it uses the repeat offsets.
"""

import struct
from bisect import bisect_right


class ZstdError(ValueError):
    """The input is not a valid Zstandard stream (or it needs a dictionary)."""


MAGIC = 0xFD2FB528
BLOCK_MAX = 1 << 17
MIN_MATCH = 4
MAX_DISTANCE = 1 << 22

# RFC 8878 Table 16 and Table 17: baseline and extra bits of each code.
LL_BASE = list(range(16)) + [16, 18, 20, 22, 24, 28, 32, 40, 48, 64, 128, 256,
                             512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
LL_BITS = [0] * 16 + [1, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 9, 10, 11, 12,
                      13, 14, 15, 16]
ML_BASE = list(range(3, 35)) + [35, 37, 39, 41, 43, 47, 51, 59, 67, 83, 99,
                                131, 259, 515, 1027, 2051, 4099, 8195,
                                16387, 32771, 65539]
ML_BITS = [0] * 32 + [1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 7, 8, 9, 10, 11,
                      12, 13, 14, 15, 16]

# RFC 8878 Section 3.1.1.3.2.2: the default distributions.
LL_DEFAULT = [4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1,
              -1, -1, -1, -1]
ML_DEFAULT = [1, 4, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1,
              -1, -1, -1, -1, -1]
OF_DEFAULT = [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]

# (max symbol, max accuracy log) of the three sequence tables.
LL_LIMITS, OF_LIMITS, ML_LIMITS = (35, 9), (31, 8), (52, 9)

_M64 = (1 << 64) - 1
_P1, _P2, _P3 = 11400714785074694791, 14029467366897019727, 1609587929392839161
_P4, _P5 = 9650029242287828579, 2870177450012600261


def _rotl(x, r):
    return ((x << r) | (x >> (64 - r))) & _M64


def _round(acc, lane):
    acc = (acc + lane * _P2) & _M64
    return (_rotl(acc, 31) * _P1) & _M64


def xxh64(data, seed=0):
    """XXH64 of data; Zstandard keeps its low 32 bits as the checksum."""
    data = bytes(data)
    n = len(data)
    i = 0
    if n >= 32:
        v = [(seed + _P1 + _P2) & _M64, (seed + _P2) & _M64, seed & _M64,
             (seed - _P1) & _M64]
        while i + 32 <= n:
            lanes = struct.unpack_from("<4Q", data, i)
            v = [_round(v[k], lanes[k]) for k in range(4)]
            i += 32
        h = (_rotl(v[0], 1) + _rotl(v[1], 7) + _rotl(v[2], 12)
             + _rotl(v[3], 18)) & _M64
        for acc in v:
            h ^= _round(0, acc)
            h = (h * _P1 + _P4) & _M64
    else:
        h = (seed + _P5) & _M64
    h = (h + n) & _M64
    while i + 8 <= n:
        h ^= _round(0, struct.unpack_from("<Q", data, i)[0])
        h = (_rotl(h, 27) * _P1 + _P4) & _M64
        i += 8
    if i + 4 <= n:
        h ^= (struct.unpack_from("<I", data, i)[0] * _P1) & _M64
        h = (_rotl(h, 23) * _P2 + _P3) & _M64
        i += 4
    while i < n:
        h ^= (data[i] * _P5) & _M64
        h = (_rotl(h, 11) * _P1) & _M64
        i += 1
    h ^= h >> 33
    h = (h * _P2) & _M64
    h ^= h >> 29
    h = (h * _P3) & _M64
    return h ^ (h >> 32)


# ---------------------------------------------------------------- bit input

class _BackBits:
    """A bitstream read from its end: the last byte holds a 1 end marker."""

    def __init__(self, buf, lo, hi):
        if hi <= lo or buf[hi - 1] == 0:
            raise ZstdError("bitstream without an end marker")
        self.buf, self.lo = buf, lo
        self.pos = (hi - lo - 1) * 8 + buf[hi - 1].bit_length() - 1

    def peek(self, n):
        pos = self.pos
        if n == 0 or pos <= 0:
            return 0
        low = pos - n
        if low >= 0:
            a = self.lo + (low >> 3)
            v = int.from_bytes(self.buf[a:self.lo + ((pos + 7) >> 3)], "little")
            return (v >> (low & 7)) & ((1 << n) - 1)
        v = int.from_bytes(self.buf[self.lo:self.lo + ((pos + 7) >> 3)], "little")
        return (v & ((1 << pos) - 1)) << (-low)   # zeros past the start

    def read(self, n):
        v = self.peek(n)
        self.pos -= n
        return v


# ---------------------------------------------------------------- FSE tables

def _read_ncount(buf, i, end, max_symbol, max_log):
    """RFC 8878 Section 4.1.1: read a normalized distribution."""
    if i >= end:
        raise ZstdError("missing FSE table description")
    chunk = bytes(buf[i:min(end, i + 1024)])
    data = int.from_bytes(chunk, "little")
    al = (chunk[0] & 15) + 5
    if al > max_log:
        raise ZstdError("FSE accuracy log too large")
    pos, remaining, threshold, nb = 4, (1 << al) + 1, 1 << al, al + 1
    norm, prev0 = [], False
    while remaining > 1 and len(norm) <= max_symbol:
        if prev0:
            while True:
                r = (data >> pos) & 3
                pos += 2
                norm.extend([0] * r)
                if r != 3:
                    break
            if len(norm) > max_symbol:
                break
        top = 2 * threshold - 1 - remaining
        v = (data >> pos) & (2 * threshold - 1)
        if (v & (threshold - 1)) < top:
            c = v & (threshold - 1)
            pos += nb - 1
        else:
            c = v - top if v >= threshold else v
            pos += nb
        c -= 1
        remaining -= abs(c)
        norm.append(c)
        prev0 = c == 0
        while remaining < threshold:
            nb -= 1
            threshold >>= 1
    if remaining != 1 or len(norm) > max_symbol + 1 or pos > 8 * len(chunk):
        raise ZstdError("bad FSE table description")
    return norm, al, i + ((pos + 7) >> 3)


def _build_table(norm, al):
    """Decoding table: one (symbol, number of bits, baseline) per state."""
    size = 1 << al
    sym = [0] * size
    high = size - 1
    nxt = [0] * len(norm)
    for s, c in enumerate(norm):
        if c == -1:
            sym[high] = s
            high -= 1
            nxt[s] = 1
        else:
            nxt[s] = c
    pos, step, mask = 0, (size >> 1) + (size >> 3) + 3, size - 1
    for s, c in enumerate(norm):
        for _ in range(max(c, 0)):
            sym[pos] = s
            pos = (pos + step) & mask
            while pos > high:
                pos = (pos + step) & mask
    if pos != 0:
        raise ZstdError("FSE distribution does not fill the table")
    table = []
    for u in range(size):
        s = sym[u]
        x = nxt[s]
        nxt[s] += 1
        nb = al - (x.bit_length() - 1)
        table.append((s, nb, (x << nb) - size))
    return table, al


def _encode_table(table, al):
    """For each symbol, the state that leads to each next state t."""
    enc = {}
    for u, (s, nb, base) in enumerate(table):
        row = enc.setdefault(s, [0] * (1 << al))
        for t in range(base, base + (1 << nb)):
            row[t] = u
    return enc


PREDEFINED_LL = _build_table(LL_DEFAULT, 6)
PREDEFINED_OF = _build_table(OF_DEFAULT, 5)
PREDEFINED_ML = _build_table(ML_DEFAULT, 6)


# ---------------------------------------------------------------- literals

def _fse_weights(buf, lo, hi):
    """RFC 8878 Section 4.2.1.2: Huffman weights in FSE form, two states."""
    norm, al, j = _read_ncount(buf, lo, hi, 255, 6)
    table, _ = _build_table(norm, al)
    br = _BackBits(buf, j, hi)
    s1, s2 = br.read(al), br.read(al)
    out = []
    while True:
        sym, nb, base = table[s1]
        out.append(sym)
        s1 = base + br.read(nb)
        if br.pos < 0:
            out.append(table[s2][0])
            break
        sym, nb, base = table[s2]
        out.append(sym)
        s2 = base + br.read(nb)
        if br.pos < 0:
            out.append(table[s1][0])
            break
        if len(out) > 255:
            raise ZstdError("too many Huffman weights")
    return out


def _read_huffman(buf, i, end):
    """RFC 8878 Section 4.2.1: a Huffman tree description."""
    if i >= end:
        raise ZstdError("missing Huffman tree description")
    head = buf[i]
    i += 1
    if head < 128:
        if i + head > end:
            raise ZstdError("truncated Huffman weights")
        weights = _fse_weights(buf, i, i + head)
        i += head
    else:
        count = head - 127
        if i + (count + 1) // 2 > end:
            raise ZstdError("truncated Huffman weights")
        weights = [buf[i + k // 2] >> 4 if k % 2 == 0 else buf[i + k // 2] & 15
                   for k in range(count)]
        i += (count + 1) // 2
    if len(weights) > 255 or max(weights) > 11:
        raise ZstdError("bad Huffman weights")
    total = sum(1 << (w - 1) for w in weights if w)
    if total == 0:
        raise ZstdError("bad Huffman weights")
    max_bits = total.bit_length()
    rest = (1 << max_bits) - total
    if rest & (rest - 1) or max_bits > 11:
        raise ZstdError("Huffman weights do not complete a tree")
    weights.append(rest.bit_length())
    # Codes go to the lowest weight first, symbols in order within a weight;
    # a symbol of weight w owns 2^(w-1) consecutive entries of the table.
    table = []
    for w in range(1, max_bits + 1):
        for s, ws in enumerate(weights):
            if ws == w:
                table.extend([(s, max_bits + 1 - w)] * (1 << (w - 1)))
    return (table, max_bits), i


def _huffman_stream(buf, lo, hi, count, huf, out):
    table, max_bits = huf
    br = _BackBits(buf, lo, hi)
    for _ in range(count):
        s, nb = table[br.peek(max_bits)]
        br.pos -= nb
        out.append(s)
    if br.pos != 0:
        raise ZstdError("Huffman stream not consumed exactly")


def _read_literals(buf, i, end, st):
    """RFC 8878 Section 3.1.1.3.1: the literals section of a block."""
    if i >= end:
        raise ZstdError("missing literals section")
    b0 = buf[i]
    kind, form = b0 & 3, (b0 >> 2) & 3
    if kind < 2:
        if form & 1 == 0:
            size, i = b0 >> 3, i + 1
        elif form == 1:
            size, i = (b0 >> 4) + (buf[i + 1] << 4), i + 2
        else:
            size = (b0 >> 4) + (buf[i + 1] << 4) + (buf[i + 2] << 12)
            i += 3
        if size > BLOCK_MAX:
            raise ZstdError("too many literals")
        if kind == 0:
            if i + size > end:
                raise ZstdError("truncated raw literals")
            return bytes(buf[i:i + size]), i + size
        if i >= end:
            raise ZstdError("truncated RLE literals")
        return bytes([buf[i]]) * size, i + 1
    head, bits = (3, 10) if form < 2 else ((4, 14) if form == 2 else (5, 18))
    if i + head > end:
        raise ZstdError("truncated literals header")
    v = int.from_bytes(buf[i:i + head], "little")
    regen = (v >> 4) & ((1 << bits) - 1)
    csize = (v >> (4 + bits)) & ((1 << bits) - 1)
    i += head
    stop = i + csize
    if stop > end or regen > BLOCK_MAX:
        raise ZstdError("bad literals sizes")
    if kind == 2:
        st["huf"], i = _read_huffman(buf, i, stop)
    elif st["huf"] is None:
        raise ZstdError("treeless literals without a previous tree")
    out = bytearray()
    if form == 0:
        _huffman_stream(buf, i, stop, regen, st["huf"], out)
    else:
        if i + 6 > stop:
            raise ZstdError("truncated jump table")
        s1, s2, s3 = struct.unpack_from("<3H", buf, i)
        i += 6
        cuts = [i, i + s1, i + s1 + s2, i + s1 + s2 + s3, stop]
        if cuts[3] > stop:
            raise ZstdError("bad jump table")
        part = (regen + 3) // 4
        for k in range(4):
            count = part if k < 3 else regen - 3 * part
            if count < 0:
                raise ZstdError("bad stream sizes")
            _huffman_stream(buf, cuts[k], cuts[k + 1], count, st["huf"], out)
    return bytes(out), stop


# ---------------------------------------------------------------- sequences

def _read_table(buf, i, end, mode, kind, st, predefined, limits):
    if mode == 0:
        return predefined, i
    if mode == 1:
        if i >= end or buf[i] > limits[0]:
            raise ZstdError("bad RLE symbol")
        return ([(buf[i], 0, 0)], 0), i + 1
    if mode == 2:
        norm, al, i = _read_ncount(buf, i, end, limits[0], limits[1])
        return _build_table(norm, al), i
    if st[kind] is None:
        raise ZstdError("repeat mode without a previous table")
    return st[kind], i


def _resolve_offset(v, ll, rep):
    """RFC 8878 Section 3.1.1.5: offset value to distance, update history."""
    if v > 3:
        d = v - 3
        rep[2], rep[1], rep[0] = rep[1], rep[0], d
        return d
    k = v - 1 + (ll == 0)
    if k == 0:
        return rep[0]
    d = rep[0] - 1 if k == 3 else rep[k]
    if k == 1:
        rep[1] = rep[0]
    else:
        rep[2], rep[1] = rep[1], rep[0]
    rep[0] = d
    return d


def _decode_block(buf, i, end, st, out, window):
    lits, i = _read_literals(buf, i, end, st)
    if i >= end:
        raise ZstdError("missing sequences section")
    b0 = buf[i]
    if b0 < 128:
        nseq, i = b0, i + 1
    elif b0 < 255:
        if i + 2 > end:
            raise ZstdError("truncated sequence count")
        nseq, i = ((b0 - 128) << 8) + buf[i + 1], i + 2
    else:
        if i + 3 > end:
            raise ZstdError("truncated sequence count")
        nseq, i = buf[i + 1] + (buf[i + 2] << 8) + 0x7F00, i + 3
    if nseq == 0:
        if i != end:
            raise ZstdError("bytes after an empty sequences section")
        out += lits
        return
    if i >= end:
        raise ZstdError("missing compression modes")
    modes = buf[i]
    i += 1
    if modes & 3:
        raise ZstdError("reserved bits set in compression modes")
    tll, i = _read_table(buf, i, end, modes >> 6, "ll", st, PREDEFINED_LL, LL_LIMITS)
    tof, i = _read_table(buf, i, end, (modes >> 4) & 3, "of", st, PREDEFINED_OF, OF_LIMITS)
    tml, i = _read_table(buf, i, end, (modes >> 2) & 3, "ml", st, PREDEFINED_ML, ML_LIMITS)
    st["ll"], st["of"], st["ml"] = tll, tof, tml
    (cll, all_), (cof, aof), (cml, aml) = tll, tof, tml
    rep = st["rep"]
    br = _BackBits(buf, i, end)                                 # @line L1
    sll, sof, sml = br.read(all_), br.read(aof), br.read(aml)   # @line L2
    lp = 0
    for k in range(nseq):                                       # @line L3
        code, nbo, baseo = cof[sof]                             # @line L4
        if code > 31:
            raise ZstdError("offset code too large")
        v = (1 << code) + br.read(code)
        code, nbm, basem = cml[sml]                             # @line L5
        m = ML_BASE[code] + br.read(ML_BITS[code])
        code, nbl, basel = cll[sll]                             # @line L6
        ll = LL_BASE[code] + br.read(LL_BITS[code])
        d = _resolve_offset(v, ll, rep)                         # @line L7
        if lp + ll > len(lits):                                 # @line L8
            raise ZstdError("sequence needs more literals than exist")
        out += lits[lp:lp + ll]
        lp += ll
        if d == 0 or d > len(out) - st["start"] or d > window:  # @line L9
            raise ZstdError("offset outside the window")
        src = len(out) - d                                      # @line L10
        if d >= m:
            out += out[src:src + m]
        else:
            for j in range(m):
                out.append(out[src + j])
        if k < nseq - 1:                                        # @line L11
            sll = basel + br.read(nbl)
            sml = basem + br.read(nbm)
            sof = baseo + br.read(nbo)
    if br.pos != 0:                                             # @line L12
        raise ZstdError("sequence bitstream not consumed exactly")
    out += lits[lp:]                                            # @line L13


# ---------------------------------------------------------------- frames

def _frame(data, i, out):
    n = len(data)
    if i >= n:
        raise ZstdError("truncated frame header")
    fhd = data[i]
    i += 1
    fcs_flag, single = fhd >> 6, (fhd >> 5) & 1
    if fhd & 8:
        raise ZstdError("reserved bit set in the frame header")
    checksum, did_flag = (fhd >> 2) & 1, fhd & 3
    window = 0
    if not single:
        if i >= n:
            raise ZstdError("truncated frame header")
        wd = data[i]
        i += 1
        wlog = 10 + (wd >> 3)
        window = (1 << wlog) + ((1 << wlog) >> 3) * (wd & 7)
    did_size = (0, 1, 2, 4)[did_flag]
    fcs_size = (1 if single else 0, 2, 4, 8)[fcs_flag]
    if i + did_size + fcs_size > n:
        raise ZstdError("truncated frame header")
    if int.from_bytes(data[i:i + did_size], "little"):
        raise ZstdError("dictionaries are not supported")
    i += did_size
    fcs = None
    if fcs_size:
        fcs = int.from_bytes(data[i:i + fcs_size], "little")
        fcs += 256 if fcs_size == 2 else 0
        i += fcs_size
    if single:
        window = fcs
    block_max = min(window, BLOCK_MAX)
    start = len(out)
    st = {"huf": None, "ll": None, "of": None, "ml": None,
          "rep": [1, 4, 8], "start": start}
    while True:
        if i + 3 > n:
            raise ZstdError("truncated block header")
        h = data[i] | (data[i + 1] << 8) | (data[i + 2] << 16)
        i += 3
        last, kind, size = h & 1, (h >> 1) & 3, h >> 3
        if size > block_max:
            raise ZstdError("block larger than the maximum")
        if kind == 0:
            if i + size > n:
                raise ZstdError("truncated raw block")
            out += data[i:i + size]
            i += size
        elif kind == 1:
            if i >= n:
                raise ZstdError("truncated RLE block")
            out += bytes([data[i]]) * size
            i += 1
        elif kind == 2:
            if i + size > n:
                raise ZstdError("truncated compressed block")
            before = len(out)
            _decode_block(data, i, i + size, st, out, window)
            if len(out) - before > block_max:
                raise ZstdError("block decodes to more than the maximum")
            i += size
        else:
            raise ZstdError("reserved block type")
        if fcs is not None and len(out) - start > fcs:
            raise ZstdError("frame longer than its content size")
        if last:
            break
    if fcs is not None and len(out) - start != fcs:
        raise ZstdError("frame content size does not match")
    if checksum:
        if i + 4 > n:
            raise ZstdError("truncated checksum")
        want = int.from_bytes(data[i:i + 4], "little")
        if xxh64(out[start:]) & 0xFFFFFFFF != want:
            raise ZstdError("checksum mismatch")
        i += 4
    return i


def decompress(data):
    """Decode one or more concatenated Zstandard or skippable frames."""
    data = bytes(data)
    out = bytearray()
    i = 0
    if not data:
        raise ZstdError("no frame")
    while i < len(data):
        if i + 4 > len(data):
            raise ZstdError("truncated magic number")
        magic = int.from_bytes(data[i:i + 4], "little")
        if 0x184D2A50 <= magic <= 0x184D2A5F:
            if i + 8 > len(data):
                raise ZstdError("truncated skippable frame")
            size = int.from_bytes(data[i + 4:i + 8], "little")
            if i + 8 + size > len(data):
                raise ZstdError("truncated skippable frame")
            i += 8 + size
        elif magic == MAGIC:
            i = _frame(data, i + 4, out)
        else:
            raise ZstdError("unknown magic number")
    return bytes(out)


# ---------------------------------------------------------------- encoder

class _BitWriter:
    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.n = 0

    def write(self, value, bits):
        self.acc |= value << self.n
        self.n += bits
        while self.n >= 8:
            self.out.append(self.acc & 255)
            self.acc >>= 8
            self.n -= 8

    def finish(self):
        self.write(1, 1)               # the end marker
        if self.n:
            self.out.append(self.acc)
        return bytes(self.out)


_ENC_LL = _encode_table(*PREDEFINED_LL)
_ENC_OF = _encode_table(*PREDEFINED_OF)
_ENC_ML = _encode_table(*PREDEFINED_ML)


def _offset_value(d, ll, rep):
    """Pick the offset value for distance d; update rep like the decoder."""
    if ll > 0:
        choices = {rep[0]: 1, rep[1]: 2, rep[2]: 3}
    else:
        choices = {rep[1]: 1, rep[2]: 2, rep[0] - 1: 3}
    v = choices.get(d, d + 3)
    used = _resolve_offset(v, ll, rep)
    assert used == d
    return v


def _encode_sequences(seqs):
    """The sequence bitstream with the predefined tables, written backward."""
    codes = []
    for ll, v, m in seqs:
        cl = bisect_right(LL_BASE, ll) - 1
        cm = bisect_right(ML_BASE, m) - 1
        co = v.bit_length() - 1
        codes.append((cl, ll - LL_BASE[cl], cm, m - ML_BASE[cm], co, v - (1 << co)))
    tll, tof, tml = PREDEFINED_LL[0], PREDEFINED_OF[0], PREDEFINED_ML[0]
    w = _BitWriter()
    sll = sof = sml = 0
    for k in range(len(seqs) - 1, -1, -1):
        cl, xl, cm, xm, co, xo = codes[k]
        if k == len(seqs) - 1:
            sll, sof, sml = _ENC_LL[cl][0], _ENC_OF[co][0], _ENC_ML[cm][0]
        else:
            ul, uo, um = _ENC_LL[cl][sll], _ENC_OF[co][sof], _ENC_ML[cm][sml]
            # The decoder reads LL, ML, OF updates, so write OF, ML, LL.
            w.write(sof - tof[uo][2], tof[uo][1])
            w.write(sml - tml[um][2], tml[um][1])
            w.write(sll - tll[ul][2], tll[ul][1])
            sll, sof, sml = ul, uo, um
        w.write(xl, LL_BITS[cl])
        w.write(xm, ML_BITS[cm])
        w.write(xo, co)
    w.write(sml, 6)
    w.write(sof, 5)
    w.write(sll, 6)
    return w.finish()


def _match_len(data, a, b, limit):
    k = 0
    while k + 32 <= limit and data[a + k:a + k + 32] == data[b + k:b + k + 32]:
        k += 32
    while k < limit and data[a + k] == data[b + k]:
        k += 1
    return k


class _Finder:
    """Hash chains over 4-byte strings."""

    def __init__(self, data, depth):
        self.data, self.depth = data, depth
        self.head = {}
        self.prev = [-1] * len(data)

    def insert(self, p):
        key = self.data[p:p + MIN_MATCH]
        if len(key) == MIN_MATCH:
            self.prev[p] = self.head.get(key, -1)
            self.head[key] = p

    def find(self, p, end):
        data = self.data
        best_len, best_d = 0, 0
        c = self.head.get(data[p:p + MIN_MATCH], -1)
        limit = end - p
        for _ in range(self.depth):
            if c < 0 or p - c > MAX_DISTANCE:
                break
            k = _match_len(data, c, p, limit)
            if k > best_len:
                best_len, best_d = k, p - c
                if k == limit:
                    break
            c = self.prev[c]
        return best_len, best_d


def _compress_block(data, start, end, rep, finder):
    seqs, lits = [], bytearray()
    p = anchor = start
    while p + MIN_MATCH <= end:
        m, d = finder.find(p, end)
        finder.insert(p)
        if m < MIN_MATCH:
            p += 1
            continue
        ll = p - anchor
        lits += data[anchor:p]
        seqs.append((ll, _offset_value(d, ll, rep), m))
        for q in range(p + 1, p + m):
            finder.insert(q)
        p = anchor = p + m
    lits += data[anchor:end]
    n = len(lits)
    if n < 32:
        body = bytearray([n << 3])
    elif n < 4096:
        body = bytearray([(n << 4 | 4) & 255, n >> 4])
    else:
        body = bytearray([(n << 4 | 12) & 255, (n >> 4) & 255, n >> 12])
    body += lits
    s = len(seqs)
    if s < 128:
        body.append(s)
    elif s < 0x7F00:
        body += bytes([(s >> 8) + 128, s & 255])
    else:
        body += bytes([255, (s - 0x7F00) & 255, (s - 0x7F00) >> 8])
    if s:
        body.append(0)                 # all three tables predefined
        body += _encode_sequences(seqs)
    return bytes(body)


def compress(data, checksum=True, depth=16):
    """Encode data as one Zstandard frame (see the module note for the subset)."""
    data = bytes(data)
    n = len(data)
    if n < 256:
        flag, fcs = 0, n.to_bytes(1, "little")
    elif n < 65536 + 256:
        flag, fcs = 1, (n - 256).to_bytes(2, "little")
    elif n < 1 << 32:
        flag, fcs = 2, n.to_bytes(4, "little")
    else:
        flag, fcs = 3, n.to_bytes(8, "little")
    out = bytearray(MAGIC.to_bytes(4, "little"))
    out.append(flag << 6 | 0x20 | checksum << 2)
    out += fcs
    if n == 0:
        out += b"\x01\x00\x00"             # one empty raw block, the last
    rep = [1, 4, 8]
    finder = _Finder(data, depth)
    for start in range(0, n, BLOCK_MAX):
        end = min(start + BLOCK_MAX, n)
        last = int(end == n)
        size = end - start
        if data.count(data[start:start + 1], start, end) == size:
            out += (last | 1 << 1 | size << 3).to_bytes(3, "little")
            out.append(data[start])
            continue
        saved = rep[:]
        body = _compress_block(data, start, end, rep, finder)
        if len(body) < size:
            out += (last | 2 << 1 | len(body) << 3).to_bytes(3, "little")
            out += body
        else:
            rep[:] = saved                 # raw blocks keep the old history
            out += (last | size << 3).to_bytes(3, "little")
            out += data[start:end]
    if checksum:
        out += (xxh64(data) & 0xFFFFFFFF).to_bytes(4, "little")
    return bytes(out)
