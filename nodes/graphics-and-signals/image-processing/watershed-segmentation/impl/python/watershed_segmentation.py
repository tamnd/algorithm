# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watershed-segmentation/. The authors are listed in prov/P0M4PZ.jsonl.

"""Watershed segmentation.

watershed_immersion computes the watershed by immersion exactly as defined
by the recursion of Vincent and Soille, in the form given by Roerdink and
Meijster (Definition 3.2):

    X_hmin   = the pixels at the lowest level
    X_(h+1)  = (regional minima at h + 1) union IZ_(T_(h+1))(X_h)

for every integer h from the least to the largest value, where T_h is the
set of pixels with value at most h and IZ is the union of the geodesic
influence zones of the basins inside T_(h+1). A pixel that is equally far
from two basins is a watershed pixel (label WSHED) for now; it can still
join a basin at a higher level, so every pass recomputes all the current
watershed pixels. A level with no pixels is skipped only when the pass
before it changed nothing, because then IZ returns the same basins again.

watershed_from_markers floods from given markers in the order of Prim's
algorithm on the edge weights max(f(p), f(q)), so every pixel gets the label
of a marker that it reaches by a path whose highest value is as low as
possible. It labels every pixel and draws no watershed lines.
"""

import heapq
from typing import Dict, List, Sequence, Tuple

WSHED = -1
_MASK = -2


def neighbors(x: int, y: int, w: int, h: int, connectivity: int):
    if connectivity == 4:
        steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    elif connectivity == 8:
        steps = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))
    else:
        raise ValueError("connectivity must be 4 or 8")
    for dx, dy in steps:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            yield nx, ny


def watershed_immersion(f: Sequence[Sequence[int]], connectivity: int = 4) -> List[List[int]]:
    """Label image: basins 1, 2, ... in order of creation, WSHED for watershed pixels."""
    h = len(f)
    w = len(f[0]) if h else 0
    lab = [[0] * w for _ in range(h)]
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    if h == 0 or w == 0:
        return lab
    levels: Dict[int, List[Tuple[int, int]]] = {}
    for y in range(h):  # @line L1
        for x in range(w):
            levels.setdefault(f[y][x], []).append((x, y))
    curlab = 0
    wshed: set = set()
    changed = True
    for v in range(min(levels), max(levels) + 1):  # @line L2
        new = levels.get(v, [])  # @line L3
        if not new and not changed:
            continue  # the same threshold set and the same basins: nothing moves
        for x, y in new:
            lab[y][x] = _MASK
        # Every non-basin pixel of the threshold set is recomputed: the new
        # pixels and all the current watershed pixels.
        region = new + list(wshed)  # @line L4  (new is in raster order)
        seen = set(region)
        dist: Dict[Tuple[int, int], int] = {}
        labels: Dict[Tuple[int, int], frozenset] = {}
        layer = []
        for x, y in region:  # @line L5
            near = {lab[ny][nx] for nx, ny in neighbors(x, y, w, h, connectivity) if lab[ny][nx] > 0}
            if near:
                dist[(x, y)] = 1
                labels[(x, y)] = frozenset(near)
                layer.append((x, y))
        d = 1
        while layer:  # @line L6
            nxt = []
            for x, y in layer:
                for q in neighbors(x, y, w, h, connectivity):
                    if q in seen and q not in dist:
                        dist[q] = d + 1
                        nxt.append(q)
            for q in nxt:
                s = set()
                for p in neighbors(q[0], q[1], w, h, connectivity):
                    if dist.get(p) == d:
                        s |= labels[p]
                labels[q] = frozenset(s)
            layer, d = nxt, d + 1
        changed = False
        for p in region:  # @line L7
            if p in dist:
                s = labels[p]
                if len(s) == 1:
                    lab[p[1]][p[0]] = next(iter(s))
                    changed = changed or p in wshed
                    wshed.discard(p)
                else:
                    lab[p[1]][p[0]] = WSHED
                    wshed.add(p)
        changed = changed or bool(new)
        for x, y in region:  # @line L8
            if lab[y][x] == _MASK:
                curlab += 1
                lab[y][x] = curlab
                stack = [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    for nx, ny in neighbors(cx, cy, w, h, connectivity):
                        if lab[ny][nx] == _MASK:
                            lab[ny][nx] = curlab
                            stack.append((nx, ny))
    return lab  # @line L9


def watershed_from_markers(f: Sequence[Sequence[int]], markers: Sequence[Sequence[int]], connectivity: int = 4) -> List[List[int]]:
    """Flood from markers (positive labels; 0 = unmarked) with a priority queue.

    A pixel q next to a labeled pixel p is queued with the key max(f(p), f(q)).
    The pixel with the least key is labeled next, with the label of the pixel
    that queued it; ties go to the earlier entry. This is Prim's algorithm for
    a minimum spanning forest rooted at the markers.
    """
    h = len(f)
    w = len(f[0]) if h else 0
    lab = [list(row) for row in markers]
    heap: list = []
    order = 0
    for y in range(h):
        for x in range(w):
            if lab[y][x] > 0:
                for nx, ny in neighbors(x, y, w, h, connectivity):
                    if lab[ny][nx] == 0:
                        heapq.heappush(heap, (max(f[y][x], f[ny][nx]), order, nx, ny, lab[y][x]))
                        order += 1
    while heap:
        _, _, x, y, l = heapq.heappop(heap)
        if lab[y][x]:
            continue
        lab[y][x] = l
        for nx, ny in neighbors(x, y, w, h, connectivity):
            if lab[ny][nx] == 0:
                heapq.heappush(heap, (max(f[y][x], f[ny][nx]), order, nx, ny, l))
                order += 1
    return lab


def regional_minima(f: Sequence[Sequence[int]], connectivity: int = 4) -> List[List[int]]:
    """Label the regional minima 1, 2, ... in raster order; 0 elsewhere."""
    h = len(f)
    w = len(f[0]) if h else 0
    lab = [[0] * w for _ in range(h)]
    done = [[False] * w for _ in range(h)]
    k = 0
    for y in range(h):
        for x in range(w):
            if done[y][x]:
                continue
            v = f[y][x]
            comp, stack, is_min = [(x, y)], [(x, y)], True
            done[y][x] = True
            while stack:
                cx, cy = stack.pop()
                for nx, ny in neighbors(cx, cy, w, h, connectivity):
                    if f[ny][nx] < v:
                        is_min = False
                    elif f[ny][nx] == v and not done[ny][nx]:
                        done[ny][nx] = True
                        comp.append((nx, ny))
                        stack.append((nx, ny))
            if is_min:
                k += 1
                for cx, cy in comp:
                    lab[cy][cx] = k
    return lab
