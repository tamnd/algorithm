# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree-mesh-generation/. The authors are listed in prov/YMYTYF.jsonl.

"""Octree tetrahedral meshing of a ball in the style of Yerry and Shephard.

The root cube is [0, S]^3 with S = 2^(depth + 1), so every box corner, box
center and quarter face center has integer coordinates. A box is a 4-tuple
(k, i, j, l): level k, side w = S / 2^k, lower corner (i, j, l) w.

The domain is the open ball |x - center|^2 < r2, with rational center and r2.
The steps are:

1. refine every leaf that meets the sphere until it reaches level depth;
2. balance the tree: leaves that share a face or an edge differ by at most
   one level;
3. fill every leaf with tetrahedra: one new point at the center of the leaf,
   joined to a fan of triangles on every square of its boundary;
4. cut the tetrahedra by the linear interpolation of
   f(x) = r2 - |x - center|^2 and keep the parts where f > 0.

All arithmetic is exact (int and Fraction). Step 3 gives a conforming mesh of
the root cube whose tetrahedra come from a finite list of shapes. Step 4 cuts
the cells at the boundary and gives no shape guarantee, as in the original
method.
"""

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg2geom import orient3d

Box = Tuple[int, int, int, int]
FACE_DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
EDGE_DIRS = [
    d
    for a in (1, -1)
    for b in (1, -1)
    for d in ((a, b, 0), (a, 0, b), (0, a, b))
]


class Octree:
    def __init__(self, depth: int):
        if depth < 1:
            raise ValueError("depth must be at least 1")
        self.depth = depth
        self.side = 1 << (depth + 1)
        self.leaves = {(0, 0, 0, 0)}
        self.internal = set()

    def width(self, k: int) -> int:
        return self.side >> k

    def lower(self, b: Box) -> tuple:
        w = self.width(b[0])
        return (b[1] * w, b[2] * w, b[3] * w)

    def split(self, b: Box) -> None:
        k, i, j, l = b
        self.leaves.remove(b)
        self.internal.add(b)
        for a in (0, 1):
            for c in (0, 1):
                for e in (0, 1):
                    self.leaves.add((k + 1, 2 * i + a, 2 * j + c, 2 * l + e))

    def unbalanced(self, b: Box) -> bool:
        """True if a leaf that shares a face or an edge with b is two or more levels finer."""
        k, i, j, l = b
        for d in FACE_DIRS + EDGE_DIRS:
            nb = (k, i + d[0], j + d[1], l + d[2])
            if nb not in self.internal:
                continue
            # children of nb that touch b: fixed along the axes of d, free along the others
            choices = [(0,) if x == 1 else (1,) if x == -1 else (0, 1) for x in d]
            for a in choices[0]:
                for c in choices[1]:
                    for e in choices[2]:
                        if (k + 1, 2 * nb[1] + a, 2 * nb[2] + c, 2 * nb[3] + e) in self.internal:
                            return True
        return False

    def corners(self) -> set:
        out = set()
        for b in self.leaves:
            w = self.width(b[0])
            x, y, z = self.lower(b)
            for a in (0, w):
                for c in (0, w):
                    for e in (0, w):
                        out.add((x + a, y + c, z + e))
        return out


def meets_sphere(lo: tuple, w: int, center: tuple, r2) -> bool:
    """True if the sphere |x - center|^2 = r2 meets the closed box lo + [0, w]^3."""
    near = far = 0
    for x0, c in zip(lo, center):
        x1 = x0 + w
        dn = c - x0 if c < x0 else (c - x1 if c > x1 else 0)
        df = max(abs(c - x0), abs(c - x1))
        near += dn * dn
        far += df * df
    return near <= r2 <= far


def build_tree(center: tuple, r2, depth: int) -> Octree:
    t = Octree(depth)  # @line L1
    while True:  # @line L2
        todo = [b for b in sorted(t.leaves) if b[0] < depth and meets_sphere(t.lower(b), t.width(b[0]), center, r2)]
        if not todo:
            break
        for b in todo:
            t.split(b)  # @line L3
    while True:  # @line L4
        bad = [b for b in sorted(t.leaves) if t.unbalanced(b)]
        if not bad:
            break
        for b in bad:
            if b in t.leaves:
                t.split(b)  # @line L5
    return t


def boundary_squares(t: Octree, b: Box):
    """The squares that make up the boundary of leaf b, as (axis, plane, u0, v0, side).

    A face of b is one square, or four if the box of the same size across it is split.
    """
    k = b[0]
    w = t.width(k)
    lo = t.lower(b)
    out = []
    for d in FACE_DIRS:
        axis = next(a for a in range(3) if d[a])
        plane = lo[axis] + (w if d[axis] == 1 else 0)
        u, v = (axis + 1) % 3, (axis + 2) % 3
        nb = (k, b[1] + d[0], b[2] + d[1], b[3] + d[2])
        if nb in t.internal:
            h = w // 2
            for a in (0, h):
                for c in (0, h):
                    out.append((axis, plane, lo[u] + a, lo[v] + c, h))
        else:
            out.append((axis, plane, lo[u], lo[v], w))
    return out


def point(axis: int, plane, a, c) -> tuple:
    p = [0, 0, 0]
    p[axis] = plane
    p[(axis + 1) % 3] = a
    p[(axis + 2) % 3] = c
    return tuple(p)


def positive(tet: Sequence[int], verts: List[tuple]) -> tuple:
    a, b, c, d = tet
    o = orient3d(verts[a], verts[b], verts[c], verts[d])
    if o == 0:
        raise AssertionError("flat tetrahedron")
    return (a, b, c, d) if o > 0 else (b, a, c, d)


class Mesh:
    def __init__(self):
        self.verts: List[tuple] = []
        self.index: Dict[tuple, int] = {}

    def vid(self, p: tuple) -> int:
        if p not in self.index:
            self.index[p] = len(self.verts)
            self.verts.append(p)
        return self.index[p]


def fill_leaves(t: Octree) -> Tuple[List[tuple], List[tuple]]:
    """Template tetrahedra of every leaf. Returns (vertices, positively oriented tetrahedra)."""
    corners = t.corners()
    m = Mesh()
    tets = []
    for b in sorted(t.leaves):  # @line L6
        w = t.width(b[0])
        lo = t.lower(b)
        cc = m.vid(tuple(x + w // 2 for x in lo))  # @line L7
        for axis, plane, u0, v0, h in boundary_squares(t, b):  # @line L8
            q = h // 2
            ring = []
            for (a, c), (a2, c2) in zip(
                [(u0, v0), (u0 + h, v0), (u0 + h, v0 + h), (u0, v0 + h)],
                [(u0 + h, v0), (u0 + h, v0 + h), (u0, v0 + h), (u0, v0)],
            ):
                ring.append(point(axis, plane, a, c))
                mid = point(axis, plane, (a + a2) // 2, (c + c2) // 2)
                if mid in corners:  # a hanging vertex of a finer neighbor
                    ring.append(mid)
            sc = m.vid(point(axis, plane, u0 + q, v0 + q))  # @line L9
            ids = [m.vid(p) for p in ring]
            for s in range(len(ids)):
                tets.append(positive((cc, sc, ids[s], ids[(s + 1) % len(ids)]), m.verts))  # @line L10
    return m.verts, tets


def split_prism(bottom: Sequence[int], top: Sequence[int], key) -> List[tuple]:
    """Cut a prism into three tetrahedra.

    bottom[i] and top[i] are joined by an edge. Each quadrilateral side gets the
    diagonal through its smallest vertex in the order key, so two prisms that
    share a quadrilateral cut it the same way. The smallest of the six vertices
    is the end of two diagonals; it sees the opposite triangle as one
    tetrahedron, and the remaining pyramid is cut by the third diagonal.
    """
    quads = [(bottom[i], bottom[(i + 1) % 3], top[(i + 1) % 3], top[i]) for i in range(3)]
    diag = []
    for q in quads:
        m = min(q, key=key)
        diag.append(frozenset((q[0], q[2])) if m in (q[0], q[2]) else frozenset((q[1], q[3])))
    v = min(list(bottom) + list(top), key=key)
    if v in top:
        bottom, top = top, bottom
        quads = [(q[3], q[2], q[1], q[0]) for q in quads]
    i = list(bottom).index(v)
    far = (i + 1) % 3  # the quad that does not contain v
    out = [(v, top[0], top[1], top[2])]
    q = quads[far]
    a, b, c, d = q  # bottom[far], bottom[far + 1], top[far + 1], top[far]
    if diag[far] == frozenset((a, c)):
        out += [(v, a, b, c), (v, a, c, d)]
    else:
        out += [(v, a, b, d), (v, b, c, d)]
    return out


def ball_values(verts: List[tuple], center: tuple, r2) -> List[Fraction]:
    """f(x) = r2 - |x - center|^2 at every vertex: positive inside the ball."""
    return [Fraction(r2) - sum((x - c) ** 2 for x, c in zip(p, center)) for p in verts]


def cut_by_sign(verts: List[tuple], tets: List[tuple], f: Sequence[Fraction]):
    """Keep the part of each tetrahedron where the linear interpolant of the values f is positive.

    Returns (vertices, tetrahedra) of the kept part. Calling it with -f gives
    the other part, cut along the same triangles.
    """
    if any(v == 0 for v in f):
        raise ValueError("the surface passes through a mesh vertex")
    m = Mesh()
    for p in verts:
        m.vid(p)
    cuts: Dict[tuple, int] = {}

    def cut(a: int, b: int) -> int:
        e = (a, b) if a < b else (b, a)
        if e not in cuts:
            pa, pb = verts[e[0]], verts[e[1]]
            s = f[e[0]] / (f[e[0]] - f[e[1]])
            cuts[e] = m.vid(tuple(x + s * (y - x) for x, y in zip(pa, pb)))
        return cuts[e]

    key = lambda i: m.verts[i]  # noqa: E731  (a total order shared by all prisms)
    out = []
    for tet in tets:  # @line L12
        pos = [v for v in tet if f[v] > 0]
        neg = [v for v in tet if f[v] < 0]
        if len(pos) == 4:  # @line L13
            pieces = [tet]
        elif len(pos) == 0:
            pieces = []
        elif len(pos) == 1:  # @line L14
            a = pos[0]
            pieces = [(a, cut(a, neg[0]), cut(a, neg[1]), cut(a, neg[2]))]
        elif len(pos) == 2:  # @line L15
            (a, b), (c, d) = pos, neg
            pieces = split_prism((a, cut(a, c), cut(a, d)), (b, cut(b, c), cut(b, d)), key)
        else:  # @line L16
            d = neg[0]
            pieces = split_prism(tuple(pos), tuple(cut(p, d) for p in pos), key)
        out.extend(positive(p, m.verts) for p in pieces)
    keep = sorted({v for tet in out for v in tet})
    new = {v: i for i, v in enumerate(keep)}
    return [m.verts[v] for v in keep], [tuple(new[v] for v in tet) for tet in out]


def octree_mesh(center: Sequence, r2, depth: int):
    """Mesh the ball |x - center|^2 < r2 inside the root cube [0, 2^(depth+1)]^3.

    Returns (tree, vertices, tetrahedra). Tetrahedra are positively oriented
    4-tuples of vertex indices.
    """
    center = tuple(Fraction(c) for c in center)
    r2 = Fraction(r2)
    t = Octree(depth)
    if r2 <= 0 or not all(0 < c < t.side and c * c > r2 and (t.side - c) ** 2 > r2 for c in center):
        raise ValueError("the ball must lie strictly inside the root cube")
    t = build_tree(center, r2, depth)
    verts, tets = fill_leaves(t)
    f = ball_values(verts, center, r2)  # @line L11
    verts, tets = cut_by_sign(verts, tets, f)
    return t, verts, tets  # @line L17
