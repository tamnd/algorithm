# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-directional-blocking-graph/. The authors are listed in prov/RMGX71.jsonl.
"""The non-directional blocking graph of a product of axis-aligned boxes.

Motion model: one infinitesimal translation. A set S of parts moves as one
rigid body by e d for a small e > 0, and the other parts stay. Hand model:
two-handed, one hand holds S and the other holds the rest.

The contact normals of boxes are the six axis directions, so their great
circles are the three coordinate planes. They cut the sphere of directions
into 26 cells: 8 open triangles, 12 open arcs and 6 points. A cell is named
by the sign vector of its directions, in {-1, 0, 1}^3 without (0, 0, 0). The
directional blocking graph DBG(s) is the same for all directions of a cell,
and the NDBG is the list of the 26 graphs.

A graph is a list out with one bit mask per part: bit j of out[i] is set
when part j blocks part i, that is, i cannot move along s without j.
"""

from assembly_boxes import members

CELLS = tuple((sx, sy, sz) for sx in (-1, 0, 1) for sy in (-1, 0, 1) for sz in (-1, 0, 1)
              if (sx, sy, sz) != (0, 0, 0))


def cell_of(d):
    """The cell of a nonzero direction vector d: its sign vector."""
    return tuple((x > 0) - (x < 0) for x in d)


def blocked(a, b, s):
    """True if box b blocks a small translation of box a along cell s.

    a + e d meets the open box b for all small e > 0 exactly when, on each
    axis, the open intervals already overlap, or they touch and d moves a
    into b on that axis.
    """
    for k in range(3):
        if a[k] < b[k + 3] and b[k] < a[k + 3]:
            continue
        if a[k + 3] == b[k] and s[k] > 0:
            continue
        if a[k] == b[k + 3] and s[k] < 0:
            continue
        return False
    return True


def build(boxes):
    """The NDBG: a dict from each of the 26 cells to its blocking graph."""
    n = len(boxes)
    ndbg = {}
    for s in CELLS:  # @line L1
        out = [0] * n
        for i in range(n):  # @line L2
            for j in range(n):
                if i != j and blocked(boxes[i], boxes[j], s):  # @line L3
                    out[i] |= 1 << j  # @line L4
        ndbg[s] = out
    return ndbg


def can_move(out, s_mask, within):
    """True if the parts s_mask can move with no part of within \\ s_mask."""
    rest = within & ~s_mask
    return all(out[i] & rest == 0 for i in members(s_mask))  # @line L5


def tarjan_sccs(out, within):
    """The strongly connected components of the graph induced on within,
    as bit masks, in the order Tarjan's algorithm completes them. A component
    is completed after every component that it can reach, so the first one
    has no arc to another component."""
    index, low, on_stack = {}, {}, set()
    stack, comps = [], []
    counter = 0
    for root in members(within):
        if root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        work = [(root, iter(members(out[root] & within)))]
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(members(out[w] & within))))
                    pushed = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = 0
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp |= 1 << w
                    if w == v:
                        break
                comps.append(comp)
    return comps


def removable(out, within):
    """A nonempty proper subset of within that can move, or None."""
    comps = tarjan_sccs(out, within)  # @line L6
    first = comps[0]  # @line L7
    if first == within:  # @line L8
        return None
    return first  # @line L9


def separate(ndbg, within):
    """A cell and a set of parts that can move along it, or None if the
    subassembly within is locked for every small translation."""
    for s in CELLS:  # @line L10
        c = removable(ndbg[s], within)
        if c is not None:
            return s, c
    return None
