# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-graph/. The authors are listed in prov/6QAKRR.jsonl.

from typing import Dict, List, Sequence, Tuple

_SEP = object()

INPLAY = 1
ELIMINATED = 2


def _prefix_function(t: Sequence[object]) -> List[int]:
    pi = [0] * len(t)
    for q in range(1, len(t)):
        k = pi[q - 1]
        while k > 0 and t[q] != t[k]:
            k = pi[k - 1]
        if t[q] == t[k]:
            k += 1
        pi[q] = k
    return pi


def all_overlaps(u: str, x: str) -> List[int]:
    """All k with 0 < k < min(|u|, |x|) such that the suffix of u of length k is a prefix of x.

    Returned in decreasing order. Cost: O(|u| + |x|) time with the prefix function of x, a separator, then u.
    """
    if not u or not x:
        return []
    t: List[object] = list(x)
    t.append(_SEP)
    t.extend(u)
    pi = _prefix_function(t)
    out: List[int] = []
    k = pi[-1]
    limit = min(len(u), len(x))
    while k > 0:
        if k < limit:
            out.append(k)
        k = pi[k - 1]
    return out


def _occurs(p: str, t: str) -> bool:
    u: List[object] = list(p)
    u.append(_SEP)
    u.extend(t)
    return any(v == len(p) for v in _prefix_function(u))


class StringGraph:
    """Exact single-strand string graph of a list of reads with minimum overlap ell.

    Vertices are the reads left after removing repeated and contained reads. The overlap
    graph keeps one edge (u, x, d) for every proper suffix-prefix match of length at least
    ell, where d >= 1 is the offset of the start of x after the start of u. The string graph
    keeps the edges that are not transitive: there is no w and a with edges (u, w, a) and
    (w, x, d - a). Precondition: ell >= 1. Build cost, worst case: O(m * n) time for the
    containment tests and the overlaps, plus O(E log E + S) time for the reduction, where S is
    the sum of deg(w) over the irreducible edges (v, w) and, for each v with two edges to the
    same read, over all edges out of v.
    """

    def __init__(self, reads: Sequence[str], ell: int) -> None:
        if ell < 1:
            raise ValueError("the minimum overlap must be at least 1")
        self.ell = ell
        # @line L1
        distinct: List[str] = []
        seen = set()
        for r in reads:
            if r and r not in seen:
                seen.add(r)
                distinct.append(r)
        self.reads: List[str] = []
        self.contained: List[str] = []
        for i, r in enumerate(distinct):
            if any(j != i and len(t) > len(r) and _occurs(r, t) for j, t in enumerate(distinct)):
                self.contained.append(r)
            else:
                self.reads.append(r)
        m = len(self.reads)
        # @line L2
        self.overlap_edges: List[List[Tuple[int, int]]] = [[] for _ in range(m)]
        for u in range(m):
            for x in range(m):
                if u == x:
                    continue
                for k in all_overlaps(self.reads[u], self.reads[x]):
                    if k >= ell:
                        self.overlap_edges[u].append((len(self.reads[u]) - k, x))
            self.overlap_edges[u].sort()
        self.edges: List[List[Tuple[int, int]]] = [[] for _ in range(m)]
        mark: Dict[Tuple[int, int], int] = {}
        # @line L3
        for v in range(m):
            out = self.overlap_edges[v]
            if not out:
                continue
            # @line L4
            for a, w in out:
                mark[(w, a)] = INPLAY
            longest = out[-1][0]
            # Skipping eliminated edges is safe only when v has at most one edge to each read.
            skip = len({w for _, w in out}) == len(out)
            # @line L5
            for a, w in out:
                # @line L6
                if skip and mark[(w, a)] != INPLAY:
                    continue
                # @line L7
                for b, x in self.overlap_edges[w]:
                    if a + b > longest:
                        break
                    # @line L8
                    if mark.get((x, a + b)) == INPLAY:
                        mark[(x, a + b)] = ELIMINATED
            # @line L9
            self.edges[v] = [(a, w) for a, w in out if mark[(w, a)] == INPLAY]
            mark.clear()

    def num_vertices(self) -> int:
        return len(self.reads)

    def num_overlap_edges(self) -> int:
        return sum(len(e) for e in self.overlap_edges)

    def num_edges(self) -> int:
        return sum(len(e) for e in self.edges)

    def out_edges(self, v: int) -> List[Tuple[int, int]]:
        """Irreducible edges out of v as (offset, head), by increasing offset."""
        return list(self.edges[v])

    def spell(self, start: int, steps: Sequence[Tuple[int, int]]) -> str:
        """String spelled by a walk: start at read `start`, then follow edges given as (offset, head).

        Each step must be an edge of the overlap graph. The result is the prefix of length d of
        each read before the last one, then the last read.
        """
        parts: List[str] = []
        cur = start
        for d, x in steps:
            if (d, x) not in self.overlap_edges[cur]:
                raise ValueError("not an edge of the overlap graph")
            parts.append(self.reads[cur][:d])
            cur = x
        parts.append(self.reads[cur])
        return "".join(parts)

    def check_invariant(self) -> None:
        """Kept edges are exactly the non-transitive overlap edges, by the definition."""
        m = len(self.reads)
        sets = [set(e) for e in self.overlap_edges]
        for i in range(m):
            for j in range(m):
                if i != j:
                    assert not _occurs(self.reads[i], self.reads[j]), "a contained read is a vertex"
        for u in range(m):
            for d, x in self.overlap_edges[u]:
                transitive = any((d - a, x) in sets[w] for a, w in self.overlap_edges[u] if a < d)
                assert ((d, x) in self.edges[u]) == (not transitive), (u, d, x)
