# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-type-analysis/. The authors are listed in prov/5D67PN.jsonl.
"""Variable type analysis (VTA): prune a call graph with the classes that
reach each variable.

variable_type_analysis(prog, initial) takes a program of the oomodel form and
a sound initial call graph initial = (R0, E0), by default the one of rapid
type analysis. It builds the type propagation graph: one node per variable
of each method of R0 and one node per field name, with an edge for each
assignment and for each parameter and result passing along E0. It seeds the
nodes with the classes of the new statements, collapses the strongly
connected components, and propagates the classes in topological order. A
call y.m(z) keeps the edges of E0 to LOOKUP(C, m) for the classes C that
reach y. Returns (R, E), with R the methods reachable from the root along E.

graph_and_seeds and prune are shared with the plain iteration of the tests.
Cost: O((n + |E0|) * K) for a program of size n and K classes.
"""

from oomodel import MAIN, lookup, subclasses


def graph_and_seeds(prog: dict, initial: tuple) -> tuple[dict, dict]:
    """The type propagation graph as successor sets, and the seed classes."""
    reach0, edges0 = initial
    succ, seed = {}, {}

    def edge(a, b):
        succ.setdefault(a, set()).add(b)
        succ.setdefault(b, set())

    by_site = {}
    for s, t in edges0:
        by_site.setdefault(s, []).append(t)
    for mid in reach0:  # @line L1
        local, stmts = prog["bodies"][mid]
        for v in local:
            succ.setdefault((mid, v), set())
        for st in stmts:
            kind = st[0]
            if kind == "new":
                seed.setdefault((mid, st[1]), set()).add(st[2])  # @line L5
            elif kind == "copy":
                edge((mid, st[2]), (mid, st[1]))  # @line L2
            elif kind == "load":
                edge(("field", st[3]), (mid, st[1]))  # @line L3
            elif kind == "store":
                edge((mid, st[3]), ("field", st[2]))  # @line L3
            else:
                _, s, x, y, m, z = st
                for t in by_site.get(s, []):  # @line L4
                    edge((mid, y), (t, "this"))
                    if z is not None:
                        edge((mid, z), (t, "p"))
                    if x is not None:
                        edge((t, "ret"), (mid, x))
    return succ, seed


def prune(prog: dict, initial: tuple, types: dict) -> tuple[set, set]:
    """Keep the edges of E0 that some class reaching the receiver explains,
    then keep what is reachable from the root."""
    below = subclasses(prog)
    reach0, edges0 = initial
    sites = {}
    for mid in reach0:
        for st in prog["bodies"][mid][1]:
            if st[0] == "call":
                sites[st[1]] = (mid, st)
    keep = {}
    for s, t in edges0:  # @line L9
        mid, (_, _, _, y, m, _) = sites[s]
        mdecl = prog["methods"][m][0]
        if any(c in below[mdecl] and lookup(prog, c, m) == t for c in types.get((mid, y), ())):
            keep.setdefault(mid, set()).add((s, t))
    reach, stack, edges = {MAIN}, [MAIN], set()  # @line L10
    while stack:
        mid = stack.pop()
        for s, t in keep.get(mid, ()):
            edges.add((s, t))
            if t not in reach:
                reach.add(t)
                stack.append(t)
    return reach, edges


def components(succ: dict) -> list[list]:
    """Tarjan's strongly connected components, without recursion. The list
    comes in reverse topological order: sinks first."""
    index, low, on, stack, out = {}, {}, set(), [], []
    counter = 0
    for root in succ:
        if root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        work = [(root, iter(succ[root]))]
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(succ[w])))
                    pushed = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def variable_type_analysis(prog: dict, initial: tuple | None = None) -> tuple[set, set]:
    if initial is None:
        from oomodel import rta_spec

        initial = rta_spec(prog)
    succ, seed = graph_and_seeds(prog, initial)
    comps = components(succ)  # @line L6
    rep = {v: i for i, comp in enumerate(comps) for v in comp}
    ctypes = [set() for _ in comps]
    for v, cs in seed.items():
        ctypes[rep[v]] |= cs
    for i in range(len(comps) - 1, -1, -1):  # @line L7
        for v in comps[i]:
            for w in succ[v]:  # @line L8
                if rep[w] != i:
                    ctypes[rep[w]] |= ctypes[i]
    types = {v: ctypes[rep[v]] for v in succ}
    return prune(prog, initial, types)  # @line L11
