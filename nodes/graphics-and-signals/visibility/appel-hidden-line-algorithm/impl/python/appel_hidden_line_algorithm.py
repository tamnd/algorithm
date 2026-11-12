# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/appel-hidden-line-algorithm/. The authors are listed in prov/EFMSAP.jsonl.

"""Appel's hidden line algorithm with quantitative invisibility (QI).

The scene is a set of closed polyhedral solids that do not cut into each
other. Each face is a planar polygon (convex or not) whose vertices are in
counterclockwise order seen from outside the solid. The view is parallel,
along the z axis: the viewer is at z = +infinity, a point (x, y, z) projects
to (x, y), and a larger z is nearer to the viewer.

The quantitative invisibility of a point p is the number of front faces
that cover p: faces whose projection contains (x, y) strictly inside and
whose plane is above p there. A point is visible when its QI is 0.

Appel's observation: along an edge, the QI changes only where the edge
passes behind a contour edge (an edge with exactly one front face), by +1
or -1, and at a vertex by the faces at that vertex. So the QI of one
vertex of each solid, found by testing all faces, gives every other QI by
walking along the edges.

The input must be in general position: no vertex projects onto another
edge or vertex, no face is seen edge on, and the projections of three
edges do not pass through one point. All arithmetic uses Fraction.
"""

from collections import deque
from fractions import Fraction


def cross2(ax, ay, bx, by):
    return ax * by - ay * bx


class Scene:
    """Closed solids merged into one list of vertices and faces."""

    def __init__(self, solids):
        self.vertices = []
        self.faces = []  # lists of global vertex indices
        self.solid_of_vertex = []
        for si, (verts, faces) in enumerate(solids):
            base = len(self.vertices)
            for v in verts:
                self.vertices.append(tuple(Fraction(c) for c in v))
                self.solid_of_vertex.append(si)
            for f in faces:
                self.faces.append([base + k for k in f])
        self.normals = [self._newell(f) for f in self.faces]
        self.planes_d = [sum(n[k] * self.vertices[f[0]][k] for k in range(3))
                         for n, f in zip(self.normals, self.faces)]
        edge_faces = {}
        for fi, f in enumerate(self.faces):
            for k in range(len(f)):
                a, b = f[k], f[(k + 1) % len(f)]
                edge_faces.setdefault((min(a, b), max(a, b)), []).append(fi)
        self.edges = sorted(edge_faces)
        self.edge_faces = edge_faces
        self.faces_at = [[] for _ in self.vertices]
        for fi, f in enumerate(self.faces):
            for v in f:
                self.faces_at[v].append(fi)

    def _newell(self, f):
        nx = ny = nz = Fraction(0)
        for k in range(len(f)):
            x1, y1, z1 = self.vertices[f[k]]
            x2, y2, z2 = self.vertices[f[(k + 1) % len(f)]]
            nx += (y1 - y2) * (z1 + z2)
            ny += (z1 - z2) * (x1 + x2)
            nz += (x1 - x2) * (y1 + y2)
        return (nx, ny, nz)

    def is_front(self, fi):
        return self.normals[fi][2] > 0

    def depth_on_plane(self, fi, x, y):
        """z of the plane of face fi above the point (x, y)."""
        n, d = self.normals[fi], self.planes_d[fi]
        return (d - n[0] * x - n[1] * y) / n[2]


def inside_projection(scene, fi, x, y):
    """1 if (x, y) is strictly inside the projection of face fi, 0 if outside, None on its boundary."""
    f = scene.faces[fi]
    inside = False
    for k in range(len(f)):
        x1, y1, _ = scene.vertices[f[k]]
        x2, y2, _ = scene.vertices[f[(k + 1) % len(f)]]
        if cross2(x2 - x1, y2 - y1, x - x1, y - y1) == 0 and \
                min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            return None
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                inside = not inside
    return 1 if inside else 0


def qi_of_point(scene, p, skip=()):
    """QI of p by testing every front face (the starting step of Appel)."""
    count = 0
    for fi in range(len(scene.faces)):
        if fi in skip or not scene.is_front(fi):
            continue
        r = inside_projection(scene, fi, p[0], p[1])
        if r is None:
            raise ValueError("degenerate: a point projects onto a face boundary")
        if r and scene.depth_on_plane(fi, p[0], p[1]) > p[2]:
            count += 1
    return count


def _corner_contains(scene, fi, v, dx, dy):
    """Does the direction (dx, dy) from vertex v point strictly into face fi's projection?"""
    f = scene.faces[fi]
    k = f.index(v)
    a = scene.vertices[f[k - 1]]
    b = scene.vertices[f[(k + 1) % len(f)]]
    o = scene.vertices[v]
    ax, ay = a[0] - o[0], a[1] - o[1]
    bx, by = b[0] - o[0], b[1] - o[1]
    if cross2(bx, by, ax, ay) > 0:  # convex corner, front faces are counterclockwise
        return cross2(bx, by, dx, dy) > 0 and cross2(dx, dy, ax, ay) > 0
    return not (cross2(ax, ay, dx, dy) >= 0 and cross2(dx, dy, bx, by) >= 0)


def cover_at(scene, v, w):
    """Number of front faces at v that cover the edge v w just after v."""
    p, q = scene.vertices[v], scene.vertices[w]
    d = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
    count = 0
    for fi in scene.faces_at[v]:
        if not scene.is_front(fi) or w in scene.faces[fi] and _is_edge_of(scene.faces[fi], v, w):
            continue
        n = scene.normals[fi]
        below = n[0] * d[0] + n[1] * d[1] + n[2] * d[2] < 0  # the edge goes under the plane
        if below and _corner_contains(scene, fi, v, d[0], d[1]):
            count += 1
    return count


def _is_edge_of(face, a, b):
    m = len(face)
    for k in range(m):
        if {face[k], face[(k + 1) % m]} == {a, b}:
            return True
    return False


def contour_edges(scene):
    """Edges with exactly one front face, directed as in that face."""
    out = []
    for (a, b), fs in scene.edge_faces.items():
        fronts = [fi for fi in fs if scene.is_front(fi)]
        if len(fronts) == 1:
            f = scene.faces[fronts[0]]
            k = f.index(a)
            if f[(k + 1) % len(f)] == b:
                out.append((a, b))
            else:
                out.append((b, a))
    return out


def crossings(scene, u, w, contours):
    """Points where the edge u w passes behind a contour edge: (t, +1 or -1)."""
    p0, p1 = scene.vertices[u], scene.vertices[w]
    ex, ey = p1[0] - p0[0], p1[1] - p0[1]
    out = []
    for a, b in contours:
        if a in (u, w) or b in (u, w):
            continue
        q0, q1 = scene.vertices[a], scene.vertices[b]
        cx, cy = q1[0] - q0[0], q1[1] - q0[1]
        den = cross2(ex, ey, cx, cy)
        if den == 0:
            continue
        rx, ry = q0[0] - p0[0], q0[1] - p0[1]
        t = cross2(rx, ry, cx, cy) / den
        s = cross2(rx, ry, ex, ey) / den
        if not (0 < t < 1 and 0 < s < 1):
            continue
        ze = p0[2] + t * (p1[2] - p0[2])
        zc = q0[2] + s * (q1[2] - q0[2])
        if zc > ze:  # the contour edge is in front of the edge here
            # The front face lies to the left of a -> b. Crossing from its
            # right to its left goes under that face.
            out.append((t, 1 if cross2(cx, cy, ex, ey) > 0 else -1))
    return out


def appel_hidden_lines(solids):
    """QI along every edge.

    solids: list of (vertices, faces). Returns (scene, pieces), where pieces
    maps each edge (u, w), u < w, to a list of (t0, t1, qi) along the
    segment from vertex u to vertex w. The visible parts are those with qi 0.
    """
    scene = Scene(solids)
    contours = contour_edges(scene)  # @line L1
    qi = [None] * len(scene.vertices)
    adj = [[] for _ in scene.vertices]
    for a, b in scene.edges:
        adj[a].append(b)
        adj[b].append(a)
    pieces = {}
    seen_solid = set()
    for start in range(len(scene.vertices)):  # @line L2
        si = scene.solid_of_vertex[start]
        if si in seen_solid:
            continue
        seen_solid.add(si)
        qi[start] = qi_of_point(scene, scene.vertices[start], skip=set(scene.faces_at[start]))  # @line L3
        queue = deque([start])  # @line L4
        while queue:  # @line L5
            u = queue.popleft()
            for w in adj[u]:  # @line L6
                key = (min(u, w), max(u, w))
                if key in pieces:
                    continue
                q = qi[u] + cover_at(scene, u, w)  # @line L7
                events = sorted(crossings(scene, u, w, contours))  # @line L8
                run, t_prev = [], Fraction(0)
                for t, delta in events:  # @line L9
                    run.append((t_prev, t, q))
                    q += delta
                    t_prev = t
                run.append((t_prev, Fraction(1), q))
                if q - cover_at(scene, w, u) < 0:
                    raise ValueError("degenerate input: negative QI")
                if qi[w] is None:  # @line L10
                    qi[w] = q - cover_at(scene, w, u)
                    queue.append(w)
                if u > w:  # store along the direction low index -> high index
                    run = [(1 - t1, 1 - t0, k) for t0, t1, k in reversed(run)]
                pieces[key] = run
    return scene, pieces  # @line L11


def visible_segments(scene, pieces):
    """The parts with QI 0 as 3D segments."""
    out = []
    for (u, w), run in pieces.items():
        p0, p1 = scene.vertices[u], scene.vertices[w]
        for t0, t1, k in run:
            if k == 0:
                out.append((tuple(p0[c] + t0 * (p1[c] - p0[c]) for c in range(3)),
                            tuple(p0[c] + t1 * (p1[c] - p0[c]) for c in range(3))))
    return out


CUBE_FACES = [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]]


def cube(lo, hi):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    verts = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    return verts, [list(f) for f in CUBE_FACES]


if __name__ == "__main__":
    shear = lambda p: (p[0] + p[2] / 3, p[1] + p[2] / 5, p[2])  # noqa: E731
    back_v, back_f = cube((0, 0, 0), (4, 4, 1))
    front_v, front_f = cube((1, 1, 3), (2, 2, 4))
    solids = [([shear(tuple(map(Fraction, v))) for v in back_v], back_f),
              ([shear(tuple(map(Fraction, v))) for v in front_v], front_f)]
    scene, pieces = appel_hidden_lines(solids)
    for (u, w), run in sorted(pieces.items()):
        print(u, w, [(str(a), str(b), k) for a, b, k in run])
