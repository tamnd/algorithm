# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ultrametric-contour-map/. The authors are listed in prov/6B2NMJ.jsonl.

"""Ultrametric contour map from an initial partition and edge strengths.

The image is a grid of w columns and h rows. A pixel is (u, v), and a value at
(u, v) is img[v][u]. Boundaries lie on the grid edges between 4-neighbors:
eh[v][u] is the strength of the edge between (u, v) and (u + 1, v), and
ev[v][u] is the strength of the edge between (u, v) and (u, v + 1).

The algorithm merges, one pair at a time, the two adjacent regions whose
common boundary has the least mean strength. The level of a merge is that mean.
The UCM value of a grid edge is the level of the merge that first puts its two
pixels in one region. Strengths may be int, float or Fraction.
"""

import heapq


def components(labels):
    """Return (comp, r): the 4-connected components of equal labels, numbered 0 .. r - 1 in raster order."""
    h, w = len(labels), len(labels[0])
    comp = [[-1] * w for _ in range(h)]
    r = 0
    for v0 in range(h):
        for u0 in range(w):
            if comp[v0][u0] >= 0:
                continue
            comp[v0][u0] = r
            stack = [(u0, v0)]
            while stack:
                u, v = stack.pop()
                for x, y in ((u + 1, v), (u - 1, v), (u, v + 1), (u, v - 1)):
                    if 0 <= x < w and 0 <= y < h and comp[y][x] < 0 and labels[y][x] == labels[v][u]:
                        comp[y][x] = r
                        stack.append((x, y))
            r += 1
    return comp, r


def grid_edges(w, h):
    """Yield (kind, u, v, p, q) for each 4-neighbor edge; kind 0 is horizontal (eh), kind 1 is vertical (ev)."""
    for v in range(h):
        for u in range(w - 1):
            yield 0, u, v, (u, v), (u + 1, v)
    for v in range(h - 1):
        for u in range(w):
            yield 1, u, v, (u, v), (u, v + 1)


def ultrametric_contour_map(labels, eh, ev):
    """Return (uh, uv, merges).

    uh and uv have the shapes of eh and ev and hold the UCM value of each grid
    edge. merges is the list of (level, a, b, c): regions a and b merge into the
    new region c at the given level. The initial regions are 0 .. r - 1 and the
    new regions get the next free ids. Ties go to the smallest pair (a, b).
    """
    h, w = len(labels), len(labels[0])
    strength = (eh, ev)
    comp, r0 = components(labels)  # @line L1
    # adj[a][b] = [S, n, keys] is shared by a and b. keys lists the pairs of
    # initial regions whose common grid edges lie between a and b.
    adj = [dict() for _ in range(r0)]
    for kind, u, v, (u1, v1), (u2, v2) in grid_edges(w, h):  # @line L2
        a, b = comp[v1][u1], comp[v2][u2]
        if a != b:
            rec = adj[a].get(b)
            if rec is None:
                rec = [0, 0, [(min(a, b), max(a, b))]]
                adj[a][b] = rec
                adj[b][a] = rec
            rec[0] += strength[kind][v][u]  # @line L3
            rec[1] += 1
    heap = [(rec[0] / rec[1], a, b) for a in range(r0) for b, rec in adj[a].items() if a < b]  # @line L4
    heapq.heapify(heap)
    alive = [True] * r0
    value = {}
    merges = []
    while heap:  # @line L5
        m, a, b = heapq.heappop(heap)
        if not (alive[a] and alive[b]):  # @line L6
            continue
        c = len(alive)  # @line L7
        alive[a] = alive[b] = False
        alive.append(True)
        merges.append((m, a, b, c))
        for key in adj[a][b][2]:
            value[key] = m  # @line L8
        merged = {}
        for x in (a, b):  # @line L9
            for r, rec in adj[x].items():
                if r == a or r == b:
                    continue
                del adj[r][x]
                acc = merged.get(r)
                if acc is None:
                    merged[r] = rec
                else:
                    acc[0] += rec[0]  # @line L10
                    acc[1] += rec[1]
                    if len(acc[2]) < len(rec[2]):
                        acc[2], rec[2] = rec[2], acc[2]
                    acc[2].extend(rec[2])
            adj[x] = None
        adj.append(merged)
        for r, rec in merged.items():
            adj[r][c] = rec
            heapq.heappush(heap, (rec[0] / rec[1], r, c))
    uh = [[0] * (w - 1) for _ in range(h)]
    uv = [[0] * w for _ in range(h - 1)]
    out = (uh, uv)
    for kind, u, v, (u1, v1), (u2, v2) in grid_edges(w, h):  # @line L11
        a, b = comp[v1][u1], comp[v2][u2]
        if a != b:
            out[kind][v][u] = value[(min(a, b), max(a, b))]
    return uh, uv, merges  # @line L12


def threshold(uh, uv, t):
    """Return a label map of the components of the grid edges with UCM value at most t."""
    h, w = len(uh), len(uh[0]) + 1
    parent = list(range(w * h))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for kind, u, v, (u1, v1), (u2, v2) in grid_edges(w, h):
        val = uh[v][u] if kind == 0 else uv[v][u]
        if val <= t:
            parent[find(v1 * w + u1)] = find(v2 * w + u2)
    return [[find(v * w + u) for u in range(w)] for v in range(h)]
