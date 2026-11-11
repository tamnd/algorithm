# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genomic-data-encoding/. The authors are listed in prov/9E652P.jsonl.

"""Two basic encodings of DNA.

1. Two-bit packing (PACK and UNPACK). Each of A, C, G, T takes 2 bits, with the
   base codes of the UCSC 2bit format (T = 0, C = 1, A = 2, G = 3) and the first
   base in the high bits of a byte. Runs of N go to a list of (start, length)
   blocks, as in the nBlocks of 2bit. Any other IUPAC code (R, Y, S, W, K, M, B,
   D, H, V) goes to a list of (position, letter) exceptions. The packed slot of
   a non-ACGT position holds 0.

2. A reference-based delta of reads (REF-ENCODE and REF-DECODE). Each read is
   given with the reference position it maps to, with substitutions only (no
   insertions or deletions). A read is stored as the position delta from the
   previous read, its length, and its substitutions, each as the offset delta
   from the previous substitution and a 2-bit code that names the read base
   among the four bases of ACGTN that differ from the reference base, in the
   order ACGTN. The integers are written as ULEB128 varints; a substitution is
   one varint holding 4 * offset_delta + code.

The byte layout is a simple one for this page; it is not the 2bit file format
and not CRAM.
"""

from collections.abc import Sequence

CODE = {"T": 0, "C": 1, "A": 2, "G": 3}
LETTER = "TCAG"
IUPAC_OTHER = set("RYSWKMBDHV")
BASES5 = "ACGTN"


# ---------------------------------------------------------------------------
# Two-bit packing with an N mask and IUPAC exceptions.
# ---------------------------------------------------------------------------


def pack(x: str) -> tuple[int, bytes, list[tuple[int, int]], list[tuple[int, str]]]:
    """Return (n, packed bytes, N blocks, exceptions)."""
    n = len(x)
    b = bytearray((n + 3) // 4)  # @line L1
    nblocks: list[tuple[int, int]] = []
    exc: list[tuple[int, str]] = []
    for i, ch in enumerate(x):  # @line L2
        v = CODE.get(ch, 0)  # @line L3
        b[i >> 2] |= v << (6 - 2 * (i & 3))  # @line L4
        if ch == "N":  # @line L5
            if nblocks and nblocks[-1][0] + nblocks[-1][1] == i:
                nblocks[-1] = (nblocks[-1][0], nblocks[-1][1] + 1)
            else:
                nblocks.append((i, 1))
        elif ch not in CODE:  # @line L6
            if ch not in IUPAC_OTHER:
                raise ValueError(f"not an IUPAC nucleotide code: {ch!r}")
            exc.append((i, ch))
    return n, bytes(b), nblocks, exc  # @line L7


def unpack(n: int, b: bytes, nblocks: Sequence[tuple[int, int]], exc: Sequence[tuple[int, str]]) -> str:
    x = [LETTER[(b[i >> 2] >> (6 - 2 * (i & 3))) & 3] for i in range(n)]  # @line L8
    for start, length in nblocks:  # @line L9
        x[start : start + length] = ["N"] * length
    for i, ch in exc:  # @line L10
        x[i] = ch
    return "".join(x)  # @line L11


def packed_size(n: int, nblocks: Sequence[tuple[int, int]], exc: Sequence[tuple[int, str]]) -> int:
    """Bytes for a simple layout: 4-byte n, the packed bases, 4-byte block and
    exception counts, 8 bytes per N block (start and length as 32-bit words),
    and 5 bytes per exception (a 32-bit position and one letter)."""
    return 4 + (n + 3) // 4 + 4 + 8 * len(nblocks) + 4 + 5 * len(exc)


# ---------------------------------------------------------------------------
# ULEB128 varints.
# ---------------------------------------------------------------------------


def put_uleb(out: bytearray, v: int) -> None:
    if v < 0:
        raise ValueError("ULEB128 needs a nonnegative integer")
    while True:
        byte = v & 0x7F
        v >>= 7
        if v:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return


def get_uleb(data: bytes, pos: int) -> tuple[int, int]:
    v = 0
    shift = 0
    while True:
        if pos >= len(data):
            raise EOFError("truncated varint")
        byte = data[pos]
        pos += 1
        v |= (byte & 0x7F) << shift
        shift += 7
        if not byte & 0x80:
            return v, pos


# ---------------------------------------------------------------------------
# Reference-based delta of mapped reads (substitutions only).
# ---------------------------------------------------------------------------


def bs_code(ref_base: str, read_base: str) -> int:
    """The index of read_base among ACGTN with ref_base left out."""
    return [c for c in BASES5 if c != ref_base].index(read_base)


def bs_base(ref_base: str, code: int) -> str:
    return [c for c in BASES5 if c != ref_base][code]


def ref_encode(ref: str, reads: Sequence[tuple[int, str]]) -> bytes:
    """reads: (position, sequence) pairs sorted by position; each sequence fits
    inside the reference at its position. Bases must be in ACGTN."""
    out = bytearray()  # @line L12
    prev = 0
    for p, y in reads:  # @line L13
        if p < prev or p + len(y) > len(ref) or any(c not in BASES5 for c in y + ref[p : p + len(y)]):
            raise ValueError("reads must be sorted, inside the reference, and over ACGTN")
        put_uleb(out, p - prev)  # @line L14
        put_uleb(out, len(y))
        prev = p
        diffs = [(j, c) for j, c in enumerate(y) if c != ref[p + j]]  # @line L15
        put_uleb(out, len(diffs))  # @line L16
        last = 0
        for j, c in diffs:  # @line L17
            put_uleb(out, 4 * (j - last) + bs_code(ref[p + j], c))
            last = j
    return bytes(out)


def ref_decode(ref: str, data: bytes, m: int) -> list[tuple[int, str]]:
    reads: list[tuple[int, str]] = []
    pos = 0
    prev = 0
    for _ in range(m):  # @line L18
        delta, pos = get_uleb(data, pos)
        length, pos = get_uleb(data, pos)
        p = prev + delta
        prev = p
        y = list(ref[p : p + length])  # @line L19
        k, pos = get_uleb(data, pos)
        last = 0
        for _ in range(k):  # @line L20
            z, pos = get_uleb(data, pos)
            j = last + (z >> 2)
            y[j] = bs_base(ref[p + j], z & 3)
            last = j
        reads.append((p, "".join(y)))  # @line L21
    return reads
