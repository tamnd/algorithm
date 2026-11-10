# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-streaming-matching/. The authors are listed in prov/ZQCPTZ.jsonl.
"""One-pass greedy matching for an insertion-only edge stream.

Keep a matching M and the set of matched vertices. On each edge {u, v}, add
it to M when both u and v are free. The result is a maximal matching of the
graph of the stream, so it has at least half as many edges as a maximum one.
Memory: the edges of M, at most n / 2 of them, and one bit per vertex.
"""

from __future__ import annotations

from typing import Iterable


class GreedyMatching:
    """The state of the one-pass greedy algorithm."""

    def __init__(self) -> None:
        self.matched: set = set()  # @line L1
        self.matching: list[tuple] = []
        self.seen = 0

    def process(self, u, v) -> bool:
        """Read one edge of the stream. Returns True if it joins the matching."""
        if u == v:
            raise ValueError("self-loops are not edges")
        self.seen += 1
        if u not in self.matched and v not in self.matched:  # @line L3
            self.matching.append((u, v))  # @line L4
            self.matched.add(u)
            self.matched.add(v)
            return True
        return False

    def check_invariant(self) -> None:
        """M is a matching and the matched set is exactly its vertices."""
        ends = [x for e in self.matching for x in e]
        assert len(ends) == len(set(ends))
        assert set(ends) == self.matched


def greedy_matching(stream: Iterable[tuple]) -> list[tuple]:
    g = GreedyMatching()
    for u, v in stream:  # @line L2
        g.process(u, v)
    return g.matching  # @line L5


def is_maximal(matching, edges) -> bool:
    """Every edge has at least one end covered by the matching."""
    covered = {x for e in matching for x in e}
    return all(u in covered or v in covered for u, v in edges)


def maximum_matching_size(edges) -> int:
    """Exact maximum matching size by branching on the edge list, for small graphs."""
    edges = list({(min(u, v), max(u, v)) for u, v in edges if u != v})

    def best(i: int, used: frozenset) -> int:
        while i < len(edges) and (edges[i][0] in used or edges[i][1] in used):
            i += 1
        if i == len(edges):
            return 0
        u, v = edges[i]
        take = 1 + best(i + 1, used | {u, v})
        skip = best(i + 1, used)
        return max(take, skip)

    return best(0, frozenset())
