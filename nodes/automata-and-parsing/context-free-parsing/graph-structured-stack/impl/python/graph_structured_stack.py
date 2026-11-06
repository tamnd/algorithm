# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graph-structured-stack/. The authors are listed in prov/5TVZ6C.jsonl.

"""Graph-structured stack (GSS): many parser stacks stored as one graph.

A node is a stack cell, identified by a pair (state, level): the state of the
parser and the number of input symbols read when the cell was pushed. An edge
v -> x means that v lies directly on x, so every path from a node down to the
root is one stack, read from top to bottom. Two stacks with the same top cell
share one node, and two stacks with the same cell below the top share the part
under it. Each edge carries a label, for example the parse tree of the grammar
symbol that the cell stands for. Edges never go up a level.
"""

from typing import Any, Hashable, Optional

Edge = tuple[int, int]


class GraphStructuredStack:
    """A graph-structured stack with find-or-create nodes, edges and path pops."""

    def __init__(self, root_state: Hashable) -> None:
        self.state: list[Hashable] = []
        self.level: list[int] = []
        self.out: list[dict[int, Any]] = []
        self.index: dict[tuple[Hashable, int], int] = {}
        self.by_level: dict[int, list[int]] = {}
        self.root, _ = self.node(root_state, 0)

    def push(self, s: Hashable, j: int, x: int, label: Any = None) -> tuple[int, bool, bool]:
        """Push a cell (s, j) on every stack whose top is x.

        Return (v, created, new_edge): the node v of the cell, whether v was
        made now, and whether the edge v -> x is new.
        """
        if self.level[x] > j:                                           # @line L1
            raise ValueError("a cell may not lie on a cell of a higher level")
        v, created = self.node(s, j)                                    # @line L2
        new_edge = self.add_edge(v, x, label)                           # @line L3
        return v, created, new_edge                                     # @line L4

    def node(self, s: Hashable, j: int) -> tuple[int, bool]:
        """Return (v, created): the node for state s at level j, made if absent."""
        if (s, j) not in self.index:                                    # @line L5
            v = len(self.state)
            self.state.append(s)
            self.level.append(j)
            self.out.append({})
            self.index[(s, j)] = v
            self.by_level.setdefault(j, []).append(v)
            return v, True
        return self.index[(s, j)], False                                # @line L6

    def add_edge(self, v: int, x: int, label: Any = None) -> bool:
        """Put v directly on x; return False if the edge was already there."""
        if self.level[x] > self.level[v]:
            raise ValueError("an edge may not go up a level")
        if x in self.out[v]:                                            # @line L7
            return False
        self.out[v][x] = label                                          # @line L8
        return True

    def pop(self, u: int, m: int, through: Optional[Edge] = None) -> list[tuple[int, tuple[Any, ...]]]:
        """Return (x, labels) for every path of m edges from u, labels bottom first.

        If `through` is an edge, only the paths that use it are returned. The
        search keeps its own stack and does not recurse.
        """
        result: list[tuple[int, tuple[Any, ...]]] = []                  # @line L9
        floor = self.level[through[0]] if through is not None else 0
        todo: list[tuple[int, int, bool, tuple[Any, ...]]] = [(u, 0, through is None, ())]
        while todo:                                                     # @line L10
            y, d, used, labels = todo.pop()                             # @line L11
            if d == m:                                                  # @line L12
                if used:
                    result.append((y, labels[::-1]))
                continue
            if not used and self.level[y] < floor:                      # @line L13
                continue
            for x, t in self.out[y].items():                            # @line L14
                todo.append((x, d + 1, used or (y, x) == through, labels + (t,)))
        return result                                                   # @line L15

    def tops(self, j: int) -> list[int]:
        """Return the nodes of level j, in the order they were made."""
        return list(self.by_level.get(j, []))

    def stacks(self, u: int, limit: int) -> set[tuple[int, ...]]:
        """Return the stacks (paths from u down to the root, bottom first)
        with at most `limit` cells. Used to read the represented stack set."""
        found: set[tuple[int, ...]] = set()
        todo: list[tuple[int, ...]] = [(u,)]
        while todo:
            path = todo.pop()
            if path[-1] == self.root:
                found.add(path[::-1])
            if len(path) < limit:
                for x in self.out[path[-1]]:
                    todo.append(path + (x,))
        return found

    def check_invariant(self) -> None:
        """Check the index, the levels and the direction of the edges."""
        n = len(self.state)
        assert len(self.level) == n and len(self.out) == n
        assert self.level[self.root] == 0
        assert len(self.index) == n
        for (s, j), v in self.index.items():
            assert self.state[v] == s and self.level[v] == j
        seen = sorted(v for vs in self.by_level.values() for v in vs)
        assert seen == list(range(n))
        for j, vs in self.by_level.items():
            assert all(self.level[v] == j for v in vs)
        for v in range(n):
            for x in self.out[v]:
                assert 0 <= x < n and self.level[x] <= self.level[v]
