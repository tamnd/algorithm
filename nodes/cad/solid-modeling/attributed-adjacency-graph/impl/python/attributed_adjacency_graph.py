# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/attributed-adjacency-graph/. The authors are listed in prov/5037C3.jsonl.

"""Feature recognition with the attributed adjacency graph of Joshi and Chang, exactly.

The input is a polyhedral solid given by planar polygons with integer
vertices. Each polygon is listed counterclockwise when seen from outside the
solid, so that its Newell normal points out (the right-hand rule). The
polygons must form a conforming mesh: each directed edge (p, q) of a polygon
is matched by exactly one edge (q, p) of another polygon. A face of the solid
may be given as several polygons; coplanar neighbors are merged into one face.

The edge between two faces is convex (label 1) or concave (label 0) as the
sign of (n_f x n_g) . (q - p) is positive or negative, where (p, q) is the
edge as it runs in the polygon of f. All coordinates are integers, so every
sign is exact.
"""

from itertools import permutations

CONVEX, CONCAVE = 1, 0


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def newell(poly):
    """Twice the area vector of a planar polygon; it points out for a counterclockwise loop seen from outside."""
    nx = ny = nz = 0
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        nx += (p[1] - q[1]) * (p[2] + q[2])
        ny += (p[2] - q[2]) * (p[0] + q[0])
        nz += (p[0] - q[0]) * (p[1] + q[1])
    return (nx, ny, nz)


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, a):
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)


def build_aag(polys):
    """Return (faces, arcs): faces is a list of sets of polygon indices, and arcs maps a pair (i, j), i < j, of face indices to a frozenset of labels."""
    normals = [newell(P) for P in polys]
    owner = {}
    for k, P in enumerate(polys):
        for i, p in enumerate(P):
            e = (tuple(p), tuple(P[(i + 1) % len(P)]))
            if e in owner:
                raise ValueError("a directed edge occurs twice: the solid is not manifold or not oriented")
            owner[e] = k
    uf = UnionFind(len(polys))
    signed = []
    for (p, q), k in owner.items():
        k2 = owner.get((q, p))  # @line L1
        if k2 is None:
            raise ValueError("an edge has no partner: the polygons do not close up")
        if k2 == k:
            continue
        s = dot(cross(normals[k], normals[k2]), sub(q, p))  # @line L2
        if s == 0 and dot(normals[k], normals[k2]) > 0:  # @line L3
            uf.union(k, k2)
        elif s == 0:  # @line L4
            raise ValueError("two faces meet at a knife edge")
        else:
            signed.append((k, k2, CONVEX if s > 0 else CONCAVE))
    roots = sorted({uf.find(k) for k in range(len(polys))})
    index = {r: i for i, r in enumerate(roots)}
    faces = [set() for _ in roots]
    for k in range(len(polys)):
        faces[index[uf.find(k)]].add(k)
    arcs = {}
    for k, k2, label in signed:  # @line L5
        a, b = index[uf.find(k)], index[uf.find(k2)]
        if a != b:
            key = (min(a, b), max(a, b))
            arcs[key] = arcs.get(key, frozenset()) | {label}
    return faces, arcs


def neighbors(n, arcs):
    adj = [dict() for _ in range(n)]
    for (a, b), lab in arcs.items():
        adj[a][b] = lab
        adj[b][a] = lab
    return adj


def match(template, comp, adj):
    """A map from the template nodes onto the component that keeps every label and every non-arc, or None."""
    k, t_arcs = template["nodes"], template["arcs"]
    if k != len(comp):  # @line L11
        return None
    t_adj = [dict() for _ in range(k)]
    for (a, b), lab in t_arcs.items():
        t_adj[a][b] = t_adj[b][a] = lab
    order = sorted(range(k), key=lambda a: -len(t_adj[a]))
    nodes = sorted(comp)
    image = {}

    def extend(depth):
        if depth == k:  # @line L14
            return True
        a = order[depth]
        for v in nodes:  # @line L12
            if v in image.values():
                continue
            if all(t_adj[a].get(b) == adj[v].get(image[b]) for b in order[:depth]):  # @line L13
                image[a] = v
                if extend(depth + 1):
                    return True
                del image[a]
        return False

    return dict(image) if extend(0) else None


def recognize(polys, templates):
    """Return (faces, arcs, results); each result is (template name or None, component, map)."""
    faces, arcs = build_aag(polys)
    adj = neighbors(len(faces), arcs)
    kept = {v for v in range(len(faces)) if any(lab != frozenset({CONVEX}) for lab in adj[v].values())}  # @line L6
    sub_adj = [{w: lab for w, lab in adj[v].items() if w in kept} if v in kept else {} for v in range(len(faces))]
    results, seen = [], set()
    for v in sorted(kept):  # @line L7
        if v in seen:
            continue
        comp, stack = {v}, [v]
        while stack:
            u = stack.pop()
            for w in sub_adj[u]:
                if w not in comp:
                    comp.add(w)
                    stack.append(w)
        seen |= comp
        for t in templates:  # @line L8
            m = match(t, comp, sub_adj)
            if m is not None:  # @line L9
                results.append((t["name"], frozenset(comp), m))
                break
        else:
            results.append((None, frozenset(comp), None))  # @line L10
    return faces, arcs, results


def match_brute_force(template, comp, adj):
    """Reference: try every bijection."""
    k, t_arcs = template["nodes"], template["arcs"]
    if k != len(comp):
        return None
    nodes = sorted(comp)
    for perm in permutations(nodes):
        if all(t_arcs.get((a, b), t_arcs.get((b, a))) == adj[perm[a]].get(perm[b]) for a in range(k) for b in range(a + 1, k)):
            return dict(enumerate(perm))
    return None


# --- templates ---------------------------------------------------------------


def template(name, k, concave_pairs):
    return {"name": name, "nodes": k, "arcs": {(a, b): frozenset({CONCAVE}) for a, b in concave_pairs}}


TEMPLATES = [
    template("pocket", 5, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)]),
    template("blind slot", 4, [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]),
    template("through hole", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    template("blind step", 3, [(0, 1), (0, 2), (1, 2)]),
    template("through slot", 3, [(0, 1), (0, 2)]),
    template("step", 2, [(0, 1)]),
]


# --- building test solids ---------------------------------------------------


def voxel_brep(cells):
    """The boundary of a union of unit cubes, as one outward square per exposed cube face."""
    cells = set(cells)
    polys = []
    for (i, j, k) in cells:
        for axis in range(3):
            for side in (0, 1):
                nb = [i, j, k]
                nb[axis] += 1 if side else -1
                if tuple(nb) in cells:
                    continue
                c = [i, j, k]
                c[axis] += side
                u, w = (axis + 1) % 3, (axis + 2) % 3
                sq = []
                for du, dw in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    p = list(c)
                    p[u] += du
                    p[w] += dw
                    sq.append(tuple(p))
                out = [0, 0, 0]
                out[axis] = 1 if side else -1
                if dot(newell(sq), tuple(out)) < 0:
                    sq.reverse()
                polys.append(sq)
    return polys


def box_cells(x0, x1, y0, y1, z0, z1):
    return {(i, j, k) for i in range(x0, x1) for j in range(y0, y1) for k in range(z0, z1)}


def prism(profile, length):
    """A profile in the xz plane, counterclockwise with x to the right and z up, extruded along y from 0 to length."""
    cap0 = [(x, 0, z) for (x, z) in profile]
    cap1 = [(x, length, z) for (x, z) in reversed(profile)]
    sides = []
    for i, a in enumerate(profile):
        b = profile[(i + 1) % len(profile)]
        sides.append([(b[0], 0, b[1]), (a[0], 0, a[1]), (a[0], length, a[1]), (b[0], length, b[1])])
    return [cap0, cap1] + sides


def signed_volume6(polys):
    """Six times the volume enclosed by the polygons, positive when they face out."""
    total = 0
    for P in polys:
        for i in range(1, len(P) - 1):
            total += dot(P[0], cross(P[i], P[i + 1]))
    return total
