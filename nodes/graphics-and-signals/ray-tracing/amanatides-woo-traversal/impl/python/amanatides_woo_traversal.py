# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amanatides-woo-traversal/. The authors are listed in prov/4NS679.jsonl.
"""Amanatides and Woo (1987) traversal of a uniform 3D grid.

The grid has nx * ny * nz cubic cells of side `size`, with its lowest corner at `lo`. The ray is
the segment o + t d for t in [t0, t1]. Coordinates may be float or Fraction; with Fraction the
walk is exact.
"""

import math


def clip_to_box(o, d, lo, hi, t0, t1):
    """Slab method: the parameter interval of [t0, t1] inside the closed box [lo, hi], or None."""
    for a in range(3):
        if d[a] == 0:
            if o[a] < lo[a] or o[a] > hi[a]:
                return None
            continue
        ta, tb = (lo[a] - o[a]) / d[a], (hi[a] - o[a]) / d[a]
        if ta > tb:
            ta, tb = tb, ta
        t0, t1 = max(t0, ta), min(t1, tb)
        if t0 > t1:
            return None
    return t0, t1


def traverse(o, d, lo, size, dims, t0=0, t1=math.inf):
    """Yield (cell, t_in, t_out) for each grid cell that the segment visits, in order.

    t_in and t_out are the parameters where the segment enters and leaves the cell. Each step
    moves to a face neighbor; ties (two boundaries crossed at the same t) go to the later axis,
    as in the comparisons of the paper.
    """
    hi = tuple(lo[a] + dims[a] * size for a in range(3))
    span = clip_to_box(o, d, lo, hi, t0, t1)  # @line L1
    if span is None:
        return
    t_enter, t_end = span
    cell, step, t_max, t_delta = [0, 0, 0], [0, 0, 0], [math.inf] * 3, [math.inf] * 3
    for a in range(3):
        p = o[a] + t_enter * d[a]
        cell[a] = min(max(math.floor((p - lo[a]) / size), 0), dims[a] - 1)  # @line L2
        if d[a] > 0:  # @line L3
            step[a] = 1
            t_max[a] = (lo[a] + (cell[a] + 1) * size - o[a]) / d[a]
            t_delta[a] = size / d[a]
        elif d[a] < 0:
            step[a] = -1
            t_max[a] = (lo[a] + cell[a] * size - o[a]) / d[a]
            t_delta[a] = -size / d[a]
    t_in = t_enter
    while True:  # @line L4
        if t_max[0] < t_max[1]:  # @line L5
            a = 0 if t_max[0] < t_max[2] else 2
        else:
            a = 1 if t_max[1] < t_max[2] else 2
        t_out = min(t_max[a], t_end)
        yield (cell[0], cell[1], cell[2]), t_in, t_out  # @line L6
        if t_max[a] > t_end:  # @line L7
            return
        cell[a] += step[a]  # @line L8
        if cell[a] < 0 or cell[a] >= dims[a]:  # @line L9
            return
        t_in = t_max[a]
        t_max[a] += t_delta[a]  # @line L10


def cells(o, d, lo, size, dims, t0=0, t1=math.inf):
    """The list of visited cells, in order."""
    return [c for c, _, _ in traverse(o, d, lo, size, dims, t0, t1)]


def box_hit(o, d, box, t0, t1):
    """Entry parameter of the segment into a closed axis-aligned box (lo, hi), or None."""
    span = clip_to_box(o, d, box[0], box[1], t0, t1)
    return None if span is None else span[0]


def build_grid(boxes, lo, size, dims):
    """Put the index of each box into every cell that its closed extent overlaps."""
    grid = {}
    for idx, (blo, bhi) in enumerate(boxes):
        rng = []
        for a in range(3):
            first = max(math.floor((blo[a] - lo[a]) / size), 0)
            last = min(math.floor((bhi[a] - lo[a]) / size), dims[a] - 1)
            rng.append(range(first, last + 1))
        for i in rng[0]:
            for j in rng[1]:
                for k in rng[2]:
                    grid.setdefault((i, j, k), []).append(idx)
    return grid


def grid_first_hit(grid, boxes, o, d, lo, size, dims, t0=0, t1=math.inf, check_cell=True):
    """Closest hit (t, index) of the segment against the boxes, through the grid, or None.

    A hit found in a cell is accepted only if it lies before the exit of that cell; an object
    that spans several cells can be hit beyond the cell while a nearer object waits in the next
    cell. The `tested` set is the mailbox: each object is tested at most once per ray.
    """
    tested = {}
    for cell, t_in, t_out in traverse(o, d, lo, size, dims, t0, t1):
        best = None
        for idx in grid.get(cell, ()):
            if idx not in tested:
                tested[idx] = box_hit(o, d, boxes[idx], t0, t1)
            t = tested[idx]
            if t is not None and (not check_cell or t <= t_out):
                if best is None or (t, idx) < best:
                    best = (t, idx)
        if best is not None:
            return best
    return None
