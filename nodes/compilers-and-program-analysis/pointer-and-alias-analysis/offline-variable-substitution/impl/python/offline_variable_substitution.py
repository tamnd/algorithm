# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-variable-substitution/. The authors are listed in prov/Q7GZTS.jsonl.
"""Offline variable substitution for Andersen's analysis.

substitute(stmts) looks at the statements before any solving and gives
each variable a representative, rep[v], such that variables with the same
representative surely have the same least points-to set. It works on the
copy graph, with an edge q -> p for each p = q:

* the variables on one cycle of copies have equal sets;
* a variable that gets values only through copies, not through p = &a,
  p = *q, or a store into it (which needs its address to be taken), has
  the union of the sets of its copy sources; if all its sources carry one
  label, it has the same set as them.

ovs(stmts) rewrites the statements over the representatives, solves the
smaller system with a worklist solver, and maps the result back. The
result is exactly Andersen's least solution. The addresses in the sets
stay the original locations: the set of a location a is stored at rep[a].
"""

from collections import deque

import ptsgen

EMPTY = 0  # the label of variables whose least set is surely empty


def sccs(names, succ):
    """Tarjan's algorithm, without recursion. Returns the strongly
    connected components in reverse topological order."""
    index, low, on_stack = {}, {}, set()
    stack, out = [], []
    counter = 0
    for root in names:
        if root in index:
            continue
        work = [(root, iter(succ[root]))]
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
                    work.append((w, iter(succ[w])))
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


def substitute(stmts):
    names = ptsgen.variables(stmts)
    succ = {v: [] for v in names}
    pred = {v: [] for v in names}
    for kind, x, y in stmts:
        if kind == "copy" and x != y:
            succ[y].append(x)  # @line L1
            pred[x].append(y)
    indirect = set()
    for kind, x, y in stmts:
        if kind == "addr":
            indirect.add(x)  # @line L2
            indirect.add(y)
        elif kind == "load":
            indirect.add(x)
    comp_of = {}
    comps = sccs(names, succ)
    for i, comp in enumerate(comps):
        for v in comp:
            comp_of[v] = i
    label = {}
    fresh = 0
    for i in reversed(range(len(comps))):  # @line L3
        comp = comps[i]
        if any(v in indirect for v in comp):
            fresh += 1
            label[i] = fresh  # @line L4
            continue
        incoming = {label[comp_of[q]] for v in comp for q in pred[v]  # @line L5
                    if comp_of[q] != i} - {EMPTY}
        if not incoming:
            label[i] = EMPTY  # @line L6
        elif len(incoming) == 1:
            label[i] = incoming.pop()  # @line L7
        else:
            fresh += 1
            label[i] = fresh  # @line L8
    first = {}
    for v in names:
        first.setdefault(label[comp_of[v]], v)
    return {v: first[label[comp_of[v]]] for v in names}  # @line L9


def rewrite(stmts, rep):
    out = []
    seen = set()
    for kind, x, y in stmts:
        if kind == "addr":
            s = (kind, rep[x], y)  # @line L10
        else:
            s = (kind, rep[x], rep[y])
        if (kind == "copy" and s[1] == s[2]) or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def solve(reduced, rep):
    """Andersen's worklist solver with difference propagation, where the
    set of the location a lives at the node rep[a]."""
    nodes = set(rep.values())
    pts = {r: set() for r in nodes}
    delta = {r: set() for r in nodes}
    succ = {r: set() for r in nodes}
    loads = {r: [] for r in nodes}
    stores = {r: [] for r in nodes}
    work = deque()

    def propagate(s, v):
        new = s - pts[v]
        if new:
            pts[v] |= new
            if not delta[v]:
                work.append(v)
            delta[v] |= new

    def add_edge(u, v):
        if u != v and v not in succ[u]:
            succ[u].add(v)
            propagate(pts[u], v)

    for kind, x, y in reduced:
        if kind == "addr":
            propagate({y}, x)
        elif kind == "copy":
            add_edge(y, x)
        elif kind == "load":
            loads[y].append(x)
        else:
            stores[x].append(y)
    while work:
        n = work.popleft()
        d, delta[n] = delta[n], set()
        for a in d:
            for p in loads[n]:
                add_edge(rep[a], p)  # @line L11
            for q in stores[n]:
                add_edge(q, rep[a])
        for w in list(succ[n]):
            propagate(d, w)
    return pts


def ovs(stmts):
    rep = substitute(stmts)
    reduced = rewrite(stmts, rep)
    m = solve(reduced, rep)
    stats = {"variables": len(rep), "nodes": len(set(rep.values())),
             "statements": len(set(stmts)), "reduced": len(reduced)}
    return {v: set(m[rep[v]]) for v in rep}, stats  # @line L12


def points_to(text):
    return ovs(ptsgen.parse(text))[0]
