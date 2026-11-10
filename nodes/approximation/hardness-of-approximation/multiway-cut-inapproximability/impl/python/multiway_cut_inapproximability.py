# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiway-cut-inapproximability/. The authors are listed in prov/4GNDEM.jsonl.
"""The cost-preserving reduction from vertex cover to node multiway cut.

A graph is (n, edges). The new graph keeps the vertices 0 .. n-1 and adds a terminal n + v joined to v.
For small instances only: the solvers try every vertex set.
"""

from itertools import combinations


def vc_to_node_multiway_cut(n: int, edges: list[tuple[int, int]]) -> tuple[int, list[tuple[int, int]], list[int]]:
    """Return (number of vertices, edges, terminals). Only the vertices 0 .. n-1 may be deleted."""
    return 2 * n, list(edges) + [(v, n + v) for v in range(n)], list(range(n, 2 * n))


def separates(nv: int, edges: list[tuple[int, int]], terminals: list[int], deleted: set[int]) -> bool:
    """True if no path joins two terminals after the deleted vertices are removed."""
    adj = {v: [] for v in range(nv)}
    for u, v in edges:
        if u not in deleted and v not in deleted:
            adj[u].append(v)
            adj[v].append(u)
    tset = set(terminals)
    for t in terminals:
        seen, stack = {t}, [t]
        while stack:
            for y in adj[stack.pop()]:
                if y not in seen:
                    if y in tset:
                        return False
                    seen.add(y)
                    stack.append(y)
    return True


def is_vertex_cover(edges: list[tuple[int, int]], c: set[int]) -> bool:
    return all(u in c or v in c for u, v in edges)


def min_node_multiway_cut(nv: int, edges: list[tuple[int, int]], terminals: list[int]) -> int:
    free = [v for v in range(nv) if v not in set(terminals)]
    for size in range(len(free) + 1):
        for s in combinations(free, size):
            if separates(nv, edges, terminals, set(s)):
                return size
    raise ValueError("two terminals are adjacent")


def vertex_cover_number(n: int, edges: list[tuple[int, int]]) -> int:
    for size in range(n + 1):
        for c in combinations(range(n), size):
            if is_vertex_cover(edges, set(c)):
                return size
    return n
