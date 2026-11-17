# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pseudoalignment/. The authors are listed in prov/6KKBA9.jsonl.

"""Pseudoalignment of reads to a transcriptome, in the style of kallisto.

The index holds every k-mer of every transcript and of its reverse
complement, with its color: the set of transcript ids that contain it. The
k-mers are nodes of a de Bruijn graph, with an edge from x to y when x[1:] ==
y[:-1]. A contig is a maximal run of nodes x_0, ..., x_r in which each x_j
has exactly one successor, x_{j+1}, which has exactly one predecessor, x_j,
and the same color. So all k-mers of a contig have one color.

pseudoalign(read) returns the intersection of the colors of the read k-mers
that are in the index. After a hit at position p of a contig c, it jumps to
the last read k-mer that can still lie in c, and if that k-mer is the one at
the expected place in c, it skips all the k-mers in between.

What this leaves out, compared with kallisto: canonical k-mers (here both
strands are stored), the compact storage of colors and contigs, paired-end
reads, fragment length and the EM, which is on the EM isoform quantification
page. Positions are 0-based.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Tuple

from bioseq import kmers, revcomp

Color = FrozenSet[int]


class PseudoIndex:
    """The colored de Bruijn graph of a set of transcripts, cut into contigs."""

    def __init__(self, transcripts: Sequence[str], k: int):
        if k <= 0:
            raise ValueError("k must be positive")
        self.k = k
        colors: Dict[str, set] = {}
        for t, seq in enumerate(transcripts):
            for s in (seq, revcomp(seq)):
                for x in kmers(s, k):
                    colors.setdefault(x, set()).add(t)
        self.color: Dict[str, Color] = {x: frozenset(v) for x, v in colors.items()}
        self.contigs: List[List[str]] = []
        self.contig_color: List[Color] = []
        self.where: Dict[str, Tuple[int, int]] = {}
        self._build_contigs()

    def successors(self, x: str) -> List[str]:
        return [y for y in (x[1:] + b for b in "ACGT") if y in self.color]

    def predecessors(self, x: str) -> List[str]:
        return [y for y in (b + x[:-1] for b in "ACGT") if y in self.color]

    def _next(self, x: str) -> Optional[str]:
        """The node that follows x inside its contig, or None if x ends its contig."""
        out = self.successors(x)
        if len(out) != 1:
            return None
        y = out[0]
        if y == x or len(self.predecessors(y)) != 1 or self.color[y] != self.color[x]:
            return None
        return y

    def _add(self, run: List[str]) -> None:
        cid = len(self.contigs)
        self.contigs.append(run)
        self.contig_color.append(self.color[run[0]])
        for p, x in enumerate(run):
            self.where[x] = (cid, p)

    def _build_contigs(self) -> None:
        nodes = sorted(self.color)
        has_prev = {y for y in (self._next(x) for x in nodes) if y is not None}
        for x in nodes:
            if x in has_prev:
                continue
            run = [x]
            while (y := self._next(run[-1])) is not None:
                run.append(y)
            self._add(run)
        for x in nodes:
            if x in self.where:
                continue
            # x lies on a cycle of contig edges: cut the cycle before x.
            run = [x]
            while (y := self._next(run[-1])) is not None and y != x:
                run.append(y)
            self._add(run)

    def kmer_at(self, cid: int, p: int) -> str:
        return self.contigs[cid][p]


def pseudoalign(index: PseudoIndex, read: str, trace: Optional[list] = None) -> Color:
    """The set of transcripts compatible with read; empty if no read k-mer is in the index.

    If trace is a list, the read positions that were looked up are appended to it.
    """
    k, L = index.k, len(read)
    E: Optional[Color] = None  # @line L1
    i = 0  # @line L2
    while i <= L - k:  # @line L3
        x = read[i:i + k]  # @line L4
        if trace is not None:
            trace.append(i)
        if x in index.where:  # @line L5
            c, p = index.where[x]  # @line L6
            E = index.contig_color[c] if E is None else E & index.contig_color[c]
            d = min(len(index.contigs[c]) - 1 - p, L - k - i)  # @line L7
            if d > 0 and read[i + d:i + d + k] == index.kmer_at(c, p + d):  # @line L8
                i = i + d + 1
            else:
                i = i + 1
        else:
            i = i + 1  # @line L9
    return E if E is not None else frozenset()  # @line L10


def naive_pseudoalign(index: PseudoIndex, read: str) -> Color:
    """The same set computed by looking up every k-mer of the read."""
    E: Optional[Color] = None
    for x in kmers(read, index.k):
        if x in index.color:
            E = index.color[x] if E is None else E & index.color[x]
    return E if E is not None else frozenset()


def equivalence_classes(index: PseudoIndex, reads: Iterable[str]) -> List[Tuple[Tuple[int, ...], int]]:
    """Count the reads by their compatible set. Reads with an empty set are left out."""
    counts: Counter = Counter()
    for r in reads:
        e = pseudoalign(index, r)
        if e:
            counts[tuple(sorted(e))] += 1
    return sorted(counts.items())
