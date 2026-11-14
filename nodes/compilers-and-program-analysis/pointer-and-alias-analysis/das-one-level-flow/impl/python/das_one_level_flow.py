# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/das-one-level-flow/. The authors are listed in prov/ADSKYW.jsonl.
"""Das's one-level flow points-to analysis.

das(stmts) takes statements in the four forms of ptsgen and returns a dict
from each variable to the set of variables it may point to.

Each location a has a value node V(a), which stands for the values stored in
a. Value nodes are kept in a union-find forest. A root has a base set of
locations (the addresses stored there directly), at most one deref node
(the value node of the locations that those values point to) and flow edges.
An assignment adds a flow edge from the value node of its right side to the
value node of its left side: this one level is directional, as in
Andersen's analysis. The deref nodes at the two ends of the edge are
unified, as in Steensgaard's analysis, so every level below the top is
shared. At the end, the set of a value node is the union of the base sets of
all nodes that reach it along flow edges.
"""

from collections import deque

import ptsgen


def _build(stmts):
    names = ptsgen.variables(stmts)
    parent, rank, base, deref = [], [], [], []

    def new():
        parent.append(len(parent))
        rank.append(0)
        base.append(set())
        deref.append(None)
        return len(parent) - 1

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def get_deref(u):
        u = find(u)
        if deref[u] is None:
            deref[u] = new()  # @line L9
        return find(deref[u])

    def unify(x, y):
        work = deque([(x, y)])
        while work:  # @line L10
            x, y = work.popleft()
            x, y = find(x), find(y)
            if x == y:
                continue
            if rank[x] < rank[y]:
                x, y = y, x
            parent[y] = x  # @line L11
            if rank[x] == rank[y]:
                rank[x] += 1
            base[x] |= base[y]  # @line L12
            dx, dy = deref[x], deref[y]
            if dx is None:
                deref[x] = dy
            elif dy is not None:
                work.append((dx, dy))  # @line L13

    edges = []

    def flow(u, v):
        edges.append((u, v))  # @line L7
        unify(get_deref(u), get_deref(v))  # @line L8

    V = {a: new() for a in names}  # @line L1
    for kind, x, y in stmts:  # @line L2
        if kind == "addr":
            base[find(V[x])].add(y)  # @line L3
            unify(V[y], get_deref(V[x]))
        elif kind == "copy":
            flow(V[y], V[x])  # @line L4
        elif kind == "load":
            flow(get_deref(V[y]), V[x])  # @line L5
        else:
            flow(V[y], get_deref(V[x]))  # @line L6
    return names, V, find, base, edges


def das(stmts):
    names, V, find, base, edges = _build(stmts)
    succ = {}
    for u, v in edges:
        u, v = find(u), find(v)
        if u != v:
            succ.setdefault(u, set()).add(v)
    # Phase 2: for each location, a search along the flow edges from the
    # nodes whose base set holds it.
    holders = {}
    for r in {find(i) for i in range(len(base))}:
        for a in base[r]:
            holders.setdefault(a, []).append(r)
    sets = {}
    for a, starts in holders.items():  # @line L14
        seen = set(starts)
        stack = list(starts)
        while stack:
            u = stack.pop()
            sets.setdefault(u, set()).add(a)  # @line L15
            for w in succ.get(u, ()):
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return {v: set(sets.get(find(V[v]), ())) for v in names}  # @line L16


def value_classes(stmts):
    """The groups of variables whose value nodes were unified, as sorted
    lists. Variables in one group have equal sets."""
    names, V, find, _, _ = _build(stmts)
    groups = {}
    for v in names:
        groups.setdefault(find(V[v]), []).append(v)
    return sorted(sorted(g) for g in groups.values())


def points_to(text):
    return das(ptsgen.parse(text))
