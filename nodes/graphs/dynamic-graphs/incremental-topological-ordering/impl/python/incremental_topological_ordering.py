# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-topological-ordering/. The authors are listed in prov/D5SS95.jsonl.

"""Incremental topological ordering by local reordering (Pearce and Kelly).

The structure keeps a bijection between the vertices and the positions
0, ..., n - 1 such that every edge goes from a smaller to a larger position.
Inserting an edge (u, v) with pos(u) > pos(v) searches forward from v among
the positions up to pos(u) and backward from u among the positions from
pos(v). If the forward search reaches u, the edge closes a cycle and is
rejected. Otherwise the two visited sets swap places within the positions they
already use. Insertions only; deterministic; O(K log K) time per insertion,
where K counts the visited vertices and their edges.
"""


class IncrementalTopologicalOrder:
    def __init__(self, n: int) -> None:
        self.n = n
        self.out: list[list[int]] = [[] for _ in range(n)]
        self.inn: list[list[int]] = [[] for _ in range(n)]
        self.pos = list(range(n))  # position of each vertex
        self.at = list(range(n))   # vertex at each position

    def add_edge(self, u: int, v: int) -> bool:
        """Insert (u, v); return False, and leave the graph as it was, on a cycle."""
        if u == v:
            return False
        lo, hi = self.pos[v], self.pos[u]
        if hi < lo:  # @line L1
            self.out[u].append(v)
            self.inn[v].append(u)
            return True
        # Forward search from v, inside the window of positions up to pos(u).
        fwd = {v}
        stack = [v]
        while stack:  # @line L2
            x = stack.pop()
            for y in self.out[x]:
                if y == u:
                    return False  # @line L3
                if y not in fwd and self.pos[y] < hi:
                    fwd.add(y)
                    stack.append(y)
        # Backward search from u, inside the window of positions from pos(v).
        bwd = {u}
        stack = [u]
        while stack:  # @line L4
            x = stack.pop()
            for y in self.inn[x]:
                if y not in bwd and self.pos[y] > lo:
                    bwd.add(y)
                    stack.append(y)
        # Reorder: the backward set first, then the forward set, in the old slots.
        b = sorted(bwd, key=self.pos.__getitem__)  # @line L5
        f = sorted(fwd, key=self.pos.__getitem__)
        slots = sorted(self.pos[x] for x in b + f)
        for x, p in zip(b + f, slots):  # @line L6
            self.pos[x] = p
            self.at[p] = x
        self.out[u].append(v)
        self.inn[v].append(u)
        return True

    def order(self) -> list[int]:
        return list(self.at)  # @line L7
