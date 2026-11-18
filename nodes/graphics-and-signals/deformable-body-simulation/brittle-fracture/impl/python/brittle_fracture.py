# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brittle-fracture/. The authors are listed in prov/PNJ37X.jsonl.
"""Brittle fracture after O'Brien and Hodgins (1999), on a 2D triangle mesh.

Each element has the St. Venant-Kirchhoff stress S = 2 mu E + lambda tr(E) I
with the Green strain E = (F^T F - I) / 2, and the nodal forces
G = -V0 F S D_m^(-T) on the nodes 1 and 2, node 0 getting minus the sum.
S is split by its eigenvalues into a tensile part S+ and a compressive part
S-, and the nodal forces of S+ are the tensile forces f+ (f- = f - f+).

At a node, with m(a) = a a^T / |a| (and m(0) = 0), the separation tensor is

    sep = 1/2 ( -m(sum f+) + sum m(f+) + m(sum f-) - sum m(f-) ),

where the sums run over the elements at the node. If its largest eigenvalue
exceeds the toughness tau, the mesh is split at the node along the line
with the eigenvector as normal: the node is duplicated, the elements that
the line crosses are cut, and their neighbours across the cut edge are cut
too, so the mesh stays conforming. The new crack tip points are not
duplicated, so a crack grows one node at a time.

The snapping thresholds, the velocity damping and the rule of at most one
split per step are tuning choices of this file.
"""

import math

from anim import det, inv, mul, transpose


def edge_matrix(p, t):
    a, b, c = p[t[0]], p[t[1]], p[t[2]]
    return [[b[0] - a[0], c[0] - a[0]], [b[1] - a[1], c[1] - a[1]]]


def sym_eig2(s):
    """Eigenvalues (larger first) and unit eigenvectors of a symmetric 2 by 2 matrix."""
    a, b, d = s[0][0], 0.5 * (s[0][1] + s[1][0]), s[1][1]
    m, r = 0.5 * (a + d), math.hypot(0.5 * (a - d), b)
    phi = 0.5 * math.atan2(2.0 * b, a - d)
    n1 = (math.cos(phi), math.sin(phi))
    return (m + r, m - r), (n1, (-n1[1], n1[0]))


def outer_m(f):
    """m(a) = a a^T / |a|, with m(0) = 0."""
    n = math.hypot(f[0], f[1])
    if n == 0.0:
        return [[0.0, 0.0], [0.0, 0.0]]
    return [[f[0] * f[0] / n, f[0] * f[1] / n], [f[1] * f[0] / n, f[1] * f[1] / n]]


def split_stress(s):
    """Return (S+, S-) with S+ + S- = S, S+ positive and S- negative semidefinite."""
    vals, vecs = sym_eig2(s)
    sp = [[0.0, 0.0], [0.0, 0.0]]
    for lam, n in zip(vals, vecs):
        if lam > 0.0:
            for i in range(2):
                for j in range(2):
                    sp[i][j] += lam * n[i] * n[j]
    sm = [[s[i][j] - sp[i][j] for j in range(2)] for i in range(2)]
    return sp, sm


class Mesh:
    """A 2D triangle mesh that can be cut. Positions are lists of [x, y]."""

    def __init__(self, rest, tris, mu, lam, density=1.0):
        self.rest = [list(map(float, p)) for p in rest]
        self.x = [list(map(float, p)) for p in rest]
        self.v = [[0.0, 0.0] for _ in rest]
        self.tris = [tuple(t) for t in tris]
        self.mu, self.lam, self.density = mu, lam, density
        self.update_rest()

    def update_rest(self):
        self.dm_inv, self.v0 = [], []
        self.mass = [0.0] * len(self.rest)
        for t in self.tris:
            dm = edge_matrix(self.rest, t)
            if det(dm) <= 0.0:
                raise ValueError("each triangle needs a positive rest orientation")
            self.dm_inv.append(inv(dm))
            self.v0.append(0.5 * det(dm))
            for a in t:
                self.mass[a] += self.density * 0.5 * det(dm) / 3.0  # @line L11


def stvk_stress(f, mu, lam):
    """S = 2 mu E + lambda tr(E) I with the Green strain E."""
    c = mul(transpose(f), f)
    e = [[0.5 * (c[i][j] - (1.0 if i == j else 0.0)) for j in range(2)] for i in range(2)]
    tr = e[0][0] + e[1][1]
    return [[2.0 * mu * e[i][j] + (lam * tr if i == j else 0.0) for j in range(2)] for i in range(2)]


def _nodal(mesh, e, f, s):
    """The three nodal forces of the stress S of element e."""
    g = mul(mul(f, s), transpose(mesh.dm_inv[e]))
    v0 = mesh.v0[e]
    g1 = (-v0 * g[0][0], -v0 * g[1][0])
    g2 = (-v0 * g[0][1], -v0 * g[1][1])
    return [(-g1[0] - g2[0], -g1[1] - g2[1]), g1, g2]


def element_forces(mesh, x=None):
    """Return (f, fplus) per element: lists of three nodal forces each."""
    x = mesh.x if x is None else x
    out = []
    for e, t in enumerate(mesh.tris):
        f = mul(edge_matrix(x, t), mesh.dm_inv[e])  # @line L1
        s = stvk_stress(f, mesh.mu, mesh.lam)
        sp, _ = split_stress(s)  # @line L2
        out.append((_nodal(mesh, e, f, s), _nodal(mesh, e, f, sp)))  # @line L3
    return out


def stvk_energy(mesh, x):
    tot = 0.0
    for e, t in enumerate(mesh.tris):
        f = mul(edge_matrix(x, t), mesh.dm_inv[e])
        c = mul(transpose(f), f)
        e00, e11, e01 = 0.5 * (c[0][0] - 1.0), 0.5 * (c[1][1] - 1.0), 0.5 * c[0][1]
        tr = e00 + e11
        tot += mesh.v0[e] * (mesh.mu * (e00 * e00 + e11 * e11 + 2 * e01 * e01) + 0.5 * mesh.lam * tr * tr)
    return tot


def separation_tensors(mesh, forces=None):
    """The separation tensor of every node. Cost Theta(n + m)."""
    forces = element_forces(mesh) if forces is None else forces
    n = len(mesh.x)
    fp = [[0.0, 0.0] for _ in range(n)]
    fm = [[0.0, 0.0] for _ in range(n)]
    sum_mp = [[[0.0, 0.0], [0.0, 0.0]] for _ in range(n)]
    sum_mm = [[[0.0, 0.0], [0.0, 0.0]] for _ in range(n)]
    for t, (f, fplus) in zip(mesh.tris, forces):
        for k, a in enumerate(t):
            p = fplus[k]
            q = (f[k][0] - p[0], f[k][1] - p[1])
            mp, mq = outer_m(p), outer_m(q)
            for i in range(2):
                fp[a][i] += p[i]
                fm[a][i] += q[i]
                for j in range(2):
                    sum_mp[a][i][j] += mp[i][j]
                    sum_mm[a][i][j] += mq[i][j]
    sep = []
    for a in range(n):  # @line L4
        mp, mq = outer_m(fp[a]), outer_m(fm[a])
        sep.append([[0.5 * (-mp[i][j] + sum_mp[a][i][j] + mq[i][j] - sum_mm[a][i][j]) for j in range(2)]
                    for i in range(2)])
    return sep


def _signed(n, origin, p):
    return n[0] * (p[0] - origin[0]) + n[1] * (p[1] - origin[1])


def _rotate_to(t, a):
    i = t.index(a)
    return t[i:] + t[:i]


def split_node(mesh, node, normal, snap_angle=0.1, snap_ratio=0.05):
    """Cut the mesh at node along the line through it with the given normal.

    Return the index of the new node, or None if all the elements at the node
    lie on one side of the line (no split is possible).
    """
    xv = mesh.x[node]
    nn = math.hypot(normal[0], normal[1])
    normal = (normal[0] / nn, normal[1] / nn)
    for ray in ((-normal[1], normal[0]), (normal[1], -normal[0])):  # @line L8
        incident = [k for k, t in enumerate(mesh.tris) if node in t]
        snapped = False
        for k in incident:
            for a in mesh.tris[k]:
                if a == node:
                    continue
                d = (mesh.x[a][0] - xv[0], mesh.x[a][1] - xv[1])
                ang = math.atan2(d[0] * ray[1] - d[1] * ray[0], d[0] * ray[0] + d[1] * ray[1])
                if abs(ang) < snap_angle:
                    snapped = True
        if snapped:
            continue
        for k in incident:
            v, a, b = _rotate_to(mesh.tris[k], node)
            da = (mesh.x[a][0] - xv[0], mesh.x[a][1] - xv[1])
            db = (mesh.x[b][0] - xv[0], mesh.x[b][1] - xv[1])
            ca = ray[0] * da[1] - ray[1] * da[0]
            cb = ray[0] * db[1] - ray[1] * db[0]
            if not (ca < 0.0 < cb):
                continue
            s = ca / (ca - cb)
            p_dir = (da[0] + s * (db[0] - da[0]), da[1] + s * (db[1] - da[1]))
            if p_dir[0] * ray[0] + p_dir[1] * ray[1] <= 0.0:
                continue
            if s < snap_ratio or s > 1.0 - snap_ratio:
                break
            _cut_edge(mesh, k, a, b, s)
            break
    side = {}
    for k, t in enumerate(mesh.tris):  # @line L9
        if node in t:
            cx = sum(mesh.x[i][0] for i in t) / 3.0
            cy = sum(mesh.x[i][1] for i in t) / 3.0
            side[k] = _signed(normal, xv, (cx, cy))
    if not any(d < 0.0 for d in side.values()) or not any(d > 0.0 for d in side.values()):
        mesh.update_rest()
        return None
    new = len(mesh.x)  # @line L10
    mesh.x.append(list(mesh.x[node]))
    mesh.rest.append(list(mesh.rest[node]))
    mesh.v.append(list(mesh.v[node]))
    for k, d in side.items():
        if d < 0.0:
            mesh.tris[k] = tuple(new if i == node else i for i in mesh.tris[k])
    mesh.update_rest()
    return new


def _cut_edge(mesh, k, a, b, s):
    """Add a node p on edge (a, b) at the parameter s and cut both triangles at the edge."""
    p = len(mesh.x)
    for arr in (mesh.x, mesh.rest, mesh.v):
        arr.append([(1.0 - s) * arr[a][i] + s * arr[b][i] for i in range(2)])
    v = _rotate_to(mesh.tris[k], a)[2]
    mesh.tris[k] = (v, a, p)
    mesh.tris.append((v, p, b))
    for j, t in enumerate(mesh.tris):
        if j != k and a in t and b in t and p not in t:
            r = _rotate_to(t, b)
            if r[1] == a:
                w = r[2]
                mesh.tris[j] = (b, p, w)
                mesh.tris.append((p, a, w))
            break


def fracture_step(mesh, dt, tau, fixed=(), prescribed=None, damping=0.0):
    """One step: forces, separation tensors, at most one split, symplectic Euler.

    prescribed maps a node to a fixed velocity. Return the new node or None.
    """
    forces = element_forces(mesh)
    sep = separation_tensors(mesh, forces)
    best, node, normal = tau, None, None
    for a, st in enumerate(sep):  # @line L5
        vals, vecs = sym_eig2(st)
        if vals[0] > best:
            best, node, normal = vals[0], a, vecs[0]
    new = None
    if node is not None:  # @line L6
        new = split_node(mesh, node, normal)
    n = len(mesh.x)
    ftot = [[0.0, 0.0] for _ in range(n)]
    for t, (f, _) in zip(mesh.tris, element_forces(mesh)):
        for k, a in enumerate(t):
            ftot[a][0] += f[k][0]
            ftot[a][1] += f[k][1]
    fixed = set(fixed)
    prescribed = prescribed or {}
    for i in range(n):  # @line L7
        if i in fixed:
            mesh.v[i] = [0.0, 0.0]
            continue
        if i in prescribed:
            mesh.v[i] = list(prescribed[i])
        else:
            mesh.v[i] = [(1.0 - damping * dt) * (mesh.v[i][k] + dt * ftot[i][k] / mesh.mass[i]) for k in range(2)]
        mesh.x[i] = [mesh.x[i][k] + dt * mesh.v[i][k] for k in range(2)]
    return new


def grid(nx, ny, w, h):
    """A rectangle of nx by ny cells, each cut into two triangles along alternating diagonals."""
    rest = [(w * i / nx, h * j / ny) for j in range(ny + 1) for i in range(nx + 1)]
    tris = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            b, c, d = a + 1, a + nx + 2, a + nx + 1
            if (i + j) % 2 == 0:
                tris += [(a, b, c), (a, c, d)]
            else:
                tris += [(a, b, d), (b, c, d)]
    return rest, tris


def components(mesh):
    """The number of connected pieces of the mesh (by shared nodes)."""
    parent = list(range(len(mesh.x)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for t in mesh.tris:
        for a in t[1:]:
            parent[find(a)] = find(t[0])
    return len({find(t[0]) for t in mesh.tris})
