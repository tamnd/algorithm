# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-representation/. The authors are listed in prov/MR3WHM.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from boundary_representation import BRep, InvalidBRep, newell

# ---- building solids from coordinates ----


def rect(axis, c, a0, a1, b0, b1, normal):
    """The rectangle at coordinate c on axis, spanning [a0, a1] x [b0, b1] on the two other
    axes, as a loop of points whose Newell normal points along normal * e_axis."""
    b, d = (axis + 1) % 3, (axis + 2) % 3

    def pt(s, t):
        p = [0, 0, 0]
        p[axis], p[b], p[d] = c, s, t
        return tuple(p)

    loop = [pt(a0, b0), pt(a1, b0), pt(a1, b1), pt(a0, b1)]
    return loop if normal > 0 else loop[::-1]


def box(lo, hi, sign=1):
    """The 6 faces of the box [lo, hi], each one loop; sign -1 makes the normals point in."""
    faces = []
    for axis in range(3):
        b, d = (axis + 1) % 3, (axis + 2) % 3
        for end, nrm in ((lo[axis], -1), (hi[axis], 1)):
            faces.append([rect(axis, end, lo[b], hi[b], lo[d], hi[d], nrm * sign)])
    return faces


def make(coord_faces):
    """Index the points of faces given by coordinates and build the B-rep."""
    ids, pts = {}, []
    faces = []
    for loops in coord_faces:
        face = []
        for loop in loops:
            lp = []
            for p in loop:
                if p not in ids:
                    ids[p] = len(pts)
                    pts.append(p)
                lp.append(ids[p])
            face.append(lp)
        faces.append(face)
    return BRep(pts, faces), pts, faces


def frame():
    """The square frame [0, 3] x [0, 3] x [0, 1] with the hole (1, 2) x (1, 2): genus 1."""
    fs = []
    for z, nrm in ((0, -1), (1, 1)):
        outer = rect(2, z, 0, 3, 0, 3, nrm)
        ring = rect(2, z, 1, 2, 1, 2, -nrm)
        fs.append([outer, ring])
    for axis in (0, 1):
        b, d = (axis + 1) % 3, (axis + 2) % 3
        other = 1 - axis  # the in-plane axis that is not z
        for c, nrm, span in ((0, -1, (0, 3)), (3, 1, (0, 3)), (1, 1, (1, 2)), (2, -1, (1, 2))):
            lo = {other: span[0], 2: 0}
            hi = {other: span[1], 2: 1}
            fs.append([rect(axis, c, lo[b], hi[b], lo[d], hi[d], nrm)])
    return fs


def boss():
    """A 4 x 4 x 1 plate with a 2 x 2 x 1 block on top: the top face of the plate has a ring."""
    fs = [f for f in box((0, 0, 0), (4, 4, 1)) if newell(f[0][0:4])[2] <= 0]
    fs.append([rect(2, 1, 0, 4, 0, 4, 1), rect(2, 1, 1, 3, 1, 3, -1)])
    fs += [f for f in box((1, 1, 1), (3, 3, 2)) if newell(f[0])[2] >= 0]
    return fs


# ---- the examples of the page ----


def test_cube():
    b, _, _ = make(box((0, 0, 0), (1, 1, 1)))
    assert b.validate() == {"V": 8, "E": 12, "F": 6, "L": 6, "R": 0, "S": 1, "H": 0}
    assert b.volume() == 1
    for v in range(8):
        assert len(b.neighbors(v)) == 3 and len(set(b.faces_around(v))) == 3
    for f in range(6):
        assert len(b.adjacent_faces(f)) == 4


def test_frame_has_one_hole():
    b, _, _ = make(frame())
    c = b.validate()
    assert c == {"V": 16, "E": 24, "F": 10, "L": 12, "R": 2, "S": 1, "H": 1}
    assert c["V"] - c["E"] + c["F"] - (c["L"] - c["F"]) - 2 * (c["S"] - c["H"]) == 0
    assert b.volume() == 8


def test_boss_has_a_ring():
    b, _, _ = make(boss())
    assert b.validate() == {"V": 16, "E": 24, "F": 11, "L": 12, "R": 1, "S": 1, "H": 0}
    assert b.volume() == 20


def test_cavity_has_two_shells():
    b, _, _ = make(box((0, 0, 0), (3, 3, 3)) + box((1, 1, 1), (2, 2, 2), -1))
    assert b.validate() == {"V": 16, "E": 24, "F": 12, "L": 12, "R": 0, "S": 2, "H": 0}
    assert b.volume() == 26


def test_fraction_coordinates():
    h = Fraction(1, 3)
    b, _, _ = make(box((0, 0, 0), (h, 1, 2)))
    assert b.validate()["H"] == 0
    assert b.volume() == Fraction(2, 3)


# ---- invalid input ----


def test_open_surface_is_rejected():
    with pytest.raises(InvalidBRep, match="only one face"):
        make(box((0, 0, 0), (1, 1, 1))[:5])


def test_reversed_face_is_rejected():
    fs = box((0, 0, 0), (1, 1, 1))
    fs[0] = [fs[0][0][::-1]]
    with pytest.raises(InvalidBRep, match="used twice"):
        make(fs)


def test_inside_out_is_rejected():
    b, _, _ = make(box((0, 0, 0), (1, 1, 1), -1))
    with pytest.raises(InvalidBRep, match="inward"):
        b.validate()


def test_non_planar_face_is_rejected():
    fs = box((0, 0, 0), (2, 2, 2))
    b, pts, faces = make(fs)
    v = pts.index((2, 2, 2))
    pts2 = list(pts)
    pts2[v] = (3, 3, 3)
    with pytest.raises(InvalidBRep, match="not planar"):
        BRep(pts2, faces).validate()


def test_cubes_on_an_edge_are_rejected():
    with pytest.raises(InvalidBRep, match="used twice"):
        make(box((0, 0, 0), (1, 1, 1)) + box((1, 1, 0), (2, 2, 1)))


def test_cubes_on_a_vertex_are_rejected():
    b, _, _ = make(box((0, 0, 0), (1, 1, 1)) + box((1, 1, 1), (2, 2, 2)))
    with pytest.raises(InvalidBRep, match="non-manifold"):
        b.validate()


def test_wrong_ring_orientation_is_rejected():
    fs = frame()
    fs[1] = [fs[1][0], fs[1][1][::-1]]
    with pytest.raises(InvalidBRep):
        make(fs)[0].validate()


# ---- random voxel solids against a scan of the face list ----

DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def voxel_faces(cells):
    """The boundary squares of a set of unit cells, each oriented outward."""
    fs = []
    for c in sorted(cells):
        for d in DIRS:
            nb = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
            if nb in cells:
                continue
            axis = [i for i in range(3) if d[i]][0]
            sgn = d[axis]
            b, e = (axis + 1) % 3, (axis + 2) % 3
            pos = c[axis] + (1 if sgn > 0 else 0)
            fs.append([rect(axis, pos, c[b], c[b] + 1, c[e], c[e] + 1, sgn)])
    return fs


def well_composed(cells, n):
    """No critical configuration: no diagonal pair of cells around an edge, and no
    2 x 2 x 2 block with only two opposite cells full or only two opposite cells empty."""
    def full(p):
        return p in cells

    for axis in range(3):
        b, e = (axis + 1) % 3, (axis + 2) % 3
        for base in product(range(-1, n + 1), repeat=3):
            q = [[None, None], [None, None]]
            for i, j in product((0, 1), repeat=2):
                p = list(base)
                p[b] += i
                p[e] += j
                q[i][j] = full(tuple(p))
            if q[0][0] == q[1][1] and q[0][1] == q[1][0] and q[0][0] != q[0][1]:
                return False
    for base in product(range(-1, n + 1), repeat=3):
        blk = {(i, j, k): full((base[0] + i, base[1] + j, base[2] + k)) for i, j, k in product((0, 1), repeat=3)}
        cnt = sum(blk.values())
        for i, j, k in product((0, 1), repeat=3):
            a, o = blk[(i, j, k)], blk[(1 - i, 1 - j, 1 - k)]
            if cnt == 2 and a and o:
                return False
            if cnt == 6 and not a and not o:
                return False
    return True


def components(cells):
    """The number of 6-connected components of a set of cells (flood fill)."""
    seen, count = set(), 0
    for c in cells:
        if c in seen:
            continue
        count += 1
        seen.add(c)
        stack = [c]
        while stack:
            x = stack.pop()
            for d in DIRS:
                y = (x[0] + d[0], x[1] + d[1], x[2] + d[2])
                if y in cells and y not in seen:
                    seen.add(y)
                    stack.append(y)
    return count


def cubical_euler(cells):
    """V - E + F - C of the union of the closed unit cubes."""
    verts, edges, squares = set(), set(), set()
    for c in cells:
        x, y, z = c
        for i, j, k in product((0, 1), repeat=3):
            verts.add((2 * (x + i), 2 * (y + j), 2 * (z + k)))
        for axis in range(3):
            for i, j in product((0, 1), repeat=2):
                p = [2 * x, 2 * y, 2 * z]
                p[axis] += 1
                p[(axis + 1) % 3] += 2 * i
                p[(axis + 2) % 3] += 2 * j
                edges.add(tuple(p))
                q = [2 * x + 1, 2 * y + 1, 2 * z + 1]
                q[axis] = 2 * (c[axis] + i)
                squares.add(tuple(q))
    return len(verts) - len(edges) + len(squares) - len(cells)


def scan_checks(b, pts, faces):
    """Each query of the B-rep against a direct scan of the input face list."""
    used = {}
    for f, loops in enumerate(faces):
        for loop in loops:
            for i, u in enumerate(loop):
                used[(u, loop[(i + 1) % len(loop)])] = f
    assert b.face_boundary(0) == faces[0]
    for f, loops in enumerate(faces):
        assert b.face_boundary(f) == loops
        scan_adj = {used[(v, u)] for (u, v), g in used.items() if g == f}
        assert b.adjacent_faces(f) == scan_adj
    for (u, v), f in used.items():
        assert b.edge_faces(u, v) == (f, used[(v, u)])
    for v in range(len(pts)):
        scan_nb = {w for (u, w) in used if u == v}
        nb = b.neighbors(v)
        assert len(nb) == len(scan_nb) and set(nb) == scan_nb
        scan_faces = sorted(f for (u, w), f in used.items() if u == v)
        fa = b.faces_around(v)
        assert sorted(fa) == scan_faces
        # the edge to the next neighbor lies between consecutive faces around v
        for i, w in enumerate(nb):
            w_next = nb[(i + 1) % len(nb)]
            assert used[(v, w)] == fa[i]
            assert used[(w_next, v)] == fa[i]


def random_cells(rng, k):
    """Random cells: a random subset of a cube for even k, a drilled plate for odd k."""
    if k % 2 == 0:
        n = rng.choice((2, 3, 3, 4))
        p = rng.choice((0.4, 0.6, 0.8))
        return {c for c in product(range(n), repeat=3) if rng.random() < p}, n
    dims = (rng.choice((3, 4, 5)), rng.choice((3, 4, 5)), rng.choice((1, 2, 3)))
    drill = {(x, y) for x in range(1, dims[0] - 1) for y in range(1, dims[1] - 1) if rng.random() < 0.4}
    cells = {c for c in product(*(range(d) for d in dims)) if (c[0], c[1]) not in drill and rng.random() >= 0.05}
    if min(dims) >= 3 and rng.random() < 0.5:  # a cavity of one cell
        cells.discard(tuple(rng.randrange(1, d - 1) for d in dims))
    return cells, max(dims)


def test_random_voxel_solids():
    rng = random.Random(20260)
    tested = rejected = with_holes = with_cavities = 0
    k = 0
    while tested < 600:
        k += 1
        cells, n = random_cells(rng, k)
        if not cells:
            continue
        wc = well_composed(cells, n)
        try:
            b, pts, faces = make(voxel_faces(cells))
            counts = b.validate()
            ok = True
        except InvalidBRep:
            ok = False
        assert ok == wc
        if not ok:
            rejected += 1
            continue
        tested += 1
        empty = {c for c in product(range(-1, n + 1), repeat=3) if c not in cells}
        shells = components(cells) + components(empty) - 1
        holes = shells - cubical_euler(cells)
        assert counts["S"] == shells and counts["H"] == holes
        assert counts["F"] == len(faces) and counts["R"] == 0
        assert counts["V"] - counts["E"] + counts["F"] - counts["R"] == 2 * (counts["S"] - counts["H"])
        assert b.volume() == len(cells)
        scan_checks(b, pts, faces)
        with_holes += counts["H"] > 0
        with_cavities += counts["S"] > components(cells)
    assert rejected > 0 and with_holes >= 50 and with_cavities >= 5
