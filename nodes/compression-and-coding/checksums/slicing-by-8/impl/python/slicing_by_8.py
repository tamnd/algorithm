# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slicing-by-8/. The authors are listed in prov/K8JNYQ.jsonl.

"""Slicing-by-4 and slicing-by-8 (Kounavis and Berry 2005) for reflected
32-bit CRCs, such as CRC-32/ISO-HDLC and CRC-32/ISCSI (CRC-32C).

The register is kept in reversed bit order, as in zlib. Table k gives the
effect of one byte followed by k zero bytes. Each function also counts the
table lookups and the dependent register updates, because Python timings do
not show the effect that matters on a real CPU.
"""


def reflect(value: int, width: int) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def make_tables(poly: int, k: int) -> list[list[int]]:
    """Tables T_0 .. T_{k-1} for the 32-bit generator with normal poly."""
    rpoly = reflect(poly, 32)
    t0 = []
    for v in range(256):  # @line L1
        reg = v
        for _ in range(8):
            reg = (reg >> 1) ^ rpoly if reg & 1 else reg >> 1
        t0.append(reg)
    tables = [t0]
    for j in range(1, k):  # @line L2
        prev = tables[-1]
        tables.append([(prev[i] >> 8) ^ t0[prev[i] & 0xFF] for i in range(256)])  # @line L3
    return tables


class Counter:
    def __init__(self) -> None:
        self.lookups = 0  # table reads
        self.steps = 0  # register updates, each depends on the one before

    def __repr__(self) -> str:
        return f"Counter(lookups={self.lookups}, steps={self.steps})"


def _bytewise(reg: int, data: bytes, t0: list[int], cnt: Counter) -> int:
    for v in data:
        reg = (reg >> 8) ^ t0[(reg ^ v) & 0xFF]
        cnt.lookups += 1
        cnt.steps += 1
    return reg


def crc32_bytewise(data: bytes, poly: int, cnt: Counter | None = None, tables=None) -> int:
    """Sarwate's table-driven CRC, for comparison."""
    cnt = cnt or Counter()
    tables = tables or make_tables(poly, 1)
    return _bytewise(0xFFFFFFFF, data, tables[0], cnt) ^ 0xFFFFFFFF


def crc32_slicing4(data: bytes, poly: int, cnt: Counter | None = None, tables=None) -> int:
    cnt = cnt or Counter()
    t0, t1, t2, t3 = tables or make_tables(poly, 4)
    reg = 0xFFFFFFFF
    n4 = len(data) - len(data) % 4
    for i in range(0, n4, 4):
        c = reg ^ int.from_bytes(data[i:i + 4], "little")
        reg = t3[c & 0xFF] ^ t2[(c >> 8) & 0xFF] ^ t1[(c >> 16) & 0xFF] ^ t0[c >> 24]
        cnt.lookups += 4
        cnt.steps += 1
    return _bytewise(reg, data[n4:], t0, cnt) ^ 0xFFFFFFFF


def crc32_slicing8(data: bytes, poly: int, cnt: Counter | None = None, tables=None) -> int:
    cnt = cnt or Counter()
    t0, t1, t2, t3, t4, t5, t6, t7 = tables or make_tables(poly, 8)
    reg = 0xFFFFFFFF  # @line L4
    n8 = len(data) - len(data) % 8
    for i in range(0, n8, 8):  # @line L5
        c = reg ^ int.from_bytes(data[i:i + 4], "little")  # @line L6
        b = data[i + 4:i + 8]  # @line L7
        reg = (t7[c & 0xFF] ^ t6[(c >> 8) & 0xFF] ^ t5[(c >> 16) & 0xFF] ^ t4[c >> 24]  # @line L8
               ^ t3[b[0]] ^ t2[b[1]] ^ t1[b[2]] ^ t0[b[3]])
        cnt.lookups += 8
        cnt.steps += 1
    reg = _bytewise(reg, data[n8:], t0, cnt)  # @line L9
    return reg ^ 0xFFFFFFFF  # @line L10


CRC32_POLY = 0x04C11DB7  # CRC-32/ISO-HDLC, check 0xCBF43926
CRC32C_POLY = 0x1EDC6F41  # CRC-32/ISCSI, check 0xE3069283
