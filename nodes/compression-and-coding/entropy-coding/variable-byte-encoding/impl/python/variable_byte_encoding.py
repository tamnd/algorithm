# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-byte-encoding/. The authors are listed in prov/JRS6JT.jsonl.

"""Variable-byte codes for integers.

- Unsigned LEB128 (the protobuf varint): 7 data bits per byte, low group first,
  high bit set on every byte except the last.
- Signed LEB128 (DWARF, WebAssembly): two's complement, sign taken from bit 6
  of the last byte.
- ZigZag: maps signed integers to unsigned ones, 0, -1, 1, -2, ... -> 0, 1, 2, 3, ...
- Stream VByte (Lemire, Kurz and Rupp 2018): 32-bit integers in groups of 4,
  with 2-bit length codes in a separate control stream.
"""

from collections.abc import Sequence


def uleb128_encode(x: int, out: bytearray) -> None:
    """Append the unsigned LEB128 code of x >= 0 to out."""
    if x < 0:
        raise ValueError("unsigned LEB128 needs x >= 0")
    while True:  # @line L1
        b = x & 0x7F  # @line L2
        x >>= 7
        if x != 0:  # @line L3
            b |= 0x80
        out.append(b)  # @line L4
        if x == 0:  # @line L5
            return


def uleb128_decode(data: bytes, pos: int = 0, max_bytes: int | None = None) -> tuple[int, int]:
    """Read one unsigned LEB128 value at data[pos]. Return (value, next pos)."""
    x = 0  # @line L6
    shift = 0
    count = 0
    while True:  # @line L7
        if pos >= len(data):
            raise EOFError("truncated LEB128 value")
        b = data[pos]  # @line L8
        pos += 1
        count += 1
        if max_bytes is not None and count > max_bytes:
            raise ValueError("LEB128 value too long")
        x |= (b & 0x7F) << shift  # @line L9
        shift += 7
        if b < 0x80:  # @line L10
            return x, pos  # @line L11


def sleb128_encode(v: int, out: bytearray) -> None:
    """Append the signed LEB128 code of v to out (DWARF 5, Section 7.6)."""
    while True:
        b = v & 0x7F
        v >>= 7  # arithmetic shift: Python ints keep their sign
        done = (v == 0 and b & 0x40 == 0) or (v == -1 and b & 0x40 != 0)
        out.append(b if done else b | 0x80)
        if done:
            return


def sleb128_decode(data: bytes, pos: int = 0) -> tuple[int, int]:
    x = 0
    shift = 0
    while True:
        if pos >= len(data):
            raise EOFError("truncated LEB128 value")
        b = data[pos]
        pos += 1
        x |= (b & 0x7F) << shift
        shift += 7
        if b < 0x80:
            if b & 0x40:
                x -= 1 << shift
            return x, pos


def uleb128_length(x: int) -> int:
    return max(1, -(-x.bit_length() // 7))


def zigzag_encode(v: int) -> int:
    """0, -1, 1, -2, 2, ... -> 0, 1, 2, 3, 4, ... (protobuf sint32 and sint64)."""
    return 2 * v if v >= 0 else -2 * v - 1


def zigzag_decode(z: int) -> int:
    return (z >> 1) ^ -(z & 1)


def encode_all(values: Sequence[int]) -> bytes:
    out = bytearray()
    for v in values:
        uleb128_encode(v, out)
    return bytes(out)


def decode_all(data: bytes) -> list[int]:
    out = []
    pos = 0
    while pos < len(data):
        x, pos = uleb128_decode(data, pos)
        out.append(x)
    return out


# ---------------------------------------------------------------------------
# Stream VByte
# ---------------------------------------------------------------------------


def _byte_length(x: int) -> int:
    if x < 1 << 8:
        return 1
    if x < 1 << 16:
        return 2
    if x < 1 << 24:
        return 3
    return 4


def stream_vbyte_encode(values: Sequence[int]) -> tuple[bytes, bytes]:
    """Return (control stream, data stream) for 32-bit unsigned values.

    Each control byte holds four 2-bit codes, code = byte length - 1, the first
    value of the group in the two low bits. Data bytes are little-endian.
    """
    control = bytearray((len(values) + 3) // 4)
    data = bytearray()
    for i, x in enumerate(values):
        if not 0 <= x < 1 << 32:
            raise ValueError("Stream VByte codes 32-bit unsigned integers")
        n = _byte_length(x)
        control[i >> 2] |= (n - 1) << (2 * (i & 3))
        data += x.to_bytes(n, "little")
    return bytes(control), bytes(data)


def stream_vbyte_decode(count: int, control: bytes, data: bytes) -> list[int]:
    out = []
    pos = 0
    for i in range(count):
        n = ((control[i >> 2] >> (2 * (i & 3))) & 3) + 1
        if pos + n > len(data):
            raise EOFError("truncated Stream VByte data")
        out.append(int.from_bytes(data[pos : pos + n], "little"))
        pos += n
    return out
