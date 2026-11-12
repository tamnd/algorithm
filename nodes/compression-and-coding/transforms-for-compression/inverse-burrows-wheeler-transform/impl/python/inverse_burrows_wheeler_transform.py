# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-burrows-wheeler-transform/. The authors are listed in prov/411QAF.jsonl.

"""Inverse Burrows-Wheeler transform with the LF mapping.

L is the BWT of T$, where the sentinel $ is unique and smaller than each
symbol of T. LF(i) = C[L[i]] + (the number of times L[i] occurs in L[0 .. i-1]),
where C[c] is the number of symbols of L that are smaller than c. Row 0 of the
sorted rotations is $T, so L[0] is the last symbol of T, and each LF step moves
one symbol to the left in T. The time is O(n + sigma) with counting, and the
extra space is O(n + sigma).
"""

from collections.abc import Sequence
from typing import TypeVar

S = TypeVar("S")


def lf_mapping(last: Sequence[S]) -> list[int]:
    """LF[i] for each row i, by counting. Symbols must be comparable and hashable."""
    count: dict = {}
    for c in last:  # @line L1
        count[c] = count.get(c, 0) + 1
    smaller: dict = {}
    total = 0
    for c in sorted(count):  # @line L2
        smaller[c] = total
        total += count[c]
    seen = dict.fromkeys(count, 0)  # @line L3
    lf = [0] * len(last)
    for i, c in enumerate(last):  # @line L4
        lf[i] = smaller[c] + seen[c]  # @line L5
        seen[c] += 1  # @line L6
    return lf


def inverse_bwt(last: str, sentinel: str = "$") -> str:
    """Recover T from L = BWT(T$). Time O(n log sigma) here (the sort of the
    distinct symbols); O(n + sigma) with an array of counts over a fixed alphabet.

    Precondition: last holds the sentinel exactly once, and the sentinel is
    smaller than every other symbol of last.
    """
    if last.count(sentinel) != 1:
        raise ValueError("L must hold the sentinel exactly once")
    if min(last) != sentinel:
        raise ValueError("the sentinel must be the smallest symbol")
    lf = lf_mapping(last)
    n = len(last) - 1
    out = [""] * n
    r = 0  # @line L7
    for j in range(n - 1, -1, -1):  # @line L8
        out[j] = last[r]  # @line L9
        r = lf[r]  # @line L10
    return "".join(out)  # @line L11


def inverse_bwt_forward(last: str, sentinel: str = "$") -> str:
    """The same inversion, read from left to right with psi = LF^(-1).

    psi(j) is the row whose rotation starts one position to the right of the
    rotation of row j. Row r with L[r] = $ is the row of T$ itself.
    """
    lf = lf_mapping(last)
    psi = [0] * len(last)
    for i, j in enumerate(lf):
        psi[j] = i
    n = len(last) - 1
    first = sorted(last)
    out = []
    r = last.index(sentinel)  # the row of T$ itself, which starts with T[0]
    for _ in range(n):
        out.append(first[r])
        r = psi[r]
    return "".join(out)


def inverse_bwt_rotations(last: str, index: int) -> str:
    """Invert the 1994 convention: L is the last column of the sorted rotations
    of T (no sentinel) and index is a row equal to T."""
    n = len(last)
    if n == 0:
        return ""
    lf = lf_mapping(last)
    out = [""] * n
    r = index
    for j in range(n - 1, -1, -1):
        out[j] = last[r]
        r = lf[r]
    return "".join(out)


def inverse_bwt_bytes(last: bytes, index: int) -> bytes:
    """Invert the byte form (L without the sentinel, the row of the sentinel).

    The sentinel is put back as -1, which is smaller than each byte.
    """
    codes: list[int] = list(last)
    codes.insert(index, -1)
    lf = lf_mapping(codes)
    n = len(last)
    out = bytearray(n)
    r = 0
    for j in range(n - 1, -1, -1):
        out[j] = codes[r]
        r = lf[r]
    return bytes(out)
