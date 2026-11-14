# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-naming-scheme/. The authors are listed in prov/5S5Z62.jsonl.

"""Generic names for the edges and vertices of a toy planar modeler.

The modeler builds a part from a history: a base rectangle, then a list of
cut operations, each one rectangle or a pattern of several rectangles. The
part is the base minus the open cuts, and its
boundary is a set of cycles of axis-parallel edges, with the material on the
left. Every edge lies on one side of one rectangle of the history, and that
(operation, side) pair is its generative label. A cut can split a side into
several edges with the same label, and the copies of a pattern share their
labels, so the label alone is not a name.

The naming step follows Capoyleas, Chen and Hoffmann: the name of an entity
is the operation and the generator that made it, extended by the names of
its neighbours until it is unique. Here the neighbours are the edges before
and after it on its boundary cycle. The window of radius r of an edge is the
tuple of the labels of the 2r + 1 edges centred on it; once the window wraps
around the cycle, the cycle length is added. The level of an edge is the
least r at which its window is unique in the model, or the largest cycle
length if no window is unique. A vertex is named by the names of its two
edges.

Resolution computes the windows of the new model at the stored level and
returns every entity with an equal window. If the new model has the same
labelled boundary as the old one, up to the choice of the start of each
cycle and the order of the cycles, the result is exactly the set of images
of the entity under all label-preserving isomorphisms: one entity when the
name was unique, and all the symmetric candidates otherwise.

Precondition: the coordinates of all rectangles are integers, two x-sides
or two y-sides share a coordinate only if they are the same side of copies
in one pattern, and the copies of a pattern do not overlap.
Cost: for c cut rectangles the part has O(c^2) grid cells, built in O(c^3)
time, and the boundary has n = O(c^2) edges. Naming takes O(n L^2) time for
the largest cycle length L <= n, since level r costs O(n r), and resolving
one name takes O(n L).
"""

from __future__ import annotations

from typing import Sequence

Label = tuple[str, str]
Rect = tuple[int, int, int, int]          # x0, y0, x1, y1


class Part:
    """The boundary of base minus cuts, as cycles of labelled edges."""

    def __init__(self, base: Rect, ops: Sequence):
        """ops[k] is one rectangle, or a list of rectangles cut by one
        pattern operation, which all get the label of operation k + 1."""
        rects = [("base", base)]
        for k, op in enumerate(ops):
            for r in ([op] if isinstance(op[0], int) else op):
                rects.append(("cut%d" % (k + 1), tuple(r)))
        cuts = [r for name, r in rects[1:]]
        owner_x: dict[int, Label] = {}
        owner_y: dict[int, Label] = {}
        for name, (x0, y0, x1, y1) in rects:
            assert x0 < x1 and y0 < y1
            for v, side, own in ((x0, "left", owner_x), (x1, "right", owner_x),
                                 (y0, "bottom", owner_y), (y1, "top", owner_y)):
                assert own.get(v, (name, side)) == (name, side), "coordinates must be distinct"
                own[v] = (name, side)
        xs, ys = sorted(owner_x), sorted(owner_y)
        self.xs, self.ys = xs, ys

        def inside(i, j):
            if not (0 <= i < len(xs) - 1 and 0 <= j < len(ys) - 1):
                return False
            cx, cy = xs[i] + xs[i + 1], ys[j] + ys[j + 1]   # twice the centre
            x0, y0, x1, y1 = base
            if not (2 * x0 < cx < 2 * x1 and 2 * y0 < cy < 2 * y1):
                return False
            return not any(2 * a < cx < 2 * c and 2 * b < cy < 2 * d for a, b, c, d in cuts)

        self.cells = {(i, j) for i in range(len(xs) - 1) for j in range(len(ys) - 1) if inside(i, j)}
        # unit boundary segments between grid nodes, directed with material on the left
        succ: dict[tuple[int, int], list[tuple[int, int]]] = {}
        seg_label: dict[tuple, Label] = {}

        def add(a, b, lab):
            succ.setdefault(a, []).append(b)
            seg_label[(a, b)] = lab

        for i in range(len(xs)):
            for j in range(len(ys) - 1):
                left, right = inside(i - 1, j), inside(i, j)
                if left and not right:
                    add((i, j), (i, j + 1), owner_x[xs[i]])
                elif right and not left:
                    add((i, j + 1), (i, j), owner_x[xs[i]])
        for i in range(len(xs) - 1):
            for j in range(len(ys)):
                below, above = inside(i, j - 1), inside(i, j)
                if above and not below:
                    add((i, j), (i + 1, j), owner_y[ys[j]])
                elif below and not above:
                    add((i + 1, j), (i, j), owner_y[ys[j]])

        def turn_rank(d_in, d_out):
            # prefer the left turn, then straight, then right: it keeps the
            # boundary of each cell at a pinch vertex in its own cycle
            cr = d_in[0] * d_out[1] - d_in[1] * d_out[0]
            return -cr if cr else 0

        used: set[tuple] = set()
        self.cycles: list[list[Label]] = []        # labels of the edges, in order
        self.edge_geom: list[list[tuple]] = []      # (start node, end node) of each edge
        for a0 in sorted(succ):
            for b0 in sorted(succ[a0]):
                if (a0, b0) in used:
                    continue
                segs = []
                a, b = a0, b0
                while (a, b) not in used:
                    used.add((a, b))
                    segs.append((a, b))
                    d_in = (b[0] - a[0], b[1] - a[1])
                    c = min(succ[b], key=lambda c: turn_rank(d_in, (c[0] - b[0], c[1] - b[1])))
                    a, b = b, c
                # merge runs of segments with one direction and one label into edges
                def key(s):
                    return (s[1][0] - s[0][0], s[1][1] - s[0][1], seg_label[s])
                k = 0
                while key(segs[k - 1]) == key(segs[k]):
                    k += 1
                segs = segs[k:] + segs[:k]
                labels, geom = [], []
                for s in segs:
                    if labels and key(s) == key(prev):
                        geom[-1] = (geom[-1][0], s[1])
                    else:
                        labels.append(seg_label[s])
                        geom.append(s)
                    prev = s
                self.cycles.append(labels)
                self.edge_geom.append(geom)
        self.edges = [(c, i) for c in range(len(self.cycles)) for i in range(len(self.cycles[c]))]

    def area(self) -> int:
        """The area enclosed by the cycles, by the shoelace formula."""
        tot = 0
        for geom in self.edge_geom:
            for (a, b) in geom:
                ax, ay, bx, by = self.xs[a[0]], self.ys[a[1]], self.xs[b[0]], self.ys[b[1]]
                tot += ax * by - bx * ay
        return tot // 2

    def label(self, e) -> Label:
        return self.cycles[e[0]][e[1]]

    def vertices(self):
        """A vertex is the pair (edge before it, edge after it) on a cycle."""
        return [((c, i - 1 if i else len(cyc) - 1), (c, i))
                for c, cyc in enumerate(self.cycles) for i in range(len(cyc))]

    def window(self, e, r: int):
        c, i = e
        cyc = self.cycles[c]
        L = len(cyc)
        return (L if 2 * r + 1 > L else 0, tuple(cyc[(i + d) % L] for d in range(-r, r + 1)))


def name_edges(part: Part) -> dict:
    """The generic name (level, window) of every edge."""
    top = max((len(c) for c in part.cycles), default=0)
    level = {}
    pending = set(part.edges)
    r = 0
    while pending and r <= top:  # @line L1
        count: dict = {}
        for e in part.edges:  # @line L2
            w = part.window(e, r)
            count[w] = count.get(w, 0) + 1
        for e in list(pending):  # @line L3
            if count[part.window(e, r)] == 1 or r == top:  # @line L4
                level[e] = r
                pending.discard(e)
        r += 1
    return {e: (level[e], part.window(e, level[e])) for e in part.edges}  # @line L5


def resolve_edge(name, part: Part) -> set:
    """All edges of part with the given name."""
    r, w = name
    return {e for e in part.edges if part.window(e, r) == w}  # @line L6


def name_vertices(part: Part, edge_names: dict) -> dict:
    return {v: (edge_names[v[0]], edge_names[v[1]]) for v in part.vertices()}  # @line L7


def resolve_vertex(name, part: Part) -> set:
    a, b = resolve_edge(name[0], part), resolve_edge(name[1], part)
    return {v for v in part.vertices() if v[0] in a and v[1] in b}  # @line L8
