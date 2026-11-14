# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tutte-embedding/. The authors are listed in prov/BD4HAH.jsonl.

import random
from fractions import Fraction

from mp3geom import boundary_loop, directed_edges, euler_characteristic, neighbours, orient2d
from tutte_embedding import circle_polygon, is_valid_embedding, mean_value_weights, tutte_embedding, uniform_weights


def random_disk(rng, steps):
    """A random triangulated disk (a simplicial complex), oriented counterclockwise.

    It starts from one triangle and applies random 1-to-3 face splits, inner
    edge splits, boundary ears and inner edge flips.
    """
    faces = [(0, 1, 2)]
    nv = 3
    for _ in range(steps):
        op = rng.randrange(4)
        de = directed_edges(faces)
        if op == 0:
            f = rng.randrange(len(faces))
            a, b, c = faces.pop(f)
            faces += [(a, b, nv), (b, c, nv), (c, a, nv)]
            nv += 1
        elif op == 1:
            inner = [e for e in de if (e[1], e[0]) in de and e[0] < e[1]]
            if not inner:
                continue
            a, b = rng.choice(inner)
            f1, k1 = de[(a, b)]
            f2, k2 = de[(b, a)]
            c = faces[f1][(k1 + 2) % 3]
            d = faces[f2][(k2 + 2) % 3]
            faces = [t for g, t in enumerate(faces) if g not in (f1, f2)]
            faces += [(a, nv, c), (nv, b, c), (b, nv, d), (nv, a, d)]
            nv += 1
        elif op == 2:
            bd = [e for e in de if (e[1], e[0]) not in de]
            a, b = rng.choice(bd)
            faces.append((b, a, nv))
            nv += 1
        else:
            inner = [e for e in de if (e[1], e[0]) in de and e[0] < e[1]]
            if not inner:
                continue
            a, b = rng.choice(inner)
            f1, k1 = de[(a, b)]
            f2, k2 = de[(b, a)]
            c = faces[f1][(k1 + 2) % 3]
            d = faces[f2][(k2 + 2) % 3]
            nb = neighbours(faces)
            if d in nb[c] or len(nb[a]) <= 3 or len(nb[b]) <= 3:
                continue
            faces = [t for g, t in enumerate(faces) if g not in (f1, f2)]
            faces += [(c, d, b), (d, c, a)]
    return faces


def random_weights(rng, faces):
    nb = neighbours(faces)
    w = {}
    for i in nb:
        raw = {j: Fraction(rng.randint(1, 9)) for j in nb[i]}
        s = sum(raw.values())
        w[i] = {j: x / s for j, x in raw.items()}
    return w


def polygon_area2(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))


def check_embedding(faces, corners, weights, pos):
    loop = boundary_loop(faces)
    for v, c in zip(loop, corners):
        assert pos[v] == tuple(c)
    for i in weights:
        if i in loop:
            continue
        avg = (sum(l * pos[j][0] for j, l in weights[i].items()), sum(l * pos[j][1] for j, l in weights[i].items()))
        assert avg == pos[i]
    assert is_valid_embedding(faces, pos)
    assert sum(orient2d(pos[a], pos[b], pos[c]) for a, b, c in faces) == polygon_area2(corners)


def test_example_of_the_page() -> None:
    faces = [(0, 1, 4), (1, 5, 4), (1, 2, 5), (2, 3, 5), (3, 4, 5), (3, 0, 4)]
    corners = [(0, 0), (12, 0), (12, 12), (0, 12)]
    pos = tutte_embedding(faces, corners)
    assert pos[4] == (Fraction(24, 5), Fraction(24, 5))
    assert pos[5] == (Fraction(36, 5), Fraction(36, 5))
    check_embedding(faces, corners, uniform_weights(faces), pos)


def test_random_disks_have_no_flipped_triangle() -> None:
    rng = random.Random(20260512)
    for trial in range(40):
        faces = random_disk(rng, rng.randint(3, 30))
        assert euler_characteristic(faces) == 1
        k = len(boundary_loop(faces))
        corners = circle_polygon(k)
        for weights in (uniform_weights(faces), random_weights(rng, faces)):
            pos = tutte_embedding(faces, corners, weights)
            check_embedding(faces, corners, weights, pos)


def test_integer_convex_polygon() -> None:
    # The points (i, i^2) are in strictly convex position, counterclockwise.
    rng = random.Random(7)
    for _ in range(20):
        faces = random_disk(rng, 25)
        k = len(boundary_loop(faces))
        parabola = [(i, i * i) for i in range(k)]
        w = random_weights(rng, faces)
        check_embedding(faces, parabola, w, tutte_embedding(faces, parabola, w))


def test_nonconvex_boundary_can_flip() -> None:
    # A wheel: centre 5, boundary 0..4 on a non-convex arrow.
    faces = [(0, 1, 5), (1, 2, 5), (2, 3, 5), (3, 4, 5), (4, 0, 5)]
    corners = [(0, 0), (10, 0), (10, 10), (9, 1), (0, 1)]
    pos = tutte_embedding(faces, corners)
    assert pos[5] == (Fraction(29, 5), Fraction(12, 5))
    assert min(orient2d(pos[a], pos[b], pos[c]) for a, b, c in faces) < 0
    assert not is_valid_embedding(faces, pos)


def test_mean_value_weights_reproduce_a_planar_mesh() -> None:
    rng = random.Random(11)
    done = 0
    while done < 10:
        faces = random_disk(rng, 20)
        k = len(boundary_loop(faces))
        corners = circle_polygon(k)
        planar = tutte_embedding(faces, corners, random_weights(rng, faces))
        w = mean_value_weights(planar, faces)
        assert all(x > 0 for i in w for x in w[i].values())
        again = tutte_embedding(faces, [tuple(float(c) for c in p) for p in corners], w)
        for v in planar:
            assert abs(again[v][0] - float(planar[v][0])) < 1e-9
            assert abs(again[v][1] - float(planar[v][1])) < 1e-9
        done += 1


def nested_triangles(layers):
    """Triangles a_t b_t c_t, t = 0..layers, each joined to the next by a band of 6 triangles."""
    faces = []
    for t in range(layers):
        a, b, c, a2, b2, c2 = 3 * t, 3 * t + 1, 3 * t + 2, 3 * t + 3, 3 * t + 4, 3 * t + 5
        faces += [(a, b, a2), (b, b2, a2), (b, c, b2), (c, c2, b2), (c, a, c2), (a, a2, c2)]
    faces.append((3 * layers, 3 * layers + 1, 3 * layers + 2))
    return faces


def test_nested_triangles_exact_and_float() -> None:
    faces = nested_triangles(30)
    corners = [(0, 0), (1, 0), (0, 1)]
    exact = tutte_embedding(faces, corners)
    signs = [orient2d(exact[a], exact[b], exact[c]) for a, b, c in faces]
    assert all(s > 0 for s in signs)
    assert min(signs) < Fraction(1, 10**49)
    w = {i: {j: float(x) for j, x in d.items()} for i, d in uniform_weights(faces).items()}
    approx = tutte_embedding(faces, [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], w)
    wrong = sum(1 for a, b, c in faces if not orient2d(approx[a], approx[b], approx[c]) > 0)
    assert wrong > 0


def test_circle_polygon_is_strictly_convex() -> None:
    for k in range(3, 40):
        pts = circle_polygon(k)
        assert all(x * x + y * y == 1 for x, y in pts)
        for i in range(k):
            for j in range(k):
                if j not in (i, (i + 1) % k):
                    assert orient2d(pts[i], pts[(i + 1) % k], pts[j]) > 0
