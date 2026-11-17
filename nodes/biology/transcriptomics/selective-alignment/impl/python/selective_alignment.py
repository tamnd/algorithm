# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-alignment/. The authors are listed in prov/1P4EX1.jsonl.

"""Selective alignment of reads to a transcriptome with decoys, in the style of Salmon.

The targets are transcripts and decoys (for example genome regions that look
like transcripts). For each orientation of the read, the exact k-mer hits on
each target are chained by dynamic programming, the chains far below the best
one are dropped, and every remaining chain is checked by a real alignment of
the read in a window of the target around the chain. An alignment is valid
when its score is at least tau times the best possible score. If the best
valid score on a decoy is strictly greater than the best valid score on a
transcript, the read is discarded; otherwise the valid transcript alignments
are returned.

What this leaves out, compared with Salmon: the pufferfish index and its
uni-MEMs (here a plain k-mer hash), the limits on the number of chaining
predecessors, affine gaps and the ksw2 extension alignment (here a linear gap
semiglobal alignment from bioseq), soft-clipping, the alignment cache, read
pairs and the quantification. Positions are 0-based.
"""

from __future__ import annotations

from typing import Dict, List, NamedTuple, Sequence, Tuple

from bioseq import revcomp, semiglobal_align

MATCH, MISMATCH, GAP = 2, -4, -4


class Hit(NamedTuple):
    target: int
    strand: str
    score: int
    start: int


def build_index(targets: Sequence[str], k: int) -> Dict[str, List[Tuple[int, int]]]:
    """Map each k-mer to the list of (target id, position) where it occurs."""
    index: Dict[str, List[Tuple[int, int]]] = {}
    for t, seq in enumerate(targets):
        for r in range(len(seq) - k + 1):
            index.setdefault(seq[r:r + k], []).append((t, r))
    return index


def chain(anchors: Sequence[Tuple[int, int]], k: int, band: int) -> Tuple[int, List[Tuple[int, int]]]:
    """The best chain of anchors (q, r), each an exact k-mer match of read q to target r.

    An anchor j can follow i if q_i < q_j, r_i < r_j and the diagonals differ by at
    most band. The step gains min(q_j - q_i, r_j - r_i, k) and loses the difference
    of the diagonals. Returns (score, chain); the score of one anchor is k.
    """
    a = sorted(set(anchors), key=lambda x: (x[1], x[0]))
    if not a:
        return 0, []
    f = [k] * len(a)
    back = [-1] * len(a)
    for j, (qj, rj) in enumerate(a):
        for i in range(j):
            qi, ri = a[i]
            gap = abs((rj - qj) - (ri - qi))
            if qi < qj and ri < rj and gap <= band:
                s = f[i] + min(qj - qi, rj - ri, k) - gap
                if s > f[j]:
                    f[j], back[j] = s, i
    j = max(range(len(a)), key=lambda x: (f[x], -x))
    best, out = f[j], []
    while j >= 0:
        out.append(a[j])
        j = back[j]
    return best, out[::-1]


def selective_align(read: str, targets: Sequence[str], is_decoy: Sequence[bool],
                    index: Dict[str, List[Tuple[int, int]]], k: int, band: int = 8,
                    chain_frac: float = 0.65, score_frac: float = 0.65) -> List[Hit]:
    """Return the valid alignments of read to transcripts, or [] if the read is discarded."""
    L = len(read)
    cands = []  # @line L1
    for strand, q in (("+", read), ("-", revcomp(read))):  # @line L2
        hits: Dict[int, List[Tuple[int, int]]] = {}
        for i in range(L - k + 1):
            for t, r in index.get(q[i:i + k], ()):
                hits.setdefault(t, []).append((i, r))
        for t in sorted(hits):  # @line L3
            s, c = chain(hits[t], k, band)
            cands.append((s, t, strand, q, c))  # @line L4
    if not cands:
        return []
    best_chain = max(c[0] for c in cands)  # @line L5
    cands = [c for c in cands if c[0] >= chain_frac * best_chain]  # @line L6
    valid: List[Hit] = []
    for s, t, strand, q, c in cands:
        (q1, r1), (q2, r2) = c[0], c[-1]
        lo = max(0, r1 - q1 - band)
        hi = min(len(targets[t]), r2 + (L - q2) + band)
        score, _, start = semiglobal_align(q, targets[t][lo:hi], MATCH, MISMATCH, GAP, with_start=True)  # @line L7
        if score >= score_frac * MATCH * L:  # @line L8
            valid.append(Hit(t, strand, score, lo + start))
    best_decoy = max((h.score for h in valid if is_decoy[h.target]), default=None)
    best_tx = max((h.score for h in valid if not is_decoy[h.target]), default=None)
    if best_decoy is not None and (best_tx is None or best_decoy > best_tx):  # @line L9
        return []
    return sorted(h for h in valid if not is_decoy[h.target])  # @line L10
