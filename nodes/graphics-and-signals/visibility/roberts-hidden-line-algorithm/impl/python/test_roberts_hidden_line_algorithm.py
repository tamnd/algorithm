# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roberts-hidden-line-algorithm/. The authors are listed in prov/T1KFDC.jsonl.

import random
from fractions import Fraction as F

from roberts_hidden_line_algorithm import ConvexBody, box, roberts_hidden_lines


def hidden_at(point, bodies, eye):
    """Exact per-sample depth test against every body, its own body included.

    The point is hidden if some alpha > 0 puts point + alpha e strictly
    inside a body, that is, with every f_k < 0.
    """
    h = (point[0], point[1], point[2], F(1))
    for body in bodies:
        lo, hi = F(0), None
        empty = False
        for k in range(len(body.planes)):
            c = body.value(k, h)
            d = body.value(k, eye)
            if d == 0:
                if c >= 0:
                    empty = True
                    break
            elif d > 0:  # c + alpha d < 0  <=>  alpha < -c / d
                bound = -c / d
                hi = bound if hi is None else min(hi, bound)
            else:  # alpha > -c / d
                lo = max(lo, -c / d)
        if empty:
            continue
        if hi is None or lo < hi:
            return True
    return False


def check(bodies, eye, rng, samples=6):
    eye = tuple(F(c) for c in eye)
    result = roberts_hidden_lines(bodies, eye)
    total = sum(len(b.edges) for b in bodies)
    assert len(result) == total
    for bi, (u, v), pieces in result:
        p0, p1 = bodies[bi].vertices[u], bodies[bi].vertices[v]
        cuts = sorted({F(0), F(1)} | {t for piece in pieces for t in piece})
        ts = [(a + b) / 2 for a, b in zip(cuts, cuts[1:])]
        ts += [F(rng.randint(1, 9998), 9999) for _ in range(samples)]
        for t in ts:
            if t in cuts:
                continue
            p = tuple(p0[k] + t * (p1[k] - p0[k]) for k in range(3))
            seen = any(a < t < b for a, b in pieces)
            assert seen == (not hidden_at(p, bodies, eye)), (bi, (u, v), t, pieces)
        for a, b in pieces:
            assert 0 <= a < b <= 1
    return result


def affine_body(rng, kind, scale=6, spread=10):
    if kind == "tetra":
        base = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    else:
        base = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
        faces = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
    while True:
        m = [[F(rng.randint(-scale, scale), 2) for _ in range(3)] for _ in range(3)]
        det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
               - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
               + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        if det != 0:
            break
    off = [F(rng.randint(-spread, spread)) for _ in range(3)]
    verts = [tuple(sum(m[r][c] * p[c] for c in range(3)) + off[r] for r in range(3)) for p in base]
    return ConvexBody(verts, faces)


def test_cube_above_slab_orthographic():
    big = box((0, 0, 0), (4, 4, 1))
    small = box((1, 1, 2), (2, 2, 3))
    rng = random.Random(1)
    result = check([big, small], (1, 2, 5, 0), rng)
    # The eye is far above, so the small cube is fully visible except for
    # the edges hidden by its own front faces.
    hidden_small = [e for bi, e, p in result if bi == 1 and not p]
    assert len(hidden_small) == 3


def test_cube_in_front_of_cube_perspective():
    back = box((0, 0, 0), (2, 2, 2))
    front = box((F(1, 2), F(1, 2), 4), (F(3, 2), F(3, 2), 5))
    rng = random.Random(2)
    result = check([back, front], (1, 1, 10, 1), rng)
    # The front cube hides no edge of the back cube completely: from the eye
    # at (1, 1, 10) its shadow on the plane z = 2 is a square inside the top face.
    for bi, e, pieces in result:
        if bi == 0:
            assert pieces in ([], [(0, 1)])


def test_partial_hiding():
    # A thin plate in front hides the middle of a long edge.
    rod = box((0, 0, 0), (10, 1, 1))
    plate = box((4, -5, 3), (6, 5, 4))
    rng = random.Random(3)
    result = check([rod, plate], (0, 0, 1, 0), rng)
    top = [p for bi, (u, v), p in result
           if bi == 0 and rod.vertices[u][2] == 1 and rod.vertices[v][2] == 1
           and rod.vertices[u][1] == rod.vertices[v][1]]
    assert top and all(p == [(0, F(2, 5)), (F(3, 5), 1)] for p in top)


def test_random_scenes_orthographic():
    rng = random.Random(10)
    for _ in range(40):
        bodies = [affine_body(rng, rng.choice(["tetra", "box"])) for _ in range(rng.randint(2, 4))]
        d = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(1, 4), 0)
        check(bodies, d, rng)


def test_random_scenes_perspective():
    rng = random.Random(20)
    done = 0
    while done < 30:
        bodies = [affine_body(rng, rng.choice(["tetra", "box"])) for _ in range(rng.randint(2, 4))]
        eye = (rng.randint(-8, 8), rng.randint(-8, 8), rng.randint(40, 60), 1)
        e = tuple(F(c) for c in eye)
        if any(all(b.value(k, e) <= 0 for k in range(len(b.planes))) for b in bodies):
            continue  # the eye must be outside every body
        check(bodies, eye, rng)
        done += 1


def test_back_edges_of_one_body():
    # One convex body alone: an edge is hidden exactly when both faces face away.
    rng = random.Random(30)
    for _ in range(30):
        body = affine_body(rng, rng.choice(["tetra", "box"]))
        d = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(1, 4), 0)
        result = check([body], d, rng)
        for _, e, pieces in result:
            assert pieces in ([], [(0, 1)])
