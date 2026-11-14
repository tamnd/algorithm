# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-cycle-elimination/. The authors are listed in prov/DDXZCS.jsonl.
"""Andersen's analysis with online cycle elimination.

oce(stmts) takes statements in the four forms of ptsgen and returns
(pts, stats). pts is the least solution of the subset constraints, the same
result as Andersen's analysis. Each time an edge u -> v is added to the
constraint graph, a search looks for a path from v back to u. If there is
one, every node on such a path is merged with u and v into one node of a
union-find forest, since they must all have the same set. The graph of the
merged nodes then has no cycle. The locations stay distinct: only the nodes
that hold the sets are merged. stats counts the searches and the merges, and
gives the merged classes and the edges between them at the end.

This version searches the whole graph for each new edge. Fahndrich, Foster,
Su and Aiken search only part of it, so they can miss cycles; see the page.
"""

from collections import deque

import ptsgen


def oce(stmts):
    names = ptsgen.variables(stmts)
    parent = {v: v for v in names}  # @line L1
    pts = {v: set() for v in names}
    succ = {v: set() for v in names}
    loads = {v: set() for v in names}  # loads[x]: the p with p = *x
    stores = {v: set() for v in names}  # stores[x]: the q with *x = q
    stats = {"searches": 0, "merged": 0}
    work = deque()
    queued = set()

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def push(v):
        if v not in queued:
            queued.add(v)
            work.append(v)

    def on_paths(src, dst):
        """The nodes on some path from src to dst, or an empty set."""
        stats["searches"] += 1
        seen = {src}
        stack = [src]
        while stack:
            x = stack.pop()
            for w in succ[x]:
                w = find(w)
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        if dst not in seen:
            return set()
        pred = {x: [] for x in seen}
        for x in seen:
            for w in succ[x]:
                pred[find(w)].append(x)
        back = {dst}
        stack = [dst]
        while stack:
            x = stack.pop()
            for w in pred[x]:
                if w not in back:
                    back.add(w)
                    stack.append(w)
        return back

    def collapse(nodes, r):
        for x in sorted(nodes):  # @line L16
            if x != r:
                parent[x] = r  # @line L17
                pts[r] |= pts[x]
                succ[r] |= succ[x]
                loads[r] |= loads[x]
                stores[r] |= stores[x]
                stats["merged"] += 1
        succ[r] = {find(w) for w in succ[r]} - {r}  # @line L18
        push(r)

    def add_edge(u, v):
        u, v = find(u), find(v)  # @line L11
        if u == v or v in succ[u]:
            return
        succ[u].add(v)  # @line L12
        cycle = on_paths(v, u)  # @line L13
        if cycle:
            collapse(cycle, u)  # @line L14
            return
        if not pts[u] <= pts[v]:  # @line L15
            pts[v] |= pts[u]
            push(v)

    for kind, x, y in stmts:
        if kind == "addr":
            pts[x].add(y)  # @line L2
            push(x)
        elif kind == "load":
            loads[y].add(x)
        elif kind == "store":
            stores[x].add(y)
    for kind, x, y in stmts:
        if kind == "copy":
            add_edge(y, x)  # @line L3
    while work:  # @line L4
        n = work.popleft()
        queued.discard(n)
        if find(n) != n:  # @line L5
            continue
        for a in list(pts[n]):  # @line L6
            for p in list(loads[n]):
                add_edge(a, p)  # @line L7
            for q in list(stores[n]):
                add_edge(q, a)  # @line L8
        n = find(n)
        for w in list(succ[n]):  # @line L9
            w = find(w)
            if w != n and not pts[n] <= pts[w]:
                pts[w] |= pts[n]
                push(w)
    stats["classes"] = {}
    for v in names:
        stats["classes"].setdefault(find(v), []).append(v)
    stats["edges"] = {(find(u), find(w)) for u in names if find(u) == u
                      for w in succ[u] if find(w) != u}
    return {v: set(pts[find(v)]) for v in names}, stats  # @line L10


def points_to(text):
    return oce(ptsgen.parse(text))[0]
