# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-separation-query/. The authors are listed in prov/W0ZM3T.jsonl.

"""Answer d-separation queries in a DAG in O(|V| + |E|) time.

The DAG has the nodes 0 .. n - 1 and a list of directed edges (u, v), which
mean u -> v. The function reachable is the reachable set algorithm of Koller
and Friedman (Algorithm 3.1): it returns the nodes that an active trail from
the source set reaches, given the evidence set.
"""

UP = 0    # the trail enters the node from one of its children
DOWN = 1  # the trail enters the node from one of its parents


def adjacency(n: int, edges: list[tuple[int, int]]) -> tuple[list[list[int]], list[list[int]]]:
    parents: list[list[int]] = [[] for _ in range(n)]
    children: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        parents[v].append(u)
        children[u].append(v)
    return parents, children


def reachable(n: int, edges: list[tuple[int, int]], xs: set[int], zs: set[int]) -> set[int]:
    """Return the nodes not in zs that an active trail from xs reaches given zs."""
    parents, children = adjacency(n, edges)
    anc = [False] * n  # @line L1
    stack = list(zs)
    while stack:
        y = stack.pop()
        if not anc[y]:
            anc[y] = True
            stack.extend(parents[y])
    in_z = [False] * n
    for z in zs:
        in_z[z] = True
    seen = [[False, False] for _ in range(n)]
    found: set[int] = set()
    states = [(x, UP) for x in xs]  # @line L2
    while states:  # @line L3
        y, d = states.pop()  # @line L4
        if seen[y][d]:  # @line L5
            continue
        seen[y][d] = True  # @line L6
        if not in_z[y]:  # @line L7
            found.add(y)
        if d == UP and not in_z[y]:  # @line L8
            states.extend((p, UP) for p in parents[y])  # @line L9
            states.extend((c, DOWN) for c in children[y])
        elif d == DOWN:  # @line L10
            if not in_z[y]:  # @line L11
                states.extend((c, DOWN) for c in children[y])
            if anc[y]:  # @line L12
                states.extend((p, UP) for p in parents[y])
    return found  # @line L13


def d_separated(n: int, edges: list[tuple[int, int]], xs: set[int], ys: set[int], zs: set[int]) -> bool:
    """Decide whether xs and ys are d-separated given zs (the three sets are disjoint)."""
    if xs & ys or xs & zs or ys & zs:
        raise ValueError("the sets X, Y and Z must be disjoint")
    return not (reachable(n, edges, xs, zs) & ys)
