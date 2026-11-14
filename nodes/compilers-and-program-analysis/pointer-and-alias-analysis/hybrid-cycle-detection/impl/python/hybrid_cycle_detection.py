# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-cycle-detection/. The authors are listed in prov/NC36D7.jsonl.
"""Andersen's analysis with lazy and hybrid cycle detection.

hybrid(stmts, lazy=True, offline=True) returns (pts, stats), where pts is
the least solution of the subset constraints, the result of Andersen's
analysis. Nodes whose sets must be equal are merged in a union-find forest.

Offline part (hybrid cycle detection, HCD). Before solving, build a graph
with a node v and a ref node *v for each variable v, and the edges q -> p
for p = q, *q -> p for p = *q, and q -> *p for *p = q. The cycles of copies
are merged at once. For each strongly connected component C with a ref node
*a and a variable node b, record (b, R) for a, where R holds the pointers
of the other ref nodes of C. While solving, once every pointer in R has a
non-empty set, each x in the set of a is merged with b: the offline cycle
then exists in the real graph, with x in place of *a.

Online part (lazy cycle detection, LCD). When an edge n -> w is about to
carry the set of n and the set of w is already equal to it, which is a hint
of a cycle, search once for a path from w back to n and merge its nodes.

stats counts the merges of each kind and the searches.
"""

from collections import deque

import ptsgen


def sccs(nodes, succ):
    """Tarjan's algorithm, without recursion. Returns the strongly
    connected components in reverse topological order."""
    index, low, on_stack = {}, {}, set()
    stack, out = [], []
    counter = 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(succ.get(root, ())))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        while work:
            v, it = work[-1]
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(succ.get(w, ()))))
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    u = work[-1][0]
                    low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = stack.pop()
                        on_stack.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    out.append(comp)
    return out


def offline_plan(stmts):
    """The copy cycles to merge at once, and the table H of HCD."""
    names = ptsgen.variables(stmts)
    copies, graph = {}, {}
    for kind, x, y in stmts:
        if kind == "copy":
            copies.setdefault(y, []).append(x)
            graph.setdefault(("v", y), []).append(("v", x))
        elif kind == "load":
            graph.setdefault(("r", y), []).append(("v", x))
        elif kind == "store":
            graph.setdefault(("v", y), []).append(("r", x))
    groups = [c for c in sccs(names, copies) if len(c) > 1]
    nodes = [("v", v) for v in names] + [("r", v) for v in names]
    table = {}
    for comp in sccs(nodes, graph):  # @line L3
        refs = sorted(x for k, x in comp if k == "r")
        plain = sorted(x for k, x in comp if k == "v")
        if refs and plain:
            for a in refs:
                rest = tuple(c for c in refs if c != a)
                table.setdefault(a, []).append((plain[0], rest))
    return groups, table


def hybrid(stmts, lazy=True, offline=True):
    names = ptsgen.variables(stmts)
    parent = {v: v for v in names}
    pts = {v: set() for v in names}
    succ = {v: set() for v in names}
    loads = {v: set() for v in names}
    stores = {v: set() for v in names}
    table = {v: [] for v in names}
    checked = set()
    stats = {"offline": 0, "hcd": 0, "lcd": 0, "searches": 0}
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

    def merge(nodes, kind):
        roots = sorted({find(x) for x in nodes})
        if len(roots) < 2:
            return
        r = roots[0]
        for x in roots[1:]:
            parent[x] = r
            pts[r] |= pts[x]
            succ[r] |= succ[x]
            loads[r] |= loads[x]
            stores[r] |= stores[x]
            table[r] += table[x]
            stats[kind] += 1
        succ[r] = {find(w) for w in succ[r]} - {r}
        push(r)

    def on_paths(src, dst):
        """The roots on some path from src to dst, or an empty set."""
        stats["searches"] += 1
        seen, stack = {src}, [src]
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
        back, stack = {dst}, [dst]
        while stack:
            x = stack.pop()
            for w in pred[x]:
                if w not in back:
                    back.add(w)
                    stack.append(w)
        return back

    def add_edge(u, v):
        u, v = find(u), find(v)
        if u != v and v not in succ[u]:
            succ[u].add(v)
            if not pts[u] <= pts[v]:
                pts[v] |= pts[u]
                push(v)

    for kind, x, y in stmts:
        if kind == "addr":
            pts[x].add(y)
        elif kind == "copy":
            succ[y].add(x)
        elif kind == "load":
            loads[y].add(x)
        else:
            stores[x].add(y)
    if offline:
        groups, plan = offline_plan(stmts)  # @line L1
        for a, entries in plan.items():
            table[a] += entries  # @line L4
        for group in groups:
            merge(group, "offline")  # @line L2
    for v in names:
        if find(v) == v and pts[v]:
            push(v)  # @line L5
    while work:  # @line L6
        n = work.popleft()
        queued.discard(n)
        if find(n) != n:  # @line L7
            continue
        for b, rest in list(table[n]):
            if all(pts[find(c)] for c in rest):  # @line L8
                for a in list(pts[n]):
                    merge([a, b], "hcd")  # @line L9
        n = find(n)
        for a in list(pts[n]):  # @line L10
            for p in list(loads[n]):
                add_edge(a, p)
            for q in list(stores[n]):
                add_edge(q, a)
        n = find(n)
        for w in list(succ[n]):  # @line L11
            w, n = find(w), find(n)
            if w == n:
                continue
            if lazy and pts[w] == pts[n] and (n, w) not in checked:  # @line L12
                checked.add((n, w))
                cycle = on_paths(w, n)  # @line L13
                if cycle:
                    merge(cycle, "lcd")  # @line L14
                    continue
            if not pts[n] <= pts[w]:  # @line L15
                pts[w] |= pts[n]
                push(w)
    return {v: set(pts[find(v)]) for v in names}, stats  # @line L16


def points_to(text):
    return hybrid(ptsgen.parse(text))[0]
