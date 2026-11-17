# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cage-based-deformation/. The authors are listed in prov/K9W6TX.jsonl.
import math
import random

from cage_based_deformation import Binding, mean_value_coordinates

L_SHAPE = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
SQUARE = [(0, 0), (1, 0), (1, 1), (0, 1)]


def inside_l(p):
    return 0 < p[0] < 2 and 0 < p[1] < 2 and not (p[0] >= 1 and p[1] >= 1)


def sample(rng, count):
    out = []
    while len(out) < count:
        p = (rng.uniform(0, 2), rng.uniform(0, 2))
        if inside_l(p):
            out.append(p)
    return out


def test_partition_of_unity_and_linear_precision():
    rng = random.Random(71)
    for p in sample(rng, 50):
        w = mean_value_coordinates(p, L_SHAPE)
        assert abs(sum(w) - 1) < 1e-12
        x = sum(a * c[0] for a, c in zip(w, L_SHAPE))
        y = sum(a * c[1] for a, c in zip(w, L_SHAPE))
        assert math.dist((x, y), p) < 1e-12


def test_square_center_and_vertices():
    w = mean_value_coordinates((0.5, 0.5), SQUARE)
    assert all(abs(a - 0.25) < 1e-12 for a in w)
    assert mean_value_coordinates((1, 0), SQUARE) == [0.0, 1.0, 0.0, 0.0]
    w = mean_value_coordinates((0.25, 0.0), SQUARE)
    assert abs(w[0] - 0.75) < 1e-12 and abs(w[1] - 0.25) < 1e-12


def test_negative_weight_in_nonconvex_cage():
    w = mean_value_coordinates((0.875, 1.375), L_SHAPE)
    assert abs(w[2] + 0.0097336) < 1e-6


def test_nonnegative_in_convex_cage():
    rng = random.Random(72)
    hexagon = [(math.cos(k * math.pi / 3), math.sin(k * math.pi / 3)) for k in range(6)]
    for _ in range(50):
        p = (rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8))
        if math.hypot(*p) < 0.85:
            assert min(mean_value_coordinates(p, hexagon)) > 0


def test_identity_and_affine_invariance():
    rng = random.Random(73)
    pts = sample(rng, 30)
    b = Binding(pts, L_SHAPE)
    assert all(math.dist(p, q) < 1e-12 for p, q in zip(pts, b.deform(L_SHAPE)))

    def aff(p):
        return (1.3 * p[0] - 0.4 * p[1] + 2.0, 0.2 * p[0] + 0.9 * p[1] - 1.0)

    moved = b.deform([aff(c) for c in L_SHAPE])
    assert all(math.dist(aff(p), q) < 1e-12 for p, q in zip(pts, moved))
    # The coordinates do not change under a similarity of the cage and the point.
    for p in pts[:10]:
        w1 = mean_value_coordinates(p, L_SHAPE)
        sim = [(2 * c[0] + 1, 2 * c[1] - 3) for c in L_SHAPE]
        w3 = mean_value_coordinates((2 * p[0] + 1, 2 * p[1] - 3), sim)
        assert max(abs(a - c) for a, c in zip(w1, w3)) < 1e-12


def test_worked_example():
    # Slide the top edge of the L by 0.5 to the right; the point (0.5, 1.5) follows by about 0.346.
    moved = [(0, 0), (2, 0), (2, 1), (1, 1), (1.5, 2), (0.5, 2)]
    (q,) = Binding([(0.5, 1.5)], L_SHAPE).deform(moved)
    assert abs(q[0] - 0.8463525) < 1e-6 and abs(q[1] - 1.5) < 1e-12


def test_point_on_line_of_edge():
    # (1, 0.5) is on the line x = 1 of the edge (1, 1) -> (1, 2), but not on it.
    w = mean_value_coordinates((1.0, 0.5), L_SHAPE)
    assert abs(sum(w) - 1) < 1e-12
    x = sum(a * c[0] for a, c in zip(w, L_SHAPE))
    y = sum(a * c[1] for a, c in zip(w, L_SHAPE))
    assert math.dist((x, y), (1.0, 0.5)) < 1e-12
