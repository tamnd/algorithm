# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vizing-algorithm/. The authors are listed in prov/5TRSEH.jsonl.

from collections.abc import Sequence


def vizing_algorithm(n: int, edges: Sequence[tuple[int, int]]) -> list[int]:
    """Color the edges of a simple graph with at most Delta + 1 colors (Misra and Gries).

    The vertices are 0 .. n-1 and edges lists the edges (u, v) with u != v and no
    repeats. Returns a list col with col[i] in 1 .. Delta + 1 the color of edges[i],
    such that edges with a common end get different colors. Edges are colored one
    at a time: build a maximal fan at u, flip the path of colors c and d that starts
    at u, rotate a prefix of the fan and color the last edge of it with d.
    Time O(m (n + Delta^2)), space O(n + m).
    """
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    k = max(deg, default=0) + 1
    at: list[dict[int, int]] = [{} for _ in range(n)]  # at[x][color] = other end
    color: dict[tuple[int, int], int] = {}

    def get(x: int, y: int) -> int:
        return color.get((x, y), 0)

    def put(x: int, y: int, c: int) -> None:
        old = color.pop((x, y), 0)
        color.pop((y, x), None)
        if old:
            del at[x][old]
            del at[y][old]
        if c:
            color[(x, y)] = color[(y, x)] = c
            at[x][c] = y
            at[y][c] = x

    def free(x: int) -> int:
        return next(c for c in range(1, k + 1) if c not in at[x])

    nbrs: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        nbrs[u].append(v)
        nbrs[v].append(u)

    for u, v in edges:  # @line L1
        fan = [v]  # @line L2: a maximal fan of u starting at v
        in_fan = {v}
        grown = True
        while grown:
            grown = False
            for x in nbrs[u]:
                cx = get(u, x)
                if x not in in_fan and cx and cx not in at[fan[-1]]:
                    fan.append(x)
                    in_fan.add(x)
                    grown = True
                    break
        c = free(u)  # @line L3
        d = free(fan[-1])
        path: list[tuple[int, int]] = []  # @line L4: flip the cd-path from u
        x, want = u, d
        while want in at[x]:
            y = at[x][want]
            path.append((x, y))
            x, want = y, (c if want == d else d)
        old = [get(a, b) for a, b in path]
        for a, b in path:
            put(a, b, 0)
        for (a, b), o in zip(path, old):
            put(a, b, c if o == d else d)
        j = 0  # @line L5: first w such that fan[..w] is a fan and d is free at w
        while d in at[fan[j]]:
            j += 1
            assert get(u, fan[j]) not in at[fan[j - 1]]
        for i in range(j):  # @line L6: rotate fan[0 .. j]
            nxt = get(u, fan[i + 1])
            put(u, fan[i + 1], 0)
            put(u, fan[i], nxt)
        put(u, fan[j], d)  # @line L7
    return [get(u, v) for u, v in edges]  # @line L8
