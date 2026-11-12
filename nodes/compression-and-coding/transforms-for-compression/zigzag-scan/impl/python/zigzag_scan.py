# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zigzag-scan/. The authors are listed in prov/4K7DEC.jsonl.

"""The zigzag scan of an n x n block, as in JPEG (ITU-T T.81, Figure A.6),
and the JPEG run-length step for the 63 AC coefficients of an 8 x 8 block:
pairs (run, value) with ZRL = (15, 0) for 16 zeros and EOB = (0, 0).

A position is (row, col): row is the vertical frequency and col the
horizontal one. The scan costs O(n^2) time and space.
"""

from typing import List, Sequence, Tuple

ZRL = (15, 0)
EOB = (0, 0)


def zigzag_order(n: int) -> List[Tuple[int, int]]:
    """The positions of an n x n block in zigzag order (n >= 1).

    Anti-diagonal s = row + col is visited in order s = 0, 1, ..., 2n - 2.
    On an odd diagonal the row grows; on an even diagonal it falls. So the
    first step goes right, to (0, 1), as in JPEG.
    """
    order = []  # @line L1
    for s in range(2 * n - 1):  # @line L2
        lo, hi = max(0, s - n + 1), min(s, n - 1)  # @line L3
        rows = range(lo, hi + 1) if s % 2 == 1 else range(hi, lo - 1, -1)  # @line L4
        for r in rows:  # @line L5
            order.append((r, s - r))  # @line L6
    return order  # @line L7


def scan(block: Sequence[Sequence[int]]) -> List[int]:
    """Read a square block into a list in zigzag order."""
    return [block[r][c] for r, c in zigzag_order(len(block))]


def unscan(seq: Sequence[int], n: int) -> List[List[int]]:
    """Inverse of scan: write a list of n * n values back into a block."""
    block = [[0] * n for _ in range(n)]
    for v, (r, c) in zip(seq, zigzag_order(n)):
        block[r][c] = v
    return block


def ac_run_length(zz: Sequence[int]) -> List[Tuple[int, int]]:
    """JPEG pairs (run of zeros, nonzero value) for zz[1:], with ZRL and EOB.

    A ZRL is written only when a nonzero value follows; a trailing run of
    zeros becomes one EOB. No EOB follows when the last value is nonzero.
    """
    out: List[Tuple[int, int]] = []
    run = 0
    for v in zz[1:]:
        if v == 0:
            run += 1
            continue
        while run > 15:
            out.append(ZRL)
            run -= 16
        out.append((run, v))
        run = 0
    if run > 0:
        out.append(EOB)
    return out


def ac_run_length_decode(pairs: Sequence[Tuple[int, int]], dc: int, length: int = 64) -> List[int]:
    """Inverse of ac_run_length: rebuild the zigzag list with the DC value."""
    zz = [dc]
    for run, v in pairs:
        if (run, v) == EOB:
            break
        if (run, v) == ZRL:
            zz.extend([0] * 16)
            continue
        zz.extend([0] * run)
        zz.append(v)
    if len(zz) > length:
        raise ValueError("too many coefficients")
    zz.extend([0] * (length - len(zz)))
    return zz
