# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-flow-sensitive-pointer-analysis/. The authors are listed in prov/9J9RX5.jsonl.
"""Staged sparse flow-sensitive points-to analysis, after Hardekopf and Lin.

A program is (stmts, succ): stmts[i] is the statement of node i in the four
forms of ptsgen (("addr", p, a), ("copy", p, q), ("load", p, q) for p = *q
and ("store", p, q) for *p = q), and succ[i] lists the successors of node i
in the control flow graph. Node 0 is the entry. A name that matches h<digits>
is a heap location that stands for many objects, so it never gets a strong
update. At the entry every pointer points to nothing.

sparse_fs(stmts, succ) runs three stages:
1. andersen(stmts), the flow-insensitive auxiliary analysis;
2. DEF and USE sets for each node, computed with the auxiliary result, and
   the def-use edges: d -v-> u when d may define v, u may use v, and some
   path of the graph goes from d to u with no node strictly between them
   that may define v;
3. a worklist that recomputes a node only when one of its inputs changed,
   and sends a changed value along the def-use edges of that variable only.

It returns (ins, outs, users): ins[(u, v)] is the points-to set of v just
before node u, for every reachable u and v in USE(u); outs[(d, v)] is the set
of v just after node d, for v in DEF(d); users[(d, v)] lists the nodes u of
the def-use edges d -v-> u.
"""

import re
from collections import deque

HEAP = re.compile(r"h\d+")


def is_heap(a):
    return HEAP.fullmatch(a) is not None


def andersen(stmts):
    """Andersen's analysis by a constraint graph with difference propagation,
    the solver of the Andersen page."""
    names = {}
    for _, x, y in stmts:
        names.setdefault(x, None)
        names.setdefault(y, None)
    pts = {v: set() for v in names}
    succ = {v: set() for v in names}
    delta = {v: set() for v in names}
    loads = {v: set() for v in names}
    stores = {v: set() for v in names}
    work = deque()
    queued = set()

    def push(v):
        if v not in queued:
            queued.add(v)
            work.append(v)

    def propagate(s, v):
        new = s - pts[v]
        if new:
            pts[v] |= new
            delta[v] |= new
            push(v)

    def add_edge(u, v):
        if v not in succ[u]:
            succ[u].add(v)
            propagate(pts[u], v)

    for kind, x, y in stmts:
        if kind == "addr":
            pts[x].add(y)
            delta[x].add(y)
            push(x)
        elif kind == "load":
            loads[y].add(x)
        elif kind == "store":
            stores[x].add(y)
    for kind, x, y in stmts:
        if kind == "copy":
            add_edge(y, x)
    while work:
        n = work.popleft()
        queued.discard(n)
        d = delta[n]
        delta[n] = set()
        for a in d:
            for p in loads[n]:
                add_edge(a, p)
            for q in stores[n]:
                add_edge(q, a)
        for w in list(succ[n]):
            propagate(d, w)
    return pts


def reachable(succ):
    seen = {0}
    stack = [0]
    while stack:
        n = stack.pop()
        for m in succ[n]:
            if m not in seen:
                seen.add(m)
                stack.append(m)
    return sorted(seen)


def def_use(stmt, aux):
    """The locations that the statement may define and may read."""
    kind, x, y = stmt
    if kind == "addr":
        return {x}, set()
    if kind == "copy":
        return {x}, {y}
    if kind == "load":
        return {x}, {y} | aux.get(y, set())
    return set(aux.get(x, ())), {x, y} | aux.get(x, set())


def transfer(stmt, v, get):
    """The new set of v after the statement, for v in DEF; get(w) gives the
    set of w before it."""
    kind, x, y = stmt
    if kind == "addr":
        return frozenset([y])  # @line L12
    if kind == "copy":
        return get(y)
    if kind == "load":
        out = set()
        for b in get(y):
            out |= get(b)
        return frozenset(out)
    targets = get(x)
    if not targets:
        return frozenset()  # @line L13
    if targets == {v} and not is_heap(v):
        return get(y)  # @line L14
    if v in targets:
        return get(v) | get(y)  # @line L15
    return get(v)


def sparse_fs(stmts, succ):
    aux = andersen(stmts)  # @line L1
    nodes = reachable(succ)
    defs, uses = {}, {}
    for n in nodes:
        defs[n], uses[n] = def_use(stmts[n], aux)  # @line L2
    users, sources = {}, {}
    for d in nodes:
        for v in defs[d]:  # @line L3
            found = []
            seen = set()
            stack = list(succ[d])
            while stack:
                u = stack.pop()
                if u in seen:
                    continue
                seen.add(u)
                if v in uses[u]:
                    found.append(u)  # @line L4
                if v not in defs[u]:
                    stack.extend(succ[u])
            users[(d, v)] = sorted(found)
            for u in found:
                sources.setdefault((u, v), []).append(d)
    outs = {(d, v): frozenset() for d in nodes for v in defs[d]}

    def read(n):
        def get(w):
            s = set()
            for d in sources.get((n, w), ()):
                s |= outs[(d, w)]
            return frozenset(s)

        return get

    work = deque(nodes)  # @line L5
    queued = set(nodes)
    while work:  # @line L6
        n = work.popleft()  # @line L7
        queued.discard(n)
        get = read(n)  # @line L8
        for v in sorted(defs[n]):
            new = transfer(stmts[n], v, get)  # @line L9
            if new != outs[(n, v)]:
                outs[(n, v)] = new  # @line L10
                for u in users[(n, v)]:
                    if u not in queued:
                        queued.add(u)
                        work.append(u)
    ins = {(u, w): read(u)(w) for u in nodes for w in uses[u]}
    return ins, outs, users  # @line L11
