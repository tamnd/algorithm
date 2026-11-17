# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wire-deformation/. The authors are listed in prov/TTFYST.jsonl.
import math
import random

from wire_deformation import closest_parameter, default_falloff, deform, deform_many, point_at


def close(a, b, eps=1e-12):
    return all(abs(x - y) <= eps for x, y in zip(a, b))


REF = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (3.0, 0.0, 0.0)]


def test_wire_equal_to_reference_is_identity():
    rng = random.Random(31)
    ref = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(6)]
    for _ in range(30):
        p = tuple(rng.uniform(-1.5, 1.5) for _ in range(3))
        assert close(deform(p, ref, ref, 0.8), p)


def test_far_points_do_not_move():
    wire = [(x, y + 1.0, z) for x, y, z in REF]
    rng = random.Random(32)
    for _ in range(30):
        p = (rng.uniform(-1, 4), rng.uniform(-3, 3), rng.uniform(-3, 3))
        _, d = closest_parameter(REF, p)
        if d >= 0.5:
            assert deform(p, REF, wire, 0.5, s=2.0) == p


def test_point_on_reference_follows_the_wire():
    wire = [(0.0, 0.0, 0.0), (1.0, 0.5, 0.0), (2.0, 0.5, 0.5), (3.0, 1.0, 0.0)]
    for u in (0.0, 0.3, 1.0, 1.75, 2.5, 3.0):
        p = point_at(REF, u)
        assert close(deform(p, REF, wire, 0.7, s=1.5), point_at(wire, u), 1e-12)


def test_translated_straight_wire_moves_points_by_falloff_times_offset():
    t = (0.0, 0.25, -0.5)
    wire = [tuple(a + b for a, b in zip(v, t)) for v in REF]
    rng = random.Random(33)
    for _ in range(30):
        p = (rng.uniform(0.2, 2.8), rng.uniform(-1, 1), rng.uniform(-1, 1))
        _, d = closest_parameter(REF, p)
        f = default_falloff(d / 1.2)
        q = deform(p, REF, wire, 1.2)
        assert close(q, tuple(a + f * b for a, b in zip(p, t)), 1e-12)


def test_worked_example():
    # A point at distance 0.5 from a straight wire of radius 1: F = (1 - 0.25)^2 = 0.5625.
    wire = [(x, 1.0, 0.0) for x, _, _ in REF]
    q = deform((1.5, 0.5, 0.0), REF, wire, 1.0)
    assert close(q, (1.5, 0.5 + 0.5625, 0.0))
    # With s = 2 the offset 0.5 from R grows to 0.5 (1 + 0.5625) first.
    q2 = deform((1.5, 0.5, 0.0), REF, wire, 1.0, s=2.0)
    assert close(q2, (1.5, 0.5 * 1.5625 + 0.5625, 0.0))


def test_closest_point_matches_dense_sampling():
    rng = random.Random(34)
    ref = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(5)]
    for _ in range(20):
        p = tuple(rng.uniform(-1.5, 1.5) for _ in range(3))
        u, d = closest_parameter(ref, p)
        best = min(math.dist(p, point_at(ref, k / 1000)) for k in range(4001))
        assert d <= best + 1e-12
        assert best - d < 2e-3
        assert abs(math.dist(p, point_at(ref, u)) - d) < 1e-12


def test_falloff_shape():
    assert default_falloff(0.0) == 1.0
    assert default_falloff(1.0) == 0.0
    h = 1e-6
    assert abs((default_falloff(1.0) - default_falloff(1.0 - h)) / h) < 1e-5
    xs = [k / 100 for k in range(101)]
    vals = [default_falloff(x) for x in xs]
    assert all(a >= b for a, b in zip(vals, vals[1:]))


def test_rotation_turns_offsets_with_the_tangent():
    # Turn a straight wire by 90 degrees about its first vertex in the xy plane.
    ref = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    wire = [(0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    # A point at u = 0 with offset (0, 0, 0.2): the axis is z, so it does not turn.
    q = deform((0.0, 0.0, 0.2), ref, wire, 10.0)
    assert close(q, (0.0, 0.0, 0.2), 1e-12)
    # With a big radius F is near 1 and an offset along y turns towards -x.
    q = deform((0.0, 0.2, 0.0), ref, wire, 1e6)
    assert close(q, (-0.2, 0.0, 0.0), 1e-9)


def test_many_wires():
    w1 = [(x, 1.0, 0.0) for x, _, _ in REF]
    p = (1.5, 0.5, 0.0)
    single = deform(p, REF, w1, 1.0)
    assert close(deform_many(p, [(REF, w1, 1.0, 1.0)]), single)
    # Two equal wires give the same result as one.
    assert close(deform_many(p, [(REF, w1, 1.0, 1.0), (REF, w1, 1.0, 1.0)], m=2.0), single)
    # A wire that does not move adds a zero move with weight 0.
    assert close(deform_many(p, [(REF, w1, 1.0, 1.0), (REF, REF, 1.0, 1.0)], m=1.0), single)
