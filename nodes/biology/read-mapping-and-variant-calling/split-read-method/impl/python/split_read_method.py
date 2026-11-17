# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-read-method/. The authors are listed in prov/TDWFBV.jsonl.
"""Split-read calls of deletions and short insertions, in the style of Pindel.

The input is a reference string ref, a read r that did not map as a whole
(already turned to the forward strand of ref), and a window [lo, hi) of ref
where the read must lie. In a paired library the window comes from the mapped
mate (the anchor): it starts at the anchor and is about two insert sizes long.

The method grows the read from both ends by pattern growth:

1. the longest prefix r[:a] that occurs in the window, with its set of
   occurrences, grown one base at a time;
2. the longest suffix r[L-b:] that occurs in the window at or after the
   start p of the prefix, grown the same way from the right end.

Each part must occur once. If the prefix starts at p and the suffix ends at
e, the read is ref[p:p+i] + ref[e-(L-i):e] for a deletion of D = e - p - L
bases, and the same holds with D < 0 for an insertion of -D bases. The split
point i can move over a range when the bases next to the breakpoint repeat
(microhomology); the call takes the leftmost i, as in VCF normalization.

What this code leaves out compared with Pindel: mismatches in the two parts,
the search of the reverse strand and of the other mate, large insertions
whose two ends come from two reads, inversions and tandem duplications, the
grouping of reads of one event across samples, and the quality scores.
"""

from __future__ import annotations

from typing import List, Optional, Tuple


def grow_prefix(ref: str, r: str, lo: int, hi: int) -> Tuple[int, List[int]]:
    """The longest a such that r[:a] occurs in ref[lo:hi], and the start positions of r[:a]."""
    occ = [x for x in range(lo, hi) if ref[x] == r[0]] if r else []  # @line L1
    if not occ:
        return 0, []
    a = 1
    while a < len(r):  # @line L2
        nxt = [x for x in occ if x + a < hi and ref[x + a] == r[a]]
        if not nxt:
            break
        occ, a = nxt, a + 1
    return a, occ


def grow_suffix(ref: str, r: str, lo: int, hi: int) -> Tuple[int, List[int]]:
    """The longest b such that r[L-b:] occurs in ref[lo:hi], and the end positions (exclusive)."""
    L = len(r)
    occ = [x + 1 for x in range(lo, hi) if ref[x] == r[-1]] if r else []
    if not occ:
        return 0, []
    b = 1
    while b < L:
        nxt = [e for e in occ if e - b - 1 >= lo and ref[e - b - 1] == r[L - b - 1]]
        if not nxt:
            break
        occ, b = nxt, b + 1
    return b, occ


def split_read(ref: str, r: str, lo: int, hi: int, min_part: int = 10,
               max_ins: int = 20) -> Optional[Tuple[str, int, int, str]]:
    """Return (kind, pos, size, inserted) or None.

    kind is "DEL" or "INS". For a DEL, ref[pos:pos+size] is deleted. For an
    INS, the bases inserted are put before ref[pos]. inserted is the inserted
    sequence ("" for a DEL). None means no unique split with both parts of at
    least min_part bases, or that the read maps as a whole.
    """
    L = len(r)
    hi = min(hi, len(ref))
    a, P = grow_prefix(ref, r, lo, hi)
    if a == L or a < min_part or len(P) != 1:  # @line L3
        return None
    p = P[0]
    b, Q = grow_suffix(ref, r, p, hi)  # @line L4
    if b < min_part or len(Q) != 1:  # @line L5
        return None
    e = Q[0]
    D = e - p - L  # @line L6
    if D == 0 or -D > max_ins:
        return None
    ins = max(-D, 0)
    # The split points i with r[:i] in the prefix and the rest in the suffix.
    first, last = max(L - ins - b, 1), min(a, L - ins - 1)  # @line L7
    if max(first, min_part) > min(last, L - ins - min_part):
        return None
    if D > 0:
        return "DEL", p + first, D, ""  # @line L8
    return "INS", p + first, ins, r[first:first + ins]  # @line L9
