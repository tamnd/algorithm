# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jpeg-compression/. The authors are listed in prov/2JBQT3.jsonl.

"""A baseline sequential JPEG coder (ITU-T T.81) for 8-bit greyscale images.

The subset: one component, 8-bit samples, the baseline process (SOF0) with
Huffman coding, one scan, no restart intervals, and the example tables of
Annex K (Table K.1 for quantization, K.3.3 for the Huffman tables). The
encoder writes a JFIF APP0 segment. The decoder reads any one-component
SOF0 file with 8-bit quantization tables and no restart markers; it skips
APPn and COM segments. Colour, chroma subsampling, restart markers, the
progressive, lossless and hierarchical processes, and arithmetic coding are
not implemented.

An image is a list of rows of integers in 0..255. Encoding and decoding cost
O(H W) time: each 8 x 8 block costs a constant number of operations
(1024 multiplications for the separable DCT).
"""

import math
from typing import Dict, List, Sequence, Tuple

# ---------------------------------------------------------------- tables

# Table K.1, luminance quantization table, in natural (row) order.
K1_LUMINANCE = [
    16, 11, 10, 16, 24, 40, 51, 61,
    12, 12, 14, 19, 26, 58, 60, 55,
    14, 13, 16, 24, 40, 57, 69, 56,
    14, 17, 22, 29, 51, 87, 80, 62,
    18, 22, 37, 56, 68, 109, 103, 77,
    24, 35, 55, 64, 81, 104, 113, 92,
    49, 64, 78, 87, 103, 121, 120, 101,
    72, 92, 95, 98, 112, 100, 103, 99,
]

# K.3.3.1: DC luminance, BITS (number of codes of length 1..16) and HUFFVAL.
DC_LUMINANCE_BITS = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
DC_LUMINANCE_VALUES = list(range(12))

# K.3.3.2: AC luminance.
AC_LUMINANCE_BITS = [0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7D]
AC_LUMINANCE_VALUES = [
    0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
    0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xA1, 0x08, 0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0,
    0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28,
    0x29, 0x2A, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
    0x4A, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
    0x6A, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7,
    0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5,
    0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2,
    0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8,
    0xF9, 0xFA,
]

SOI, EOI, APP0, DQT, SOF0, DHT, SOS, COM, DRI = 0xD8, 0xD9, 0xE0, 0xDB, 0xC0, 0xC4, 0xDA, 0xFE, 0xDD


def zigzag_order() -> List[int]:
    """Natural index 8 r + c of each zigzag position (T.81, Figure A.6)."""
    order = []
    for s in range(15):
        rows = range(max(0, s - 7), min(s, 7) + 1)
        for r in (rows if s % 2 == 1 else reversed(rows)):
            order.append(8 * r + (s - r))
    return order


ZIGZAG = zigzag_order()


def scaled_table(quality: int, base: Sequence[int] = K1_LUMINANCE) -> List[int]:
    """Scale a table by the IJG quality rule (1..100; 50 keeps the table).

    This rule comes from the Independent JPEG Group software, not from T.81.
    Entries are clamped to 1..255, as 8-bit tables need.
    """
    if not 1 <= quality <= 100:
        raise ValueError("quality must be in 1..100")
    scale = 5000 // quality if quality < 50 else 200 - 2 * quality
    return [min(255, max(1, (q * scale + 50) // 100)) for q in base]


# ------------------------------------------------- Huffman tables (Annex C)

def code_sizes(bits: Sequence[int]) -> List[int]:
    """HUFFSIZE, Figure C.1: the length of each code, in HUFFVAL order."""
    return [length for length in range(1, 17) for _ in range(bits[length - 1])]


def code_words(sizes: Sequence[int]) -> List[int]:
    """HUFFCODE, Figure C.2: consecutive codes, shifted left at each new length."""
    codes = []
    code = 0
    si = sizes[0] if sizes else 0
    for s in sizes:
        while s > si:
            code <<= 1
            si += 1
        codes.append(code)
        code += 1
    return codes


def encoder_table(bits: Sequence[int], values: Sequence[int]) -> Dict[int, Tuple[int, int]]:
    """EHUFCO and EHUFSI, Figure C.3: symbol -> (code, length)."""
    sizes = code_sizes(bits)
    return {v: (c, s) for v, c, s in zip(values, code_words(sizes), sizes)}


class DecoderTable:
    """MINCODE, MAXCODE and VALPTR of Figure F.15, for DECODE (Figure F.16)."""

    def __init__(self, bits: Sequence[int], values: Sequence[int]) -> None:
        codes = code_words(code_sizes(bits))
        self.values = list(values)
        self.mincode = [0] * 17
        self.maxcode = [-1] * 18
        self.valptr = [0] * 17
        j = 0
        for length in range(1, 17):
            if bits[length - 1]:
                self.valptr[length] = j
                self.mincode[length] = codes[j]
                j += bits[length - 1]
                self.maxcode[length] = codes[j - 1]
        self.maxcode[17] = 0xFFFFF  # ends the search on a bad code


# ------------------------------------------------------------- bit I/O

class BitWriter:
    """Packs bits MSB first; writes 0x00 after each 0xFF byte (F.1.2.3)."""

    def __init__(self) -> None:
        self.out = bytearray()
        self.acc = 0
        self.n = 0

    def write(self, value: int, length: int) -> None:
        self.acc = (self.acc << length) | (value & ((1 << length) - 1))
        self.n += length
        while self.n >= 8:
            self.n -= 8
            byte = (self.acc >> self.n) & 0xFF
            self.out.append(byte)
            if byte == 0xFF:
                self.out.append(0x00)
        self.acc &= (1 << self.n) - 1

    def flush(self) -> bytes:
        """Pad the last byte with 1-bits (B.1.1.5)."""
        if self.n:
            self.write((1 << (8 - self.n)) - 1, 8 - self.n)
        return bytes(self.out)


class BitReader:
    """Reads entropy-coded data; drops each 0x00 that follows 0xFF."""

    def __init__(self, data: bytes, pos: int) -> None:
        self.data = data
        self.pos = pos
        self.byte = 0
        self.left = 0

    def bit(self) -> int:
        if self.left == 0:
            if self.pos >= len(self.data):
                raise ValueError("entropy-coded data ended early")
            b = self.data[self.pos]
            if b == 0xFF:
                if self.pos + 1 >= len(self.data) or self.data[self.pos + 1] != 0x00:
                    raise ValueError("marker inside entropy-coded data")
                self.pos += 1
            self.pos += 1
            self.byte, self.left = b, 8
        self.left -= 1
        return (self.byte >> self.left) & 1

    def bits(self, n: int) -> int:
        v = 0
        for _ in range(n):
            v = (v << 1) | self.bit()
        return v

    def decode(self, t: DecoderTable) -> int:
        """DECODE, Figure F.16: read bits until the code is at most MAXCODE."""
        code = self.bit()
        length = 1
        while code > t.maxcode[length]:
            code = (code << 1) | self.bit()
            length += 1
            if length > 16:
                raise ValueError("bad Huffman code")
        return t.values[t.valptr[length] + code - t.mincode[length]]


def category(v: int) -> int:
    """SSSS: the number of bits of |v| (Tables F.1 and F.2)."""
    return abs(v).bit_length()


def extra_bits(v: int, s: int) -> int:
    """The s low bits of v, or of v - 1 when v < 0 (F.1.2.1)."""
    return v if v >= 0 else v + (1 << s) - 1


def extend(bits: int, s: int) -> int:
    """EXTEND, Figure F.12: undo extra_bits."""
    return bits if s == 0 or bits >= 1 << (s - 1) else bits - (1 << s) + 1


# ------------------------------------------------------------------ DCT

_M = [[(math.sqrt(0.5) if u == 0 else 1.0) / 2 * math.cos((2 * x + 1) * u * math.pi / 16) for x in range(8)] for u in range(8)]


def fdct(block: Sequence[float]) -> List[float]:
    """The 8 x 8 FDCT of A.3.3 on 64 samples in row order (orthonormal)."""
    tmp = [sum(_M[u][x] * block[8 * y + x] for x in range(8)) for y in range(8) for u in range(8)]
    return [sum(_M[v][y] * tmp[8 * y + u] for y in range(8)) for v in range(8) for u in range(8)]


def idct(coef: Sequence[float]) -> List[float]:
    """The 8 x 8 IDCT of A.3.3, the transpose of fdct."""
    tmp = [sum(_M[v][y] * coef[8 * v + u] for v in range(8)) for y in range(8) for u in range(8)]
    return [sum(_M[u][x] * tmp[8 * y + u] for u in range(8)) for y in range(8) for x in range(8)]


def quantize(f: float, q: int) -> int:
    """Round f / q to the nearest integer, halves away from zero (A.3.4)."""
    k = int(math.floor(abs(f) / q + 0.5))
    return k if f >= 0 else -k


# -------------------------------------------------------------- encoder

def _segment(marker: int, payload: bytes) -> bytes:
    return bytes([0xFF, marker]) + (len(payload) + 2).to_bytes(2, "big") + payload


def _blocks(img: Sequence[Sequence[int]]) -> Tuple[int, int, List[List[int]]]:
    """Cut the image into 8 x 8 blocks in raster order, repeating the edge samples."""
    h, w = len(img), len(img[0])
    bh, bw = (h + 7) // 8, (w + 7) // 8
    blocks = []
    for by in range(bh):
        for bx in range(bw):
            blocks.append([img[min(8 * by + y, h - 1)][min(8 * bx + x, w - 1)] for y in range(8) for x in range(8)])
    return bh, bw, blocks


def encode(img: Sequence[Sequence[int]], qtable: Sequence[int] = K1_LUMINANCE) -> bytes:
    """Baseline JPEG file for an 8-bit greyscale image, qtable in row order."""
    h, w = len(img), len(img[0])
    if not (1 <= h <= 65535 and 1 <= w <= 65535) or not all(1 <= q <= 255 for q in qtable):
        raise ValueError("bad size or table")
    dc_table = encoder_table(DC_LUMINANCE_BITS, DC_LUMINANCE_VALUES)
    ac_table = encoder_table(AC_LUMINANCE_BITS, AC_LUMINANCE_VALUES)
    head = bytearray([0xFF, SOI])  # @line L1
    head += _segment(APP0, b"JFIF\x00\x01\x02\x00\x00\x01\x00\x01\x00\x00")
    head += _segment(DQT, bytes([0x00] + [qtable[z] for z in ZIGZAG]))
    head += _segment(SOF0, bytes([8]) + h.to_bytes(2, "big") + w.to_bytes(2, "big") + bytes([1, 1, 0x11, 0]))
    head += _segment(DHT, bytes([0x00] + DC_LUMINANCE_BITS + DC_LUMINANCE_VALUES))
    head += _segment(DHT, bytes([0x10] + AC_LUMINANCE_BITS + AC_LUMINANCE_VALUES))
    head += _segment(SOS, bytes([1, 1, 0x00, 0, 63, 0]))
    bw = BitWriter()
    pred = 0  # @line L2
    for block in _blocks(img)[2]:  # @line L3
        coef = fdct([s - 128 for s in block])  # @line L4
        sq = [quantize(coef[i], qtable[i]) for i in range(64)]  # @line L5
        zz = [sq[z] for z in ZIGZAG]  # @line L6
        diff = zz[0] - pred  # @line L7
        pred = zz[0]
        s = category(diff)
        bw.write(*dc_table[s])
        bw.write(extra_bits(diff, s), s)
        run = 0
        for k in range(1, 64):  # @line L8
            v = zz[k]
            if v == 0:
                run += 1
                continue
            while run > 15:
                bw.write(*ac_table[0xF0])  # ZRL
                run -= 16
            s = category(v)
            bw.write(*ac_table[(run << 4) | s])
            bw.write(extra_bits(v, s), s)
            run = 0
        if run:
            bw.write(*ac_table[0x00])  # EOB
    data = bw.flush()  # @line L9
    return bytes(head) + data + bytes([0xFF, EOI])  # @line L10


# -------------------------------------------------------------- decoder

def decode(data: bytes) -> List[List[int]]:
    """Decode a one-component baseline JPEG file without restart markers."""
    if data[:2] != bytes([0xFF, SOI]):
        raise ValueError("no SOI")
    pos = 2
    qtables: Dict[int, List[int]] = {}
    htables: Dict[Tuple[int, int], DecoderTable] = {}
    frame = None
    while True:  # @line L11
        if data[pos] != 0xFF:
            raise ValueError("marker expected")
        while data[pos + 1] == 0xFF:  # fill bytes
            pos += 1
        marker = data[pos + 1]
        length = int.from_bytes(data[pos + 2:pos + 4], "big")
        body = data[pos + 4:pos + 2 + length]
        pos += 2 + length
        if marker == DQT:
            i = 0
            while i < len(body):
                pq, tq = body[i] >> 4, body[i] & 15
                if pq != 0:
                    raise NotImplementedError("16-bit quantization tables")
                table = [0] * 64
                for k in range(64):
                    table[ZIGZAG[k]] = body[i + 1 + k]
                qtables[tq] = table
                i += 65
        elif marker == DHT:
            i = 0
            while i < len(body):
                tc, th = body[i] >> 4, body[i] & 15
                bits = list(body[i + 1:i + 17])
                values = list(body[i + 17:i + 17 + sum(bits)])
                htables[(tc, th)] = DecoderTable(bits, values)
                i += 17 + sum(bits)
        elif marker == SOF0:
            if body[0] != 8 or body[5] != 1:
                raise NotImplementedError("only 8-bit, one-component frames")
            frame = (int.from_bytes(body[1:3], "big"), int.from_bytes(body[3:5], "big"), body[6], body[8])
        elif marker == SOS:
            break
        elif 0xE0 <= marker <= 0xEF or marker == COM:
            continue
        else:
            raise NotImplementedError("marker 0x%02X" % marker)
    if frame is None or body[0] != 1 or body[1] != frame[2] or (body[3], body[4], body[5]) != (0, 63, 0):
        raise NotImplementedError("only one sequential scan of the frame's component")
    h, w, _, tq = frame
    if h == 0:
        raise NotImplementedError("DNL marker")
    q = qtables[tq]
    dct, act = htables[(0, body[2] >> 4)], htables[(1, body[2] & 15)]
    reader = BitReader(data, pos)
    bh, bw = (h + 7) // 8, (w + 7) // 8
    out = [[0] * (8 * bw) for _ in range(8 * bh)]
    pred = 0
    for b in range(bh * bw):
        zz = [0] * 64
        s = reader.decode(dct)  # @line L12
        pred += extend(reader.bits(s), s)
        zz[0] = pred
        k = 1
        while k < 64:  # @line L13
            rs = reader.decode(act)
            r, s = rs >> 4, rs & 15
            if s == 0:
                if r != 15:  # EOB
                    break
                k += 16  # ZRL
                continue
            k += r
            if k > 63:
                raise ValueError("run past the end of the block")
            zz[k] = extend(reader.bits(s), s)
            k += 1
        coef = [0] * 64
        for i in range(64):
            coef[ZIGZAG[i]] = zz[i] * q[ZIGZAG[i]]
        samples = idct(coef)  # @line L14
        by, bx = divmod(b, bw)
        for y in range(8):
            row = out[8 * by + y]
            for x in range(8):
                row[8 * bx + x] = max(0, min(255, int(math.floor(samples[8 * y + x] + 128.5))))
    pos = reader.pos
    if data[pos:pos + 2] != bytes([0xFF, EOI]):
        raise ValueError("no EOI after the scan")
    return [row[:w] for row in out[:h]]  # @line L15
