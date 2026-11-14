# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/escape-analysis/. The authors are listed in prov/JVVDBX.jsonl.
"""Escape analysis with threads, on top of a field-sensitive Andersen analysis.

A program is a dict from method names to (params, body). params is a list of
parameter names, and body is a list of statements in these forms:

    ("new", x, s)            x = new object at allocation site s
    ("copy", x, y)           x = y
    ("load", x, y, f)        x = y.f
    ("store", x, f, y)       x.f = y
    ("gload", x, g)          x = global g
    ("gstore", g, y)         global g = y
    ("call", x, m, args)     x = m(args), args is a list of local names
    ("start", m, args)       start a new thread that runs m(args)
    ("ret", y)               the method will return the value of y

Each allocation site appears in one "new" statement. Names are local to their
method; globals have their own name space.

escape(program) returns a dict from each allocation site to one of
    GLOBAL  an object from the site may be reachable from a global or from a
            thread other than the one that made it;
    ARG     not GLOBAL, but an object may be reachable from a parameter or
            the return value of the method that made it, so it may outlive
            the activation that made it;
    NONE    an object never leaves the activation that made it and the
            methods it calls: it can live on the stack, and its locks can go.
"""

from collections import deque

NONE, ARG, GLOBAL = "none", "arg", "global"


def points_to(program):
    """Andersen's analysis with fields, globals, calls, returns and thread
    starts, by a constraint graph with difference propagation. The nodes are
    ("v", m, x) for a local, ("r", m) for the return value of m, ("g", g) for
    a global and ("f", s, f) for field f of the objects of site s."""
    pts, succ, delta, loads, stores = {}, {}, {}, {}, {}
    work = deque()
    queued = set()

    def node(n):
        if n not in pts:
            pts[n], succ[n], delta[n] = set(), set(), set()
            loads[n], stores[n] = [], []
        return n

    def push(n):
        if n not in queued:
            queued.add(n)
            work.append(n)

    def propagate(s, n):
        new = s - pts[n]
        if new:
            pts[n] |= new
            delta[n] |= new
            push(n)

    def add_edge(u, v):
        node(u)
        node(v)
        if v not in succ[u]:
            succ[u].add(v)
            propagate(pts[u], v)

    def var(m, x):
        return node(("v", m, x))

    for m, (params, body) in program.items():
        node(("r", m))
        for p in params:
            var(m, p)
        for st in body:
            kind = st[0]
            if kind == "new":
                propagate({st[2]}, var(m, st[1]))
            elif kind == "copy":
                add_edge(var(m, st[2]), var(m, st[1]))
            elif kind == "load":
                loads[var(m, st[2])].append((st[3], var(m, st[1])))
            elif kind == "store":
                stores[var(m, st[1])].append((st[2], var(m, st[3])))
            elif kind == "gload":
                add_edge(node(("g", st[2])), var(m, st[1]))
            elif kind == "gstore":
                add_edge(var(m, st[2]), node(("g", st[1])))
            elif kind in ("call", "start"):
                callee, args = (st[2], st[3]) if kind == "call" else (st[1], st[2])
                for p, a in zip(program[callee][0], args):
                    add_edge(var(m, a), var(callee, p))
                if kind == "call":
                    add_edge(node(("r", callee)), var(m, st[1]))
            elif kind == "ret":
                add_edge(var(m, st[1]), node(("r", m)))
    while work:
        n = work.popleft()
        queued.discard(n)
        d = delta[n]
        delta[n] = set()
        for a in d:
            for f, x in loads[n]:
                add_edge(node(("f", a, f)), x)
            for f, y in stores[n]:
                add_edge(y, node(("f", a, f)))
        for w in list(succ[n]):
            propagate(d, w)
    return pts


def heap_graph(pts):
    """Site s -> the sites that some field of an object of s may point to."""
    heap = {}
    for n, s in pts.items():
        if n[0] == "f":
            heap.setdefault(n[1], set()).update(s)
    return heap


def closure(heap, start):
    seen = set(start)
    stack = list(start)
    while stack:
        s = stack.pop()
        for t in heap.get(s, ()):
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def escape(program):
    pts = points_to(program)  # @line L1
    heap = heap_graph(pts)
    roots = set()
    for n, s in pts.items():
        if n[0] == "g":
            roots |= s
    for m, (_, body) in program.items():
        for st in body:
            if st[0] == "start":
                for a in st[2]:
                    roots |= pts[("v", m, a)]  # @line L2
    shared = closure(heap, roots)  # @line L3
    state = {}
    for m, (params, body) in program.items():  # @line L4
        out = set(pts[("r", m)])
        for p in params:
            out |= pts[("v", m, p)]  # @line L5
        out = closure(heap, out)  # @line L6
        for st in body:
            if st[0] == "new":  # @line L7
                s = st[2]
                if s in shared:
                    state[s] = GLOBAL  # @line L8
                elif s in out:
                    state[s] = ARG  # @line L9
                else:
                    state[s] = NONE  # @line L10
    return state  # @line L11
