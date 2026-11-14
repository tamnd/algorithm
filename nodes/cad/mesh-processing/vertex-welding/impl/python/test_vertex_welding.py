# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-welding/. The authors are listed in prov/09QVC4.jsonl.

import random
from fractions import Fraction

from vertex_welding import clean_face, weld, weld_classes

# ---- brute force: all pairs, then the components of the eps-graph ----


def brute_classes(points, eps):
    n = len(points)
    adj = [[j for j in range(n) if j != i and
            sum((a - b) ** 2 for a, b in zip(points[i], points[j])) <= eps * eps] for i in range(n)]
    rep = [-1] * n
    for s in range(n):
        if rep[s] != -1:
            continue
        rep[s] = s
        stack = [s]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if rep[y] == -1:
                    rep[y] = s
                    stack.append(y)
    return rep


# ---- tests ----


def test_page_example_square_soup():
    d = Fraction(1, 10000)
    pts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (d, 0, 0), (1, 1 + d, 0), (0, 1, 0)]
    r = weld(pts, [(0, 1, 2), (3, 4, 5)], Fraction(1, 1000))
    assert r.new_index == [0, 1, 2, 0, 2, 3]
    assert r.faces == [(0, 1, 2), (0, 2, 3)]
    assert r.points[0] == (0, 0, 0) and r.dropped == [] and r.non_manifold_edges == []


def test_chaining():
    eps = Fraction(1)
    pts = [(Fraction(9, 10) * k, 0, 0) for k in range(5)]  # neighbours 0.9 apart, ends 3.6 apart
    assert weld_classes(pts, eps) == [0, 0, 0, 0, 0]
    pts2 = [(0, 0, 0), (1, 0, 0), (Fraction(21, 10), 0, 0)]  # exactly eps counts, more does not
    assert weld_classes(pts2, eps) == [0, 0, 2]


def test_collapsed_faces_and_new_non_manifold_edges():
    eps = Fraction(1, 100)
    pts = [(0, 0, 0), (1, 0, 0), (Fraction(1, 1000), 0, 0), (0, 1, 0)]
    r = weld(pts, [(0, 1, 2), (0, 1, 3)], eps)
    assert r.dropped == [0] and r.faces == [(0, 1, 2)]
    # three sheets of triangles meeting along one edge after welding
    pts = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0), (0, 0, 1),
           (0, 0, 0), (1, 0, 0), (0, -1, 0)]
    r = weld(pts, [(0, 1, 2), (3, 4, 5), (6, 7, 8)], eps)
    assert r.non_manifold_edges == [(0, 1)]


def test_clean_face():
    assert clean_face([1, 1, 2, 3, 3, 1]) == (1, 2, 3)
    assert clean_face([4, 4, 4]) == (4,)


def test_against_brute_force_random():
    rng = random.Random(1996)
    for it in range(700):
        n = rng.randint(1, 30)
        eps = Fraction(rng.randint(1, 6), rng.randint(1, 4))
        centres = [tuple(Fraction(rng.randint(-20, 20), 2) for _ in range(3)) for _ in range(rng.randint(1, 6))]
        pts = []
        for _ in range(n):
            c = rng.choice(centres)
            pts.append(tuple(x + Fraction(rng.randint(-8, 8), 4) for x in c))
        if it % 5 == 0:  # points on cell borders and at exact distance eps
            pts = [tuple(eps * rng.randint(-3, 3) for _ in range(3)) for _ in range(n)]
        assert weld_classes(pts, eps) == brute_classes(pts, eps)
        faces = [tuple(rng.sample(range(n), 3)) for _ in range(rng.randint(0, 8))] if n >= 3 else []
        r = weld(pts, faces, eps)
        rep = brute_classes(pts, eps)
        reps = sorted(set(rep))
        assert len(r.points) == len(reps)
        for f, face in enumerate(faces):
            mapped = [reps.index(rep[v]) for v in face]
            if len(set(mapped)) == 3:
                assert tuple(mapped) in r.faces
            else:
                assert f in r.dropped


def test_two_dimensional_points():
    pts = [(0, 0), (Fraction(1, 2), 0), (5, 5)]
    assert weld_classes(pts, Fraction(1, 2)) == [0, 0, 2]
