# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-bruijn-graph/. The authors are listed in prov/ZCP03V.jsonl.

"""A de Bruijn graph of order K over strings, stored as hash tables of letters."""

from itertools import product
from typing import Dict, Iterable, List, Optional, Sequence


class DeBruijnGraph:
    """Vertices are (K-1)-mers; each distinct K-mer x is an edge x[:-1] -> x[1:].

    Precondition: K >= 2. Edge multiplicities count the copies added.
    Cost: add_kmer O(K) expected, add_read O(|r| K) expected,
    successors and predecessors O(sigma K), spell O(K + w).
    """

    def __init__(self, k: int) -> None:
        if k < 2:
            raise ValueError("need K >= 2")
        self.k = k
        self.out: Dict[str, Dict[str, int]] = {}
        self.inn: Dict[str, Dict[str, int]] = {}

    def add_kmer(self, x: str) -> None:
        k = self.k
        if len(x) != k:
            raise ValueError("a K-mer must have length K")
        # @line L1
        u, v = x[: k - 1], x[1:]
        # @line L2
        for w in (u, v):
            self.out.setdefault(w, {})
            self.inn.setdefault(w, {})
        # @line L3
        self.out[u][x[k - 1]] = self.out[u].get(x[k - 1], 0) + 1
        # @line L4
        self.inn[v][x[0]] = self.inn[v].get(x[0], 0) + 1

    def add_read(self, r: str) -> None:
        k = self.k
        # @line L5
        for i in range(0, len(r) - k + 1):
            self.add_kmer(r[i : i + k])

    def successors(self, u: str) -> List[str]:
        # @line L6
        return [u[1:] + c for c in self.out.get(u, {})]

    def predecessors(self, v: str) -> List[str]:
        # @line L7
        return [a + v[:-1] for a in self.inn.get(v, {})]

    def spell(self, walk: Sequence[str]) -> str:
        """The string spelled by a walk; raises ValueError if it is not a walk."""
        if not walk:
            raise ValueError("a walk has at least one vertex")
        for t in range(1, len(walk)):
            if walk[t] not in self.successors(walk[t - 1]):
                raise ValueError("not a walk")
        # @line L8
        s = [walk[0]]
        # @line L9
        for t in range(1, len(walk)):
            s.append(walk[t][-1])
        # @line L10
        return "".join(s)

    def vertices(self) -> List[str]:
        return list(self.out)

    def edges(self) -> Dict[str, int]:
        """Each distinct K-mer with its multiplicity."""
        return {u + c: m for u, row in self.out.items() for c, m in row.items()}

    def eulerian_walk(self) -> Optional[List[str]]:
        """A walk using each distinct edge once, or None (Hierholzer, iterative)."""
        edges = self.edges()
        if not edges:
            return None
        outdeg = {u: len(row) for u, row in self.out.items()}
        indeg = {v: len(row) for v, row in self.inn.items()}
        starts = [u for u in self.out if outdeg[u] - indeg[u] == 1]
        ends = [u for u in self.out if indeg[u] - outdeg[u] == 1]
        balanced = all(abs(outdeg[u] - indeg[u]) <= 1 for u in self.out)
        if not balanced or len(starts) > 1 or len(ends) > 1 or len(starts) != len(ends):
            return None
        start = starts[0] if starts else next(u for u in self.out if outdeg[u] > 0)
        nxt = {u: sorted(row) for u, row in self.out.items()}
        pos = {u: 0 for u in self.out}
        stack, path = [start], []
        while stack:
            u = stack[-1]
            if pos[u] < len(nxt[u]):
                c = nxt[u][pos[u]]
                pos[u] += 1
                stack.append(u[1:] + c)
            else:
                path.append(stack.pop())
        path.reverse()
        if len(path) != len(edges) + 1:
            return None
        return path

    def check_invariant(self, kmers: Optional[Iterable[str]] = None) -> None:
        k = self.k
        assert set(self.out) == set(self.inn)
        for w in self.out:
            assert len(w) == k - 1
        for u, row in self.out.items():
            for c, m in row.items():
                assert m >= 1
                v = u[1:] + c
                assert v in self.inn and self.inn[v].get(u[0]) == m
        assert sum(sum(r.values()) for r in self.out.values()) == sum(
            sum(r.values()) for r in self.inn.values()
        )
        if kmers is not None:
            count: Dict[str, int] = {}
            for x in kmers:
                count[x] = count.get(x, 0) + 1
            assert self.edges() == count
            ends = {x[:-1] for x in count} | {x[1:] for x in count}
            assert set(self.out) == ends


def complete_graph(alphabet: str, k: int) -> DeBruijnGraph:
    """The complete de Bruijn graph with all K-mers over the alphabet as edges."""
    g = DeBruijnGraph(k)
    for t in product(alphabet, repeat=k):
        g.add_kmer("".join(t))
    return g
