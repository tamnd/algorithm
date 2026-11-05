# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-arborescence/. The authors are listed in prov/04S04K.jsonl.


def edmonds_arborescence(n: int, arcs: list[tuple[int, int, float]], root: int) -> list[int] | None:
    """Return the indices of a minimum arborescence rooted at root, or None.

    The vertices are 0 .. n - 1 and arcs[i] = (u, v, c) is an arc from u to
    v of cost c. Costs may be negative and may tie; parallel arcs and
    self-loops are allowed. Self-loops and arcs into the root are never
    used. The result is None when some vertex is not reachable from the
    root, since then no spanning arborescence exists. Ties between the
    arcs into a vertex are broken by the smaller index.

    Cost: at most n - 1 contractions of O(n + m) each, so O(m n) time.
    """
    work = [(u, v, c, i) for i, (u, v, c) in enumerate(arcs)]
    chosen = _solve(n, work, root)
    return None if chosen is None else sorted(chosen)


def _solve(n: int, arcs: list[tuple[int, int, float, int]], root: int) -> list[int] | None:
    """Solve one level; arcs[i][3] is the index of the arc one level up."""
    best = [-1] * n
    for i, (u, v, c, _) in enumerate(arcs):  # @line L1
        if u != v and v != root and (best[v] < 0 or c < arcs[best[v]][2]):  # @line L2
            best[v] = i
    if any(best[v] < 0 for v in range(n) if v != root):  # @line L3
        return None
    cycle = _find_cycle(n, arcs, best, root)
    if not cycle:  # @line L4
        return [best[v] for v in range(n) if v != root]
    in_cycle = [False] * n  # @line L5
    for v in cycle:
        in_cycle[v] = True
    label = [0] * n
    k = 0
    for v in range(n):
        if not in_cycle[v]:
            label[v] = k
            k += 1
    for v in cycle:
        label[v] = k
    child = []
    for i, (u, v, c, _) in enumerate(arcs):  # @line L6
        if label[u] != label[v]:
            cost = c - arcs[best[v]][2] if in_cycle[v] else c
            child.append((label[u], label[v], cost, i))
    sub = _solve(k + 1, child, label[root])  # @line L7
    if sub is None:  # @line L8
        return None
    chosen = [child[j][3] for j in sub]
    entry = next(arcs[i][1] for i in chosen if in_cycle[arcs[i][1]])  # @line L9
    return chosen + [best[v] for v in cycle if v != entry]  # @line L10


def _find_cycle(n: int, arcs: list[tuple[int, int, float, int]], best: list[int], root: int) -> list[int]:
    """Return the vertices of a cycle of the arcs best[v], or [] if none."""
    mark = [0] * n
    for s in range(n):
        x = s
        while x != root and mark[x] == 0:
            mark[x] = s + 1
            x = arcs[best[x]][0]
        if x != root and mark[x] == s + 1:
            cycle = [x]
            y = arcs[best[x]][0]
            while y != x:
                cycle.append(y)
                y = arcs[best[y]][0]
            return cycle
    return []
