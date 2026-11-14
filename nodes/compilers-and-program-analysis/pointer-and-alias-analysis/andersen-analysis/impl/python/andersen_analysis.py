# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/andersen-analysis/. The authors are listed in prov/MBB0JP.jsonl.
"""Andersen's inclusion-based points-to analysis.

andersen(stmts) takes statements in the four forms of ptsgen
(("addr", p, a), ("copy", p, q), ("load", p, q) for p = *q and
("store", p, q) for *p = q) and returns the least solution of the subset
constraints, as a dict from each variable to the set of variables it may
point to. It keeps a constraint graph with an edge u -> v for each
inclusion pts(u) <= pts(v), and a worklist of nodes whose sets have grown.
Each node also keeps delta, the part of its set that it has not yet sent
along its edges or used for its loads and stores (difference propagation).

may_alias(pts, p, q) tells if *p and *q may be the same location.
"""

from collections import deque

import ptsgen


def andersen(stmts):
    names = ptsgen.variables(stmts)
    pts = {v: set() for v in names}  # @line L1
    succ = {v: set() for v in names}
    delta = {v: set() for v in names}
    loads = {v: set() for v in names}  # loads[q]: the p with p = *q
    stores = {v: set() for v in names}  # stores[p]: the q with *p = q
    work = deque()  # @line L2
    queued = set()

    def push(v):
        if v not in queued:
            queued.add(v)
            work.append(v)

    def propagate(s, v):
        new = s - pts[v]  # @line L14
        if new:  # @line L15
            pts[v] |= new  # @line L16
            delta[v] |= new
            push(v)

    def add_edge(u, v):
        if v not in succ[u]:  # @line L12
            succ[u].add(v)  # @line L13
            propagate(pts[u], v)

    for kind, x, y in stmts:
        if kind == "addr":
            pts[x].add(y)  # @line L3
            delta[x].add(y)
            push(x)
        elif kind == "load":
            loads[y].add(x)
        elif kind == "store":
            stores[x].add(y)
    for kind, x, y in stmts:
        if kind == "copy":
            add_edge(y, x)  # @line L4
    while work:  # @line L5
        n = work.popleft()  # @line L6
        queued.discard(n)
        d = delta[n]
        delta[n] = set()
        for a in d:  # @line L7
            for p in loads[n]:
                add_edge(a, p)  # @line L8
            for q in stores[n]:
                add_edge(q, a)  # @line L9
        for w in list(succ[n]):
            propagate(d, w)  # @line L10
    return pts  # @line L11


def may_alias(pts, p, q):
    """True if the locations *p and *q may be the same."""
    return bool(pts.get(p, set()) & pts.get(q, set()))


def points_to(text):
    """Run the analysis on a program written in toy IR notation."""
    return andersen(ptsgen.parse(text))
