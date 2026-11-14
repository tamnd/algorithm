# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/demand-driven-points-to/. The authors are listed in prov/MGQX2W.jsonl.
"""Demand-driven inclusion-based points-to analysis.

demand_points_to(stmts, queries) takes statements in the four forms of
ptsgen (("addr", p, a), ("copy", p, q), ("load", p, q) for p = *q and
("store", p, q) for *p = q) and a list of query variables. It returns
(answer, demanded): answer maps each query to its set in the least solution
of Andersen's subset constraints, and demanded is the set of variables whose
sets the run had to compute.

The run only builds the part of Andersen's constraint graph that the
queries need. A variable is demanded when a query names it, or when the set
of a demanded variable depends on it: the source of a copy, the pointer of a
load and the targets of that pointer, and, for a demanded variable whose
address is taken, the pointer and the source of every store that may write
to it. This is the magic-sets form of Andersen's rules with the first
argument bound. Each demanded variable keeps delta, the part of its set that
it has not yet sent along its edges or used for loads and stores.
"""

from collections import deque


def demand_points_to(stmts, queries):
    addr_into, copy_into, load_into = {}, {}, {}
    loads_of, stores_of = {}, {}
    stores, taken = [], set()
    for kind, x, y in stmts:
        if kind == "addr":
            addr_into.setdefault(x, []).append(y)
            taken.add(y)
        elif kind == "copy":
            copy_into.setdefault(x, []).append(y)
        elif kind == "load":
            load_into.setdefault(x, []).append(y)
            loads_of.setdefault(y, []).append(x)
        else:
            stores_of.setdefault(x, []).append(y)
            stores.append((x, y))

    pts, delta, succ = {}, {}, {}
    starting = deque()
    work = deque()
    queued = set()

    def demand(v):
        if v not in pts:  # @line L14
            pts[v], delta[v], succ[v] = set(), set(), set()
            starting.append(v)

    def add(s, v):
        new = s - pts[v]  # @line L15
        if new:
            pts[v] |= new
            delta[v] |= new
            if v not in queued:
                queued.add(v)
                work.append(v)

    def edge(u, v):
        demand(u)  # @line L13
        if v not in succ[u]:
            succ[u].add(v)
            add(pts[u], v)

    def start(v):
        add(set(addr_into.get(v, ())), v)  # @line L9
        for y in copy_into.get(v, ()):
            edge(y, v)  # @line L10
        for y in load_into.get(v, ()):
            demand(y)  # @line L11
            for b in list(pts[y]):
                edge(b, v)
        if v in taken:
            for p, q in stores:
                demand(p)  # @line L12
                if v in pts[p]:
                    edge(q, v)

    for q in queries:
        demand(q)  # @line L1
    while starting or work:  # @line L2
        if starting:
            start(starting.popleft())  # @line L3
            continue
        n = work.popleft()  # @line L4
        queued.discard(n)
        d = delta[n]
        delta[n] = set()
        for a in d:
            for x in loads_of.get(n, ()):
                if x in pts:
                    edge(a, x)  # @line L5
            if a in pts:
                for q in stores_of.get(n, ()):
                    edge(q, a)  # @line L6
        for w in list(succ[n]):
            add(d, w)  # @line L7
    return {q: pts[q] for q in queries}, set(pts)  # @line L8
