# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/branch-and-bound-motif-search/. The authors are listed in prov/6XQ8GR.jsonl.
"""Exact motif search by branch and bound, on the tree of start positions and
on the tree of string prefixes (the median string search).

Positions are 0-based in this code; the page numbers them from 1.
"""

from typing import List, NamedTuple, Optional, Sequence, Tuple

from bioseq import DNA, hamming, kmers

_INDEX = {a: k for k, a in enumerate(DNA)}


class MotifResult(NamedTuple):
    """An optimal choice of sites: the 0-based starts, the motif score and the tree nodes visited."""

    starts: Tuple[int, ...]
    score: int
    nodes: int


class MedianResult(NamedTuple):
    """A median string, its total distance and the tree nodes visited."""

    pattern: str
    distance: int
    nodes: int


def _check(seqs: Sequence[str], L: int) -> None:
    if L <= 0:
        raise ValueError("L must be positive")
    if not seqs:
        raise ValueError("need at least one sequence")
    for s in seqs:
        if len(s) < L:
            raise ValueError("every sequence must have length at least L")
        if set(s) - set(DNA):
            raise ValueError("sequences must be over ACGT")


def motif_score(windows: Sequence[str]) -> int:
    """The number of letters that differ from the consensus: sum over columns of n - max count."""
    n = len(windows)
    return sum(n - max(col.count(a) for a in DNA) for col in zip(*windows))


def consensus(windows: Sequence[str]) -> str:
    """A consensus string; among letters with the same count, the first in ACGT order wins."""
    return "".join(max(DNA, key=lambda a: (col.count(a), -_INDEX[a])) for col in zip(*windows))


def total_distance(pattern: str, seqs: Sequence[str]) -> int:
    """D(v): the sum over the sequences of the Hamming distance from v to its closest window."""
    L = len(pattern)
    return sum(min(hamming(pattern, w) for w in kmers(s, L)) for s in seqs)


def bb_motif_search(seqs: Sequence[str], L: int) -> MotifResult:
    """Branch and bound over the tree of start positions.

    A node of depth i fixes the windows of the first i sequences. Its partial
    score, the motif score of those i rows, never drops when rows are added,
    so a node whose partial score is not below the best complete score is cut.
    Returns the lexicographically first optimal tuple of starts.
    Cost: O(L W^n) time in the worst case, W = G - L + 1, and O(n + L) space.
    """
    _check(seqs, L)
    n = len(seqs)
    wins = [kmers(s, L) for s in seqs]
    starts = [0] * n
    best = n * L + 1  # @line L1
    best_starts: Optional[Tuple[int, ...]] = None
    counts = [[0] * 4 for _ in range(L)]  # @line L2
    nodes = 0

    def partial(rows: int) -> int:
        return sum(rows - max(c) for c in counts)

    def search(i: int) -> None:
        # i rows are placed; the pseudocode calls this SEARCH(i + 1).
        nonlocal best, best_starts, nodes
        nodes += 1
        if i == n:  # @line L5
            sc = partial(n)  # @line L6
            if sc < best:  # @line L7
                best, best_starts = sc, tuple(starts)
            return  # @line L8
        for q, w in enumerate(wins[i]):  # @line L9
            starts[i] = q  # @line L10
            for j, a in enumerate(w):
                counts[j][_INDEX[a]] += 1
            if partial(i + 1) < best:  # @line L11
                search(i + 1)
            for j, a in enumerate(w):  # @line L12
                counts[j][_INDEX[a]] -= 1

    search(0)  # @line L3
    assert best_starts is not None
    return MotifResult(best_starts, best, nodes)  # @line L4


def bb_median_string(seqs: Sequence[str], L: int) -> MedianResult:
    """Branch and bound over the tree of prefixes of the candidate string.

    For a prefix u of length k, m[i][q] is the Hamming distance from u to the
    first k letters of window q of sequence i. The sum over i of the smallest
    m[i][q] is a lower bound on D(v) for every extension v of u, and equals D(u)
    at a leaf. Returns the lexicographically first median string (ACGT order).
    Cost: O(4^L n W) time in the worst case and O(n W + L) space.
    """
    _check(seqs, L)
    n = len(seqs)
    best = n * L + 1  # @line L13
    best_pattern: Optional[str] = None
    m: List[List[int]] = [[0] * (len(s) - L + 1) for s in seqs]  # @line L14
    prefix: List[str] = []
    nodes = 0

    def extend(k: int) -> None:
        nonlocal best, best_pattern, nodes
        nodes += 1
        bound = sum(min(row) for row in m)  # @line L17
        if bound >= best:  # @line L18
            return
        if k == L:  # @line L19
            best, best_pattern = bound, "".join(prefix)
            return
        for a in DNA:  # @line L20
            for s, row in zip(seqs, m):  # @line L21
                for q in range(len(row)):
                    if s[q + k] != a:
                        row[q] += 1
            prefix.append(a)
            extend(k + 1)  # @line L22
            prefix.pop()
            for s, row in zip(seqs, m):  # @line L23
                for q in range(len(row)):
                    if s[q + k] != a:
                        row[q] -= 1

    extend(0)  # @line L15
    assert best_pattern is not None
    return MedianResult(best_pattern, best, nodes)  # @line L16
