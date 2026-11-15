# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-algebra-consistency/. The authors are listed in prov/TYA2PW.jsonl.

"""Consistency of a point algebra network by strongly connected components.

A label is a mask over the base relations <, =, > (bits 0, 1, 2), as in
qcn.point_algebra(). The pair (i, j) with label {<, =} means x_i <= x_j.
"""

LT, EQ, GT = 1, 2, 4
LE = LT | EQ  # {<, =}


def _converse(r: int) -> int:
    return (r & EQ) | (LT if r & GT else 0) | (GT if r & LT else 0)


def _scc(n: int, succ: list[list[int]]) -> list[int]:
    """Tarjan's algorithm without recursion. comp[v] numbers the components
    in reverse topological order: an edge u -> v has comp[u] >= comp[v]."""
    index = [-1] * n
    low = [0] * n
    comp = [-1] * n
    stack: list[int] = []
    counter = ncomp = 0
    for root in range(n):
        if index[root] != -1:
            continue
        work = [(root, 0)]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        while work:
            v, pos = work[-1]
            if pos < len(succ[v]):
                work[-1] = (v, pos + 1)
                w = succ[v][pos]
                if index[w] == -1:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    work.append((w, 0))
                elif comp[w] == -1:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    comp[w] = ncomp
                    if w == v:
                        break
                ncomp += 1
    return comp


def point_algebra_consistency(n: int, net: dict[tuple[int, int], int]) -> list[int] | None:
    """Return integers v[0 .. n-1] that satisfy every label, or None if the
    network is inconsistent.

    net maps pairs (i, j), i < j, to masks over {<, =, >}; a missing pair has
    the universal label. Cost: O(n + e) for e labelled pairs, so O(n^2).
    """
    if any(r == 0 for r in net.values()):  # @line L1
        return None
    succ: list[list[int]] = [[] for _ in range(n)]  # @line L2
    for (i, j), r in net.items():  # @line L3
        for a, b, s in ((i, j, r), (j, i, _converse(r))):
            if s & LE == s:
                succ[a].append(b)
    comp = _scc(n, succ)  # @line L4
    for (i, j), r in net.items():  # @line L5
        if comp[i] == comp[j] and not r & EQ:  # @line L6
            return None
    top = max(comp, default=-1)
    return [top - comp[v] for v in range(n)]  # @line L7
