# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/branch-and-reduce/. The authors are listed in prov/HSNMTD.jsonl.
"""Branch and reduce for maximum independent set.

Reduction rules: take a vertex of degree 0 or 1; delete a vertex u that has a
neighbor v with N[v] a subset of N[u]. When every vertex has degree 2, the graph
is a union of cycles and is solved directly. Otherwise branch on a vertex of
maximum degree: leave it out, or take it and delete its closed neighborhood.
The search uses an explicit stack, so deep trees do not hit the recursion limit.
"""

from __future__ import annotations

from typing import Iterable, Optional

Graph = dict[int, set[int]]


def delete(g: Graph, vs: Iterable[int]) -> None:
    """Delete the vertices vs from g, in place."""
    for v in list(vs):
        if v in g:
            for u in g.pop(v):
                if u in g:
                    g[u].discard(v)


def reduce_graph(g: Graph, chosen: list[int], stats: Optional[dict[str, int]] = None) -> None:
    """Apply the reduction rules until none applies. Taken vertices go to chosen."""
    while True:
        v = next((x for x in g if len(g[x]) <= 1), None)
        if v is not None:
            if not g[v]:  # @line L5
                chosen.append(v)
                delete(g, [v])
            else:  # @line L6
                chosen.append(v)
                delete(g, [v, *g[v]])
            if stats is not None:
                stats["reductions"] += 1
            continue
        hit = None
        for v in g:  # @line L7
            closed = g[v] | {v}
            for u in g[v]:
                if closed <= g[u] | {u}:
                    hit = u
                    break
            if hit is not None:
                break
        if hit is None:
            return
        delete(g, [hit])
        if stats is not None:
            stats["reductions"] += 1


def cycles_mis(g: Graph) -> list[int]:
    """Maximum independent set of a graph in which every vertex has degree 2."""
    out: list[int] = []
    seen: set[int] = set()
    for start in sorted(g):
        if start in seen:
            continue
        cycle = [start]
        seen.add(start)
        prev, cur = None, start
        while True:
            nxt = min(u for u in g[cur] if u != prev) if prev is not None else min(g[cur])
            if nxt == start:
                break
            cycle.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt
        out.extend(cycle[0:2 * (len(cycle) // 2):2])
    return out


def max_independent_set(
    n: int, edges: Iterable[tuple[int, int]], stats: Optional[dict[str, int]] = None
) -> tuple[int, list[int]]:
    """Return (size, vertices) of a maximum independent set of the graph on 0..n-1."""
    if stats is not None:
        stats.update(nodes=0, leaves=0, reductions=0)
    g0: Graph = {v: set() for v in range(n)}
    for u, v in edges:
        if u != v:
            g0[u].add(v)
            g0[v].add(u)
    best: list[int] = []  # @line L1
    stack: list[tuple[Graph, list[int]]] = [(g0, [])]
    while stack:  # @line L2
        g, chosen = stack.pop()  # @line L3
        if stats is not None:
            stats["nodes"] += 1
        reduce_graph(g, chosen, stats)  # @line L4
        if all(len(g[v]) <= 2 for v in g):  # @line L8
            chosen = chosen + cycles_mis(g)  # @line L9
            if stats is not None:
                stats["leaves"] += 1
            if len(chosen) > len(best):
                best = chosen
            continue
        v = max(g, key=lambda x: (len(g[x]), -x))  # @line L10
        g_out = {x: set(nb) for x, nb in g.items()}
        delete(g_out, [v])
        g_in = {x: set(nb) for x, nb in g.items()}
        delete(g_in, [v, *g[v]])
        stack.append((g_out, chosen))  # @line L11
        stack.append((g_in, chosen + [v]))  # @line L12
    return len(best), sorted(best)  # @line L13
