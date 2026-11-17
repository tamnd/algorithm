# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/acyclic-join-evaluation/. The authors are listed in prov/K0Q46K.jsonl.

"""Alpha-acyclicity test and join tree construction by GYO ear removal.

A query is a list of edges; each edge is a collection of attribute names.
An edge e of the remaining set is an *ear* with *witness* f if every attribute
of e that occurs in some other remaining edge also occurs in f. The GYO
reduction (Graham 1979; Yu and Ozsoyoglu 1979) removes ears one at a time and
makes the witness the parent of the ear. The hypergraph is alpha-acyclic if
and only if this ends with one edge, and then the parent pointers form a join
tree: for each attribute, the edges that hold it form a connected subtree.

This direct version takes O(r^2 * w) time per removal for r edges of width at
most w. Tarjan and Yannakakis (1984) give a linear-time test.
"""

from collections import Counter
from collections.abc import Sequence


def gyo_join_tree(edges: Sequence[Sequence[str]]) -> list[int] | None:
    """Return parent pointers of a join tree (-1 at the root), or None if cyclic."""
    sets = [frozenset(e) for e in edges]
    r = len(sets)
    if r == 0:
        return []
    parent = [-1] * r
    alive = set(range(r))
    count = Counter(a for s in sets for a in s)   # number of alive edges per attribute
    while len(alive) > 1:
        found = None
        for e in sorted(alive):
            shared = {a for a in sets[e] if count[a] > 1}
            for f in sorted(alive):
                if f != e and shared <= sets[f]:
                    found = (e, f)
                    break
            if found:
                break
        if found is None:
            return None
        e, f = found
        parent[e] = f
        alive.discard(e)
        for a in sets[e]:
            count[a] -= 1
    return parent


def has_running_intersection(edges: Sequence[Sequence[str]], parent: Sequence[int]) -> bool:
    """Check that parent is a tree and that each attribute's edges are connected in it."""
    r = len(edges)
    if r == 0:
        return True
    if sum(1 for p in parent if p < 0) != 1:
        return False
    adj: list[list[int]] = [[] for _ in range(r)]
    for u, p in enumerate(parent):
        if p >= 0:
            adj[u].append(p)
            adj[p].append(u)
    # Connected with r - 1 edges means a tree.
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    if len(seen) != r:
        return False
    for a in {a for e in edges for a in e}:
        hold = {i for i, e in enumerate(edges) if a in e}
        start = next(iter(hold))
        reach, stack = {start}, [start]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w in hold and w not in reach:
                    reach.add(w)
                    stack.append(w)
        if reach != hold:
            return False
    return True
