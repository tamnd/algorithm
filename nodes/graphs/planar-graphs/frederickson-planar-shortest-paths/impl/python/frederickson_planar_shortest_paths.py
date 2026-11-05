# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frederickson-planar-shortest-paths/. The authors are listed in prov/0AZZWY.jsonl.
"""Single-source shortest paths with two levels of divisions, after
Frederickson (1987).

Input: n, a list of arcs (u, v, length) with length >= 0, and a source.
The graph may be directed; the division uses the underlying undirected
graph. No embedding is given: the divisions are found by splitting a
breadth-first order in half again and again, a simple separator rule that
gives small boundaries on grids and meshes. The answer is correct for any
division and any graph; the time bound needs the boundaries of an
r-division, which a planar separator algorithm guarantees.

Output: the list of distances from the source, with float('inf') for
vertices that cannot be reached. Everything is iterative.
"""

import heapq
import math

INF = float("inf")


def _divide(verts, nbr, r):
    """Split verts into regions of at most r vertices: order each part by
    breadth-first search and cut the order in the middle."""
    regions = []
    todo = [list(verts)]
    while todo:
        part = todo.pop()
        if len(part) <= r:
            regions.append(part)
            continue
        inside = set(part)
        order = []
        seen = set()
        for s in part:
            if s in seen:
                continue
            seen.add(s)
            queue = [s]
            i = 0
            while i < len(queue):
                x = queue[i]
                i += 1
                for y in nbr[x]:
                    if y in inside and y not in seen:
                        seen.add(y)
                        queue.append(y)
            order.extend(queue)
        half = len(order) // 2
        todo.append(order[:half])
        todo.append(order[half:])
    return regions


def _pieces(verts, arcs, r, terminals):
    """An edge division of the subgraph (verts, arcs): a list of pieces
    (vertex set, arc list), and for each piece its boundary: the vertices
    that are in another piece, or in terminals."""
    nbr = {x: [] for x in verts}
    for u, v, _ in arcs:
        nbr[u].append(v)
        nbr[v].append(u)
    regions = _divide(verts, nbr, r)
    region_of = {}
    for i, reg in enumerate(regions):
        for x in reg:
            region_of[x] = i
    pv = [set(reg) for reg in regions]
    pa = [[] for _ in regions]
    for a in arcs:
        i = min(region_of[a[0]], region_of[a[1]])
        pa[i].append(a)
        pv[i].add(a[0])
        pv[i].add(a[1])
    count = {}
    for vs in pv:
        for x in vs:
            count[x] = count.get(x, 0) + 1
    pieces = []
    for vs, al in zip(pv, pa):
        bnd = [x for x in vs if count[x] > 1 or x in terminals]
        pieces.append((vs, al, bnd))
    return pieces


def _dijkstra(arcs, start):
    """Dijkstra on the arcs of one piece, from the labels in start."""
    out = {}
    for u, v, w in arcs:
        out.setdefault(u, []).append((v, w))
    dist = dict(start)
    heap = [(d, x) for x, d in start.items()]
    heapq.heapify(heap)
    done = set()
    while heap:
        d, x = heapq.heappop(heap)
        if x in done:
            continue
        done.add(x)
        for y, w in out.get(x, ()):
            nd = d + w
            if nd < dist.get(y, INF):
                dist[y] = nd
                heapq.heappush(heap, (nd, y))
    return dist


def _boundary_search(pieces, table, start):
    """Dijkstra on the boundary vertices of a division, with one heap entry
    per piece; table[i][b][b2] is the distance from b to b2 inside piece i."""
    d = dict(start)  # @line L13
    settled = set()
    where = {}
    for i, (_, _, bnd) in enumerate(pieces):
        for b in bnd:
            where.setdefault(b, []).append(i)
    key = [INF] * len(pieces)
    heap = []

    def rescan(i):
        m = INF
        for b in pieces[i][2]:
            if b not in settled:
                db = d.get(b, INF)
                if db < m:
                    m = db
        return m

    for b in start:  # @line L14
        for i in where.get(b, ()):
            key[i] = rescan(i)
            heapq.heappush(heap, (key[i], i))
    while heap:  # @line L15
        k, i = heapq.heappop(heap)  # @line L16
        if k != key[i]:
            continue
        m = rescan(i)
        if m != k:
            key[i] = m
            if m < INF:
                heapq.heappush(heap, (m, i))
            continue
        b = None  # @line L17
        for x in pieces[i][2]:
            if x not in settled and d.get(x, INF) == k:
                b = x
                break
        settled.add(b)
        for j in where[b]:  # @line L18
            row = table[j][b]
            for b2, w in row.items():  # @line L19
                if b2 not in settled and k + w < d.get(b2, INF):
                    d[b2] = k + w
            key[j] = rescan(j)  # @line L20
            if key[j] < INF:
                heapq.heappush(heap, (key[j], j))
    return d  # @line L21


def shortest_paths(n, arcs, source, r1=None, r2=None):
    """Distances from source in the graph on 0..n-1 with the given arcs."""
    if not 0 <= source < n:
        raise ValueError("source out of range")
    for u, v, w in arcs:
        if not (0 <= u < n and 0 <= v < n) or w < 0:
            raise ValueError("arcs need ends in range and lengths >= 0")
    if r1 is None:  # @line L1
        r1 = max(4, math.ceil(math.log2(max(n, 2))))
    if r2 is None:
        r2 = max(2, math.ceil(math.log2(r1)) ** 2)
    top = _pieces(range(n), arcs, r1, {source})  # @line L2
    table1 = []
    for vs, al, bnd in top:  # @line L3
        small = _pieces(vs, al, r2, set(bnd))  # @line L4
        table2 = []
        for svs, sal, sbnd in small:  # @line L5
            rows = {}
            for b in sbnd:
                dist = _dijkstra(sal, {b: 0})  # @line L6
                rows[b] = {x: dist[x] for x in sbnd if x != b and x in dist}
            table2.append(rows)
        rows = {}
        for b in bnd:  # @line L7
            dist = _boundary_search(small, table2, {b: 0})  # @line L8
            rows[b] = {x: dist[x] for x in bnd if x != b and x in dist}
        table1.append(rows)
    d = _boundary_search(top, table1, {source: 0})  # @line L9
    result = [INF] * n
    result[source] = 0
    for vs, al, bnd in top:  # @line L10
        start = {b: d[b] for b in bnd if b in d}
        if not start:
            continue
        dist = _dijkstra(al, start)  # @line L11
        for x, dx in dist.items():
            if dx < result[x]:
                result[x] = dx
    return result  # @line L12
