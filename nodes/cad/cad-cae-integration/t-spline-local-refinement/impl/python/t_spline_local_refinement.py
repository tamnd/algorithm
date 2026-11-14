# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-spline-local-refinement/. The authors are listed in prov/WVHYV3.jsonl.

"""Local refinement of analysis-suitable bicubic T-splines (Scott, Li, Sederberg, Hughes).

The T-mesh lives on a fixed integer grid of index space (see the t-spline
page): vertical lines 0..m with knot values sv, horizontal lines 0..n with
values tv, and sets of unit edges. A grid line that has no edge is not part of
the T-mesh; refinement may add edges on it. Lines 0, 1, m - 1, m and
0, 1, n - 1, n must be complete. Use Fraction for exact results.

refine(T1, R) adds the requested edges R to T1, then adds insertion edges, one
at a time and greedily, until the coupled extension graph has no edges. It
returns the refined mesh and the refinement operator, so that the surface is
the same.
"""

from fractions import Fraction

DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
OPP = {"R": "L", "L": "R", "U": "D", "D": "U"}


class TMesh:
    def __init__(self, sv, tv):
        self.sv, self.tv = list(sv), list(tv)
        self.m, self.n = len(sv) - 1, len(tv) - 1
        self.h, self.v = set(), set()

    def copy(self):
        o = TMesh(self.sv, self.tv)
        o.h, o.v = set(self.h), set(self.v)
        return o

    def add_h(self, i0, i1, j):
        for i in range(min(i0, i1), max(i0, i1)):
            self.h.add((i, j))

    def add_v(self, i, j0, j1):
        for j in range(min(j0, j1), max(j0, j1)):
            self.v.add((i, j))

    def add_lines(self, cols, rows):
        """Add the complete vertical lines cols and horizontal lines rows."""
        for i in cols:
            self.add_v(i, 0, self.n)
        for j in rows:
            self.add_h(0, self.m, j)

    def on_v(self, i, j):
        return (i, j) in self.v or (i, j - 1) in self.v

    def on_h(self, i, j):
        return (i, j) in self.h or (i - 1, j) in self.h

    def is_vertex(self, i, j):
        return self.on_v(i, j) and self.on_h(i, j)

    def has_edge(self, i, j, d):
        if d == "R":
            return (i, j) in self.h
        if d == "L":
            return (i - 1, j) in self.h
        if d == "U":
            return (i, j) in self.v
        return (i, j - 1) in self.v

    def crosses(self, i, j, d):
        """Does the point (i, j) lie on an edge perpendicular to direction d?"""
        return self.on_v(i, j) if d in "RL" else self.on_h(i, j)

    def inside(self, i, j):
        return 0 <= i <= self.m and 0 <= j <= self.n

    def anchors(self):
        return [(i, j) for j in range(2, self.n - 1) for i in range(2, self.m - 1) if self.is_vertex(i, j)]

    def march(self, i, j, d, count):
        """Points met when walking from (i, j) in direction d that lie on perpendicular edges."""
        di, dj = DIRS[d]
        out = []
        while len(out) < count:
            i, j = i + di, j + dj
            if not self.inside(i, j):
                break
            if self.crosses(i, j, d):
                out.append((i, j))
        return out

    def local_index_vectors(self, i, j):
        r = [p[0] for p in self.march(i, j, "R", 2)]
        l = [p[0] for p in self.march(i, j, "L", 2)]
        u = [p[1] for p in self.march(i, j, "U", 2)]
        d = [p[1] for p in self.march(i, j, "D", 2)]
        if min(len(r), len(l), len(u), len(d)) < 2:
            raise ValueError("a ray left the mesh; complete the outer lines")
        return (tuple(l[::-1] + [i] + r), tuple(d[::-1] + [j] + u))

    def functions(self):
        """The blending functions as {anchor: (s index vector, t index vector)}."""
        return {A: self.local_index_vectors(*A) for A in self.anchors()}


def face_extensions_and_junctions(mesh):
    """The T-junction extensions of the mesh in index space.

    For each vertex and each missing direction d whose opposite edge exists,
    the face extension marches in direction d to the second point on a
    perpendicular edge; the edge extension marches the other way to the first
    such point. Returns a list of (junction, d, face_end, edge_end).
    """
    out = []
    for i in range(mesh.m + 1):
        for j in range(mesh.n + 1):
            if not mesh.is_vertex(i, j):
                continue
            for d in "RLUD":
                di, dj = DIRS[d]
                if not mesh.inside(i + di, j + dj):
                    continue  # the outer boundary of the index domain
                if not mesh.has_edge(i, j, d) and mesh.has_edge(i, j, OPP[d]):
                    face = mesh.march(i, j, d, 2)
                    edge = mesh.march(i, j, OPP[d], 1)
                    out.append(((i, j), d, face[-1], edge[0]))
    return out


def segment(ext):
    """The closed segment of a T-junction extension, as (horizontal?, line, lo, hi)."""
    (i, j), d, f, e = ext
    if d in "RL":
        return True, j, min(f[0], e[0]), max(f[0], e[0])
    return False, i, min(f[1], e[1]), max(f[1], e[1])


def crossing_pairs(exts):
    segs = [segment(x) for x in exts]
    pairs = []
    for a, (ha, la, loa, hia) in enumerate(segs):
        for b, (hb, lb, lob, hib) in enumerate(segs):
            if ha and not hb and loa <= lb <= hia and lob <= la <= hib:
                pairs.append((a, b))
    return pairs


def is_analysis_suitable(mesh):
    """No horizontal T-junction extension meets a vertical one (closed segments)."""
    return not crossing_pairs(face_extensions_and_junctions(mesh))


def _strictly_inside(p, a, b, d):
    if d in "RL":
        return p[1] == a[1] and min(a[0], b[0]) < p[0] < max(a[0], b[0])
    return p[0] == a[0] and min(a[1], b[1]) < p[1] < max(a[1], b[1])


def coupled_weight(ext1, mesh2):
    """Weight of the coupled extension graph E(T1->2): crossings in T2 plus loop edges.

    A loop edge is a face extension of T2 that ends strictly inside a face
    extension of T1 with the same direction, on the same line.
    """
    ext2 = face_extensions_and_junctions(mesh2)
    w = len(crossing_pairs(ext2))
    for _, d, f2, _ in ext2:
        if any(d1 == d and _strictly_inside(f2, J1, f1, d) for J1, d1, f1, _ in ext1):
            w += 1
    return w, ext2


def insertion_edges(ext1, mesh2):
    """Candidate edges: from a T-junction of nonzero weight to the next perpendicular line."""
    ext2 = face_extensions_and_junctions(mesh2)
    pairs = crossing_pairs(ext2)
    busy = {a for a, _ in pairs} | {b for _, b in pairs}
    for k, (J, d, f2, _) in enumerate(ext2):
        for J1, d1, f1, _ in ext1:
            if d1 == d and _strictly_inside(f2, J1, f1, d):
                busy.add(k)
    cands = []
    for k in sorted(busy):
        J, d, _, _ = ext2[k]
        nxt = mesh2.march(J[0], J[1], d, 1)
        if nxt:
            cands.append((J, nxt[0], d))
    return sorted(set(cands))


def add_edge(mesh, cand):
    (i0, j0), (i1, j1), d = cand
    if d in "RL":
        mesh.add_h(i0, i1, j0)
    else:
        mesh.add_v(i0, j0, j1)


def refine(mesh1, request):
    """Scott, Li, Sederberg and Hughes's local refinement.

    mesh1 must be analysis-suitable. request is a list of ("h", i0, i1, j) and
    ("v", i, j0, j1) segments. Returns (mesh2, M, added) where M[A][B] is the
    coefficient of the new function B in the old function A, and added lists
    the insertion edges in the order they were added.
    """
    ext1 = face_extensions_and_junctions(mesh1)
    mesh2 = mesh1.copy()  # @line L1
    for seg in request:
        if seg[0] == "h":
            mesh2.add_h(seg[1], seg[2], seg[3])
        else:
            mesh2.add_v(seg[1], seg[2], seg[3])
    W, _ = coupled_weight(ext1, mesh2)  # @line L2
    added = []
    while W > 0:  # @line L3
        best = None
        for cand in insertion_edges(ext1, mesh2):  # @line L4
            trial = mesh2.copy()
            add_edge(trial, cand)
            w, _ = coupled_weight(ext1, trial)
            if best is None or w < best[0]:  # @line L5
                best = (w, cand)
        add_edge(mesh2, best[1])  # @line L6
        W = best[0]
        added.append(best[1])
    return mesh2, refinement_operator(mesh1, mesh2), added


def insert_one(knots, x, values):
    """Boehm's rule for one cubic B-spline with index knots; see the t-spline page."""
    tau = sorted(list(knots) + [x])
    t = [values[k] for k in knots]
    u = values[x]
    c0 = Fraction(1) if u >= t[3] else (u - t[0]) / (t[3] - t[0])
    c1 = Fraction(1) if u <= t[1] else (t[4] - u) / (t[4] - t[1])
    return [(c0, tuple(tau[:5])), (c1, tuple(tau[1:]))]


def refine_vector(knots, lines, values):
    """Write B[knots] in the B-splines on knots plus lines: {5 index knots: coefficient}."""
    funcs = {tuple(knots): Fraction(1)}
    for x in sorted(lines):
        nxt = {}
        for kn, c in funcs.items():
            parts = insert_one(kn, x, values) if kn[0] < x < kn[-1] and x not in kn else [(1, kn)]
            for c2, k2 in parts:
                if c2:
                    nxt[k2] = nxt.get(k2, Fraction(0)) + c * c2
        funcs = nxt
    return funcs


def refinement_operator(mesh1, mesh2):
    """M[A][B] with N_A (old) = sum_B M[A][B] N_B (new), by basis function refinement.

    For each pair with the index domain of B inside that of A, the knots of B
    are inserted into the local knot vectors of A, and the coefficient of the
    piece that equals N_B is taken. The coefficient of a fine B-spline depends
    only on the coarse knots and its own knots (the discrete B-splines of the
    Oslo algorithm), so one pair at a time gives the right value. Whether the
    sum reproduces N_A is the nesting property, which the tests check.
    """
    old, new = mesh1.functions(), mesh2.functions()
    M = {}
    for A, (sA, tA) in old.items():  # @line L7
        row = {}
        for B, (sB, tB) in new.items():
            if sA[0] <= sB[0] and sB[-1] <= sA[-1] and tA[0] <= tB[0] and tB[-1] <= tA[-1]:
                ds = refine_vector(sA, set(sB) - set(sA), mesh2.sv)  # @line L8
                dt = refine_vector(tA, set(tB) - set(tA), mesh2.tv)
                c = ds.get(sB, 0) * dt.get(tB, 0)  # @line L9
                if c:
                    row[B] = c  # @line L10
        M[A] = row
    return M


def new_control_points(M, Q):
    """Homogeneous control points of the new mesh: Q_B = sum_A M[A][B] Q_A."""
    out = {}
    for A, row in M.items():
        for B, c in row.items():
            acc = out.setdefault(B, [Fraction(0)] * len(Q[A]))
            for k, q in enumerate(Q[A]):
                acc[k] += c * q
    return {B: tuple(v) for B, v in out.items()}  # @line L11


def bspline(knots, x, last=None):
    """Cubic B-spline (degree len - 2) on the knot values at x, by Cox-de Boor."""
    p = len(knots) - 2
    x = Fraction(x)
    vals = [Fraction(int(a <= x < b or (last is not None and a < b == last == x))) for a, b in zip(knots, knots[1:])]
    for d in range(1, p + 1):
        vals = [
            (((x - knots[k]) / (knots[k + d] - knots[k]) * vals[k]) if knots[k + d] != knots[k] else 0)
            + (((knots[k + d + 1] - x) / (knots[k + d + 1] - knots[k + 1]) * vals[k + 1]) if knots[k + d + 1] != knots[k + 1] else 0)
            for k in range(len(vals) - 1)
        ]
    return vals[0]


def blend(mesh, idx, s, t):
    si, ti = idx
    return bspline([mesh.sv[k] for k in si], s, mesh.sv[-1]) * bspline([mesh.tv[k] for k in ti], t, mesh.tv[-1])


def evaluate(mesh, Q, s, t):
    """The surface from homogeneous control points Q (dict on anchors), projected."""
    acc = None
    for A, idx in mesh.functions().items():
        b = blend(mesh, idx, s, t)
        if b:
            term = [b * q for q in Q[A]]
            acc = term if acc is None else [x + y for x, y in zip(acc, term)]
    return tuple(x / acc[-1] for x in acc[:-1])
