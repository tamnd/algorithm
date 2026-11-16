# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buss-kernel/. The authors are listed in prov/0V3DF3.jsonl.
"""Buss kernel for vertex cover parameterized by the solution size k.

The input is a graph given as a list of edges and an integer k. The output is
an equivalent instance (G', k') with k' <= k, at most k'^2 edges and at most
k'^2 + k' vertices, and the set F of vertices that every small cover must hold.
The function runs in O(n + m) time, where n is the number of vertices that
appear in an edge and m is the number of edges.
"""

from collections.abc import Hashable, Sequence
from dataclasses import dataclass, field

Edge = tuple[Hashable, Hashable]

# The trivial no-instance: one edge and budget 0.
NO_INSTANCE: tuple[tuple[int, int], ...] = ((0, 1),)


@dataclass(frozen=True)
class Kernel:
    """The result of the Buss rules.

    edges and k form the reduced instance. forced holds the vertices that the
    high-degree rule put in the cover; it is empty when the result is the
    trivial no-instance. A cover S of the kernel with |S| <= k gives the cover
    S | forced of the input graph, of size at most the input k.
    """

    edges: list[Edge]
    k: int
    forced: set[Hashable] = field(default_factory=set)

    @property
    def vertices(self) -> set[Hashable]:
        """Return the vertices of the kernel. None of them is isolated."""
        return {x for e in self.edges for x in e}

    @property
    def is_trivial_no(self) -> bool:
        """Return True if the kernel is the trivial no-instance."""
        return self.k == 0 and len(self.edges) > 0


def buss_kernel(edges: Sequence[Edge], k: int) -> Kernel:
    """Apply the Buss rules to (G, k) and return the kernel.

    Self-loops are not allowed. Parallel edges are merged. The graph has no
    isolated vertices because it is given by its edges, so the rule at L5
    acts only on vertices that lose all their edges.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    adj: dict[Hashable, set[Hashable]] = {}
    for u, v in edges:
        if u == v:
            raise ValueError("self-loops are not allowed")
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    # Buckets of vertices by degree. The highest nonempty bucket only moves
    # down, because a degree never grows, so the scan costs O(n) in total.
    top = max((len(s) for s in adj.values()), default=0)
    bucket: list[set[Hashable]] = [set() for _ in range(top + 1)]
    for v, s in adj.items():
        bucket[len(s)].add(v)
    forced: set[Hashable] = set()  # @line L1
    while True:
        while top > 0 and not bucket[top]:
            top -= 1
        if not (k >= 0 and top > k):  # @line L2
            break
        v = bucket[top].pop()  # @line L3
        for u in adj[v]:
            d = len(adj[u])
            bucket[d].discard(u)
            adj[u].discard(v)
            bucket[d - 1].add(u)
        del adj[v]
        forced.add(v)
        k -= 1
    if k < 0:  # @line L4
        return Kernel(list(NO_INSTANCE), 0)
    for v in [v for v, s in adj.items() if not s]:  # @line L5
        del adj[v]
    m = sum(len(s) for s in adj.values()) // 2
    if m > k * k or len(adj) > k * k + k:  # @line L6
        return Kernel(list(NO_INSTANCE), 0)
    kept: list[Edge] = []
    done: set[Hashable] = set()
    for u, s in adj.items():
        done.add(u)
        kept.extend((u, v) for v in s if v not in done)
    return Kernel(kept, k, forced)  # @line L7
