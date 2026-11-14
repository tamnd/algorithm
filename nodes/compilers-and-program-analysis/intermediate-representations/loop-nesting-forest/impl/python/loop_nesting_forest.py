# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loop-nesting-forest/. The authors are listed in prov/EMNP01.jsonl.
"""A loop nesting forest by repeated strongly connected components.

loop_forest(n, edges, root) returns a list of loops. Each loop is a dict
with "nodes" (the sorted vertices of the loop, inner loops included),
"headers" (its entry vertices, sorted) and "parent" (the index of the
smallest loop that contains it, or -1). The loops are the nontrivial
strongly connected components of the part that root reaches; inside each
loop, the headers are removed and the rest is split again. The headers of a
loop are its vertices with a predecessor outside the loop, and root, if the
loop contains it. This choice of headers is the one of Steensgaard; on a
reducible graph each loop then has one header and is the union of the
natural loops of that header.

innermost(n, loops) gives, for each vertex, the index of the innermost loop
that contains it, or -1. cfg_loops(prog) works on the blocks of a toy IR
program and uses labels.
"""

import toyir


def _sccs(nodes, succ):
    """Tarjan's algorithm with an explicit stack, on the subgraph induced by
    the set nodes. Returns the components as lists."""
    index = {}
    low = {}
    on = set()
    stack = []
    out = []
    counter = 0
    for s in sorted(nodes):
        if s in index:
            continue
        index[s] = low[s] = counter
        counter += 1
        stack.append(s)
        on.add(s)
        work = [(s, iter(succ[s]))]
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in nodes:
                    continue
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(succ[w])))
                    advanced = True
                    break
                if w in on and index[w] < low[v]:
                    low[v] = index[w]
            if advanced:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                if low[v] < low[u]:
                    low[u] = low[v]
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


def loop_forest(n, edges, root):
    if n < 1 or not 0 <= root < n:
        raise ValueError("a flow graph needs n >= 1 vertices and a root in range")
    succ = [[] for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("edge endpoint out of range")
        succ[a].append(b)
    seen = {root}  # @line L1
    stack = [root]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    pred = [[] for _ in range(n)]
    for a, b in edges:
        if a in seen:
            pred[b].append(a)

    loops = []
    regions = [(seen, -1)]
    while regions:  # @line L2
        region, parent = regions.pop()  # @line L3
        for comp in _sccs(region, succ):  # @line L4
            body = set(comp)
            v = comp[0]
            if len(comp) == 1 and v not in succ[v]:  # @line L5
                continue
            heads = {x for x in body if x == root or any(p not in body for p in pred[x])}  # @line L6
            loops.append({"nodes": sorted(body), "headers": sorted(heads), "parent": parent})  # @line L7
            regions.append((body - heads, len(loops) - 1))  # @line L8
    return loops  # @line L9


def innermost(n, loops):
    """The innermost loop of each vertex, or -1. A loop comes after its
    parent in the list, so the last loop that contains a vertex is the
    innermost one."""
    out = [-1] * n
    for i, loop in enumerate(loops):
        for v in loop["nodes"]:
            out[v] = i
    return out


def depth(loops, i):
    """The number of loops on the path from loop i up to its root."""
    d = 0
    while i != -1:
        d += 1
        i = loops[i]["parent"]
    return d


def cfg_loops(prog):
    """The loops of a toy IR program, with block labels instead of numbers."""
    labels = list(prog.blocks)
    index = {lab: i for i, lab in enumerate(labels)}
    edges = [(index[a], index[b]) for a, b in toyir.edges(prog)]
    loops = loop_forest(len(labels), edges, 0)
    return [
        {
            "nodes": [labels[v] for v in loop["nodes"]],
            "headers": [labels[v] for v in loop["headers"]],
            "parent": loop["parent"],
        }
        for loop in loops
    ]
