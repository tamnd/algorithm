# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crc32c/. The authors are listed in prov/7288F4.jsonl.

"""CRC-32C (Castagnoli): the CRC-32/ISCSI entry of the CRC catalogue.

width 32, poly 0x1EDC6F41 (reflected 0x82F63B78), init 0xFFFFFFFF,
refin and refout true, xorout 0xFFFFFFFF, check 0xE3069283,
residue 0xB798B438.
"""

POLY = 0x1EDC6F41
POLY_REFLECTED = 0x82F63B78


def _make_table() -> list[int]:
    table = []
    for v in range(256):  # @line L1
        reg = v
        for _ in range(8):
            reg = (reg >> 1) ^ POLY_REFLECTED if reg & 1 else reg >> 1
        table.append(reg)
    return table


TABLE = _make_table()


def crc32c_update(reg: int, data: bytes) -> int:
    """Advance the reflected register over data, with no init and no xorout.
    This is what one x86 SSE4.2 CRC32 instruction does for 1 to 8 bytes."""
    for v in data:  # @line L3
        reg = (reg >> 8) ^ TABLE[(reg ^ v) & 0xFF]  # @line L4
    return reg


def crc32c(data: bytes, crc: int = 0) -> int:
    """CRC-32C of data. Pass a previous result as crc to continue it."""
    reg = crc ^ 0xFFFFFFFF  # @line L2
    reg = crc32c_update(reg, data)
    return reg ^ 0xFFFFFFFF  # @line L5


def crc32c_bitwise(data: bytes) -> int:
    """The same CRC with one shift per bit, for the tests."""
    reg = 0xFFFFFFFF
    for v in data:
        reg ^= v
        for _ in range(8):
            reg = (reg >> 1) ^ POLY_REFLECTED if reg & 1 else reg >> 1
    return reg ^ 0xFFFFFFFF


def to_wire(crc: int) -> bytes:
    """The four bytes of the digest in the order of RFC 3720, Appendix B.4:
    least significant byte first."""
    return crc.to_bytes(4, "little")


def syndromes(nbits: int, poly: int = POLY) -> list[int]:
    """s_i = x^i mod G(x) for i < nbits, in the normal domain. An error
    pattern is undetected exactly when the XOR of its s_i is 0."""
    g = (1 << 32) | poly
    out, s = [], 1
    for _ in range(nbits):
        out.append(s)
        s <<= 1
        if s >> 32:
            s ^= g
    return out


def has_weight_2_or_4(nbits: int, poly: int = POLY) -> bool:
    """True if some codeword of length nbits has weight 2 or 4.

    Weight 2: two equal syndromes. Weight 4: two different pairs with the
    same XOR of syndromes. When all syndromes differ, two such pairs share no
    index, so they give four distinct positions.
    """
    s = syndromes(nbits, poly)
    if len(set(s)) < nbits:
        return True
    seen = set()
    for a in range(nbits):
        sa = s[a]
        for b in range(a + 1, nbits):
            v = sa ^ s[b]
            if v in seen:
                return True
            seen.add(v)
    return False
