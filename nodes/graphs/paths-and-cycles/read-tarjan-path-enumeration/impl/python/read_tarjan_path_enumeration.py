# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-tarjan-path-enumeration/. The authors are listed in prov/89EF45.jsonl.


def read_tarjan_path_enumeration(
    n: int, edges: list[tuple[int, int]], s: int, t: int, directed: bool = True
) -> list[list[int]]:
    """Return every simple path from s to t, each as a list of vertices.

    Vertices are 0 .. n-1. If directed is False, each edge (u, v) can be used both
    ways. Parallel edges are merged (a path is a vertex sequence) and self-loops are
    ignored, since no simple path uses them. Every step that the search takes leads to
    a new path, so the time is O((n + m)(N + 1)) for N paths and the delay between two
    outputs is O(n + m); the pending branches take O(n m) extra space in the worst case.
    """
    out_sets: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            out_sets[u].add(v)
            if not directed:
                out_sets[v].add(u)
    out = [sorted(x) for x in out_sets]
    inc: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in out[u]:
            inc[v].append(u)

    paths: list[list[int]] = []
    if s == t:  # @line L1
        return [[s]]
    if _find_path(out, s, t, set()) is None:  # @line L2
        return paths
    # a pending branch is (full path of the parent, cut length, next vertex)
    stack: list[tuple[list[int], int, int]] = [([s], 0, -1)]  # @line L3
    while stack:  # @line L4
        full, cut, x = stack.pop()  # @line L5
        prefix = full if x < 0 else full[:cut] + [x]
        u = prefix[-1]
        if u == t:  # @line L6
            paths.append(prefix)
            continue
        blocked = set(prefix[:-1])  # @line L7
        p = _find_path(out, u, t, blocked)  # @line L8
        assert p is not None
        whole = prefix + p[1:]  # @line L9
        paths.append(whole)
        k = len(p) - 1  # @line L10
        for v in p[:k]:
            blocked.add(v)
        reach = _reverse_reach(inc, t, blocked)
        base = len(prefix) - 1
        for i in range(k - 1, -1, -1):  # @line L11
            if i < k - 1:  # @line L12
                w = p[i + 1]
                blocked.discard(w)
                if any(y in reach for y in out[w]):
                    _grow(inc, w, blocked, reach)
            for y in out[p[i]]:  # @line L13
                if y != p[i + 1] and y in reach:
                    stack.append((whole, base + i + 1, y))  # @line L14
    return paths


def _find_path(out: list[list[int]], u: int, t: int, blocked: set[int]) -> list[int] | None:
    """Iterative DFS for a path from u to t that avoids blocked; O(n + m)."""
    parent = {u: u}
    todo = [u]
    while todo:
        a = todo.pop()
        if a == t:
            path = [t]
            while path[-1] != u:
                path.append(parent[path[-1]])
            path.reverse()
            return path
        for b in out[a]:
            if b not in parent and b not in blocked:
                parent[b] = a
                todo.append(b)
    return None


def _reverse_reach(inc: list[list[int]], t: int, blocked: set[int]) -> set[int]:
    """The vertices outside blocked that reach t avoiding blocked."""
    reach = {t}
    _spread(inc, [t], blocked, reach)
    return reach


def _grow(inc: list[list[int]], w: int, blocked: set[int], reach: set[int]) -> None:
    reach.add(w)
    _spread(inc, [w], blocked, reach)


def _spread(inc: list[list[int]], todo: list[int], blocked: set[int], reach: set[int]) -> None:
    while todo:
        a = todo.pop()
        for b in inc[a]:
            if b not in reach and b not in blocked:
                reach.add(b)
                todo.append(b)
