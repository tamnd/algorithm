# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-cover-branching/. The authors are listed in prov/XFZWRM.jsonl.
"""Bounded search tree for vertex cover parameterized by the solution size k.

vertex_cover_branching is the edge branching of the page: take an edge {u, v}
that no chosen vertex covers, and try u, then v. The search tree has depth at
most k and at most 2^(k+1) - 1 nodes, so the time is O(2^k (n + m)).

vertex_cover_degree3 is the variant of the page: branch on a vertex v of
degree at least 3 (take v, or take all its neighbors), and solve a graph of
maximum degree 2 directly. Its search tree has O(1.4656^k) leaves.

Both use an explicit stack, because k can be as large as n.
"""

from collections.abc import Hashable, Sequence

Edge = tuple[Hashable, Hashable]


def _search(edges: Sequence[Edge], k: int) -> tuple[set[Hashable] | None, int]:
    """Run the edge branching and return (cover or None, number of search tree nodes).

    A node is a call of VC-BRANCH. The node keeps the chosen vertices in a
    set; the frames on the stack hold the index of the branching edge and the
    side (0 for u, 1 for v) that the node tried last. Every edge before the
    branching edge is covered, so the child scans the edge list from the next
    index. This makes no difference to the worst case, but it is cheap.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    for u, v in edges:
        if u == v:
            raise ValueError("self-loops are not allowed")
    m = len(edges)
    chosen: set[Hashable] = set()
    frames: list[list[int]] = []  # [edge index, side]
    start = 0
    nodes = 0
    while True:
        nodes += 1  # enter a node with the budget k - len(frames)
        i = start
        while i < m and (edges[i][0] in chosen or edges[i][1] in chosen):
            i += 1
        if i == m:  # @line L1
            return set(chosen), nodes
        if len(frames) < k:  # @line L2
            frames.append([i, 0])  # @line L3
            chosen.add(edges[i][0])  # @line L4
            start = i + 1
            continue
        # Return NONE from this node and go back up to the next open branch.
        while frames:
            j, side = frames[-1]
            chosen.discard(edges[j][side])
            if side == 0:
                frames[-1][1] = 1
                chosen.add(edges[j][1])  # @line L5
                start = j + 1
                break
            frames.pop()  # @line L6
        else:
            return None, nodes


def vertex_cover_branching(edges: Sequence[Edge], k: int) -> set[Hashable] | None:
    """Return a vertex cover of size at most k, or None if there is none."""
    return _search(edges, k)[0]


def search_tree_nodes(edges: Sequence[Edge], k: int) -> int:
    """Return the number of nodes that the edge branching visits."""
    return _search(edges, k)[1]


def _cover_of_max_degree_two(adj: dict[Hashable, set[Hashable]]) -> set[Hashable]:
    """Return a least vertex cover of a graph whose degrees are all at most 2.

    Each component is a path or a cycle. Walk it in order and take every
    second vertex: the odd positions of a path with p vertices (p // 2 of
    them), or the even positions of a cycle with p vertices ((p + 1) // 2).
    """
    cover: set[Hashable] = set()
    seen: set[Hashable] = set()
    # Paths first, from an end, so that a cycle is the only thing left.
    for s in [v for v, nb in adj.items() if len(nb) == 1] + [v for v, nb in adj.items() if len(nb) == 2]:
        if s in seen:
            continue
        order = [s]
        seen.add(s)
        prev, cur = None, s
        while True:
            nxt = [w for w in adj[cur] if w != prev and w not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            order.append(cur)
        first = 1 if len(adj[s]) == 1 else 0
        cover.update(order[first::2])
    return cover


def vertex_cover_degree3(edges: Sequence[Edge], k: int) -> tuple[set[Hashable] | None, int]:
    """Return (a cover of size at most k or None, number of leaves of the search tree).

    A node with budget b picks a vertex v of largest degree d. If d <= 2 the
    node is a leaf and solves the graph directly. Otherwise it tries v with
    budget b - 1, then the d neighbors of v with budget b - d; a branch with a
    negative budget is not entered. A node that enters no branch is a leaf.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    adj: dict[Hashable, set[Hashable]] = {}
    for u, v in edges:
        if u == v:
            raise ValueError("self-loops are not allowed")
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    chosen: list[Hashable] = []
    removed: list[tuple[Hashable, set[Hashable]]] = []  # undo log

    def remove(x: Hashable) -> None:
        nb = adj.pop(x)
        for y in nb:
            adj[y].discard(x)
        removed.append((x, nb))
        chosen.append(x)

    def undo(mark: int) -> None:
        while len(removed) > mark:
            x, nb = removed.pop()
            adj[x] = nb
            for y in nb:
                adj[y].add(x)
            chosen.pop()

    leaves = 0
    # A frame is [budget, phase, v, mark]. Phase 0: not started, 1: in the
    # v branch, 2: in the neighbor branch.
    frames: list[list] = [[k, 0, None, 0]]
    while frames:
        f = frames[-1]
        budget, phase = f[0], f[1]
        if phase == 0:
            v = max(adj, key=lambda x: len(adj[x]), default=None)
            if v is None or len(adj[v]) <= 2:
                leaves += 1
                rest = _cover_of_max_degree_two(adj) if v is not None else set()
                if len(rest) <= budget:
                    return set(chosen) | rest, leaves
                frames.pop()
                continue
            f[2], f[3] = v, len(removed)
        v, mark = f[2], f[3]
        undo(mark)
        if phase == 0 and budget >= 1:
            f[1] = 1
            remove(v)
            frames.append([budget - 1, 0, None, 0])
            continue
        if phase <= 1 and budget >= len(adj[v]):
            f[1] = 2
            for w in list(adj[v]):
                remove(w)
            frames.append([budget - len(removed) + mark, 0, None, 0])
            continue
        if phase == 0:
            leaves += 1  # neither branch fits in the budget
        frames.pop()
    return None, leaves
