# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-motif-search/. The authors are listed in prov/5WRFD0.jsonl.
"""Greedy motif search (GreedyMotifSearch of Compeau and Pevzner), with or
without pseudocounts.

Positions are 0-based in this code; the page numbers them from 1.
"""

from typing import List, NamedTuple, Sequence, Tuple

from bioseq import DNA, kmers

_INDEX = {a: k for k, a in enumerate(DNA)}


class GreedyResult(NamedTuple):
    """The chosen windows, their 0-based starts and their motif score."""

    motifs: Tuple[str, ...]
    starts: Tuple[int, ...]
    score: int


def motif_score(windows: Sequence[str]) -> int:
    """The number of letters that differ from the consensus: sum over columns of n - max count."""
    n = len(windows)
    return sum(n - max(col.count(a) for a in DNA) for col in zip(*windows))


def count_matrix(windows: Sequence[str], L: int, pseudo: int) -> List[List[int]]:
    """counts[j][a] = the number of windows with letter a in column j, plus pseudo."""
    counts = [[pseudo] * 4 for _ in range(L)]
    for w in windows:
        for j, a in enumerate(w):
            counts[j][_INDEX[a]] += 1
    return counts


def most_probable(seq: str, counts: List[List[int]]) -> int:
    """The 0-based start of the first window of seq with the largest profile probability.

    The profile is counts[j][a] / (row sum). The row sums are equal, so the
    largest probability is the largest product of counts, computed exactly with
    integers. If every product is 0, the first window wins.
    """
    L = len(counts)
    best_q, best_v = 0, -1
    for q, w in enumerate(kmers(seq, L)):
        v = 1
        for j, a in enumerate(w):
            v *= counts[j][_INDEX[a]]
            if v == 0:
                break
        if v > best_v:
            best_q, best_v = q, v
    return best_q


def greedy_motif_search(seqs: Sequence[str], L: int, pseudo: int = 0) -> GreedyResult:
    """Try each window of the first sequence as a seed; extend it one sequence at a time
    with the most probable window under the profile of the windows chosen so far.

    pseudo is the pseudocount added to every count (0 in the first version of
    Compeau and Pevzner, 1 for Laplace's rule). Among seeds with the same score
    the first one wins. Cost: O(W^2 n L) time for W = G - L + 1, O(nL) space.
    """
    if L <= 0:
        raise ValueError("L must be positive")
    if not seqs:
        raise ValueError("need at least one sequence")
    for s in seqs:
        if len(s) < L or set(s) - set(DNA):
            raise ValueError("sequences must be over ACGT with length at least L")
    if pseudo < 0:
        raise ValueError("pseudo must be at least 0")
    n = len(seqs)
    best_starts = tuple([0] * n)  # @line L1
    best_motifs = tuple(s[:L] for s in seqs)
    best_score = motif_score(best_motifs)
    for q in range(len(seqs[0]) - L + 1):  # @line L2
        starts = [q]  # @line L3
        motifs = [seqs[0][q:q + L]]
        counts = count_matrix([], L, pseudo)
        for i in range(1, n):  # @line L4
            for j, a in enumerate(motifs[-1]):  # @line L5
                counts[j][_INDEX[a]] += 1
            p = most_probable(seqs[i], counts)  # @line L6
            starts.append(p)
            motifs.append(seqs[i][p:p + L])
        sc = motif_score(motifs)
        if sc < best_score:  # @line L7
            best_starts, best_motifs, best_score = tuple(starts), tuple(motifs), sc
    return GreedyResult(best_motifs, best_starts, best_score)  # @line L8
