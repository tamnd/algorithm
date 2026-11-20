# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newest-vertex-bisection/. The authors are listed in prov/GGH2BB.jsonl.

"""Newest vertex bisection (NVB) of a conforming triangulation in 2D.

A mesh is (coords, elements, boundary). coords is a list of (x, y) points.
An element [z1, z2, z3] has the refinement edge z1 z2 and the newest vertex
z3, the vertex opposite the refinement edge. boundary is a list of boundary
edges [a, b]; they are split together with the elements, so that boundary
conditions can follow the refinement.

refine marks the refinement edges of the marked elements, closes the set of
marked edges (a marked edge of an element forces its refinement edge), and
then bisects each element one, two or three times. The result is the
smallest conforming NVB refinement in which every marked element is
bisected at least once. Cost: O(M) for M elements with a hash map
(real-RAM, expected time of the hash map).
"""


def _edge(a, b):
    return (a, b) if a < b else (b, a)


def refine(coords, elements, boundary, marked):
    """Return the refined mesh (coords, elements, boundary)."""
    coords = list(coords)
    touching = {}
    for t, z in enumerate(elements):
        for r in range(3):
            touching.setdefault(_edge(z[r], z[(r + 1) % 3]), []).append(t)
    split = {}
    stack = []
    for t in marked:  # @line L1
        e = _edge(elements[t][0], elements[t][1])
        if e not in split:
            split[e] = None
            stack.append(e)
    while stack:  # closure over a work list  # @line L2
        e = stack.pop()
        for t in touching[e]:  # @line L3
            z = elements[t]
            r = _edge(z[0], z[1])
            if r not in split:  # @line L4
                split[r] = None
                stack.append(r)
    for e in split:  # @line L5
        (xa, ya), (xb, yb) = coords[e[0]], coords[e[1]]
        split[e] = len(coords)
        coords.append(((xa + xb) / 2, (ya + yb) / 2))
    new = []
    for z1, z2, z3 in elements:  # @line L6
        m = split.get(_edge(z1, z2))
        if m is None:
            new.append([z1, z2, z3])
            continue
        left = split.get(_edge(z3, z1))  # @line L7
        right = split.get(_edge(z2, z3))
        if left is None:
            new.append([z3, z1, m])
        else:
            new.extend([[m, z3, left], [z1, m, left]])  # @line L8
        if right is None:
            new.append([z2, z3, m])
        else:
            new.extend([[m, z2, right], [z3, m, right]])  # @line L9
    bnew = []
    for a, b in boundary:
        m = split.get(_edge(a, b))
        if m is None:
            bnew.append([a, b])
        else:
            bnew.extend([[a, m], [m, b]])
    return coords, new, bnew  # @line L10


def refine_by_hanging_nodes(coords, elements, boundary, marked):
    """Second method, used as an oracle: bisect the marked elements once, then
    bisect any element that has a hanging node on an edge until none is left.
    Cost O(M^2) in the worst case.
    """
    coords = list(coords)
    where = {p: i for i, p in enumerate(coords)}

    def midpoint(a, b):
        (xa, ya), (xb, yb) = coords[a], coords[b]
        p = ((xa + xb) / 2, (ya + yb) / 2)
        if p not in where:
            where[p] = len(coords)
            coords.append(p)
        return where[p]

    def bisect(z):
        m = midpoint(z[0], z[1])
        return [[z[2], z[0], m], [z[1], z[2], m]]

    marked = set(marked)
    elements = [c for t, z in enumerate(elements) for c in (bisect(z) if t in marked else [z])]
    while True:
        out, changed = [], False
        for z in elements:
            hanging = False
            for r in range(3):
                (xa, ya), (xb, yb) = coords[z[r]], coords[z[(r + 1) % 3]]
                if ((xa + xb) / 2, (ya + yb) / 2) in where:
                    hanging = True
            if hanging:
                out.extend(bisect(z))
                changed = True
            else:
                out.append(z)
        elements = out
        if not changed:
            break
    bnew = []
    work = [list(e) for e in boundary]
    while work:
        a, b = work.pop()
        (xa, ya), (xb, yb) = coords[a], coords[b]
        p = ((xa + xb) / 2, (ya + yb) / 2)
        if p in where:
            work.extend([[a, where[p]], [where[p], b]])
        else:
            bnew.append([a, b])
    return coords, elements, bnew


def hanging_nodes(coords, elements):
    """Return the list of (element, edge) pairs whose edge midpoint is a mesh vertex."""
    used = {coords[v] for z in elements for v in z}
    bad = []
    for t, z in enumerate(elements):
        for r in range(3):
            (xa, ya), (xb, yb) = coords[z[r]], coords[z[(r + 1) % 3]]
            if ((xa + xb) / 2, (ya + yb) / 2) in used:
                bad.append((t, r))
    return bad


def is_conforming(coords, elements, boundary):
    """Check that every edge lies in two elements or is a boundary edge, and that no node hangs."""
    count = {}
    for z in elements:
        for r in range(3):
            e = _edge(z[r], z[(r + 1) % 3])
            count[e] = count.get(e, 0) + 1
    bset = {_edge(a, b) for a, b in boundary}
    for e, c in count.items():
        if c > 2 or (c == 1 and e not in bset):
            return False
    return all(count.get(e) == 1 for e in bset) and not hanging_nodes(coords, elements)


def area(coords, z):
    """Return the signed area of the element z."""
    (x0, y0), (x1, y1), (x2, y2) = coords[z[0]], coords[z[1]], coords[z[2]]
    return ((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)) / 2


def shape_key(coords, z, digits=9):
    """Return a key that is equal for similar triangles: sorted squared side ratios."""
    p = [coords[v] for v in z]
    s = sorted((p[r][0] - p[(r + 1) % 3][0]) ** 2 + (p[r][1] - p[(r + 1) % 3][1]) ** 2 for r in range(3))
    return (round(s[0] / s[2], digits), round(s[1] / s[2], digits))
