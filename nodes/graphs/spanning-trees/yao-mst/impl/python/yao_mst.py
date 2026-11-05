# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-mst/. The authors are listed in prov/CXZBFW.jsonl.

import math


def _select(items: list, r: int, key) -> object:
    """Return the item of rank r (0-based) in items under key, by median of medians."""
    while True:
        if len(items) <= 5:
            return sorted(items, key=key)[r]
        groups = [sorted(items[i:i + 5], key=key) for i in range(0, len(items), 5)]
        medians = [g[len(g) // 2] for g in groups]
        pivot = _select(medians, len(medians) // 2, key)
        pk = key(pivot)
        low = [x for x in items if key(x) < pk]
        high = [x for x in items if key(x) > pk]
        if r < len(low):
            items = low
        elif r == len(low):
            return pivot
        else:
            r -= len(low) + 1
            items = high


def _split(items: list, k: int, key) -> list[list]:
    """Split items into k groups, each key in a group below each key in the next."""
    if k == 1 or not items:
        return [items] + [[] for _ in range(k - 1)]
    k1 = k // 2
    r = len(items) * k1 // k
    if r == 0:
        low, high = [], items
    else:
        pk = key(_select(items, r - 1, key))
        low = [x for x in items if key(x) <= pk]
        high = [x for x in items if key(x) > pk]
    return _split(low, k1, key) + _split(high, k - k1, key)


def yao_mst(n: int, edges: list[tuple[int, int, float]], phases: int | None = None) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest, in increasing order.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge of weight w. Weights may be negative and may tie; ties are broken by
    the edge index, so the result is the unique minimum forest for the order
    (w, index). The graph may be disconnected, and parallel edges and
    self-loops are allowed. phases is the number of plain Borůvka phases
    before the grouped phases; the default is ceil(log2 log2 n).

    Cost: O(m log log n) time and O(n + m) extra space, where m = len(edges).
    """
    key = lambda i: (edges[i][2], i)
    forest: list[int] = []  # @line L1
    comp = list(range(n))

    def find(x: int) -> int:
        while comp[x] != x:
            comp[x] = comp[comp[x]]
            x = comp[x]
        return x

    def boruvka_phase() -> bool:
        best: dict[int, int] = {}
        for i, (u, v, _) in enumerate(edges):
            a, b = find(u), find(v)
            if a == b:
                continue
            for c in (a, b):
                if c not in best or key(i) < key(best[c]):
                    best[c] = i
        for i in set(best.values()):
            a, b = find(edges[i][0]), find(edges[i][1])
            if a != b:
                comp[a] = b
                forest.append(i)
        return bool(best)

    if phases is None:
        phases = math.ceil(math.log2(math.log2(n))) if n > 2 else 1
    for _ in range(phases):  # @line L2
        if not boruvka_phase():
            break
    # The contracted graph H: one vertex for each component, only edges between components.
    reps = sorted({find(x) for x in range(n)})
    inc: dict[int, list[int]] = {r: [] for r in reps}
    for i, (u, v, _) in enumerate(edges):
        a, b = find(u), find(v)
        if a != b:
            inc[a].append(i)
            inc[b].append(i)
    hv = [r for r in reps if inc[r]]
    k = max(1, math.ceil(math.log2(len(hv)))) if len(hv) > 1 else 1  # @line L3
    groups: dict[int, list[list[int]]] = {}
    cur: dict[int, int] = {}
    for v in hv:  # @line L4
        groups[v] = _split(inc[v], k, key)  # @line L5
        cur[v] = 0  # @line L6

    while True:  # @line L7
        best: dict[int, int] = {}
        for x in hv:  # @line L8
            c = find(x)  # @line L9
            while True:  # @line L10
                g = [i for i in groups[x][cur[x]] if find(edges[i][0]) != find(edges[i][1])]
                groups[x][cur[x]] = g
                if g or cur[x] == k - 1:
                    break
                cur[x] += 1
            if g:
                ev = min(g, key=key)  # @line L11
                if c not in best or key(ev) < key(best[c]):
                    best[c] = ev  # @line L12
        if not best:
            break
        for i in set(best.values()):  # @line L13
            a, b = find(edges[i][0]), find(edges[i][1])
            if a != b:
                comp[a] = b
                forest.append(i)
    return sorted(forest)  # @line L14
