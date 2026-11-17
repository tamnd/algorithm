# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-mappable-prefix-alignment/. The authors are listed in prov/YWMA4M.jsonl.

"""Spliced alignment of a read to a genome by maximal mappable prefixes, in the style of STAR.

Seed search: from read position i, the maximal mappable prefix (MMP) is the
longest prefix of read[i:] that occurs in the genome. It is found by binary
search in the suffix array, with all its genome positions. Seeds that are long
enough and map to few enough places give candidate diagonals (genome position
minus read position). The search goes on from the base after the MMP.

Stitching: a dynamic program over read positions and the candidate diagonals
finds the best alignment in which each read base sits on one diagonal, the
diagonal can jump forward by an intron length, and both ends can be
soft-clipped. Matches score +1, mismatches -1, and an intron costs 2 if its
motif is GT-AG or CT-AC and 8 otherwise.

What this leaves out, compared with STAR: the search in the reverse direction
and from extra start points, the pre-index of L-mers, the clustering of seeds
into windows around anchors, insertions and deletions, the reverse strand of
the read, read pairs, chimeric alignments, the annotated junctions and the
report of several alignments. The scores are choices of this code, not the
defaults of STAR. Positions are 0-based.
"""

from __future__ import annotations

from typing import Iterable, List, NamedTuple, Optional, Sequence, Tuple

MATCH, MISMATCH = 1, -1
CANONICAL_PENALTY, NONCANONICAL_PENALTY = 2, 8
CANONICAL = {("GT", "AG"), ("CT", "AC")}


class Alignment(NamedTuple):
    score: int
    pos: int
    cigar: str


def suffix_array(g: str) -> List[int]:
    """The start positions of the suffixes of g in lexicographic order (a simple O(n^2 log n) build)."""
    return sorted(range(len(g)), key=lambda i: g[i:])


def _lcp(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def _lower(g: str, sa: Sequence[int], p: str, strict: bool) -> int:
    """First index of sa whose suffix, cut to len(p), is >= p (or > p if strict)."""
    lo, hi = 0, len(sa)
    m = len(p)
    while lo < hi:
        mid = (lo + hi) // 2
        s = g[sa[mid]:sa[mid] + m]
        if s < p or (strict and s == p):
            lo = mid + 1
        else:
            hi = mid
    return lo


def mmp(g: str, sa: Sequence[int], s: str) -> Tuple[int, List[int]]:
    """Return (l, positions): the longest prefix of s that occurs in g, and all its start positions in g."""
    pos = _lower(g, sa, s, False)
    best = 0
    for j in (pos - 1, pos):
        if 0 <= j < len(sa):
            best = max(best, _lcp(s, g[sa[j]:sa[j] + len(s)]))
    if best == 0:
        return 0, []
    p = s[:best]
    return best, sorted(sa[_lower(g, sa, p, False):_lower(g, sa, p, True)])


def junction_penalty(g: str, start: int, end: int) -> int:
    """The cost of the intron g[start:end], by its first two and last two bases."""
    if (g[start:start + 2], g[end - 2:end]) in CANONICAL:
        return CANONICAL_PENALTY
    return NONCANONICAL_PENALTY


def stitch(read: str, g: str, diagonals: Iterable[int], min_intron: int = 20,
           max_intron: int = 1000) -> Optional[Alignment]:
    """The best alignment of a substring of read that puts each base on one of the diagonals.

    Read base x on diagonal d is aligned to g[x + d]. From one base to the next the
    diagonal stays the same, or grows by an intron length in [min_intron, max_intron].
    Bases before the start and after the end are soft-clipped.
    """
    D = sorted(set(diagonals))
    L, n = len(read), len(g)
    F: List[List[Optional[int]]] = [[None] * len(D) for _ in range(L)]
    back: List[List[Optional[int]]] = [[None] * len(D) for _ in range(L)]
    best: Optional[Tuple[int, int, int]] = None
    for x in range(L):
        for a, d in enumerate(D):
            if not 0 <= x + d < n:
                continue
            here, from_ = 0, None
            if x > 0:
                for b, e in enumerate(D):
                    prev = F[x - 1][b]
                    if prev is None:
                        continue
                    if b == a:
                        v = prev
                    elif min_intron <= d - e <= max_intron:
                        v = prev - junction_penalty(g, x + e, x + d)
                    else:
                        continue
                    if v > here:
                        here, from_ = v, b
            F[x][a] = here + (MATCH if read[x] == g[x + d] else MISMATCH)
            back[x][a] = from_
            if best is None or F[x][a] > best[0]:
                best = (F[x][a], x, a)
    if best is None or best[0] <= 0:
        return None
    score, x, a = best
    end = x
    path = []
    while True:
        path.append(D[a])
        b = back[x][a]
        if b is None:
            break
        x, a = x - 1, b
    start = x
    path.reverse()
    ops = [f"{start}S"] if start else []
    run = 1
    for prev, cur in zip(path, path[1:]):
        if cur == prev:
            run += 1
        else:
            ops += [f"{run}M", f"{cur - prev}N"]
            run = 1
    ops.append(f"{run}M")
    if end < L - 1:
        ops.append(f"{L - 1 - end}S")
    return Alignment(score, start + path[0], "".join(ops))


def mmp_align(read: str, g: str, sa: Sequence[int], s_min: int = 8, n_max: int = 10,
              min_intron: int = 20, max_intron: int = 1000, min_frac: float = 0.66,
              trace: Optional[list] = None) -> Optional[Alignment]:
    """Align read to g: seeds by maximal mappable prefixes, then stitching. None if unmapped."""
    L = len(read)
    diagonals = set()  # @line L1
    i = 0
    while i < L:  # @line L2
        l, places = mmp(g, sa, read[i:])  # @line L3
        if trace is not None:
            trace.append((i, l, len(places)))
        if l >= s_min and len(places) <= n_max:  # @line L4
            diagonals.update(p - i for p in places)
        i += l + 1  # @line L5
    aln = stitch(read, g, diagonals, min_intron, max_intron)  # @line L6
    if aln is not None and aln.score >= min_frac * L:  # @line L7
        return aln
    return None  # @line L8
