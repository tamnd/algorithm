# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-scalable-texture-compression/. The authors are listed in prov/XB2HVD.jsonl.

"""A stated subset of the ASTC decoder: bounded integer sequence encoding
(BISE) in both directions, and the decoding of one 2D LDR block with one
partition, one weight plane and the color endpoint modes 8 (RGB direct) and
12 (RGBA direct).

Every block has 128 bits:
- bits 0..10: the block mode (weight grid size, weight range, dual plane);
- bits 11..12: the partition count minus 1;
- bits 13..16: the color endpoint mode (for one partition);
- bits 17 upward: the color values, as one BISE stream;
- bits 127 downward: the weights, as one BISE stream with the bit order
  reversed (bit k of the stream is bit 127 - k of the block).

Out of the subset (an error is raised): void-extent blocks, dual-plane
blocks, more than one partition, other color endpoint modes, HDR, sRGB and
3D blocks. Illegal blocks decode to the LDR error color.

The decoder returns the 16-bit values that the interpolation produces, before
the conversion to the output format. Nothing here is an encoder in the
sense of a search: pack_block only writes given fields into a block.
"""

from fractions import Fraction
from math import ceil

BLOCK_BITS = 128
FOOTPRINTS = [(4, 4), (5, 4), (5, 5), (6, 5), (6, 6), (8, 5), (8, 6), (8, 8),
              (10, 5), (10, 6), (10, 8), (10, 10), (12, 10), (12, 12)]
ERROR_COLOR = (0xFFFF, 0, 0xFFFF, 0xFFFF)  # opaque magenta, the LDR error color


def bits_per_texel(width, height):
    return Fraction(BLOCK_BITS, width * height)


# ---------------------------------------------------------------- BISE

# kind -> (values per group, packed bits per group, packed bits after each value)
GROUP = {
    "bits": (1, 0, (0,)),
    "trit": (5, 8, (2, 2, 1, 2, 1)),  # m0 T[1:0] m1 T[3:2] m2 T[4] m3 T[6:5] m4 T[7]
    "quint": (3, 7, (3, 2, 2)),  # m0 Q[2:0] m1 Q[4:3] m2 Q[6:5]
}


def ise_params(max_value):
    """A range 0..max_value with max_value + 1 = 2^n, 3 * 2^n or 5 * 2^n."""
    count = max_value + 1
    for kind, f in (("bits", 1), ("trit", 3), ("quint", 5)):
        if count % f == 0:
            q = count // f
            if q & (q - 1) == 0:
                return kind, q.bit_length() - 1
    raise ValueError(f"0..{max_value} is not a BISE range")


def ise_rate(max_value):
    """The exact number of bits per value, n + 8/5 for trits, n + 7/3 for quints."""
    kind, n = ise_params(max_value)
    size, packed, _ = GROUP[kind]
    return n + Fraction(packed, size)


def ise_bits(count, max_value):
    return ceil(count * ise_rate(max_value))


def bit(x, i):
    return (x >> i) & 1


def decode_trits(t):
    """The 8-bit packed field T -> five trits (t0, ..., t4)."""
    if (t >> 2) & 7 == 7:
        c = ((t >> 5) & 7) << 2 | (t & 3)
        t4 = t3 = 2
    else:
        c = t & 31
        if (t >> 5) & 3 == 3:
            t4, t3 = 2, bit(t, 7)
        else:
            t4, t3 = bit(t, 7), (t >> 5) & 3
    if c & 3 == 3:
        t2, t1, t0 = 2, bit(c, 4), bit(c, 3) << 1 | (bit(c, 2) & (1 - bit(c, 3)))
    elif (c >> 2) & 3 == 3:
        t2, t1, t0 = 2, 2, c & 3
    else:
        t2, t1, t0 = bit(c, 4), (c >> 2) & 3, bit(c, 1) << 1 | (bit(c, 0) & (1 - bit(c, 1)))
    return (t0, t1, t2, t3, t4)


def decode_quints(q):
    """The 7-bit packed field Q -> three quints (q0, q1, q2)."""
    if (q >> 1) & 3 == 3 and (q >> 5) & 3 == 0:
        nq0 = 1 - bit(q, 0)
        q2 = bit(q, 0) << 2 | (bit(q, 4) & nq0) << 1 | (bit(q, 3) & nq0)
        return (4, 4, q2)
    if (q >> 1) & 3 == 3:
        q2 = 4
        c = ((q >> 3) & 3) << 3 | (3 - ((q >> 5) & 3)) << 1 | bit(q, 0)
    else:
        q2 = (q >> 5) & 3
        c = q & 31
    if c & 7 == 5:
        q1, q0 = 4, (c >> 3) & 3
    else:
        q1, q0 = (c >> 3) & 3, c & 7
    return (q0, q1, q2)


DECODE_TABLE = {
    "bits": [(0,)],
    "trit": [decode_trits(t) for t in range(256)],
    "quint": [decode_quints(q) for q in range(128)],
}

# The encoder uses the smallest packed field for each tuple. For a short last
# group this keeps the bits past the end of the stream zero (see the proof).
ENCODE_TABLE = {}
for _kind, _table in DECODE_TABLE.items():
    ENCODE_TABLE[_kind] = {}
    for _code, _tuple in enumerate(_table):
        ENCODE_TABLE[_kind].setdefault(_tuple, _code)


def ise_encode(values, max_value):
    """Values in 0..max_value -> (stream, length in bits)."""
    kind, n = ise_params(max_value)
    size, _, split = GROUP[kind]
    if any(not 0 <= v <= max_value for v in values):
        raise ValueError("value out of range")
    stream = pos = 0
    for g in range(0, len(values), size):
        group = list(values[g:g + size]) + [0] * (size - len(values[g:g + size]))
        code = ENCODE_TABLE[kind][tuple(v >> n for v in group)]
        used = 0
        for j, v in enumerate(group):
            stream |= (v & ((1 << n) - 1)) << pos
            pos += n
            stream |= ((code >> used) & ((1 << split[j]) - 1)) << pos
            pos += split[j]
            used += split[j]
    length = ise_bits(len(values), max_value)
    assert stream >> length == 0, "a bit past the end of the stream is set"
    return stream, length


def ise_decode(stream, count, max_value):
    """Read count values in 0..max_value from the low bits of stream."""
    kind, n = ise_params(max_value)
    size, _, split = GROUP[kind]
    stream &= (1 << ise_bits(count, max_value)) - 1  # @line L11
    out, pos = [], 0
    while len(out) < count:
        low, code, used = [], 0, 0
        for j in range(size):
            low.append((stream >> pos) & ((1 << n) - 1))  # @line L12
            pos += n
            code |= ((stream >> pos) & ((1 << split[j]) - 1)) << used
            pos += split[j]
            used += split[j]
        high = DECODE_TABLE[kind][code]  # @line L13
        out.extend(h << n | m for h, m in zip(high, low))  # @line L14
    return out[:count]


# ---------------------------------------------------------------- unquantization

COLOR_RANGES = [5, 7, 9, 11, 15, 19, 23, 31, 39, 47, 63, 79, 95, 127, 159, 191, 255]

# max value -> (pattern of B from bit 8 down to bit 0, C); a is bit 0 of the low bits.
COLOR_TQ = {
    5: ("000000000", 204), 9: ("000000000", 113), 11: ("b000b0bb0", 93),
    19: ("b0000bb00", 54), 23: ("cb000cbcb", 44), 39: ("cb0000cbc", 26),
    47: ("dcb000dcb", 22), 79: ("dcb0000dc", 13), 95: ("edcb000ed", 11),
    159: ("edcb0000e", 6), 191: ("fedcb000f", 5),
}
WEIGHT_TQ = {
    5: ("0000000", 50), 9: ("0000000", 28), 11: ("b000b0b", 23),
    19: ("b0000b0", 13), 23: ("cb000cb", 11),
}
WEIGHT_DIRECT = {2: (0, 32, 63), 4: (0, 16, 32, 47, 63)}

# (H, R) of the block mode -> the largest weight value
WEIGHT_RANGES = {(0, 2): 1, (0, 3): 2, (0, 4): 3, (0, 5): 4, (0, 6): 5, (0, 7): 7,
                 (1, 2): 9, (1, 3): 11, (1, 4): 15, (1, 5): 19, (1, 6): 23, (1, 7): 31}


def replicate(value, n, width):
    """Repeat the n-bit pattern of value from the top until width bits are filled."""
    out, filled = 0, 0
    while filled < width:
        out, filled = out << n | value, filled + n
    return out >> (filled - width)


def pattern_value(pattern, low):
    v = 0
    for ch in pattern:
        v = v << 1 | (0 if ch == "0" else bit(low, ord(ch) - ord("a")))
    return v


def unquant_color(value, max_value):
    """A color value in 0..max_value -> 0..255."""
    kind, n = ise_params(max_value)
    if kind == "bits":
        return replicate(value, n, 8)
    d, low = value >> n, value & ((1 << n) - 1)
    a = 0x1FF if low & 1 else 0
    pattern, c = COLOR_TQ[max_value]
    t = (d * c + pattern_value(pattern, low)) ^ a
    return (a & 0x80) | (t >> 2)


def unquant_weight(value, max_value):
    """A weight in 0..max_value -> 0..64."""
    kind, n = ise_params(max_value)
    if kind == "bits":
        t = replicate(value, n, 6)
    elif max_value in WEIGHT_DIRECT:
        t = WEIGHT_DIRECT[max_value][value]
    else:
        d, low = value >> n, value & ((1 << n) - 1)
        a = 0x7F if low & 1 else 0
        pattern, c = WEIGHT_TQ[max_value]
        t = (d * c + pattern_value(pattern, low)) ^ a
        t = (a & 0x20) | (t >> 2)
    return t + 1 if t > 32 else t


# ---------------------------------------------------------------- block decoding

def decode_block_mode(mode):
    """11 bits -> (grid width, grid height, largest weight, dual plane),
    "void" for a void-extent block, or None for a reserved mode."""
    if mode & 0x1FF == 0x1FC:
        return "void"
    a, h, d = (mode >> 5) & 3, bit(mode, 9), bit(mode, 10)
    if mode & 3:
        r = bit(mode, 4) | (mode & 3) << 1
        b, layout = (mode >> 7) & 3, (mode >> 2) & 3
        if layout == 0:
            w, g = b + 4, a + 2
        elif layout == 1:
            w, g = b + 8, a + 2
        elif layout == 2:
            w, g = a + 2, b + 8
        elif bit(mode, 8) == 0:
            w, g = a + 2, bit(mode, 7) + 6
        else:
            w, g = bit(mode, 7) + 2, a + 2
    else:
        r = bit(mode, 4) | ((mode >> 2) & 3) << 1
        if r < 2:
            return None
        layout = (mode >> 7) & 3
        if layout == 0:
            w, g = 12, a + 2
        elif layout == 1:
            w, g = a + 2, 12
        elif layout == 2:
            w, g = a + 6, ((mode >> 9) & 3) + 6
            h = d = 0
        elif bit(mode, 6):
            return None
        else:
            w, g = (10, 6) if bit(mode, 5) else (6, 10)
    return w, g, WEIGHT_RANGES[(h, r)], d


def color_range(cem, weight_bits):
    """The largest color range whose values fit in the bits left over."""
    count = 2 * (cem // 4 + 1)
    room = BLOCK_BITS - 17 - weight_bits
    fits = [r for r in COLOR_RANGES if ise_bits(count, r) <= room]
    return fits[-1] if fits else None


def blue_contract(r, g, b, a):
    return ((r + b) >> 1, (g + b) >> 1, b, a)


def endpoints(cem, v):
    """Modes 8 and 12: 6 or 8 values in 0..255 -> two RGBA endpoints."""
    if cem == 8:
        v = list(v) + [255, 255]
    if v[1] + v[3] + v[5] >= v[0] + v[2] + v[4]:
        return (v[0], v[2], v[4], v[6]), (v[1], v[3], v[5], v[7])
    return blue_contract(v[1], v[3], v[5], v[7]), blue_contract(v[0], v[2], v[4], v[6])


def infill(w, n, m, bw, bh, s, t):
    """The weight of texel (s, t) from the n x m grid w, by the fixed-point
    bilinear rule of the format."""
    ds = (1024 + bw // 2) // (bw - 1)
    dt = (1024 + bh // 2) // (bh - 1)
    gs = (ds * s * (n - 1) + 32) >> 6
    gt = (dt * t * (m - 1) + 32) >> 6
    js, fs, jt, ft = gs >> 4, gs & 15, gt >> 4, gt & 15
    v0 = js + jt * n
    w11 = (fs * ft + 8) >> 4
    w10, w01 = ft - w11, fs - w11
    w00 = 16 - fs - ft + w11

    def at(k):  # a neighbor past the grid always has the factor 0
        return w[k] if k < len(w) else 0

    return (at(v0) * w00 + at(v0 + 1) * w01 + at(v0 + n) * w10 + at(v0 + n + 1) * w11 + 8) >> 4


def interpolate(e0, e1, i):
    c0, c1 = e0 << 8 | e0, e1 << 8 | e1
    return (c0 * (64 - i) + c1 * i + 32) >> 6


def decode_block(block, bw, bh):
    """16 bytes -> bw * bh RGBA texels of 16-bit values, in raster order."""
    if len(block) != 16 or (bw, bh) not in FOOTPRINTS:
        raise ValueError("a block has 16 bytes and a legal 2D footprint")
    bits = int.from_bytes(block, "little")
    mode = decode_block_mode(bits & 0x7FF)  # @line L1
    if mode == "void":
        raise NotImplementedError("void-extent blocks are outside this subset")
    error = [ERROR_COLOR] * (bw * bh)
    if mode is None or mode[0] > bw or mode[1] > bh:
        return error
    n, m, wmax, dual = mode
    parts, cem = ((bits >> 11) & 3) + 1, (bits >> 13) & 15  # @line L2
    if dual or parts != 1 or cem not in (8, 12):
        raise NotImplementedError("only one plane, one partition and modes 8 and 12")
    wbits = ise_bits(n * m, wmax)  # @line L3
    if n * m > 64 or not 24 <= wbits <= 96:
        return error
    cmax = color_range(cem, wbits)  # @line L4
    if cmax is None:
        return error
    raw = ise_decode(bits >> 17, 2 * (cem // 4 + 1), cmax)
    v = [unquant_color(x, cmax) for x in raw]  # @line L5
    e0, e1 = endpoints(cem, v)  # @line L6
    wstream = sum(bit(bits, 127 - k) << k for k in range(wbits))
    w = [unquant_weight(x, wmax) for x in ise_decode(wstream, n * m, wmax)]  # @line L7
    out = []
    for t in range(bh):
        for s in range(bw):
            i = infill(w, n, m, bw, bh, s, t)  # @line L8
            out.append(tuple(interpolate(a, b, i) for a, b in zip(e0, e1)))  # @line L9
    return out  # @line L10


# ---------------------------------------------------------------- packing (for tests)

MODE_OF = {}
for _mode in range(2048):
    _info = decode_block_mode(_mode)
    if isinstance(_info, tuple) and _info[3] == 0:
        MODE_OF.setdefault(_info[:3], _mode)


def pack_block(n, m, wmax, cem, colors, weights):
    """Write a one-partition, one-plane block from raw (quantized) values."""
    wbits = ise_bits(n * m, wmax)
    cmax = color_range(cem, wbits)
    if len(colors) != 2 * (cem // 4 + 1) or len(weights) != n * m or cmax is None:
        raise ValueError("the fields do not fit")
    cstream, _ = ise_encode(colors, cmax)
    wstream, _ = ise_encode(weights, wmax)
    bits = MODE_OF[(n, m, wmax)] | cem << 13 | cstream << 17
    for k in range(wbits):
        bits |= bit(wstream, k) << (127 - k)
    return bits.to_bytes(16, "little"), cmax
