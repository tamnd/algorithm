# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tanner-graph/. The authors are listed in prov/68B1G5.jsonl.

"""The Tanner graph of a binary parity-check matrix.

Variable node j stands for code position j; check node i for row i of H;
there is an edge (i, j) exactly when H[i][j] = 1. Vectors are rows of bits.
"""

from collections import deque
from typing import List, Optional, Sequence, Set


class TannerGraph:
    """Adjacency lists in both directions, built from H in Theta(m n) time."""

    def __init__(self, h: Sequence[Sequence[int]]) -> None:
        self.m = len(h)  # @line L1
        self.n = len(h[0]) if h else 0
        self.var_adj: List[List[int]] = [[] for _ in range(self.n)]  # @line L2
        self.chk_adj: List[List[int]] = [[] for _ in range(self.m)]
        for i in range(self.m):  # @line L3
            for j in range(self.n):
                if h[i][j]:  # @line L4
                    self.chk_adj[i].append(j)  # @line L5
                    self.var_adj[j].append(i)  # @line L6

    def edges(self) -> int:
        return sum(len(a) for a in self.chk_adj)

    def check_invariant(self) -> bool:
        """Each edge is in both lists, once."""
        a = {(i, j) for i in range(self.m) for j in self.chk_adj[i]}
        b = {(i, j) for j in range(self.n) for i in self.var_adj[j]}
        return a == b and len(a) == self.edges()

    def syndrome(self, word: Sequence[int]) -> List[int]:
        """H word^T: one parity per check node, Theta(E)."""
        return [sum(word[j] for j in self.chk_adj[i]) & 1 for i in range(self.m)]

    def girth(self) -> Optional[int]:
        """The length of a shortest cycle, or None if the graph is a forest.

        A breadth-first search from every node; a non-tree edge between u and
        w closes a cycle through the root of length at most
        dist(u) + dist(w) + 1, and the shortest cycle is found exactly from
        any of its nodes. Theta(V E) time for V = m + n nodes.
        """
        def adj(x: int) -> List[int]:
            return [self.n + i for i in self.var_adj[x]] if x < self.n else self.chk_adj[x - self.n]

        best: Optional[int] = None
        for root in range(self.n + self.m):
            dist = {root: 0}
            parent = {root: -1}
            q = deque([root])
            while q:
                u = q.popleft()
                if best is not None and 2 * dist[u] >= best:
                    break
                for w in adj(u):
                    if w not in dist:
                        dist[w] = dist[u] + 1
                        parent[w] = u
                        q.append(w)
                    elif parent[u] != w:
                        c = dist[u] + dist[w] + 1
                        if best is None or c < best:
                            best = c
        return best

    def is_stopping_set(self, s: Set[int]) -> bool:
        """S is a stopping set when no check node has exactly one neighbor
        in S (the empty set is one)."""
        for i in {i for j in s for i in self.var_adj[j]}:
            if sum(1 for j in self.chk_adj[i] if j in s) == 1:
                return False
        return True

    def peel(self, erased: Set[int]) -> Set[int]:
        """Erasure decoding by peeling: while a check has exactly one erased
        neighbor, that position is recovered. Returns the positions that stay
        erased, which is the largest stopping set inside erased. Theta(E)."""
        left = set(erased)
        count = [sum(1 for j in self.chk_adj[i] if j in left) for i in range(self.m)]
        q = deque(i for i in range(self.m) if count[i] == 1)
        while q:
            i = q.popleft()
            if count[i] != 1:
                continue
            j = next(x for x in self.chk_adj[i] if x in left)
            left.discard(j)
            for c in self.var_adj[j]:
                count[c] -= 1
                if count[c] == 1:
                    q.append(c)
        return left
