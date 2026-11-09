# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsukiyama-algorithm/. The authors are listed in prov/32F5MK.jsonl.

from collections.abc import Iterable, Iterator


def _adjacency(n: int, edges: Iterable[tuple[int, int]]) -> list[set[int]]:
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge end out of range")
        if u == v:
            raise ValueError("self-loops are not allowed")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def maximal_independent_sets(n: int, edges: Iterable[tuple[int, int]]) -> Iterator[list[int]]:
    """Yield every maximal independent set of the graph, each once, as a sorted list.

    The vertices are 0, ..., n-1, and G_i is the subgraph on 0, ..., i-1.
    A node of the search at level i is a maximal independent set S of G_i.
    Every node has one or two children at level i + 1, so every branch ends
    in an output at level n, and the delay is O(n (n + m)).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    adj = _adjacency(n, edges)

    def is_maximal(t: set[int], i: int) -> bool:
        # Every vertex of G_i outside t has a neighbor in t.
        return all(u in t or adj[u] & t for u in range(i))

    def greedy(x: set[int], i: int) -> set[int]:
        # The first maximal independent set of G_i, in vertex order, that contains x.
        s = set(x)
        for u in range(i):
            if u not in s and not adj[u] & s:
                s.add(u)
        return s

    def search(s: set[int], i: int) -> Iterator[list[int]]:
        if i == n:  # @line L1
            yield sorted(s)
            return
        v = i  # @line L2
        if not adj[v] & s:  # @line L3
            s.add(v)  # @line L4
            yield from search(s, i + 1)
            s.discard(v)
        else:  # @line L5
            yield from search(s, i + 1)  # @line L6
            rest = s - adj[v]  # @line L7
            t = rest | {v}
            if is_maximal(t, i + 1) and greedy(rest, i) == s:  # @line L8
                yield from search(t, i + 1)  # @line L9

    yield from search(set(), 0)


def count_maximal_independent_sets(n: int, edges: Iterable[tuple[int, int]]) -> int:
    """Return the number of maximal independent sets."""
    return sum(1 for _ in maximal_independent_sets(n, edges))
