# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzo/. The authors are listed in prov/34ZTAK.jsonl.
"""LZO1X: the byte stream of lzo1x_decompress_safe, version 0 and LZO-RLE.

Subset: this file covers the LZO1X stream only (no LZO1, LZO1A, ..., LZO2A,
and no lzop file header or checksums). The decoder accepts what the Linux
lzo1x_decompress_safe accepts: version 0 streams, and version 1 (LZO-RLE)
streams that start with the bytes 17, version. The encoder is a greedy
LZO1X-1 style compressor with one hash slot per 4-byte key. It writes
version 0, or version 1 when rle=True.

A stream is a list of instructions. Each copy instruction carries a length,
a distance and S, the number (0 to 3) of literal bytes that come after it.
The meaning of an opcode below 16 depends on the state that the last
instruction left: 0 (no literals), 1 to 3, or 4 (a long literal run).
The stream ends with a copy at distance 16384 with length 3: 11 00 00.
"""

MAX_OFFSET_V0 = 0xBFFF   # M4_MAX_OFFSET_V0 in lzodefs.h
MAX_OFFSET_V1 = 0xBFFE   # M4_MAX_OFFSET_V1: 0xbfff means a zero run in v1
MIN_ZERO_RUN = 4
MAX_ZERO_RUN = 2047 + MIN_ZERO_RUN
MIN_MATCH = 4            # the encoder looks up 4-byte keys
END_MARKER = b"\x11\x00\x00"


class LzoError(ValueError):
    """The input is not a valid LZO1X stream."""


# ---------------------------------------------------------------- decoder

class _Input:
    def __init__(self, data, pos):
        self.data = data
        self.pos = pos

    def byte(self):
        if self.pos >= len(self.data):
            raise LzoError("input overrun")
        b = self.data[self.pos]
        self.pos += 1
        return b

    def le16(self):
        return self.byte() | self.byte() << 8

    def peek_le16(self):
        if self.pos + 2 > len(self.data):
            raise LzoError("input overrun")
        return self.data[self.pos] | self.data[self.pos + 1] << 8

    def take(self, k):
        if self.pos + k > len(self.data):
            raise LzoError("input overrun")
        chunk = self.data[self.pos:self.pos + k]
        self.pos += k
        return chunk

    def length(self, low, bits):
        """LEN(t, bits): the low bits of the opcode, or 2^bits - 1 + 255*zeros + byte."""
        v = low & ((1 << bits) - 1)
        if v:
            return v
        zeros = 0
        b = self.byte()
        while b == 0:
            zeros += 1
            b = self.byte()
        return (1 << bits) - 1 + 255 * zeros + b


def decompress(data):
    """Decode one LZO1X stream (version 0 or LZO-RLE) and return the bytes."""
    data = bytes(data)
    if len(data) < 3:
        raise LzoError("input overrun")
    version, start = 0, 0
    if len(data) >= 5 and data[0] == 17:                      # @line L1
        version, start = data[1], 2
    inp = _Input(data, start)
    out = bytearray()
    state = 0
    if data[start] > 17:
        t = inp.byte() - 17
        out += inp.take(t)
        state = t if t < 4 else 4
    while True:                                               # @line L2
        t = inp.byte()                                        # @line L3
        if t < 16 and state == 0:                             # @line L4
            ln = 3 + inp.length(t, 4)                         # @line L5
            out += inp.take(ln)
            state = 4
            continue
        if t < 16 and state < 4:                              # @line L6
            ln, d, s = 2, 1 + (t >> 2) + (inp.byte() << 2), t & 3
        elif t < 16:                                          # @line L7
            ln, d, s = 3, 2049 + (t >> 2) + (inp.byte() << 2), t & 3
        elif t >= 64:                                         # @line L8
            ln, d, s = (t >> 5) + 1, 1 + ((t >> 2) & 7) + (inp.byte() << 3), t & 3
        elif t >= 32:                                         # @line L9
            ln = 2 + inp.length(t, 5)
            w = inp.le16()
            d, s = 1 + (w >> 2), w & 3
        elif version and t >> 3 == 3 and inp.peek_le16() >> 2 == 0x3FFF:  # @line L10
            w = inp.le16()
            out += bytes(((t & 7) | inp.byte() << 3) + MIN_ZERO_RUN)
            s = w & 3
            out += inp.take(s)
            state = s
            continue
        else:
            ln = 2 + inp.length(t, 3)                         # @line L11
            w = inp.le16()
            d, s = ((t & 8) << 11) + (w >> 2), w & 3
            if d == 0:                                        # @line L12
                if ln != 3:
                    raise LzoError("bad end marker")
                if inp.pos != len(data):
                    raise LzoError("input not consumed")
                return bytes(out)
            d += 16384
        if d > len(out):                                      # @line L13
            raise LzoError("lookbehind overrun")
        _copy(out, d, ln)
        out += inp.take(s)                                    # @line L14
        state = s


def _copy(out, d, ln):
    """Append ln bytes from distance d; the source may overlap the output."""
    src = len(out) - d
    if d >= ln:
        out += out[src:src + ln]
        return
    while ln > 0:
        k = min(d, ln)
        out += out[src:src + k]
        ln -= k


# ---------------------------------------------------------------- encoder

class _Writer:
    def __init__(self, rle):
        self.out = bytearray(b"\x11\x01" if rle else b"")
        self.start = len(self.out)
        self.s_at = -1          # the byte that holds S of the last instruction

    def ext(self, v):
        while v > 255:
            self.out.append(0)
            v -= 255
        self.out.append(v)

    def literals(self, lits):
        t = len(lits)
        if t == 0:
            return
        out = self.out
        if len(out) == self.start:
            if t <= 238:
                out.append(17 + t)          # first byte 18..255
            else:
                out.append(0)
                self.ext(t - 18)
        elif t <= 3:
            out[self.s_at] |= t             # S bits of the last copy
        elif t <= 18:
            out.append(t - 3)
        else:
            out.append(0)
            self.ext(t - 18)
        out += lits

    def match(self, ln, d):
        out = self.out
        if ln <= 8 and d <= 2048:           # 01LDDDSS or 1LLDDDSS
            e = d - 1
            out.append(((ln - 1) << 5) | ((e & 7) << 2))
            out.append(e >> 3)
            self.s_at = len(out) - 2
            return
        if d <= 16384:                      # 001LLLLL
            e = d - 1
            if ln <= 33:
                out.append(32 | (ln - 2))
            else:
                out.append(32)
                self.ext(ln - 33)
        else:                               # 0001HLLL
            e = d - 16384
            h = (e >> 11) & 8
            if ln <= 9:
                out.append(16 | h | (ln - 2))
            else:
                out.append(16 | h)
                self.ext(ln - 9)
        out.append((e << 2) & 0xFF)
        out.append((e >> 6) & 0xFF)
        self.s_at = len(out) - 2

    def zero_run(self, r):
        r -= MIN_ZERO_RUN
        self.out += bytes((0x18 | (r & 7), 0xFC, 0xFF, r >> 3))
        self.s_at = len(self.out) - 3


def compress(data, rle=False):
    """Greedy LZO1X encoder. rle=True writes an LZO-RLE (version 1) stream."""
    data = bytes(data)
    n = len(data)
    w = _Writer(rle)
    max_off = MAX_OFFSET_V1 if rle else MAX_OFFSET_V0
    table = {}
    lit = 0
    p = 0
    while p + MIN_MATCH <= n:
        key = data[p:p + MIN_MATCH]
        if rle and p > 0 and key == b"\x00\x00\x00\x00":
            r = MIN_MATCH
            while p + r < n and r < MAX_ZERO_RUN and data[p + r] == 0:
                r += 1
            w.literals(data[lit:p])
            w.zero_run(r)
            p += r
            lit = p
            continue
        cand = table.get(key)
        table[key] = p
        if cand is None or p - cand > max_off:
            p += 1
            continue
        d = p - cand
        ln = MIN_MATCH
        while p + ln < n and data[cand + ln] == data[p + ln]:
            ln += 1
        if rle and d > 16384 and ((d - 16384) & 0x403F) == 0x403F and 261 <= ln <= 264:
            ln = 260                        # 261..264 would read as a zero run
        w.literals(data[lit:p])
        w.match(ln, d)
        p += ln
        lit = p
    w.literals(data[lit:])
    w.out += END_MARKER
    return bytes(w.out)
