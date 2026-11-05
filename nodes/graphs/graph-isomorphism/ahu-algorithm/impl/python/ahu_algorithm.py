# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ahu-algorithm/. The authors are listed in prov/9MMJGB.jsonl.

"""Aho-Hopcroft-Ullman isomorphism test for rooted trees, and its use on free trees.

A tree on the vertices 0 .. n-1 is given as a list of undirected edges. Trees are
unlabeled and uncolored: only the shape counts. Rooted trees must map root to root.
"""

from collections import deque


def _children_and_levels(n: int, edges: list[tuple[int, int]], root: int) -> tuple[list[list[int]], list[list[int]]]:
    """Return the children lists and the vertices of each depth, by BFS from root."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    children: list[list[int]] = [[] for _ in range(n)]
    depth = [-1] * n
    depth[root] = 0
    levels: list[list[int]] = [[root]]
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for w in adj[u]:
            if depth[w] < 0:
                depth[w] = depth[u] + 1
                children[u].append(w)
                if depth[w] == len(levels):
                    levels.append([])
                levels[depth[w]].append(w)
                queue.append(w)
    return children, levels


def ahu_isomorphic(t1: tuple[int, list[tuple[int, int]], int], t2: tuple[int, list[tuple[int, int]], int]) -> bool:
    """Decide whether the rooted trees t1 = (n1, edges1, root1) and t2 are isomorphic.

    Precondition: each edge list forms a tree on its n vertices. Cost O(n log n) here.
    """
    n1, e1, r1 = t1
    n2, e2, r2 = t2
    if n1 != n2:  # @line L1
        return False
    ch1, lv1 = _children_and_levels(n1, e1, r1)  # @line L2
    ch2, lv2 = _children_and_levels(n2, e2, r2)
    if len(lv1) != len(lv2):  # @line L3
        return False
    code1 = [0] * n1
    code2 = [0] * n2
    for i in range(len(lv1) - 1, -1, -1):  # @line L4
        key1 = {v: tuple(sorted(code1[c] for c in ch1[v])) for v in lv1[i]}  # @line L5
        key2 = {v: tuple(sorted(code2[c] for c in ch2[v])) for v in lv2[i]}
        distinct = sorted(set(key1.values()) | set(key2.values()))  # @line L6
        rank = {k: j for j, k in enumerate(distinct)}
        for v in lv1[i]:  # @line L7
            code1[v] = rank[key1[v]]
        for v in lv2[i]:
            code2[v] = rank[key2[v]]
        if sorted(code1[v] for v in lv1[i]) != sorted(code2[v] for v in lv2[i]):  # @line L8
            return False
    return True  # @line L9


def tree_centers(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Return the one or two centers of a free tree by peeling leaves. Cost O(n)."""
    if n == 1:
        return [0]
    deg = [0] * n
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    layer = [v for v in range(n) if deg[v] == 1]
    left = n
    while left > 2:
        left -= len(layer)
        nxt = []
        for u in layer:
            for w in adj[u]:
                deg[w] -= 1
                if deg[w] == 1:
                    nxt.append(w)
        layer = nxt
    return sorted(layer)


def free_trees_isomorphic(t1: tuple[int, list[tuple[int, int]]], t2: tuple[int, list[tuple[int, int]]]) -> bool:
    """Decide whether two free (unrooted) trees are isomorphic, by rooting them at centers."""
    n1, e1 = t1
    n2, e2 = t2
    if n1 != n2:
        return False
    c1 = tree_centers(n1, e1)
    c2 = tree_centers(n2, e2)
    if len(c1) != len(c2):
        return False
    return any(ahu_isomorphic((n1, e1, c1[0]), (n2, e2, r)) for r in c2)
