# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-redundancy-check/. The authors are listed in prov/JEXCDN.jsonl.

"""A bit-by-bit CRC in the Rocksoft parameter model of Ross Williams.

A CRC is given by width, poly, init, refin, refout and xorout. The values
check and residue are not inputs: the catalogue lists them so that an
implementation can be tested.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CRCParams:
    name: str
    width: int
    poly: int  # normal notation: the generator without its x^width term
    init: int
    refin: bool
    refout: bool
    xorout: int
    check: int  # CRC of the ASCII bytes "123456789"
    residue: int  # register after an error-free codeword, before xorout


def reflect(value: int, width: int) -> int:
    """Reverse the order of the low `width` bits of value."""
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def crc_register(data: bytes, p: CRCParams) -> int:
    """Run the shift register over data. Return the register, not reflected
    and without xorout. Each message bit enters at the top (MSB first)."""
    top = 1 << (p.width - 1)  # @line L1
    mask = (1 << p.width) - 1
    reg = p.init  # @line L2
    for byte in data:  # @line L3
        if p.refin:  # @line L4
            byte = reflect(byte, 8)
        for i in range(7, -1, -1):  # @line L5
            bit = (byte >> i) & 1
            feedback = bit ^ ((reg & top) != 0)  # @line L6
            reg = (reg << 1) & mask  # @line L7
            if feedback:  # @line L8
                reg ^= p.poly
    return reg


def crc(data: bytes, p: CRCParams) -> int:
    """The CRC value as the catalogue defines it."""
    reg = crc_register(data, p)
    if p.refout:  # @line L9
        reg = reflect(reg, p.width)
    return reg ^ p.xorout  # @line L10


def crc_reflected(data: bytes, p: CRCParams) -> int:
    """The same CRC for refin = refout = True, with a right-shifting register
    and the reflected polynomial. This is the form in zlib and most software."""
    if not (p.refin and p.refout):
        raise ValueError("needs refin and refout")
    rpoly = reflect(p.poly, p.width)
    reg = reflect(p.init, p.width)
    for byte in data:
        reg ^= byte
        for _ in range(8):
            reg = (reg >> 1) ^ rpoly if reg & 1 else reg >> 1
    return reg ^ p.xorout


def append_crc(data: bytes, p: CRCParams) -> bytes:
    """Message followed by its CRC, in the byte order that makes the codeword
    a multiple of the generator: little-endian when refout, else big-endian."""
    nbytes = (p.width + 7) // 8
    order = "little" if p.refout else "big"
    return data + crc(data, p).to_bytes(nbytes, order)


def residue_of(codeword: bytes, p: CRCParams) -> int:
    """Register over a codeword, reflected if refout, but without xorout."""
    reg = crc_register(codeword, p)
    return reflect(reg, p.width) if p.refout else reg


def poly_mod(a: int, g: int) -> int:
    """Remainder of a modulo g in GF(2)[x], with polynomials as ints."""
    dg = g.bit_length() - 1
    while a and a.bit_length() - 1 >= dg:
        a ^= g << (a.bit_length() - 1 - dg)
    return a


def poly_mulmod(a: int, b: int, g: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return poly_mod(r, g)


def forge_suffix(data: bytes, target: int, p: CRCParams) -> bytes:
    """Return width/8 bytes S such that crc(data + S) == target.

    The register after S is (R + S) x^r mod G, and x^r is invertible modulo G
    because G(0) = 1. So S = (target register) x^-r + R. This is why a CRC
    gives no protection against a deliberate change.
    """
    if p.width % 8:
        raise ValueError("needs a whole number of bytes")
    g = (1 << p.width) | p.poly
    want = target ^ p.xorout
    if p.refout:
        want = reflect(want, p.width)
    x_inv = (g ^ 1) >> 1  # x * ((G + 1) / x) = G + 1 = 1 mod G
    x_inv_r = 1
    for _ in range(p.width):
        x_inv_r = poly_mulmod(x_inv_r, x_inv, g)
    s = poly_mulmod(want, x_inv_r, g) ^ crc_register(data, p)
    out = s.to_bytes(p.width // 8, "big")
    if p.refin:
        out = bytes(reflect(b, 8) for b in out)
    return out


def crc_by_division(data: bytes, width: int, poly: int) -> int:
    """M(x) x^width mod G(x), for init = 0, no reflection and xorout = 0."""
    m = int.from_bytes(data, "big")
    g = (1 << width) | poly
    return poly_mod(m << width, g)


# Parameters copied by hand from the CRC catalogue of Greg Cook (reveng).
CATALOGUE = {
    p.name: p
    for p in [
        CRCParams("CRC-8/SMBUS", 8, 0x07, 0x00, False, False, 0x00, 0xF4, 0x00),
        CRCParams("CRC-16/ARC", 16, 0x8005, 0x0000, True, True, 0x0000, 0xBB3D, 0x0000),
        CRCParams("CRC-16/IBM-3740", 16, 0x1021, 0xFFFF, False, False, 0x0000, 0x29B1, 0x0000),
        CRCParams("CRC-16/KERMIT", 16, 0x1021, 0x0000, True, True, 0x0000, 0x2189, 0x0000),
        CRCParams("CRC-16/XMODEM", 16, 0x1021, 0x0000, False, False, 0x0000, 0x31C3, 0x0000),
        CRCParams("CRC-16/MODBUS", 16, 0x8005, 0xFFFF, True, True, 0x0000, 0x4B37, 0x0000),
        CRCParams("CRC-32/ISO-HDLC", 32, 0x04C11DB7, 0xFFFFFFFF, True, True, 0xFFFFFFFF, 0xCBF43926, 0xDEBB20E3),
        CRCParams("CRC-32/ISCSI", 32, 0x1EDC6F41, 0xFFFFFFFF, True, True, 0xFFFFFFFF, 0xE3069283, 0xB798B438),
        CRCParams("CRC-32/BZIP2", 32, 0x04C11DB7, 0xFFFFFFFF, False, False, 0xFFFFFFFF, 0xFC891918, 0xC704DD7B),
        CRCParams("CRC-32/MPEG-2", 32, 0x04C11DB7, 0xFFFFFFFF, False, False, 0x00000000, 0x0376E6E7, 0x00000000),
        CRCParams("CRC-64/XZ", 64, 0x42F0E1EBA9EA3693, 0xFFFFFFFFFFFFFFFF, True, True, 0xFFFFFFFFFFFFFFFF, 0x995DC9BBDF1939FA, 0x49958C9ABD7D353F),
    ]
}
