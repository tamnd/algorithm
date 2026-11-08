# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beneath-beyond/. The authors are listed in prov/TY8J2Y.jsonl.

import random

Point3 = tuple[int, int, int]
Triangle = tuple[int, int, int]


def sub(p: Point3, q: Point3) -> Point3:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def cross(u: Point3, v: Point3) -> Point3:
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def orient3d(a: Point3, b: Point3, c: Point3, d: Point3) -> int:
    """Six times the signed volume of abcd: positive when d is on the side that the normal
    (b - a) x (c - a) points to. Exact for int and Fraction input."""
    n = cross(sub(b, a), sub(c, a))
    w = sub(d, a)
    return n[0] * w[0] + n[1] * w[1] + n[2] * w[2]


def beneath_beyond(points: list[Point3], seed: int = 0) -> list[Triangle]:
    """Randomized incremental 3D convex hull with a conflict graph.

    Returns triangles (i, j, k) of indices into points, counterclockwise as seen from outside.
    They cover the boundary of the hull. Coplanar points may give several triangles in one
    face and vertices that are not extreme. Returns [] when the points do not span 3D space.
    Expected O(n log n) time for points in general position.
    """
    pts = points
    order = list(range(len(pts)))
    random.Random(seed).shuffle(order)  # @line L1
    # @line L2: the first four affinely independent points of the order
    base: list[int] = []
    for i in order:
        if len(base) == 0:
            base.append(i)
        elif len(base) == 1 and pts[i] != pts[base[0]]:
            base.append(i)
        elif len(base) == 2 and cross(sub(pts[base[1]], pts[base[0]]), sub(pts[i], pts[base[0]])) != (0, 0, 0):
            base.append(i)
        elif len(base) == 3 and orient3d(pts[base[0]], pts[base[1]], pts[base[2]], pts[i]) != 0:
            base.append(i)
            break
    if len(base) < 4:
        return []
    facets: dict[int, Triangle] = {}
    edge: dict[tuple[int, int], int] = {}  # directed edge -> facet that has it
    fconf: dict[int, list[int]] = {}  # facet -> points beyond it
    pconf: dict[int, set[int]] = {}  # point -> facets it sees
    next_id = 0

    def add_facet(a: int, b: int, c: int) -> int:
        nonlocal next_id
        f = next_id
        next_id += 1
        facets[f] = (a, b, c)
        edge[(a, b)] = edge[(b, c)] = edge[(c, a)] = f
        fconf[f] = []
        return f

    def beyond(f: int, q: int) -> bool:
        a, b, c = facets[f]
        return orient3d(pts[a], pts[b], pts[c], pts[q]) > 0

    def link(f: int, q: int) -> None:
        fconf[f].append(q)
        pconf.setdefault(q, set()).add(f)

    w, x, y, z = base
    for a, b, c, d in ((w, x, y, z), (w, x, z, y), (w, y, z, x), (x, y, z, w)):  # @line L3
        if orient3d(pts[a], pts[b], pts[c], pts[d]) > 0:
            b, c = c, b
        add_facet(a, b, c)
    rest = [i for i in order if i not in base]
    for q in rest:  # @line L4
        for f in list(facets):
            if beyond(f, q):
                link(f, q)
    for p in rest:  # @line L5
        visible = pconf.pop(p, set())  # @line L6
        if not visible:  # @line L7
            continue
        horizon = []  # @line L8
        for f in visible:
            a, b, c = facets[f]
            for u, v in ((a, b), (b, c), (c, a)):
                g = edge[(v, u)]
                if g not in visible:
                    horizon.append((u, v, f, g))
        new = []
        for u, v, f, g in horizon:  # @line L9
            t = add_facet(u, v, p)  # @line L10
            new.append(t)
            for q in set(fconf[f]) | set(fconf[g]):  # @line L11
                if q != p and beyond(t, q):
                    link(t, q)
        for f in visible:  # @line L12
            a, b, c = facets.pop(f)
            for u, v in ((a, b), (b, c), (c, a)):
                if edge.get((u, v)) == f:
                    del edge[(u, v)]
            for q in fconf.pop(f):
                if q != p:
                    pconf[q].discard(f)
    return list(facets.values())  # @line L13
