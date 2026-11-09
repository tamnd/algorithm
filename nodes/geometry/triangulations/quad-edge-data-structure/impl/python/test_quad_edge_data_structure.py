# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quad-edge-data-structure/. The authors are listed in prov/77AC3G.jsonl.
import random
from fractions import Fraction

from quad_edge_data_structure import QuadEdge, fan, insert_in_face, polygon


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def incircle(a, b, c, d):
    rows = [(p[0] - d[0], p[1] - d[1]) for p in (a, b, c)]
    m = [(x, y, x * x + y * y) for x, y in rows]
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def area2(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts)))


def proper_cross(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return False
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def check_axioms(qe):
    """The edge algebra laws of Guibas and Stolfi on every directed edge."""
    for q, ok in enumerate(qe.alive):
        if not ok:
            continue
        for r in range(4):
            e = 4 * q + r
            assert qe.rot(qe.rot(qe.rot(qe.rot(e)))) == e
            assert qe.rot(qe.rot(e)) != e
            assert qe.rot(qe.onext(qe.rot(qe.onext(e)))) == e
            assert qe.lnext(e) == qe.oprev(qe.sym(e))
            assert qe.onext(qe.oprev(e)) == e
            assert qe.alive[qe.onext(e) >> 2]


def check_subdivision(qe, outer_area2, vertices):
    """Faces, Euler's formula, rings, exact areas and no crossings."""
    check_axioms(qe)
    faces = qe.faces()
    edges = qe.edges()
    v = len(vertices)
    assert v - len(edges) + len(faces) == 2
    inner = [f for f in faces if area2([qe.org(e) for e in f]) > 0]
    outer = [f for f in faces if area2([qe.org(e) for e in f]) <= 0]
    assert len(outer) == 1
    for f in faces:
        for e in f:
            assert qe.dest(e) == qe.org(qe.lnext(e))
    assert sum(area2([qe.org(e) for e in f]) for f in inner) == outer_area2
    assert -area2([qe.org(e) for e in outer[0]]) == outer_area2
    for e in edges:
        ring = qe.vertex_ring(e)
        assert all(qe.org(f) == qe.org(e) for f in ring)
    segs = [(qe.org(e), qe.dest(e)) for e in edges]
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            assert not proper_cross(*segs[i], *segs[j])
    return inner, outer[0]


def check_ccw_rings(qe):
    """Around every vertex the edges must come in counterclockwise order."""
    for e in qe.edges():
        for d in (e, qe.sym(e)):
            ring = qe.vertex_ring(d)
            if len(ring) < 3:
                continue
            o = qe.org(d)
            turns = 0
            for i in range(len(ring)):
                a = qe.dest(ring[i])
                b = qe.dest(ring[(i + 1) % len(ring)])
                if orient(o, a, b) < 0:
                    turns += 1
            assert turns <= 1


def test_make_edge():
    qe = QuadEdge()
    e = qe.make_edge((0, 0), (1, 0))
    assert qe.onext(e) == e and qe.onext(qe.sym(e)) == qe.sym(e)
    assert qe.onext(qe.rot(e)) == qe.rot_inv(e)
    assert qe.lnext(e) == qe.sym(e)
    assert len(qe.faces()) == 1
    check_axioms(qe)


def test_splice_is_an_involution():
    qe = QuadEdge()
    a = qe.make_edge((0, 0), (1, 0))
    b = qe.make_edge((0, 0), (0, 1))
    before = list(qe.nxt)
    qe.splice(a, b)
    assert qe.onext(a) == b and qe.onext(b) == a
    check_axioms(qe)
    qe.splice(a, b)
    assert qe.nxt == before


def test_polygon_and_fan():
    pts = [(0, 0), (4, 0), (6, 2), (5, 5), (2, 6), (-1, 3)]
    qe = QuadEdge()
    base = polygon(qe, pts)
    inner, _ = check_subdivision(qe, area2(pts), pts)
    assert len(inner) == 1 and len(inner[0]) == 6
    assert [qe.org(e) for e in inner[0]][0] == pts[0]
    fan(qe, base)
    inner, _ = check_subdivision(qe, area2(pts), pts)
    assert len(inner) == len(pts) - 2
    assert all(len(f) == 3 for f in inner)
    assert len(qe.edges()) == 2 * len(pts) - 3
    check_ccw_rings(qe)


def test_flip_in_square():
    pts = [(0, 0), (2, 0), (2, 2), (0, 2)]
    qe = QuadEdge()
    base = polygon(qe, pts)
    fan(qe, base)
    diag = [e for e in qe.edges() if {qe.org(e), qe.dest(e)} == {(0, 0), (2, 2)}]
    assert len(diag) == 1
    qe.flip(diag[0])
    assert {qe.org(diag[0]), qe.dest(diag[0])} == {(2, 0), (0, 2)}
    inner, _ = check_subdivision(qe, area2(pts), pts)
    assert len(inner) == 2


def test_delete_edge_merges_faces():
    pts = [(0, 0), (6, 0), (8, 4), (4, 8), (0, 5)]
    qe = QuadEdge()
    base = polygon(qe, pts)
    fan(qe, base)
    for e in list(qe.edges()):
        ends = {qe.org(e), qe.dest(e)}
        if pts[0] in ends and not ends & {pts[1], pts[-1]}:
            qe.delete_edge(e)
            check_subdivision(qe, area2(pts), pts)
    inner, _ = check_subdivision(qe, area2(pts), pts)
    assert len(inner) == 1 and len(inner[0]) == 5


def locate(qe, p):
    for f in qe.faces():
        pts = [qe.org(e) for e in f]
        if len(f) == 3 and area2(pts) > 0 and all(orient(qe.org(e), qe.dest(e), p) > 0 for e in f):
            return f[0]
    return None


def lawson(qe, frozen):
    """Flip non-Delaunay interior edges until none is left."""
    changed = True
    while changed:
        changed = False
        for e in qe.edges():
            a, b = qe.org(e), qe.dest(e)
            if frozenset((a, b)) in frozen:
                continue
            c = qe.dest(qe.onext(e))
            d = qe.dest(qe.oprev(e))
            if orient(a, b, d) < 0 < orient(a, b, c) and incircle(a, b, c, d) > 0:
                if orient(c, d, a) * orient(c, d, b) < 0:
                    qe.flip(e)
                    changed = True


def test_random_insertions_and_flips():
    rng = random.Random(1985)
    for trial in range(40):
        big = [(-1000, -1000), (1000, -1000), (0, 1000)]
        qe = QuadEdge()
        polygon(qe, big)
        verts = list(big)
        for _ in range(rng.randint(1, 25)):
            p = (rng.randint(-300, 300), rng.randint(-300, 300))
            e = locate(qe, p)
            if e is None or p in verts:
                continue
            insert_in_face(qe, e, p)
            verts.append(p)
        inner, outer = check_subdivision(qe, area2(big), verts)
        assert all(len(f) == 3 for f in inner)
        assert len(inner) == 2 * len(verts) - 3 - 2
        assert len(qe.edges()) == 3 * len(verts) - 3 - 3
        check_ccw_rings(qe)
        hull = {frozenset((big[i], big[(i + 1) % 3])) for i in range(3)}
        lawson(qe, hull)
        inner, _ = check_subdivision(qe, area2(big), verts)
        for f in inner:
            a, b, c = (qe.org(e) for e in f)
            for d in verts:
                if d not in (a, b, c):
                    assert incircle(a, b, c, d) <= 0


def test_fractions():
    pts = [(Fraction(0), Fraction(0)), (Fraction(7, 3), Fraction(0)), (Fraction(5, 2), Fraction(9, 4)),
           (Fraction(1, 5), Fraction(3))]
    qe = QuadEdge()
    base = polygon(qe, pts)
    fan(qe, base)
    e = locate(qe, (Fraction(1), Fraction(1)))
    insert_in_face(qe, e, (Fraction(1), Fraction(1)))
    inner, _ = check_subdivision(qe, area2(pts), pts + [(Fraction(1), Fraction(1))])
    assert len(inner) == 4
