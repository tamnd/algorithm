# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newell-newell-sancha-algorithm/. The authors are listed in prov/GJTAMY.jsonl.

"""The Newell-Newell-Sancha depth sort, with polygon splitting.

Screen space: the viewer looks down the z axis from z = +infinity, so a
larger z is nearer. A polygon is a list of at least three vertices
(x, y, z), int or Fraction, of a planar convex polygon whose plane is not
parallel to the z axis. Pixel (i, j) is the point sample at
(i + 1/2, j + 1/2), and it is covered when it lies in the closed
projection of a polygon. All arithmetic is exact.
"""

from fractions import Fraction
from typing import Optional, Sequence, Union

Num = Union[int, Fraction]
Vertex = tuple[Fraction, Fraction, Fraction]


class Fragment:
    """A convex piece of an input polygon, with the plane of that polygon.

    The plane is n . X = d with n_z > 0, so the side n . X > d is the side
    of the viewer.
    """

    __slots__ = ("verts", "orig", "n", "d", "marked")

    def __init__(self, verts: list[Vertex], orig: int, n: tuple[Fraction, Fraction, Fraction], d: Fraction):
        self.verts, self.orig, self.n, self.d, self.marked = verts, orig, n, d, False

    def side(self, v: Vertex) -> Fraction:
        return self.n[0] * v[0] + self.n[1] * v[1] + self.n[2] * v[2] - self.d

    def lo(self, a: int) -> Fraction:
        return min(v[a] for v in self.verts)

    def hi(self, a: int) -> Fraction:
        return max(v[a] for v in self.verts)


def make_fragment(poly: Sequence[Sequence[Num]], orig: int) -> Fragment:
    verts = [(Fraction(x), Fraction(y), Fraction(z)) for x, y, z in poly]
    a, b, c = verts[0], verts[1], verts[2]
    u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    w = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
    if n[2] == 0:
        raise ValueError("a polygon is parallel to the view direction")
    if n[2] < 0:
        n = (-n[0], -n[1], -n[2])
    return Fragment(verts, orig, n, n[0] * a[0] + n[1] * a[1] + n[2] * a[2])


def common_projection(p: Fragment, q: Fragment) -> list[tuple[Fraction, Fraction]]:
    """The vertices of the closed intersection of the two projections.

    Clip the projection of p by each closed edge half-plane of q (the
    Sutherland-Hodgman step). The list is empty when the projections do not
    meet; it can hold one point or the two ends of a segment.
    """
    region = [(v[0], v[1]) for v in p.verts]
    qv = [(v[0], v[1]) for v in q.verts]
    k = len(qv)
    area2 = sum(qv[i][0] * qv[(i + 1) % k][1] - qv[(i + 1) % k][0] * qv[i][1] for i in range(k))
    sign = 1 if area2 > 0 else -1
    for i in range(k):
        (ax, ay), (bx, by) = qv[i], qv[(i + 1) % k]
        def s(pt: tuple[Fraction, Fraction]) -> Fraction:
            return sign * ((bx - ax) * (pt[1] - ay) - (by - ay) * (pt[0] - ax))
        out: list[tuple[Fraction, Fraction]] = []
        m = len(region)
        for j in range(m):
            u, w = region[j], region[(j + 1) % m]
            su, sw = s(u), s(w)
            if su >= 0:
                out.append(u)
            if (su > 0 and sw < 0) or (su < 0 and sw > 0):
                t = su / (su - sw)
                out.append((u[0] + t * (w[0] - u[0]), u[1] + t * (w[1] - u[1])))
        region = out
        if not region:
            break
    return region


def depth(f: Fragment, x: Fraction, y: Fraction) -> Fraction:
    return (f.d - f.n[0] * x - f.n[1] * y) / f.n[2]


def may_obscure(p: Fragment, q: Fragment) -> bool:
    """True when the tests T0 to T6 all fail, so p is in front of q somewhere."""
    if q.lo(2) >= p.hi(2):  # T0: q is wholly nearer in depth
        return False
    if p.hi(0) < q.lo(0) or q.hi(0) < p.lo(0):  # T1: x extents
        return False
    if p.hi(1) < q.lo(1) or q.hi(1) < p.lo(1):  # T2: y extents
        return False
    if all(q.side(v) <= 0 for v in p.verts):  # T3: p behind the plane of q
        return False
    if all(p.side(v) >= 0 for v in q.verts):  # T4: q in front of the plane of p
        return False
    region = common_projection(p, q)
    if not region:  # T5: the projections do not meet
        return False
    # T6: the depth difference is affine, so its maximum on the convex region is at a vertex.
    return any(depth(p, x, y) > depth(q, x, y) for x, y in region)


def straddles(r: Fragment, plane: Fragment) -> bool:
    s = [plane.side(v) for v in r.verts]
    return any(x > 0 for x in s) and any(x < 0 for x in s)


def split(r: Fragment, plane: Fragment) -> list[Fragment]:
    """Cut r by the plane of `plane` into its front and back pieces."""
    front: list[Vertex] = []
    back: list[Vertex] = []
    k = len(r.verts)
    for i in range(k):
        a, b = r.verts[i], r.verts[(i + 1) % k]
        sa, sb = plane.side(a), plane.side(b)
        if sa >= 0:
            front.append(a)
        if sa <= 0:
            back.append(a)
        if (sa > 0 and sb < 0) or (sa < 0 and sb > 0):
            t = sa / (sa - sb)
            m = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2]))
            front.append(m)
            back.append(m)
    return [Fragment(front, r.orig, r.n, r.d), Fragment(back, r.orig, r.n, r.d)]


def covers(verts: Sequence[Vertex], x: Fraction, y: Fraction) -> bool:
    pos = neg = False
    k = len(verts)
    for i in range(k):
        ax, ay = verts[i][0], verts[i][1]
        bx, by = verts[(i + 1) % k][0], verts[(i + 1) % k][1]
        c = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        pos, neg = pos or c > 0, neg or c < 0
    return not (pos and neg)


def find_straddle(lst: list[Fragment]) -> Optional[tuple[int, Fragment]]:
    for i, r in enumerate(lst):
        for s in lst:
            if s is not r and straddles(r, s):
                return i, s
    return None


def newell_newell_sancha(polygons: Sequence[Sequence[Sequence[Num]]], width: int, height: int,
                         background: int = -1) -> tuple[list[tuple[int, list[Vertex]]], list[list[int]]]:
    """Return (order, image).

    `order` lists the fragments, as (index of the input polygon, vertices),
    in an order where no fragment hides a part of a later one. `image[j][i]`
    is the index of the polygon painted last at pixel (i, j). At each pixel
    where one polygon is strictly nearest, that polygon is the result.

    Cost: each step tests the front fragment against up to m - 1 others,
    for m fragments in the list; m is O(n^3) in the worst case for n input
    polygons. On scenes with few depth overlaps the cost is near the
    O(n log n) of the sort.
    """
    lst = sorted((make_fragment(p, k) for k, p in enumerate(polygons)), key=lambda f: f.lo(2))  # @line L1
    out: list[Fragment] = []
    while lst:  # @line L2
        p = lst[0]  # @line L3
        q = next((r for r in lst[1:] if may_obscure(p, r)), None)  # @line L4
        if q is None:  # @line L5
            out.append(lst.pop(0))
            continue
        swap_ok = all(p.side(v) <= 0 for v in q.verts) or all(q.side(v) >= 0 for v in p.verts)
        if swap_ok and not q.marked:  # @line L6
            q.marked = True
            lst.remove(q)
            lst.insert(0, q)
            continue
        if straddles(q, p):  # @line L7
            i = lst.index(q)
            lst[i:i + 1] = split(q, p)
        elif straddles(p, q):  # @line L8
            lst[0:1] = split(p, q)
        else:  # @line L9
            # A cycle of fragments that do not cross the plane of each other
            # cannot exist, so some fragment crosses the plane of another.
            found = find_straddle(lst)
            assert found is not None
            i, s = found
            lst[i:i + 1] = split(lst[i], s)
        for r in lst:  # @line L10
            r.marked = False
    image = [[background] * width for _ in range(height)]
    for f in out:  # @line L11
        for j in range(height):
            for i in range(width):
                if covers(f.verts, Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2)):
                    image[j][i] = f.orig
    return [(f.orig, f.verts) for f in out], image
