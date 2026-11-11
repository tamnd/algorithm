# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resource-allocation-graph/. The authors are listed in prov/SGGS8W.jsonl.

"""A resource allocation graph (Holt 1972) with units, claims and reduction.

Processes are 0..n-1 and resource types are 0..m-1. The graph is stored as
two n x m matrices of edge multiplicities: req[p][r] request edges p -> r and
held[p][r] assignment edges r -> p, plus the free units avail[r] and the
claim edges claim[p] (a set of resource types). No state is global.
"""

from typing import Optional


class RAG:
    def __init__(self, n: int, units: list[int]) -> None:
        """A graph with n processes and len(units) resource types. Cost: O(n m)."""
        m = len(units)
        self.n, self.m = n, m
        self.units = list(units)
        self.avail = list(units)  # @line L1
        self.held = [[0] * m for _ in range(n)]
        self.req = [[0] * m for _ in range(n)]
        self.claim: list[set[int]] = [set() for _ in range(n)]

    def request(self, p: int, r: int, k: int = 1) -> None:
        """Add k request edges p -> r. Precondition: held + req + k <= units. Cost: O(1)."""
        if self.held[p][r] + self.req[p][r] + k > self.units[r]:
            raise ValueError("a process cannot ask for more units than exist")
        self.req[p][r] += k  # @line L2

    def grant(self, p: int) -> bool:
        """Turn all request edges of p into assignment edges if every one fits. Cost: O(m)."""
        if any(self.req[p][r] > self.avail[r] for r in range(self.m)):  # @line L3
            return False  # @line L6
        for r in range(self.m):  # @line L4
            self.avail[r] -= self.req[p][r]
            self.held[p][r] += self.req[p][r]
            self.req[p][r] = 0
        return True  # @line L5

    def release(self, p: int, r: int, k: int = 1) -> None:
        """Remove k assignment edges r -> p. Precondition: k <= held[p][r]. Cost: O(1)."""
        if k > self.held[p][r]:
            raise ValueError("a process cannot release units it does not hold")
        self.held[p][r] -= k  # @line L7
        self.avail[r] += k

    def waits_for(self, p: int) -> set[int]:
        """The processes q != p that hold a unit of a type that p requests. Cost: O(n m)."""
        return {q for r in range(self.m) if self.req[p][r] > 0  # @line L8
                for q in range(self.n) if q != p and self.held[q][r] > 0}

    def wait_for_graph(self) -> dict[int, set[int]]:
        """The projection on processes. Cost: O(n^2 m)."""
        return {p: self.waits_for(p) for p in range(self.n)}

    def reduce(self) -> list[int]:
        """Holt's reduction: the processes that no sequence of reductions removes.

        A process is reducible when each of its requests fits in the free
        units; reducing it gives back every unit it holds. Cost: O(m n^2).
        """
        work = list(self.avail)  # @line L9
        left = set(range(self.n))
        while True:
            p = next((p for p in sorted(left)  # @line L10
                      if all(self.req[p][r] <= work[r] for r in range(self.m))), None)
            if p is None:
                return sorted(left)  # @line L12
            for r in range(self.m):  # @line L11
                work[r] += self.held[p][r]
            left.remove(p)

    def add_claim(self, p: int, r: int) -> None:
        """A claim edge: p may later ask for the single unit of r. Cost: O(1)."""
        self.claim[p].add(r)  # @line L13

    def safe_grant(self, p: int, r: int) -> bool:
        """Claim edge avoidance for single unit resources.

        Precondition: every type has one unit, r is in claim[p] and p has
        asked for r. Give r to p only if the graph of request, assignment and
        claim edges then has no cycle. Cost: O(n m).
        """
        if self.avail[r] == 0:
            return False
        self.req[p][r] -= 1  # @line L14
        self.held[p][r] += 1
        self.avail[r] -= 1
        if self._claim_graph_has_cycle():  # @line L15
            self.held[p][r] -= 1
            self.avail[r] += 1
            self.req[p][r] += 1
            return False
        return True  # @line L16

    def _claim_graph_has_cycle(self) -> bool:
        """Iterative depth-first search on the bipartite graph with claim edges."""
        n, m = self.n, self.m

        def succ(v: int) -> list[int]:
            if v < n:  # a process: request and claim edges that are not yet assignments
                return [n + r for r in range(m) if self.req[v][r] > 0 or (r in self.claim[v] and self.held[v][r] == 0)]
            r = v - n  # a resource: assignment edges
            return [q for q in range(n) if self.held[q][r] > 0]

        color = [0] * (n + m)
        for s in range(n + m):
            if color[s]:
                continue
            color[s] = 1
            stack = [(s, iter(succ(s)))]
            while stack:
                v, it = stack[-1]
                w: Optional[int] = next(it, None)
                if w is None:
                    color[v] = 2
                    stack.pop()
                elif color[w] == 1:
                    return True
                elif color[w] == 0:
                    color[w] = 1
                    stack.append((w, iter(succ(w))))
        return False


def has_cycle(g: dict[int, set[int]]) -> bool:
    """Cycle test on a directed graph given as successor sets (iterative DFS). Cost: O(V + E)."""
    color = {v: 0 for v in g}
    for s in g:
        if color[s]:
            continue
        color[s] = 1
        stack = [(s, iter(sorted(g[s])))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                color[v] = 2
                stack.pop()
            elif color.get(w, 0) == 1:
                return True
            elif color.get(w, 0) == 0:
                color[w] = 1
                stack.append((w, iter(sorted(g.get(w, ())))))
    return False
