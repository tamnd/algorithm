# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brep-reconstruction-from-scans/. The authors are listed in prov/RBGNXS.jsonl.

"""Tests: the fitted planes of a scanned box give the adjacency, the edges and the corners of the true box."""

import os
import random
import sys
from itertools import product
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brep_reconstruction_from_scans import (  # noqa: E402
    BRep, adjacent_pairs, face_loop, fit_plane, plane_line, plane_vertex, reconstruct)

S = 0.1  # sample spacing


def face_grid(o, u, v, nu, nv, s=S):
    """Points at the centers of an nu by nv grid of cells of size s, from corner o along u and v."""
    return [tuple(o[k] + (i + 0.5) * s * u[k] + (j + 0.5) * s * v[k] for k in range(3))
            for i in range(nu) for j in range(nv)]


X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def box(a, b, c, s=S):
    """Six regions: faces x=0, x=a, y=0, y=b, z=0, z=c of the box [0,a] x [0,b] x [0,c]."""
    na, nb, nc = round(a / s), round(b / s), round(c / s)
    return [face_grid((0, 0, 0), Y, Z, nb, nc), face_grid((a, 0, 0), Y, Z, nb, nc),
            face_grid((0, 0, 0), X, Z, na, nc), face_grid((0, b, 0), X, Z, na, nc),
            face_grid((0, 0, 0), X, Y, na, nb), face_grid((0, 0, c), X, Y, na, nb)]


def true_box(a, b, c):
    """The true box: corners with their face sets, adjacency, and edges as (corner set, face pair)."""
    corners = {}
    for i, j, k in product((0, 1), repeat=3):
        corners[(i * a, j * b, k * c)] = frozenset((i, 2 + j, 4 + k))
    adjacency = {(f, g) for f in range(6) for g in range(f + 1, 6) if f // 2 != g // 2}
    edges = set()
    for f, g in adjacency:
        ends = frozenset(p for p, fs in corners.items() if f in fs and g in fs)
        edges.add((ends, (f, g)))
    return corners, adjacency, edges


def rotation(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    s = sqrt(sum(x * x for x in q))
    w, x, y, z = (c / s for c in q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def move(p, rm, t):
    return tuple(sum(rm[i][k] * p[k] for k in range(3)) + t[i] for i in range(3))


def dist(p, q):
    return sqrt(sum((p[k] - q[k]) ** 2 for k in range(3)))


def match(br: BRep, true_pts, tol):
    """Map each reconstructed vertex to the true corner within tol, or None if this fails."""
    m = {}
    for i, v in enumerate(br.vertices):
        near = [p for p in true_pts if dist(v, true_pts[p]) <= tol]
        if len(near) != 1:
            return None
        m[i] = near[0]
    return m if len(set(m.values())) == len(true_pts) == len(m) else None


def same_as_true_box(br: BRep, a, b, c, rm=None, t=(0, 0, 0), tol=1e-9):
    corners, adjacency, edges = true_box(a, b, c)
    rm = rm or [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    placed = {p: move(p, rm, t) for p in corners}
    m = match(br, placed, tol)
    if m is None or br.adjacency != adjacency:
        return False
    if any(br.vertex_faces[i] != corners[m[i]] for i in m):
        return False
    got = {(frozenset((m[x], m[y])), fj) for x, y, fj in br.edges}
    return len(br.edges) == 12 and got == edges and all(len(br.loops[f]) == 4 for f in range(6))


def test_box_worked_example():
    br = reconstruct(box(2.0, 1.0, 0.5), 1.5 * S, 1.5 * S)
    assert same_as_true_box(br, 2.0, 1.0, 0.5, tol=1e-12)
    assert (len(br.vertices), len(br.edges), len(br.planes)) == (8, 12, 6)
    assert br.euler() == 2
    assert br.loops[4] == [0, 2, 6, 4]


def test_random_rigid_boxes_noise_free():
    rng = random.Random(1)
    exact = 0
    for _ in range(20):
        a, b, c = (round(rng.uniform(0.5, 2.0), 1) for _ in range(3))
        rm, t = rotation(rng), [rng.uniform(-5, 5) for _ in range(3)]
        regs = [[move(p, rm, t) for p in r] for r in box(a, b, c)]
        br = reconstruct(regs, 1.5 * S, 2 * S)
        exact += same_as_true_box(br, a, b, c, rm, t, tol=1e-9) and br.euler() == 2
    assert exact == 20  # 20 of 20 trials


def test_random_noisy_boxes_measured():
    rng = random.Random(7)
    exact = 0
    for _ in range(20):
        a, b, c = (round(rng.uniform(0.5, 2.0), 1) for _ in range(3))
        rm, t = rotation(rng), [rng.uniform(-5, 5) for _ in range(3)]
        regs = [[tuple(x + rng.gauss(0, 0.002) for x in move(p, rm, t)) for p in r] for r in box(a, b, c)]
        br = reconstruct(regs, 1.5 * S, 2 * S)
        exact += same_as_true_box(br, a, b, c, rm, t, tol=0.005)
    assert exact == 20  # measured: 20 of 20, largest corner error 0.00195


def test_adjacency_matches_brute_force():
    rng = random.Random(3)
    for _ in range(10):
        regs = [[tuple(rng.uniform(0, 3) for _ in range(3)) for _ in range(rng.randint(5, 30))] for _ in range(6)]
        delta = rng.uniform(0.1, 0.6)
        brute = {(j, k) for j in range(6) for k in range(j + 1, 6)
                 if any(dist(p, q) <= delta for p in regs[j] for q in regs[k])}
        assert adjacent_pairs(regs, delta) == brute


def test_fit_plane_exact_on_plane_points():
    rng = random.Random(5)
    n = (2 / 3, -1 / 3, 2 / 3)
    u, v = (1 / sqrt(2), 0, -1 / sqrt(2)), (1 / sqrt(18), 4 / sqrt(18), 1 / sqrt(18))
    pts = [tuple(3 * n[k] + s * u[k] + t * v[k] for k in range(3))
           for s, t in ((rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(50))]
    m, c = fit_plane(pts)
    sign = 1 if m[0] > 0 else -1
    assert all(abs(sign * m[k] - n[k]) < 1e-12 for k in range(3))
    assert abs(sign * c - 3) < 1e-12


def test_line_and_vertex_of_planes():
    px, py, pz = ((1, 0, 0), 2.0), ((0, 1, 0), 3.0), ((0, 0, 1), -1.0)
    x0, d = plane_line(px, py)
    assert (x0[0], x0[1]) == (2.0, 3.0) and abs(abs(d[2]) - 1) < 1e-15
    assert plane_vertex(px, py, pz) == (2.0, 3.0, -1.0)
    assert plane_line(px, ((1, 0, 0), 5.0)) is None                       # parallel planes
    assert plane_vertex(px, py, ((0.6, 0.8, 0.0), 1.0)) is None           # three normals in one plane


def l_prism(a, b, t, h, s=S):
    """An L-shaped prism: the L is [0,a] x [0,t] united with [0,t] x [0,b], extruded from z=0 to z=h."""
    cap = [(x, y) for x, y in ((S * (i + 0.5), S * (j + 0.5)) for i in range(round(a / s)) for j in range(round(b / s)))
           if y < t or x < t]
    nh = round(h / s)
    return [[(x, y, 0.0) for x, y in cap], [(x, y, h) for x, y in cap],
            face_grid((0, 0, 0), X, Z, round(a / s), nh), face_grid((a, 0, 0), Y, Z, round(t / s), nh),
            face_grid((t, t, 0), X, Z, round((a - t) / s), nh), face_grid((t, t, 0), Y, Z, round((b - t) / s), nh),
            face_grid((0, b, 0), X, Z, round(t / s), nh), face_grid((0, 0, 0), Y, Z, round(b / s), nh)]


def test_l_prism_with_concave_edge():
    br = reconstruct(l_prism(2.0, 1.5, 0.5, 1.0), 1.5 * S, 1.5 * S)
    assert (len(br.vertices), len(br.edges), len(br.planes)) == (12, 18, 8)
    assert br.euler() == 2
    assert len(br.loops[0]) == 6 and len(br.loops[1]) == 6
    assert all(len(br.loops[f]) == 4 for f in range(2, 8))
    assert (4, 5) in br.adjacency                                          # the concave edge
    corner = [v for v in br.vertices if abs(v[0] - 0.5) < 1e-9 and abs(v[1] - 0.5) < 1e-9]
    assert len(corner) == 2


def test_delta_below_gap_finds_no_adjacency():
    br = reconstruct(box(2.0, 1.0, 0.5), 0.5 * S, 1.5 * S)                # gap across an edge is S / sqrt(2)
    assert br.adjacency == set() and br.vertices == [] and br.edges == []
    assert all(loop == [] for loop in br.loops.values())


def test_eta_below_gap_finds_no_vertex():
    br = reconstruct(box(2.0, 1.0, 0.5), 1.5 * S, 0.5 * S)                # a corner is S / sqrt(2) from its points
    assert len(br.adjacency) == 12 and br.vertices == []


def test_face_loop_rejects_open_boundary():
    br = reconstruct(box(2.0, 1.0, 0.5), 1.5 * S, 1.5 * S)
    br.edges = [e for e in br.edges if e[2] != (0, 2)]
    assert face_loop(br, 0) == [] and face_loop(br, 2) == []
    assert len(face_loop(br, 1)) == 4
