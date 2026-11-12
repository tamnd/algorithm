# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/object-instancing/. The authors are listed in prov/H66630.jsonl.

import math
import random
from fractions import Fraction as Q

from object_instancing import (
    cross,
    det3,
    dot,
    intersect_instance,
    make_instance,
    mat_vec,
    mesh_hitter,
    object_box,
    sub,
    to_world,
    trace_scene,
    triangle_hit,
    unit_sphere_hit,
    world_box,
)


def octahedron():
    v = [(Q(1), Q(0), Q(0)), (Q(-1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(-1), Q(0)), (Q(0), Q(0), Q(1)), (Q(0), Q(0), Q(-1))]
    faces = []
    for x in (0, 1):
        for y in (2, 3):
            for z in (4, 5):
                faces.append((v[x], v[y], v[z]))
    return faces


def random_mesh(rng, k):
    return [tuple(tuple(Q(rng.randint(-8, 8), 4) for _ in range(3)) for _ in range(3)) for _ in range(k)]


def random_matrix(rng):
    while True:
        a = tuple(tuple(Q(rng.randint(-6, 6), 2) for _ in range(3)) for _ in range(3))
        if det3(a) != 0:
            return a


def random_scene(rng):
    meshes = [octahedron(), random_mesh(rng, 6), random_mesh(rng, 4)]
    instances = []
    for _ in range(6):
        shift = tuple(Q(rng.randint(-20, 20), 3) for _ in range(3))
        instances.append(make_instance(rng.randrange(3), random_matrix(rng), shift))
    return meshes, instances


def flat_trace(meshes, instances, o, d):
    """Reference: map every triangle to world space and intersect it directly."""
    best = None
    for idx, inst in enumerate(instances):
        for k, tri in enumerate(meshes[inst["obj"]]):
            world_tri = tuple(to_world(inst, v) for v in tri)
            h = triangle_hit(o, d, world_tri, 0, math.inf)
            if h is not None and (best is None or h[0] < best[0]):
                best = (h[0], idx, k, h[1])
    return best


def test_instanced_scene_equals_flattened_scene_exactly():
    rng = random.Random(41)
    hits = 0
    for _ in range(8):
        meshes, instances = random_scene(rng)
        hitters = [mesh_hitter(m) for m in meshes]
        boxes = [object_box(m) for m in meshes]
        for _ in range(18):
            o = tuple(Q(rng.randint(-40, 40), 4) for _ in range(3))
            tgt = tuple(Q(rng.randint(-12, 12), 3) for _ in range(3))
            d = sub(tgt, o)
            if d == (0, 0, 0):
                continue
            got = trace_scene(instances, hitters, boxes, o, d)
            ref = flat_trace(meshes, instances, o, d)
            assert (got is None) == (ref is None)
            if got is None:
                continue
            hits += 1
            t, idx, k, p, n = got
            assert (t, idx, k) == ref[:3]
            assert p == tuple(o[i] + t * d[i] for i in range(3))
            # The normal of the mapped triangle is det(A) times the inverse transpose normal.
            assert ref[3] == tuple(det3(instances[idx]["a"]) * c for c in n)
    assert hits > 50


def test_inverse_transpose_normal_is_perpendicular_and_matrix_normal_is_not():
    rng = random.Random(42)
    for _ in range(200):
        a = random_matrix(rng)
        inst = make_instance(0, a, (Q(0), Q(0), Q(0)))
        tri = random_mesh(rng, 1)[0]
        n_obj = cross(sub(tri[1], tri[0]), sub(tri[2], tri[0]))
        n_good = mat_vec(tuple(tuple(inst["inv"][j][i] for j in range(3)) for i in range(3)), n_obj)
        for e in (sub(tri[1], tri[0]), sub(tri[2], tri[0])):
            assert dot(n_good, mat_vec(a, e)) == 0
    # Under the non-uniform scale (2, 1, 1), A n is not perpendicular to the mapped tangent.
    a = ((Q(2), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    n_obj, tangent = (Q(-3, 5), Q(4, 5), Q(0)), (Q(-4, 5), Q(-3, 5), Q(0))
    assert dot(n_obj, tangent) == 0
    assert dot(mat_vec(a, n_obj), mat_vec(a, tangent)) == Q(36, 25)


def test_mirror_instance_flips_the_winding():
    a = ((Q(-1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    inst = make_instance(0, a, (Q(0), Q(0), Q(0)))
    tri = ((Q(0), Q(0), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)))  # normal +z in object space
    hit = intersect_instance(inst, mesh_hitter([tri]), (Q(-1, 4), Q(1, 4), Q(5)), (Q(0), Q(0), Q(-1)))
    assert hit[3] == (0, 0, 1)  # the inverse transpose keeps the outward side
    world_tri = tuple(to_world(inst, v) for v in tri)
    assert cross(sub(world_tri[1], world_tri[0]), sub(world_tri[2], world_tri[0])) == (0, 0, -1)


def test_ellipsoid_example():
    a = ((2.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    inst = make_instance(0, a, (4.0, 0.0, 0.0))
    t, p, _, n = intersect_instance(inst, unit_sphere_hit, (0.0, 0.8, 0.0), (1.0, 0.0, 0.0))
    assert math.isclose(t, 2.8) and math.isclose(p[0], 2.8)
    assert math.isclose(n[0], -0.3) and math.isclose(n[1], 0.8) and n[2] == 0
    # A normalized object-space direction would give the object-space distance 1.4, not 2.8.
    t_wrong, _, _ = unit_sphere_hit((-2.0, 0.8, 0.0), (1.0, 0.0, 0.0), 0, math.inf)
    assert math.isclose(t_wrong, 1.4)


def test_float_instances_agree_with_direct_ellipsoid():
    rng = random.Random(43)
    for _ in range(300):
        sx, sy, sz = (rng.uniform(0.5, 3.0) for _ in range(3))
        c = tuple(rng.uniform(-2, 2) for _ in range(3))
        inst = make_instance(0, ((sx, 0, 0), (0, sy, 0), (0, 0, sz)), c)
        o = tuple(rng.uniform(-10, 10) for _ in range(3))
        d = tuple(rng.uniform(-1, 1) for _ in range(3))
        h = intersect_instance(inst, unit_sphere_hit, o, d)
        # Direct: solve sum(((o + t d - c) / s)^2) = 1 in world space.
        s = (sx, sy, sz)
        qa = sum((d[i] / s[i]) ** 2 for i in range(3))
        qb = 2 * sum((o[i] - c[i]) * d[i] / s[i] ** 2 for i in range(3))
        qc = sum(((o[i] - c[i]) / s[i]) ** 2 for i in range(3)) - 1
        disc = qb * qb - 4 * qa * qc
        roots = [] if disc < 0 else [r for r in ((-qb - math.sqrt(disc)) / (2 * qa), (-qb + math.sqrt(disc)) / (2 * qa)) if r > 0]
        if not roots:
            assert h is None
            continue
        assert math.isclose(h[0], roots[0], rel_tol=1e-9, abs_tol=1e-9)
        # The gradient of the implicit form is parallel to the returned normal.
        g = tuple(2 * (h[1][i] - c[i]) / s[i] ** 2 for i in range(3))
        cr = cross(g, h[3])
        assert max(abs(x) for x in cr) <= 1e-8 * math.sqrt(dot(g, g) * dot(h[3], h[3]))


def test_world_box_contains_mapped_vertices():
    rng = random.Random(44)
    for _ in range(50):
        mesh = random_mesh(rng, 5)
        inst = make_instance(0, random_matrix(rng), tuple(Q(rng.randint(-9, 9), 2) for _ in range(3)))
        lo, hi = world_box(inst, object_box(mesh))
        for tri in mesh:
            for v in tri:
                w = to_world(inst, v)
                assert all(lo[a] <= w[a] <= hi[a] for a in range(3))
