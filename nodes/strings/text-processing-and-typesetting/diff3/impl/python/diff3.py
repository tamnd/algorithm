# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diff3/. The authors are listed in prov/8YT0S8.jsonl.
"""The diff3 merge, after the algorithm of Khanna, Kunal and Pierce (FSTTCS 2007, Figure 2).

The inputs are the base o and the two versions a and b. The matchings ma (pairs
(i, j) with o[i] == a[j]) and mb (pairs (i, j) with o[i] == b[j]) are increasing
lists; by default each one is a longest matching from the shared helper. The
parse cuts the three files into stable chunks, where all three agree line by
line, and unstable chunks between them. Indices are 0-based; the paper counts
from 1.
"""

from collections.abc import Hashable, Sequence
from typing import NamedTuple

from txdiff import is_matching, lcs_matching

STABLE = "stable"
CHANGED_A = "changed in A"
CHANGED_B = "changed in B"
FALSE_CONFLICT = "falsely conflicting"
CONFLICT = "truly conflicting"
UNCHANGED = "unchanged"  # an unstable chunk with three equal pieces; only matchings that are not maximum give it


class Chunk(NamedTuple):
    kind: str
    a: list
    o: list
    b: list


def _classify(a: list, o: list, b: list) -> str:
    if a == o == b:
        return UNCHANGED
    if o == b and o != a:
        return CHANGED_A
    if o == a and o != b:
        return CHANGED_B
    if a == b and a != o:
        return FALSE_CONFLICT
    return CONFLICT


def diff3_parse(a: Sequence[Hashable], o: Sequence[Hashable], b: Sequence[Hashable],
                ma: Sequence[tuple[int, int]] | None = None,
                mb: Sequence[tuple[int, int]] | None = None) -> list[Chunk]:
    """Return the chunks of the diff3 parse of (a, o, b) for the matchings ma and mb."""
    ma = list(ma) if ma is not None else lcs_matching(o, a)
    mb = list(mb) if mb is not None else lcs_matching(o, b)
    if not is_matching(o, a, ma) or not is_matching(o, b, mb):
        raise ValueError("ma and mb must be increasing matchings of equal lines")
    in_a, in_b = set(ma), set(mb)
    a_of = dict(ma)  # line of o -> its partner in a
    b_of = dict(mb)
    chunks: list[Chunk] = []

    def emit(kind: str | None, la: int, ha: int, lo: int, ho: int, lb: int, hb: int) -> None:
        pa, po, pb = list(a[la:ha]), list(o[lo:ho]), list(b[lb:hb])
        chunks.append(Chunk(kind or _classify(pa, po, pb), pa, po, pb))

    lo = la = lb = 0  # @line L1
    while True:
        i = 1  # @line L2
        while (lo + i - 1, la + i - 1) in in_a and (lo + i - 1, lb + i - 1) in in_b:
            i += 1
        if i == 1:  # @line L3
            o_next = next((x for x in range(lo, len(o)) if x in a_of and x in b_of), None)
            if o_next is None:
                break
            ja, jb = a_of[o_next], b_of[o_next]
            emit(None, la, ja, lo, o_next, lb, jb)  # @line L4
            lo, la, lb = o_next, ja, jb
        else:
            emit(STABLE, la, la + i - 1, lo, lo + i - 1, lb, lb + i - 1)  # @line L5
            lo, la, lb = lo + i - 1, la + i - 1, lb + i - 1
    if lo < len(o) or la < len(a) or lb < len(b):  # @line L6
        emit(None, la, len(a), lo, len(o), lb, len(b))
    return chunks


def diff3_output(chunks: Sequence[Chunk]) -> tuple[list, list, list]:
    """Return the three new versions (A', O', B') of the paper: a chunk changed on one side is taken on all three."""
    out_a: list = []
    out_o: list = []
    out_b: list = []
    for c in chunks:
        if c.kind == CHANGED_A:
            parts = (c.a, c.a, c.a)
        elif c.kind == CHANGED_B:
            parts = (c.b, c.b, c.b)
        else:
            parts = (c.a, c.o, c.b)
        out_a += parts[0]
        out_o += parts[1]
        out_b += parts[2]
    return out_a, out_o, out_b


def diff3_merge(a: Sequence[Hashable], o: Sequence[Hashable], b: Sequence[Hashable],
                ma: Sequence[tuple[int, int]] | None = None, mb: Sequence[tuple[int, int]] | None = None,
                names: tuple[str, str, str] = ("A", "O", "B")) -> tuple[list, int]:
    """Return the merged lines, with a marked region for each true conflict, and the number of conflicts."""
    merged: list = []
    conflicts = 0
    for c in diff3_parse(a, o, b, ma, mb):  # @line L7
        if c.kind in (STABLE, UNCHANGED, CHANGED_A, FALSE_CONFLICT):
            merged += c.a
        elif c.kind == CHANGED_B:
            merged += c.b
        else:
            conflicts += 1
            merged += [f"<<<<<<< {names[0]}", *c.a, f"||||||| {names[1]}", *c.o, "=======", *c.b,
                       f">>>>>>> {names[2]}"]
    return merged, conflicts  # @line L8
