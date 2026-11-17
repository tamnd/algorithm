# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splice-graph/. The authors are listed in prov/7RCBRT.jsonl.

"""A splice graph built from spliced alignments on one strand of one locus.

An alignment is a list of blocks (start, end), 0-based and half-open, in
increasing order, with a gap of at least one base between consecutive blocks.
Each gap is an intron: it goes from the donor (the end of the block before
it) to the acceptor (the start of the block after it).

The nodes are the maximal intervals of covered bases that hold no donor and
no acceptor inside them: the covered region is cut at every donor and every
acceptor. The nodes are numbered in coordinate order, which is a topological
order, because every edge goes to the right. There is an edge (u, v) when one
block runs from node u into node v, which then starts where u ends, or when
an intron joins the end of u to the start of v.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import Dict, List, Sequence, Set, Tuple

Block = Tuple[int, int]
Alignment = Sequence[Block]


def _check(alignment: Alignment) -> None:
    if not alignment:
        raise ValueError("an alignment needs at least one block")
    for s, e in alignment:
        if s >= e:
            raise ValueError("a block needs start < end")
    for (_, e1), (s2, _) in zip(alignment, alignment[1:]):
        if s2 <= e1:
            raise ValueError("blocks must be in order with an intron between them")


class SpliceGraph:
    def __init__(self, alignments: Sequence[Alignment]):
        blocks: List[Block] = []
        introns: Set[Tuple[int, int]] = set()
        for a in alignments:  # @line L1
            _check(a)
            blocks.extend(a)
            introns.update((a[i][1], a[i + 1][0]) for i in range(len(a) - 1))
        cuts = {d for d, _ in introns} | {s for _, s in introns}  # @line L2
        covered: List[List[int]] = []  # @line L3
        for s, e in sorted(blocks):
            if covered and s <= covered[-1][1]:
                covered[-1][1] = max(covered[-1][1], e)
            else:
                covered.append([s, e])
        self.nodes: List[Block] = []
        for s, e in covered:  # @line L4
            pts = sorted({s, e} | {c for c in cuts if s < c < e})
            self.nodes.extend(zip(pts, pts[1:]))
        self._starts = [s for s, _ in self.nodes]
        self.edges: Set[Tuple[int, int]] = set()
        for s, e in blocks:  # @line L5
            span = self._overlapping(s, e)
            self.edges.update(zip(span, span[1:]))
        by_end: Dict[int, int] = {e: i for i, (_, e) in enumerate(self.nodes)}
        by_start: Dict[int, int] = {s: i for i, (s, _) in enumerate(self.nodes)}
        for d, a in introns:  # @line L6
            self.edges.add((by_end[d], by_start[a]))
        self.introns = sorted(introns)
        self.succ: List[List[int]] = [[] for _ in self.nodes]
        self.pred: List[List[int]] = [[] for _ in self.nodes]
        for u, v in sorted(self.edges):
            self.succ[u].append(v)
            self.pred[v].append(u)
        return  # @line L7

    def _overlapping(self, s: int, e: int) -> List[int]:
        """The ids of the nodes that overlap [s, e), in order."""
        i = bisect_right(self._starts, s) - 1
        if i < 0 or self.nodes[i][1] <= s:
            i += 1
        out = []
        while i < len(self.nodes) and self.nodes[i][0] < e:
            out.append(i)
            i += 1
        return out

    def path_of(self, alignment: Alignment) -> List[int]:
        """The node path of an alignment that was used to build the graph."""
        out: List[int] = []
        for s, e in alignment:
            out.extend(self._overlapping(s, e))
        return out

    def sources(self) -> List[int]:
        return [v for v in range(len(self.nodes)) if not self.pred[v]]

    def sinks(self) -> List[int]:
        return [v for v in range(len(self.nodes)) if not self.succ[v]]

    def count_paths(self) -> int:
        """The number of source-to-sink paths, by dynamic programming in node order."""
        ways = [0] * len(self.nodes)
        for v in range(len(self.nodes)):
            ways[v] = 1 if not self.pred[v] else sum(ways[u] for u in self.pred[v])
        return sum(ways[v] for v in self.sinks())

    def paths(self) -> List[List[int]]:
        """All source-to-sink paths, in lexicographic order of node ids."""
        out: List[List[int]] = []
        for s in self.sources():
            stack = [[s]]
            while stack:
                p = stack.pop()
                if not self.succ[p[-1]]:
                    out.append(p)
                for v in reversed(self.succ[p[-1]]):
                    stack.append(p + [v])
        return sorted(out)

    def spell(self, path: Sequence[int]) -> List[Block]:
        """The exons of a node path: runs of nodes that touch are merged into one block."""
        out: List[List[int]] = []
        for v in path:
            s, e = self.nodes[v]
            if out and out[-1][1] == s:
                out[-1][1] = e
            else:
                out.append([s, e])
        return [(s, e) for s, e in out]
