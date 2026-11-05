# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-subtree-disassembly/. The authors are listed in prov/8J5TGF.jsonl.

from collections import deque


def tarjan_subtree_disassembly(
    adj: list[list[tuple[int, float]]], s: int
) -> tuple[list[float | None] | None, list[int | None] | None, list[int] | None]:
    """Single-source shortest paths with negative-cycle detection by subtree disassembly.

    adj[u] lists the arcs (v, w) out of u, for vertices 0 .. n-1, with any real weights.
    Returns (dist, parent, None) when no negative cycle is reachable from s: dist[v] is the
    distance (None when v is unreachable) and parent is a shortest-path tree. Returns
    (None, None, cycle) when it finds a negative cycle: cycle = [c0, c1, ..., ck] with the
    arcs c0 -> c1 -> ... -> ck -> c0, of negative total weight. Worst-case time O(n m).
    """
    n = len(adj)
    dist: list[float | None] = [None] * n  # @line L1: None stands for infinity
    parent: list[int | None] = [None] * n
    children: list[set[int]] = [set() for _ in range(n)]
    in_tree = [False] * n
    in_queue = [False] * n
    dist[s] = 0
    in_tree[s] = True
    queue: deque[int] = deque([s])
    in_queue[s] = True
    while queue:  # @line L2
        u = queue.popleft()  # @line L3
        if not in_queue[u]:
            continue  # a stale entry of a vertex that was removed from the queue
        in_queue[u] = False
        du = dist[u]
        assert du is not None and in_tree[u]
        for v, w in adj[u]:  # @line L4
            dv = dist[v]
            if dv is not None and du + w >= dv:  # @line L5
                continue
            # collect the proper descendants of v; meeting u means v is an ancestor of u
            removed: list[int] = []
            found = v == u
            if in_tree[v]:
                stack = list(children[v])
                while stack and not found:
                    x = stack.pop()
                    if x == u:
                        found = True
                    removed.append(x)
                    stack.extend(children[x])
            if found:  # @line L6
                cycle = [u]  # @line L7: the tree path from v down to u, then the arc (u, v)
                while cycle[-1] != v:
                    p = parent[cycle[-1]]
                    assert p is not None
                    cycle.append(p)
                cycle.reverse()
                return None, None, cycle
            for x in removed:  # @line L8
                in_tree[x] = False
                in_queue[x] = False
                parent[x] = None
                children[x].clear()
            children[v].clear()
            dist[v] = du + w  # @line L9
            old = parent[v]
            if old is not None:
                children[old].discard(v)
            parent[v] = u
            children[u].add(v)
            in_tree[v] = True
            if not in_queue[v]:  # @line L10
                queue.append(v)
                in_queue[v] = True
    return dist, parent, None  # @line L11
