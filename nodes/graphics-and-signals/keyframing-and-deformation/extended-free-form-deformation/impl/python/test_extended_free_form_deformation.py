# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-free-form-deformation/. The authors are listed in prov/7CMXN6.jsonl.
import math
import random

from extended_free_form_deformation import NOT_FOUND, deform, embed, quarter_ring_lattice


def close(a, b, eps=1e-9):
    return all(abs(x - y) <= eps for x, y in zip(a, b))


def test_newton_recovers_the_local_coordinates():
    chunks, pts, _ = quarter_ring_lattice()
    rng = random.Random(11)
    for _ in range(40):
        c = rng.randrange(2)
        w = tuple(rng.uniform(0.02, 0.98) for _ in range(3))
        x = chunks[c].evaluate(pts, w)
        hit = embed(chunks, pts, x)
        assert hit is not NOT_FOUND
        c2, w2 = hit
        assert close(chunks[c2].evaluate(pts, w2), x)
        assert c2 == c
        assert close(w2, w, 1e-8)


def test_undeformed_lattice_is_identity():
    chunks, pts, _ = quarter_ring_lattice()
    rng = random.Random(12)
    for _ in range(30):
        c = rng.randrange(2)
        x = chunks[c].evaluate(pts, [rng.random() for _ in range(3)])
        assert close(deform(chunks, pts, pts, x), x)


def test_worked_example():
    chunks, pts, index = quarter_ring_lattice()
    x = chunks[0].evaluate(pts, (0.5, 0.5, 0.5))
    assert close(x, (1.125, 1.125, 0.5))
    moved = list(pts)
    for k in range(2):
        p = index[(1, 1, k)]
        moved[p] = (2.5, 2.5, moved[p][2])
    y = deform(chunks, pts, moved, x)
    assert close(y, (1.25, 1.25, 0.5))


def test_shared_face_is_continuous():
    chunks, pts, index = quarter_ring_lattice()
    rng = random.Random(13)
    moved = [tuple(v + rng.uniform(-0.2, 0.2) for v in p) for p in pts]
    for _ in range(20):
        t, u = rng.random(), rng.random()
        a = chunks[0].evaluate(moved, (1.0, t, u))
        b = chunks[1].evaluate(moved, (0.0, t, u))
        assert close(a, b, 1e-12)
        # Points just on each side of the shared face map to nearby points.
        eps = 1e-7
        xa = chunks[0].evaluate(pts, (1 - eps, t, u))
        xb = chunks[1].evaluate(pts, (eps, t, u))
        ya = deform(chunks, pts, moved, xa)
        yb = deform(chunks, pts, moved, xb)
        assert math.dist(ya, yb) < 1e-5


def test_point_outside_is_not_found():
    chunks, pts, _ = quarter_ring_lattice()
    for x in ((0.2, 0.2, 0.5), (3.0, 0.0, 0.5), (0.0, -1.5, 0.5), (1.2, 1.2, 1.5), (1.2, 1.2, -0.1)):
        assert embed(chunks, pts, x) is NOT_FOUND
        assert deform(chunks, pts, pts, x) is NOT_FOUND


def test_affine_motion_of_all_points_is_reproduced():
    chunks, pts, _ = quarter_ring_lattice()
    rng = random.Random(14)
    a = [[rng.uniform(-1, 1) + (2 if r == c else 0) for c in range(3)] for r in range(3)]
    b = [rng.uniform(-1, 1) for _ in range(3)]

    def aff(p):
        return tuple(sum(a[r][c] * p[c] for c in range(3)) + b[r] for r in range(3))

    moved = [aff(p) for p in pts]
    for _ in range(20):
        c = rng.randrange(2)
        x = chunks[c].evaluate(pts, [rng.random() for _ in range(3)])
        assert close(deform(chunks, pts, moved, x), aff(x), 1e-8)
