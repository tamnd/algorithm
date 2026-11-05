# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-myers-enumeration/. The authors are listed in prov/NE4VW0.jsonl.

from collections.abc import Iterator


def gabow_myers_enumeration(n: int, edges: list[tuple[int, int]]) -> Iterator[list[int]]:
    """Yield every spanning tree of an undirected graph exactly once.

    The vertices are 0 .. n - 1 and edges[i] = (u, v) is an undirected edge.
    Parallel edges are distinct edges and give distinct trees. Self-loops are
    allowed and lie in no tree. The graph is unweighted, so ties do not
    arise. If the graph is not connected it has no spanning tree and nothing
    is yielded. Each tree is a list of n - 1 edge indices, in the order in
    which the search added them.

    This is the backtracking search of Gabow and Myers: grow a tree T from
    vertex 0 depth-first, and at each level branch on an edge e leaving T
    ("trees with e", then "trees without e") until e is a bridge. The paper
    tests for a bridge in time charged to the output, which gives
    O(n + m + n N) time for N trees. This version tests for a bridge with a
    plain graph search, so each call costs O(n + m) and the total is
    O(n + m + n (n + m) N) time. Space is O(n + m) for the graph plus the
    recursion stack, whose saved copies of F take O(n m) words.
    """
    if n <= 0:
        return
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:
            adj[u].append((v, i))
            adj[v].append((u, i))
    alive = [True] * len(edges)
    in_tree = [False] * n
    tree: list[int] = []

    def connected() -> bool:
        seen = [False] * n
        seen[0] = True
        stack = [0]
        count = 1
        while stack:
            x = stack.pop()
            for y, i in adj[x]:
                if alive[i] and not seen[y]:
                    seen[y] = True
                    count += 1
                    stack.append(y)
        return count == n

    if not connected():
        return

    def outside_end(i: int) -> int:
        u, v = edges[i]
        return v if in_tree[u] else u

    def grow(stack: list[int]) -> Iterator[list[int]]:
        if len(tree) == n - 1:                                   # @line L1
            yield list(tree)
            return
        removed: list[int] = []                                  # @line L2
        while True:                                              # @line L3
            e = stack.pop()                                      # @line L4
            w = outside_end(e)
            saved = list(stack)
            stack[:] = [f for f in stack if outside_end(f) != w]  # @line L5
            tree.append(e)
            in_tree[w] = True
            stack.extend(i for y, i in adj[w] if alive[i] and not in_tree[y])
            yield from grow(stack)                               # @line L6
            tree.pop()                                           # @line L7
            in_tree[w] = False
            stack[:] = saved
            alive[e] = False                                     # @line L8
            removed.append(e)
            bridge = not connected()                             # @line L9
            if bridge:                                           # @line L10
                break
        for e in reversed(removed):                              # @line L11
            alive[e] = True
            stack.append(e)

    in_tree[0] = True
    yield from grow([i for y, i in adj[0] if y != 0])
