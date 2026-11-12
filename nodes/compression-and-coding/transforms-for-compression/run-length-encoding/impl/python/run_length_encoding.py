# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/run-length-encoding/. The authors are listed in prov/SEKR0Q.jsonl.

"""Run-length encoding and three byte formats.

rle_encode cuts a sequence into maximal runs of equal symbols and outputs a
(symbol, count) pair for each run. rle_decode writes each symbol count times.
Both take O(n) time.

Byte formats:
  pairs_*     a (count, byte) pair per run, with runs longer than 255 split.
  packbits_*  Apple PackBits (TN1023, TIFF 6.0 Section 9): a header byte n in
              0 .. 127 copies the next n + 1 bytes; n in -127 .. -1 repeats
              the next byte 1 - n times; -128 is a no-op. The encoder packs
              only runs of 3 or more bytes.
  rle1_*      the first run-length step of bzip2: a run of 4 to 255 equal
              bytes becomes 4 copies and a count byte 0 .. 251 of the extra
              copies; shorter runs stay as they are.
"""

from collections.abc import Sequence
from typing import TypeVar

S = TypeVar("S")


def rle_encode(x: Sequence[S]) -> list[tuple[S, int]]:
    """The (symbol, count) pair of each maximal run of x, in order."""
    n = len(x)
    out: list[tuple[S, int]] = []
    i = 0  # @line L1
    while i < n:  # @line L2
        j = i  # @line L3
        while j < n and x[j] == x[i]:  # @line L4
            j += 1
        out.append((x[i], j - i))  # @line L5
        i = j  # @line L6
    return out  # @line L7


def rle_decode(pairs: Sequence[tuple[S, int]]) -> list[S]:
    """Inverse of rle_encode: each symbol, count times."""
    out: list[S] = []
    for symbol, count in pairs:
        if count < 1:
            raise ValueError("a run has at least one symbol")
        out.extend([symbol] * count)
    return out


def pairs_encode(data: bytes) -> bytes:
    """(count, byte) pairs; count is 1 .. 255, so a long run takes several pairs."""
    out = bytearray()
    for b, count in rle_encode(data):
        while count > 0:
            k = min(count, 255)
            out += bytes((k, b))
            count -= k
    return bytes(out)


def pairs_decode(data: bytes) -> bytes:
    if len(data) % 2:
        raise ValueError("odd length")
    out = bytearray()
    for i in range(0, len(data), 2):
        if data[i] == 0:
            raise ValueError("a count of 0 is not valid")
        out += bytes((data[i + 1],)) * data[i]
    return bytes(out)


def packbits_encode(data: bytes) -> bytes:
    """Apple PackBits. Runs of 3 to 128 equal bytes become a repeat packet;
    other bytes go into literal packets of at most 128 bytes."""
    n = len(data)
    out = bytearray()
    lit = bytearray()

    def flush() -> None:
        if lit:
            out.append(len(lit) - 1)
            out.extend(lit)
            lit.clear()

    i = 0
    while i < n:
        j = i
        while j < n and j - i < 128 and data[j] == data[i]:
            j += 1
        run = j - i
        if run >= 3:
            flush()
            out.append(257 - run)  # the byte of the signed value 1 - run
            out.append(data[i])
            i = j
        else:
            lit.append(data[i])
            i += 1
            if len(lit) == 128:
                flush()
    flush()
    return bytes(out)


def packbits_decode(data: bytes) -> bytes:
    out = bytearray()
    i, n = 0, len(data)
    while i < n:
        h = data[i]
        h = h - 256 if h >= 128 else h
        i += 1
        if h >= 0:
            if i + h + 1 > n:
                raise ValueError("literal packet runs past the end")
            out += data[i : i + h + 1]
            i += h + 1
        elif h != -128:
            if i >= n:
                raise ValueError("repeat packet without a byte")
            out += bytes((data[i],)) * (1 - h)
            i += 1
    return bytes(out)


def rle1_encode(data: bytes) -> bytes:
    """The first run-length step of bzip2."""
    out = bytearray()
    for b, count in rle_encode(data):
        while count >= 4:
            k = min(count, 255)
            out += bytes((b, b, b, b, k - 4))
            count -= k
        out += bytes((b,)) * count
    return bytes(out)


def rle1_decode(data: bytes) -> bytes:
    out = bytearray()
    i, n = 0, len(data)
    prev, same = -1, 0
    while i < n:
        b = data[i]
        i += 1
        out.append(b)
        same = same + 1 if b == prev else 1
        prev = b
        if same == 4:
            if i >= n:
                raise ValueError("missing count byte after a run of 4")
            out += bytes((b,)) * data[i]
            i += 1
            prev, same = -1, 0
    return bytes(out)
