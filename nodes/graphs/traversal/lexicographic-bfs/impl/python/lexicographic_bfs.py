# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lexicographic-bfs/. The authors are listed in prov/SYYZ0S.jsonl.


class _Class:
    """One class of the partition: an ordered set of vertices in a doubly linked list."""

    __slots__ = ("items", "prev", "next", "stamp", "split")

    def __init__(self) -> None:
        self.items: dict[int, None] = {}
        self.prev: "_Class | None" = None
        self.next: "_Class | None" = None
        self.stamp = -1
        self.split: "_Class | None" = None


def lexicographic_bfs(adj: list[list[int]]) -> list[int]:
    """Return a lexicographic breadth-first search ordering of a simple undirected graph.

    The graph has the vertices 0 .. n-1 and the adjacency lists adj, with each edge in
    both lists and no loops or parallel edges. The search starts at vertex 0. Ties are
    broken by taking the first vertex of the first class, where the first class starts
    as 0 .. n-1 and a new class keeps the order in which its vertices were moved.
    Partition refinement gives time O(n + m) and extra space O(n).
    """
    n = len(adj)
    if n == 0:
        return []
    head = _Class()  # @line L1
    head.items = dict.fromkeys(range(n))
    cls: list[_Class | None] = [head] * n
    order: list[int] = []
    for i in range(n):  # @line L2
        first = head
        assert first is not None
        v = next(iter(first.items))  # @line L3
        del first.items[v]
        cls[v] = None
        if not first.items:
            head = first.next
            if head is not None:
                head.prev = None
        order.append(v)  # @line L4
        for w in adj[v]:  # @line L5
            d = cls[w]
            if d is None:
                continue
            if d.stamp != i:  # @line L6
                new = _Class()  # @line L7
                new.prev, new.next = d.prev, d
                if d.prev is not None:
                    d.prev.next = new
                else:
                    head = new
                d.prev = new
                d.stamp, d.split = i, new
            new = d.split
            assert new is not None
            del d.items[w]  # @line L8
            new.items[w] = None
            cls[w] = new
            if not d.items:
                if d.prev is not None:
                    d.prev.next = d.next
                if d.next is not None:
                    d.next.prev = d.prev
                if head is d:
                    head = d.next
    return order  # @line L9
