# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chvatal-art-gallery-theorem/. The authors are listed in prov/9V33Q8.jsonl.

"""Chvátal's proof of the art gallery theorem, run as an algorithm.

Chvátal proved by induction that every triangulation of a polygon with n
vertices splits into at most floor(n/3) fans. A fan is a set of triangles
that all share one vertex, its center. A guard at the center of a fan sees
every triangle of the fan, because each triangle is convex and has the
guard at a corner. So the fan centers are at most floor(n/3) vertex guards.

The induction step finds a diagonal d that cuts off 4, 5 or 6 polygon
edges (the least number that is at least 4), splits the triangulation at
d, partitions the rest by induction, and handles the small side by the
cases of the proof. This file follows those cases one for one.

The polygon is a list of points in counterclockwise order. All arithmetic
uses Fraction or int, so the tests of the triangulation are exact.
"""

from fractions import Fraction


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ear_clip(poly):
    """Triangulate a simple counterclockwise polygon. Returns index triples."""
    idx = list(range(len(poly)))
    tris = []
    while len(idx) > 3:
        m = len(idx)
        for k in range(m):
            a, b, c = idx[k - 1], idx[k], idx[(k + 1) % m]
            if orient(poly[a], poly[b], poly[c]) <= 0:
                continue
            ok = True
            for j in idx:
                if j in (a, b, c):
                    continue
                p = poly[j]
                if orient(poly[a], poly[b], p) >= 0 and orient(poly[b], poly[c], p) >= 0 \
                        and orient(poly[c], poly[a], p) >= 0:
                    ok = False
                    break
            if ok:
                tris.append((a, b, c))
                idx.pop(k)
                break
        else:
            raise ValueError("no ear found: the polygon is not simple or not counterclockwise")
    tris.append(tuple(idx))
    return tris


def _common_center(cycle, tris, choose):
    common = set(cycle)
    for t in tris:
        common &= t
    return choose(sorted(common, key=cycle.index))


def fan_partition(cycle, tris, trace=None, choose=lambda options: options[0]):
    """Split the triangulation of the polygon cycle into at most floor(len/3) fans.

    cycle: the vertex labels of the polygon in boundary order.
    tris: the triangles, as frozensets of labels. Returns [(center, [triangles])].
    trace: an optional list that gets the name of each case of the proof used.
    choose: picks the center of a small fan when it has more than one choice.
    """

    def note(name):
        if trace is not None:
            trace.append(name)

    n = len(cycle)
    if n <= 5:  # every triangulation with at most 5 vertices is a fan
        return [(_common_center(cycle, tris, choose), list(tris))]
    pos = {v: i for i, v in enumerate(cycle)}
    best = None
    for t in tris:
        for a in t:
            for b in t:
                i, j = pos[a], pos[b]
                if j <= i or j - i in (1, n - 1):
                    continue
                for start, k in ((i, j - i), (j, n - (j - i))):
                    if k >= 4 and (best is None or k < best[1]):
                        best = (start, k)
    start, k = best
    assert 4 <= k <= 6  # Lemma: the least cut that is at least 4 is at most 6
    rot = cycle[start:] + cycle[:start]
    edges = {frozenset((a, b)) for t in tris for a in t for b in t if a != b}

    def apex(r):
        for t in tris:
            if r[0] in t and r[k] in t:
                (x,) = t - {r[0], r[k]}
                p = r.index(x)
                if 0 < p < k:
                    return p
        raise AssertionError("no triangle on the diagonal")

    t = apex(rot)
    if (k == 5 and t == 3) or (k == 6 and frozenset((rot[1], rot[3])) in edges
                               and frozenset((rot[3], rot[5])) not in edges):
        rot = rot[k::-1] + rot[:k:-1]  # the mirror image: reverse the polygon
        t = apex(rot)

    def P(*ps):
        return frozenset(rot[p] for p in ps)

    def has(a, b):
        return P(a, b) in edges

    def inside(cyc):
        s = set(cyc)
        return [tr for tr in tris if tr <= s]

    def rec(cyc):
        return fan_partition(cyc, inside(cyc), trace, choose)

    g1 = rot[:k + 1]
    g2 = rot[k:] + [rot[0]]

    def merge(fans, tri, add, new_tris):
        """Add the triangles add to the fan that holds tri, then add new_tris as one new fan."""
        out = []
        for c, ts in fans:
            if tri in ts:
                ts = ts + add
            out.append((c, ts))
        return out + [(_common_center(rot, new_tris, choose), new_tris)]

    def center_of(fans, tri):
        for c, ts in fans:
            if tri in ts:
                return c
        raise AssertionError("triangle not in any fan")

    if k == 4:  # Case 1: the cut-off part is a pentagon, which is a fan
        note("1")
        return rec(g2) + [(_common_center(g1, inside(g1), choose), inside(g1))]

    if k == 5:  # Case 2: a hexagon, apex t = 2 after the mirror
        assert t == 2
        if has(2, 4):  # Case 2a: the hexagon is a fan centered at 2
            note("2a")
            return rec(g2) + [(rot[2], inside(g1))]
        g0 = g2 + [rot[2]]  # Case 2b: join T = (0, 2, 5) to the rest
        fans = rec(g0)
        T = P(0, 2, 5)
        c = center_of(fans, T)
        if c in (rot[0], rot[2]):  # Case 2b.1
            note("2b.1")
            return merge(fans, T, [P(0, 1, 2)], [P(2, 3, 5), P(3, 4, 5)])
        note("2b.2")
        return merge(fans, T, [P(2, 3, 5), P(3, 4, 5)], [P(0, 1, 2)])  # Case 2b.2

    # Case 3: k = 6, a heptagon, apex t = 3
    assert t == 3
    if has(1, 3) and has(3, 5):  # Case 3a: a fan centered at 3
        note("3a")
        return rec(g2) + [(rot[3], inside(g1))]
    if has(0, 2) and has(3, 5):  # Case 3b (Case 3c is its mirror image)
        g0 = g2 + [rot[2], rot[3]]
        fans = rec(g0)
        tri = P(0, 2, 3)
        c = center_of(fans, tri)
        if c in (rot[0], rot[2]):  # Case 3b.1
            note("3b.1")
            return merge(fans, tri, [P(0, 1, 2)], [P(3, 4, 5), P(3, 5, 6)])
        note("3b.2")
        return merge(fans, tri, [P(3, 4, 5), P(3, 5, 6)], [P(0, 1, 2)])  # Case 3b.2
    # Case 3d: the diagonals (0, 2) and (4, 6)
    assert has(0, 2) and has(4, 6)
    g0 = g2 + [rot[3]]
    fans = rec(g0)
    T = P(0, 3, 6)
    c = center_of(fans, T)
    if c == rot[3]:  # Case 3d.2: the fan is T alone, so it can be centered at 0
        note("3d.2")
        fans = [(rot[0], ts) if T in ts else (cc, ts) for cc, ts in fans]
        c = rot[0]
    if c == rot[0]:  # Case 3d.1
        note("3d.1")
        return merge(fans, T, [P(0, 1, 2), P(0, 2, 3)], [P(3, 4, 6), P(4, 5, 6)])
    note("3d.3")
    return merge(fans, T, [P(3, 4, 6), P(4, 5, 6)], [P(0, 1, 2), P(0, 2, 3)])  # Case 3d.3


def chvatal_guards(poly):
    """At most floor(n/3) vertex guards for a simple polygon, by Chvátal's fans.

    poly: points in counterclockwise order. Returns (guards, fans, triangles),
    where guards are vertex indices and fans are (center, [triangles]).
    """
    poly = [(Fraction(x), Fraction(y)) for x, y in poly]
    tris = [frozenset(t) for t in ear_clip(poly)]
    fans = fan_partition(list(range(len(poly))), tris)
    return sorted({c for c, _ in fans}), fans, tris


if __name__ == "__main__":
    comb = [(0, 0), (9, 0), (9, 1), (8, 3), (7, 1), (6, 1), (5, 3), (4, 1), (3, 1), (2, 3), (1, 1), (0, 1)]
    guards, fans, _ = chvatal_guards(comb)
    print("guards", guards)
    for c, ts in fans:
        print(c, sorted(sorted(t) for t in ts))
