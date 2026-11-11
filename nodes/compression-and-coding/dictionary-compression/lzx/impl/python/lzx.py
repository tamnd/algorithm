# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzx/. The authors are listed in prov/Y9A12Q.jsonl.
"""LZX as Microsoft cabinet (CAB) files use it.

A stream is the LZX data of one CAB folder (compression type 3, window
2^15 to 2^21 bytes). It starts with the E8 header, then holds blocks of
three types: verbatim (1), aligned offset (2) and uncompressed (3). The
output is cut into frames of 32768 bytes, and the bit stream is aligned
to 16 bits at the end of every frame. The stream does not store its
window size or its length, so the caller gives both (a CAB file keeps
them in CFFOLDER and CFDATA).

decompress covers this whole CAB format: the three block types, tree
lengths sent as differences to the previous block, the repeated offsets
R0, R1, R2, the E8 call translation and all CAB window sizes. It does
not cover LZX DELTA (reference data, chunk size fields, windows above
2^21, matches longer than 257 bytes), the reset interval of CHM and LIT
files, or the WIM variant.

compress writes one block per frame and picks the smallest of a
verbatim block, an aligned offset block and an uncompressed block. Its
parse is greedy, with a hash chain and the three repeated offsets. It
can apply the E8 translation if the caller gives a translation size.
"""

from bisect import bisect_right

FRAME = 32768
MAX_MATCH = 257
NUM_LENGTHS = 249
SLOTS = {15: 30, 16: 32, 17: 34, 18: 36, 19: 38, 20: 42, 21: 50}
EXTRA = [0, 0, 0, 0] + [min(i // 2 - 1, 17) for i in range(4, 50)]
BASE = [0]
for _i in range(1, 50):
    BASE.append(BASE[-1] + (1 << EXTRA[_i - 1]))


class LZXError(ValueError):
    """The input is not a valid LZX stream."""


# ---------------------------------------------------------------- decoder

class _Reader:
    """16-bit little-endian words, each read from its high bit down."""

    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.word = 0
        self.left = 0

    def _load(self):
        if self.pos + 2 > len(self.data):
            raise LZXError("truncated stream")
        self.word = self.data[self.pos] | self.data[self.pos + 1] << 8
        self.pos += 2
        self.left = 16

    def bit(self):
        if not self.left:
            self._load()
        self.left -= 1
        return (self.word >> self.left) & 1

    def bits(self, n):
        v = 0
        while n:
            if not self.left:
                self._load()
            k = min(n, self.left)
            self.left -= k
            n -= k
            v = (v << k) | ((self.word >> self.left) & ((1 << k) - 1))
        return v

    def align(self):
        """Drop the rest of the current word. Those bits must be 0."""
        if self.word & ((1 << self.left) - 1):
            raise LZXError("nonzero padding bits")
        self.left = 0

    def align_uncompressed(self):
        """Drop 1 to 16 bits: a full word if the stream is aligned."""
        if not self.left:
            self._load()
        self.align()

    def raw(self, n):
        if self.pos + n > len(self.data):
            raise LZXError("truncated stream")
        self.pos += n
        return self.data[self.pos - n:self.pos]


class _Code:
    """A canonical prefix code, read from its first (high) bit."""

    def __init__(self, lengths):
        self.maxlen = max(lengths, default=0)
        self.count = [0] * (self.maxlen + 1)
        for ln in lengths:
            if ln:
                self.count[ln] += 1
        self.symbols = [s for _, s in sorted((ln, s) for s, ln in enumerate(lengths) if ln)]
        left = 1
        for ln in range(1, self.maxlen + 1):
            left = 2 * left - self.count[ln]
            if left < 0:
                raise LZXError("over-subscribed code")
        if self.symbols and left:
            raise LZXError("incomplete code")

    def decode(self, r):
        if not self.symbols:
            raise LZXError("symbol read from an empty tree")
        code = first = index = 0
        for ln in range(1, self.maxlen + 1):
            code |= r.bit()
            c = self.count[ln]
            if code - first < c:
                return self.symbols[index + code - first]
            index += c
            first = (first + c) << 1
            code <<= 1
        raise LZXError("bad code")  # not reached: the code is complete


def _read_lengths(r, lens, first, last):
    """Read lens[first:last] as differences to the old values."""
    pre = _Code([r.bits(4) for _ in range(20)])
    x = first
    while x < last:
        z = pre.decode(r)
        if z == 17:
            n, v = r.bits(4) + 4, 0
        elif z == 18:
            n, v = r.bits(5) + 20, 0
        elif z == 19:
            n = r.bits(1) + 4
            z = pre.decode(r)
            if z > 16:
                raise LZXError("bad code after pretree code 19")
            v = (lens[x] - z) % 17
        else:
            n, v = 1, (lens[x] - z) % 17
        if x + n > last:
            raise LZXError("run past the end of the tree")
        lens[x:x + n] = [v] * n
        x += n


def _copy(out, d, n):
    if d >= n:
        out += out[len(out) - d:len(out) - d + n]
    else:
        for _ in range(n):
            out.append(out[-d])


def _tokens(r, out, left, end, main, length, aligned, R):
    """Decode the literals and matches of a verbatim or aligned offset
    block until the block (left bytes) or the frame (ends at end) ends."""
    while left > 0 and len(out) < end:                       # @line L1
        s = main.decode(r)                                   # @line L2
        if s < 256:                                          # @line L3
            out.append(s)
            n = 1
        else:                                                # @line L4
            h, slot = (s - 256) & 7, (s - 256) >> 3          # @line L5
            n = h + 2                                        # @line L6
            if h == 7:
                n += length.decode(r)
            if slot < 3:                                     # @line L7
                d = R[slot]
                R[0], R[slot] = R[slot], R[0]
            else:                                            # @line L8
                e = EXTRA[slot]                              # @line L9
                if aligned is not None and e >= 3:           # @line L10
                    v = (r.bits(e - 3) << 3) + aligned.decode(r)
                else:                                        # @line L11
                    v = r.bits(e)
                d = BASE[slot] + v - 2                       # @line L12
                R[0], R[1], R[2] = d, R[0], R[1]
            if not 1 <= d <= len(out) or n > left or len(out) + n > end:   # @line L13
                raise LZXError("match outside the output, block or frame")
            _copy(out, d, n)                                 # @line L14
        left -= n                                            # @line L15
    return left                                              # @line L16


def _e8_reverse(buf, start, size, e8):
    """Undo the E8 translation of one frame (as libmspack does)."""
    filesize = e8 - (1 << 32) if e8 >= 1 << 31 else e8
    i = 0
    while i < size - 10:
        if buf[start + i] != 0xE8:
            i += 1
            continue
        cur = start + i
        v = int.from_bytes(buf[cur + 1:cur + 5], "little", signed=True)
        if -cur <= v < filesize:
            rel = v - cur if v >= 0 else v + filesize
            buf[cur + 1:cur + 5] = (rel & 0xFFFFFFFF).to_bytes(4, "little")
        i += 5


def decompress(data, window_bits, size):
    """Decode an LZX stream of size output bytes with a window of
    2**window_bits bytes (15 to 21)."""
    if window_bits not in SLOTS:
        raise ValueError("window_bits must be 15 to 21")
    if size < 0:
        raise ValueError("size must not be negative")
    data = bytes(data)
    if size == 0:
        if data:
            raise LZXError("data after the end")
        return b""
    r = _Reader(data)
    nmain = 256 + 8 * SLOTS[window_bits]
    e8 = r.bits(32) if r.bit() else 0
    main_lens, len_lens = [0] * nmain, [0] * NUM_LENGTHS
    main = length = aligned = None
    R = [1, 1, 1]
    out = bytearray()
    btype, left, pad = 0, 0, False
    end = min(FRAME, size)
    while len(out) < size:
        if left == 0:
            if pad:
                r.raw(1)
                pad = False
            btype, left = r.bits(3), r.bits(24)
            if btype == 3:
                r.align_uncompressed()
                R = [int.from_bytes(r.raw(4), "little") for _ in range(3)]
                pad = left % 2 == 1
            elif btype in (1, 2):
                aligned = _Code([r.bits(3) for _ in range(8)]) if btype == 2 else None
                _read_lengths(r, main_lens, 0, 256)
                _read_lengths(r, main_lens, 256, nmain)
                main = _Code(main_lens)
                _read_lengths(r, len_lens, 0, NUM_LENGTHS)
                length = _Code(len_lens)
            else:
                raise LZXError("bad block type %d" % btype)
            continue
        if btype == 3:
            k = min(left, end - len(out))
            out += r.raw(k)
            left -= k
        else:
            left = _tokens(r, out, left, end, main, length, aligned, R)
        if len(out) == end:
            r.align()
            end = min(end + FRAME, size)
    if left:
        raise LZXError("the last block is longer than the output")
    if pad and r.pos < len(data):
        r.raw(1)
    if r.pos != len(data):
        raise LZXError("data after the end")
    if e8:
        for start in range(0, min(size, 1 << 30), FRAME):
            _e8_reverse(out, start, min(FRAME, size - start), e8)
    return bytes(out)


# ---------------------------------------------------------------- encoder

def limited_lengths(freqs, limit):
    """Optimal code lengths with no length above limit (package-merge)."""
    syms = sorted((f, s) for s, f in enumerate(freqs) if f > 0)
    lengths = [0] * len(freqs)
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


def _lengths(freqs, limit, at_least_two):
    """Complete code lengths. A tree with one used symbol gets a second
    symbol, so that its two codes are 0 and 1. An unused tree stays
    empty unless at_least_two is set."""
    used = [s for s, f in enumerate(freqs) if f]
    if len(used) >= 2:
        return limited_lengths(freqs, limit)
    lengths = [0] * len(freqs)
    if used or at_least_two:
        a = used[0] if used else 0
        lengths[a] = lengths[1 if a == 0 else 0] = 1
    return lengths


def _canonical(lengths):
    """Codes in canonical order: shorter first, then by symbol."""
    maxlen = max(lengths, default=0)
    count = [0] * (maxlen + 1)
    for ln in lengths:
        if ln:
            count[ln] += 1
    nxt, code = [0] * (maxlen + 1), 0
    for ln in range(1, maxlen + 1):
        code = (code + count[ln - 1]) << 1 if ln > 1 else 0
        nxt[ln] = code
    codes = [0] * len(lengths)
    for s, ln in enumerate(lengths):
        if ln:
            codes[s] = nxt[ln]
            nxt[ln] += 1
    return codes


def _length_ops(ops, new, old, first, last):
    """Write new[first:last] with a pretree, as differences to old."""
    toks, x = [], first
    while x < last:
        v, r = new[x], 1
        while x + r < last and new[x + r] == v:
            r += 1
        if v == 0 and r >= 20:
            k = min(r, 51)
            toks.append((18, 5, k - 20))
        elif v == 0 and r >= 4:
            k = r
            toks.append((17, 4, k - 4))
        elif r >= 4:
            k = min(r, 5)
            toks.append((19, 1, k - 4, (old[x] - v) % 17))
        else:
            k = 1
            toks.append(((old[x] - v) % 17,))
        x += k
    freq = [0] * 20
    for t in toks:
        freq[t[0]] += 1
        if t[0] == 19:
            freq[t[3]] += 1
    pl = _lengths(freq, 15, True)
    pc = _canonical(pl)
    ops.extend((pl[i], 4) for i in range(20))
    for t in toks:
        ops.append((pc[t[0]], pl[t[0]]))
        if len(t) > 1:
            ops.append((t[2], t[1]))
        if t[0] == 19:
            ops.append((pc[t[3]], pl[t[3]]))


def _block_ops(btype, tokens, size, old_main, old_len):
    """The bits of a verbatim (1) or aligned offset (2) block."""
    main_f, len_f, al_f = [0] * len(old_main), [0] * NUM_LENGTHS, [0] * 8
    for ms, ls, extra, footer in tokens:
        main_f[ms] += 1
        if ls >= 0:
            len_f[ls] += 1
        if btype == 2 and extra >= 3:
            al_f[footer & 7] += 1
    ml, ll = _lengths(main_f, 16, True), _lengths(len_f, 16, False)
    mc, lc = _canonical(ml), _canonical(ll)
    ops = [(btype, 3), (size, 24)]
    if btype == 2:
        al = _lengths(al_f, 7, True)
        ac = _canonical(al)
        ops.extend((al[i], 3) for i in range(8))
    _length_ops(ops, ml, old_main, 0, 256)
    _length_ops(ops, ml, old_main, 256, len(old_main))
    _length_ops(ops, ll, old_len, 0, NUM_LENGTHS)
    for ms, ls, extra, footer in tokens:
        ops.append((mc[ms], ml[ms]))
        if ls >= 0:
            ops.append((lc[ls], ll[ls]))
        if btype == 2 and extra >= 3:
            ops.append((footer >> 3, extra - 3))
            ops.append((ac[footer & 7], al[footer & 7]))
        elif extra:
            ops.append((footer, extra))
    return ops, ml, ll


class _Writer:
    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.n = 0

    def bits(self, n, v):
        self.acc = (self.acc << n) | v
        self.n += n
        while self.n >= 16:
            self.n -= 16
            w = (self.acc >> self.n) & 0xFFFF
            self.out += bytes((w & 0xFF, w >> 8))
        self.acc &= (1 << self.n) - 1

    def align(self):
        if self.n:
            self.bits(16 - self.n, 0)


def _match_len(buf, a, b, cap):
    if buf[a:a + cap] == buf[b:b + cap]:
        return cap
    n = 0
    while buf[a + n] == buf[b + n]:
        n += 1
    return n


class _Finder:
    """A greedy parse with a hash chain over 3-byte strings."""

    def __init__(self, buf, max_offset, depth=32):
        self.buf, self.max_offset, self.depth = buf, max_offset, depth
        self.head, self.prev, self.done = {}, [-1] * len(buf), 0

    def _insert_to(self, p):
        buf = self.buf
        for i in range(self.done, min(p, len(buf) - 2)):
            key = buf[i] | buf[i + 1] << 8 | buf[i + 2] << 16
            self.prev[i] = self.head.get(key, -1)
            self.head[key] = i
        self.done = max(self.done, p)

    def parse(self, s, e, R):
        """Tokens (main symbol, length symbol or -1, footer bits, footer)
        for buf[s:e]. R is updated as the decoder will update it."""
        buf, tokens, p = self.buf, [], s
        while p < e:
            self._insert_to(p)
            cap = min(MAX_MATCH, e - p)
            best, dist = 0, 0
            if cap >= 2:
                for d in R:
                    if d <= min(p, self.max_offset):
                        n = _match_len(buf, p - d, p, cap)
                        if n > best:
                            best, dist = n, d
            if cap >= 3 and best < cap and p + 3 <= len(buf):
                c = self.head.get(buf[p] | buf[p + 1] << 8 | buf[p + 2] << 16, -1)
                for _ in range(self.depth):
                    if c < 0 or p - c > self.max_offset:
                        break
                    n = _match_len(buf, c, p, cap)
                    if n > best and n >= 3:
                        best, dist = n, p - c
                        if n == cap:
                            break
                    c = self.prev[c]
            if best < 2:
                tokens.append((buf[p], -1, 0, 0))
                p += 1
                continue
            if dist == R[0]:
                f = 0
            elif dist == R[1]:
                f = 1
                R[0], R[1] = R[1], R[0]
            elif dist == R[2]:
                f = 2
                R[0], R[2] = R[2], R[0]
            else:
                f = dist + 2
                R[0], R[1], R[2] = dist, R[0], R[1]
            slot = f if f < 4 else bisect_right(BASE, f) - 1
            ms = 256 + 8 * slot + min(best - 2, 7)
            tokens.append((ms, best - 9 if best >= 9 else -1, EXTRA[slot], f - BASE[slot]))
            p += best
        return tokens


def _e8_forward(buf, start, size, e8):
    """The E8 translation of one frame: relative call targets become
    absolute ones. _e8_reverse undoes it."""
    i = 0
    while i < size - 10:
        if buf[start + i] != 0xE8:
            i += 1
            continue
        cur = start + i
        rel = int.from_bytes(buf[cur + 1:cur + 5], "little", signed=True)
        if -cur <= rel < e8 - cur:
            buf[cur + 1:cur + 5] = (rel + cur).to_bytes(4, "little")
        elif e8 - cur <= rel < e8:
            buf[cur + 1:cur + 5] = ((rel - e8) & 0xFFFFFFFF).to_bytes(4, "little")
        i += 5


def compress(data, window_bits=None, e8_size=0, block_type=None):
    """Encode data as an LZX stream. window_bits defaults to the smallest
    CAB window that holds the data. e8_size > 0 turns on the E8
    translation. block_type 1, 2 or 3 forces one block type."""
    data = bytes(data)
    n = len(data)
    if window_bits is None:
        window_bits = next((b for b in range(15, 22) if 1 << b >= n), 21)
    if window_bits not in SLOTS:
        raise ValueError("window_bits must be 15 to 21")
    if not 0 <= e8_size < 1 << 31:
        raise ValueError("e8_size must be 0 to 2**31 - 1")
    if block_type not in (None, 1, 2, 3):
        raise ValueError("block_type must be 1, 2 or 3")
    if n == 0:
        return b""
    buf = bytearray(data)
    if e8_size:
        for start in range(0, min(n, 1 << 30), FRAME):
            _e8_forward(buf, start, min(FRAME, n - start), e8_size)
    w = _Writer()
    w.bits(1, 1 if e8_size else 0)
    if e8_size:
        w.bits(16, e8_size >> 16)
        w.bits(16, e8_size & 0xFFFF)
    old_main = [0] * (256 + 8 * SLOTS[window_bits])
    old_len = [0] * NUM_LENGTHS
    R = [1, 1, 1]
    finder = _Finder(buf, (1 << window_bits) - 3)
    for s in range(0, n, FRAME):
        e = min(s + FRAME, n)
        saved = R[:]
        tokens = finder.parse(s, e, R)
        best = None
        for bt in (1, 2) if block_type is None else (block_type,):
            if bt == 3:
                continue
            ops, ml, ll = _block_ops(bt, tokens, e - s, old_main, old_len)
            cost = sum(k for _, k in ops)
            if best is None or cost < best[0]:
                best = (cost, ops, ml, ll)
        raw_cost = 27 + 16 + 96 + 8 * (e - s + 1)
        if block_type == 3 or (block_type is None and raw_cost < best[0]):
            R[:] = saved
            w.bits(3, 3)
            w.bits(24, e - s)
            w.bits(16 - w.n, 0)                     # 1 to 16 bits of padding
            for v in R:
                w.out += v.to_bytes(4, "little")
            w.out += buf[s:e]
            if (e - s) % 2:
                w.out.append(0)
        else:
            for v, k in best[1]:
                w.bits(k, v)
            old_main, old_len = best[2], best[3]
        w.align()                                   # the end of a frame
    return bytes(w.out)
