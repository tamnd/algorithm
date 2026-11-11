# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/table-driven-crc/. The authors are listed in prov/KSDEEZ.jsonl.

"""Table-driven CRC (Sarwate 1988): one table lookup for each byte.

The parameters follow the Rocksoft model of Ross Williams: width, poly
(normal notation), init, refin, refout, xorout. The width must be at least 8.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CRCParams:
    name: str
    width: int
    poly: int
    init: int
    refin: bool
    refout: bool
    xorout: int
    check: int


def reflect(value: int, width: int) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def make_table(width: int, poly: int) -> list[int]:
    """T[v] = v(x) * x^width mod G(x): the register after the byte v enters an
    all-zero register (normal form, top bit first)."""
    if width < 8:
        raise ValueError("width must be at least 8")
    top = 1 << (width - 1)
    mask = (1 << width) - 1
    table = []
    for v in range(256):  # @line L1
        reg = v << (width - 8)  # @line L2
        for _ in range(8):  # @line L3
            reg = ((reg << 1) & mask) ^ poly if reg & top else (reg << 1) & mask
        table.append(reg)  # @line L4
    return table


def crc_table(data: bytes, p: CRCParams, table: list[int] | None = None) -> int:
    """The CRC with a left-shifting register and one lookup for each byte."""
    if table is None:
        table = make_table(p.width, p.poly)
    shift = p.width - 8
    mask = (1 << p.width) - 1
    reg = p.init  # @line L5
    for v in data:  # @line L6
        if p.refin:  # @line L7
            v = reflect(v, 8)
        reg = ((reg << 8) & mask) ^ table[(reg >> shift) ^ v]  # @line L8
    if p.refout:  # @line L9
        reg = reflect(reg, p.width)
    return reg ^ p.xorout  # @line L10


def make_table_reflected(width: int, poly: int) -> list[int]:
    """T'[v] = reflect(T[reflect(v, 8)]): the table of the reflected form."""
    rpoly = reflect(poly, width)
    table = []
    for v in range(256):
        reg = v
        for _ in range(8):
            reg = (reg >> 1) ^ rpoly if reg & 1 else reg >> 1
        table.append(reg)
    return table


def crc_table_reflected(data: bytes, p: CRCParams, table: list[int] | None = None) -> int:
    """The form of zlib, for refin = refout = True: the register is kept in
    reversed bit order, so no byte or result is reversed."""
    if not (p.refin and p.refout):
        raise ValueError("needs refin and refout")
    if table is None:
        table = make_table_reflected(p.width, p.poly)
    reg = reflect(p.init, p.width)  # @line L11
    for v in data:  # @line L12
        reg = (reg >> 8) ^ table[(reg ^ v) & 0xFF]  # @line L13
    return reg ^ p.xorout  # @line L14


def _mulmod(a: int, b: int, g: int, width: int) -> int:
    """a * b mod g in GF(2)[x], for deg a, deg b < width = deg g."""
    r = 0
    top = 1 << width
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & top:
            a ^= g
    return r


def _x_pow_mod(e: int, g: int, width: int) -> int:
    """x^e mod g by square and multiply, for width >= 2."""
    result = 1
    base = 2
    while e:
        if e & 1:
            result = _mulmod(result, base, g, width)
        base = _mulmod(base, base, g, width)
        e >>= 1
    return result


def crc_combine(crc1: int, crc2: int, len2: int, p: CRCParams) -> int:
    """crc(A + B) from crc1 = crc(A), crc2 = crc(B) and len2 = len(B) in bytes.

    In the register domain, reg(AB) = (reg(A) + init) x^(8 len2) + reg(B)
    modulo G, with reg(.) the register before refout and xorout. The data A
    and B are not needed.
    """
    g = (1 << p.width) | p.poly

    def to_reg(c: int) -> int:
        c ^= p.xorout
        return reflect(c, p.width) if p.refout else c

    r1, r2 = to_reg(crc1), to_reg(crc2)
    shift = _x_pow_mod(8 * len2, g, p.width)
    reg = _mulmod(r1 ^ p.init, shift, g, p.width) ^ r2
    if p.refout:
        reg = reflect(reg, p.width)
    return reg ^ p.xorout


# Parameters and check values copied by hand from the CRC catalogue of
# Greg Cook (reveng).
CATALOGUE = {
    p.name: p
    for p in [
        CRCParams("CRC-16/ARC", 16, 0x8005, 0x0000, True, True, 0x0000, 0xBB3D),
        CRCParams("CRC-16/IBM-3740", 16, 0x1021, 0xFFFF, False, False, 0x0000, 0x29B1),
        CRCParams("CRC-16/XMODEM", 16, 0x1021, 0x0000, False, False, 0x0000, 0x31C3),
        CRCParams("CRC-16/KERMIT", 16, 0x1021, 0x0000, True, True, 0x0000, 0x2189),
        CRCParams("CRC-8/SMBUS", 8, 0x07, 0x00, False, False, 0x00, 0xF4),
        CRCParams("CRC-32/ISO-HDLC", 32, 0x04C11DB7, 0xFFFFFFFF, True, True, 0xFFFFFFFF, 0xCBF43926),
        CRCParams("CRC-32/ISCSI", 32, 0x1EDC6F41, 0xFFFFFFFF, True, True, 0xFFFFFFFF, 0xE3069283),
        CRCParams("CRC-32/BZIP2", 32, 0x04C11DB7, 0xFFFFFFFF, False, False, 0xFFFFFFFF, 0xFC891918),
        CRCParams("CRC-32/MPEG-2", 32, 0x04C11DB7, 0xFFFFFFFF, False, False, 0x00000000, 0x0376E6E7),
        CRCParams("CRC-64/XZ", 64, 0x42F0E1EBA9EA3693, (1 << 64) - 1, True, True, (1 << 64) - 1, 0x995DC9BBDF1939FA),
    ]
}
