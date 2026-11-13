# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pebble-game-rigidity/. The authors are listed in prov/AEGQ05.jsonl.

from typing import Sequence


class PebbleGame:
    """The (2, 3) pebble game of Jacobs and Hendrickson on the vertices 0 .. n-1.

    Each vertex starts with two free pebbles. An accepted edge is an arc of a
    directed graph, covered by one pebble of its tail, so for every vertex
    peb[v] + (out-degree of v) = 2 at all times. The accepted edges are an
    independent set of the generic 2D rigidity matroid: every set of k >= 2
    vertices spans at most 2k - 3 of them.
    """

    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError("n must be at least 1")
        self.n = n
        self.peb = [2] * n  # @line L1
        self.out: list[list[int]] = [[] for _ in range(n)]  # @line L1
        self.accepted = 0

    def find_pebble(self, x: int, y: int) -> bool:
        """Move one free pebble to x from a vertex other than x and y.

        Searches the directed graph from x by depth-first search. On success it
        reverses the arcs of the path, so x gains a pebble, the end of the path
        loses one, and the other vertices keep their counts. Cost O(n), because
        every out-degree is at most 2.
        """
        parent = {x: x}
        stack = [x]
        found = -1
        while stack and found < 0:  # @line L9
            a = stack.pop()
            for b in self.out[a]:
                if b in parent:
                    continue
                parent[b] = a
                if b != y and self.peb[b] > 0:
                    found = b
                    break
                stack.append(b)
        if found < 0:  # @line L10
            return False
        b = found
        while b != x:  # @line L11
            a = parent[b]
            self.out[a].remove(b)
            self.out[b].append(a)
            b = a
        self.peb[found] -= 1  # @line L11
        self.peb[x] += 1  # @line L11
        return True  # @line L12

    def gather(self, u: int, v: int, target: int) -> int:
        """Gather free pebbles on u and v, up to target in total (target <= 4).

        Returns peb[u] + peb[v] at the end. It is less than target only when no
        sequence of moves can put target pebbles on u and v.
        """
        for x, y in ((u, v), (v, u)):  # @line L3
            while self.peb[x] < 2 and self.peb[u] + self.peb[v] < target:  # @line L4
                if not self.find_pebble(x, y):  # @line L4
                    break
        return self.peb[u] + self.peb[v]

    def add_edge(self, u: int, v: int) -> bool:
        """Try to accept the edge uv. Returns True if it is independent.

        Precondition: 0 <= u, v < n and u != v. Cost O(n).
        """
        if u == v or not (0 <= u < self.n and 0 <= v < self.n):
            raise ValueError("an edge needs two different vertices in range")
        if self.gather(u, v, 4) == 4:  # @line L5
            self.peb[u] -= 1  # @line L6
            self.out[u].append(v)  # @line L6
            self.accepted += 1
            return True
        return False  # @line L7

    def component_of(self, u: int, v: int) -> frozenset[int]:
        """The rigid component that contains u and v, for an edge uv already offered.

        Gathers three pebbles on u and v. Then a vertex is in the component
        exactly when it cannot reach a free pebble on a vertex other than u
        and v. Cost O(n).
        """
        self.gather(u, v, 3)  # @line L15
        rev: list[list[int]] = [[] for _ in range(self.n)]
        for a in range(self.n):
            for b in self.out[a]:
                rev[b].append(a)
        seen = [False] * self.n
        stack = [w for w in range(self.n) if w != u and w != v and self.peb[w] > 0]
        for w in stack:
            seen[w] = True
        while stack:  # @line L16
            b = stack.pop()
            for a in rev[b]:
                if not seen[a]:
                    seen[a] = True
                    stack.append(a)
        return frozenset(w for w in range(self.n) if not seen[w])  # @line L17


def pebble_game(n: int, edges: Sequence[tuple[int, int]]) -> list[bool]:
    """Run the (2, 3) pebble game on the edges in the given order.

    Returns one flag per edge: True if the edge is independent of the edges
    accepted before it, False if it is redundant. The accepted edges are the
    greedy basis of the generic 2D rigidity matroid for this order.
    Precondition: n >= 1, and each edge has two different ends in 0 .. n-1.
    Repeated edges are allowed (the second copy is redundant).
    Cost O(n m) time and O(n + m) space for m edges.
    """
    game = PebbleGame(n)
    marks = [game.add_edge(u, v) for u, v in edges]  # @line L2
    return marks  # @line L8


def rigidity_rank(n: int, edges: Sequence[tuple[int, int]]) -> int:
    """Rank of the edge set in the generic 2D rigidity matroid. Cost O(n m)."""
    return sum(pebble_game(n, edges))


def is_generically_rigid(n: int, edges: Sequence[tuple[int, int]]) -> bool:
    """True if the graph is generically rigid in the plane. Cost O(n m)."""
    return n == 1 or rigidity_rank(n, edges) == 2 * n - 3


def is_laman(n: int, edges: Sequence[tuple[int, int]]) -> bool:
    """True if the graph is generically minimally rigid in the plane.

    That is 2n - 3 edges and at most 2k - 3 edges on every k >= 2 vertices.
    A single vertex with no edges counts as minimally rigid. The game stops at
    the first redundant edge, so the cost is O(n^2).
    """
    if n == 1:
        return len(edges) == 0
    if len(edges) != 2 * n - 3:
        return False
    game = PebbleGame(n)
    return all(game.add_edge(u, v) for u, v in edges)


def rigid_components(n: int, edges: Sequence[tuple[int, int]]) -> list[frozenset[int]]:
    """The rigid components of the graph: the maximal vertex sets X with |X| >= 2
    whose induced subgraph is generically rigid in the plane.

    Every edge lies in exactly one component, and two components share at most
    one vertex. Isolated vertices are in no component. The components come in
    the order of their first edge. Cost O(n m).
    """
    game = PebbleGame(n)
    for u, v in edges:  # @line L13
        game.add_edge(u, v)
    comps: list[frozenset[int]] = []  # @line L13
    member: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:  # @line L14
        if member[u] & member[v]:  # @line L14
            continue
        comp = game.component_of(u, v)
        for w in comp:
            member[w].add(len(comps))
        comps.append(comp)  # @line L17
    return comps  # @line L18
