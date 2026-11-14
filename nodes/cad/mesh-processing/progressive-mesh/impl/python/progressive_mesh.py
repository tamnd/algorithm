# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/progressive-mesh/. The authors are listed in prov/WJ1E5T.jsonl.

"""A progressive mesh (after Hoppe 1996): a base mesh and a list of vertex splits.

The mesh keeps stable ids: pos maps a vertex id to its position, faces maps a
face id to an oriented triangle (right-hand rule), and star maps a vertex id
to the ids of its faces. An edge collapse ecol(vs, vt, p) removes the faces
fl = (vs, vt, vl) and fr = (vt, vs, vr) (one of them may be missing on the
boundary), renames vt to vs in the other faces of vt, and moves vs to p. It
returns the record of the vertex split that undoes it: the ids vs, vt, vl, vr,
the old positions of vs and vt, and the ids and corners of fl and fr. The
split does not store which faces go back to vt: they are the faces around vs
counterclockwise from the edge to vr up to the edge to vl.
"""

from collections import namedtuple
from fractions import Fraction

OMEGA = -1  # the extra vertex that closes the boundary in the link condition

VSplit = namedtuple("VSplit", "vs vt vl vr ps pt fl fr")


class Mesh:
    def __init__(self, vertices, faces):
        self.pos = {v: tuple(p) for v, p in enumerate(vertices)}
        self.faces = {f: tuple(t) for f, t in enumerate(faces)}
        self.star = {v: set() for v in self.pos}
        for f, t in self.faces.items():
            if len(set(t)) != 3:
                raise ValueError("face %r repeats a vertex" % (f,))
            for v in t:
                self.star[v].add(f)

    def copy(self):
        m = Mesh([], [])
        m.pos = dict(self.pos)
        m.faces = dict(self.faces)
        m.star = {v: set(s) for v, s in self.star.items()}
        return m

    def state(self):
        """Everything that defines the mesh, for exact comparisons."""
        return dict(self.pos), dict(self.faces)


def rotate(tri, v):
    """The triangle tri as (v, a, b), keeping its orientation."""
    k = tri.index(v)
    return tri[k], tri[(k + 1) % 3], tri[(k + 2) % 3]


def fan(mesh, v):
    """Around v counterclockwise: a -> (b, face id) for each face (v, a, b)."""
    out = {}
    for f in mesh.star[v]:
        _, a, b = rotate(mesh.faces[f], v)
        out[a] = (b, f)
    return out


def edge_faces(mesh, vs, vt):
    """((id, vl) of the face with the directed edge vs -> vt, (id, vr) of the face with vt -> vs); None if absent."""
    fl = fr = None
    for f in mesh.star[vs] & mesh.star[vt]:
        v, a, b = rotate(mesh.faces[f], vs)
        if a == vt:
            fl = (f, b)
        else:
            fr = (f, a)
    return fl, fr


def link(mesh, v):
    """The vertices and edges of the link of v, after closing the boundary with OMEGA."""
    nxt = fan(mesh, v)
    verts, edges = set(), set()
    for a, (b, _) in nxt.items():
        verts |= {a, b}
        edges.add(frozenset((a, b)))
    ends = {b for b, _ in nxt.values()}
    for a in nxt:
        if a not in ends:  # the edge v -> a has no face on its other side
            verts.add(OMEGA)
            edges.add(frozenset((a, OMEGA)))
    for b in ends:
        if b not in nxt:  # the edge b -> v has no face on its other side
            verts.add(OMEGA)
            edges.add(frozenset((b, OMEGA)))
    return verts, edges


def link_condition(mesh, vs, vt):
    """True if Lk(vs) and Lk(vt) meet exactly in Lk(vs vt): the collapse keeps the surface a manifold."""
    fl, fr = edge_faces(mesh, vs, vt)
    if fl is None and fr is None:
        return False
    lk_e = {x[1] for x in (fl, fr) if x is not None}
    if fl is None or fr is None:
        lk_e.add(OMEGA)
    vs_verts, vs_edges = link(mesh, vs)  # @line L12
    vt_verts, vt_edges = link(mesh, vt)
    return (vs_verts & vt_verts) == lk_e and not (vs_edges & vt_edges)  # @line L13


def ecol(mesh, vs, vt, p):
    """Collapse the edge vs vt into vs at position p, and return the vertex split that undoes it."""
    fl, fr = edge_faces(mesh, vs, vt)  # @line L1
    vl = fl[1] if fl else None
    vr = fr[1] if fr else None
    if vl == vr or not link_condition(mesh, vs, vt):  # @line L2
        raise ValueError("the collapse of %r %r breaks the link condition" % (vs, vt))
    rec = VSplit(vs, vt, vl, vr, mesh.pos[vs], mesh.pos[vt],  # @line L3
                 (fl[0], mesh.faces[fl[0]]) if fl else None, (fr[0], mesh.faces[fr[0]]) if fr else None)
    for x in (fl, fr):
        if x is not None:
            f = x[0]
            for v in mesh.faces.pop(f):  # @line L4
                mesh.star[v].discard(f)
    for f in mesh.star.pop(vt):
        mesh.faces[f] = tuple(vs if v == vt else v for v in mesh.faces[f])  # @line L5
        mesh.star[vs].add(f)
    mesh.pos[vs] = p  # @line L6
    del mesh.pos[vt]
    return rec  # @line L7


def vsplit(mesh, rec):
    """Undo the edge collapse that returned rec."""
    vs, vt, vl, vr = rec.vs, rec.vt, rec.vl, rec.vr
    nxt = fan(mesh, vs)
    ends = {b for b, _ in nxt.values()}
    starts = [x for x in nxt if x not in ends]
    if len(starts) > 1:
        raise ValueError("vertex %r has more than one fan" % (vs,))
    # Walk counterclockwise from the edge to vr (or from the start of the fan) to the edge
    # to vl (or to the end of the fan), passing over the boundary gap of vs if there is one.
    a = vr if vr is not None else starts[0]
    moved = []
    while a != vl:  # @line L8
        if a not in nxt:
            if vl is None or not starts or len(moved) > len(nxt):
                break
            a = starts[0]
            continue
        b, f = nxt[a]
        moved.append(f)
        a = b
    mesh.star[vt] = set()
    for f in moved:
        mesh.faces[f] = tuple(vt if v == vs else v for v in mesh.faces[f])  # @line L9
        mesh.star[vs].discard(f)
        mesh.star[vt].add(f)
    mesh.pos[vs], mesh.pos[vt] = rec.ps, rec.pt  # @line L10
    for x in (rec.fl, rec.fr):
        if x is not None:
            f, tri = x
            mesh.faces[f] = tri  # @line L11
            for v in tri:
                mesh.star[v].add(f)


def edges(mesh):
    return sorted({tuple(sorted((t[k], t[(k + 1) % 3]))) for t in mesh.faces.values() for k in range(3)})


def squared_length(mesh, a, b):
    return sum((x - y) ** 2 for x, y in zip(mesh.pos[a], mesh.pos[b]))


def build(vertices, faces, target):
    """Collapse the shortest legal edge to its midpoint until target vertices remain or no edge is legal.

    Returns (base mesh, vertex splits in refinement order). Coordinates should be int or
    Fraction so that the costs and midpoints are exact.
    """
    mesh = Mesh(vertices, faces)
    records = []
    while len(mesh.pos) > target:
        best = None
        for a, b in edges(mesh):
            if link_condition(mesh, a, b):
                key = (squared_length(mesh, a, b), a, b)
                if best is None or key < best:
                    best = key
        if best is None:
            break
        _, vs, vt = best  # @line L14
        p = tuple(Fraction(x + y, 2) for x, y in zip(mesh.pos[vs], mesh.pos[vt]))
        records.append(ecol(mesh, vs, vt, p))
    records.reverse()
    return mesh, records  # @line L15


def refine(base, records, k=None):
    """The mesh after the first k vertex splits (all of them if k is None)."""
    mesh = base.copy()
    for rec in records[:k]:
        vsplit(mesh, rec)
    return mesh
