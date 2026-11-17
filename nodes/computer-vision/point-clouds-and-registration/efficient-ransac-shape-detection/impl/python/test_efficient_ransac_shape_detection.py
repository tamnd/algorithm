# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/efficient-ransac-shape-detection/. The authors are listed in prov/NAW12G.jsonl.

import math
import random

import pytest

from efficient_ransac_shape_detection import (
    Candidate,
    Octree,
    compatible,
    detect_shapes,
    fit_cylinder,
    fit_plane,
    fit_sphere,
    hit_probability,
    largest_component,
)

COS10 = math.cos(math.radians(10))


def close(a, b, tol=1e-9):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def unit(v):
    length = math.sqrt(sum(x * x for x in v))
    return tuple(x / length for x in v)


def test_example_fits() -> None:
    plane = fit_plane([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 0, 1), (0, 0, -1), (0, 0, 1)], 0.01, COS10)
    assert plane[0] == "plane" and close(plane[1][0], (0, 0, 1)) and abs(plane[1][1]) < 1e-12
    sphere = fit_sphere([(1, 0, 0), (0, 1, 0), (0, 0, 1)], [(1, 0, 0), (0, 1, 0), (0, 0, 1)], 0.01, COS10, 10)
    assert sphere[0] == "sphere" and close(sphere[1][0], (0, 0, 0)) and abs(sphere[1][1] - 1) < 1e-12
    cyl = fit_cylinder([(1, 0, 0), (0, 1, 5), (-1, 0, 2)], [(1, 0, 0), (0, 1, 0), (-1, 0, 0)], 0.01, COS10, 10)
    assert cyl[0] == "cylinder" and close(cyl[1][0], (0, 0, 0)) and abs(abs(cyl[1][1][2]) - 1) < 1e-12
    assert abs(cyl[1][2] - 1) < 1e-12


def test_fits_reject_bad_normals_and_bad_third_points() -> None:
    tilted = unit((1, 0, 1))
    assert fit_plane([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 0, 1), tilted, (0, 0, 1)], 0.01, COS10) is None
    # The third point is off the sphere through the first two.
    assert fit_sphere([(1, 0, 0), (0, 1, 0), (0, 0, 2)], [(1, 0, 0), (0, 1, 0), (0, 0, 1)], 0.01, COS10, 10) is None
    # Parallel normals give no sphere and no cylinder.
    ps, ns = [(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 0, 1)] * 3
    assert fit_sphere(ps, ns, 0.01, COS10, 10) is None and fit_cylinder(ps, ns, 0.01, COS10, 10) is None


def scene(rng):
    pts, nrm, label = [], [], []

    def add(p, n, lab):
        pts.append(tuple(x + rng.gauss(0, 0.002) for x in p))
        s = rng.choice([-1.0, 1.0])
        nrm.append(tuple(s * x for x in n))
        label.append(lab)

    for _ in range(300):
        add((rng.uniform(0, 3), rng.uniform(0, 3), 0.0), (0.0, 0.0, 1.0), "plane")
    for _ in range(250):
        u = unit([rng.gauss(0, 1) for _ in range(3)])
        add(tuple(c + 0.8 * x for c, x in zip((1.5, 1.5, 2.5), u)), u, "sphere")
    for _ in range(250):
        t = rng.uniform(0, 2 * math.pi)
        add((5 + 0.6 * math.cos(t), rng.uniform(0, 3), 1 + 0.6 * math.sin(t)), (math.cos(t), 0.0, math.sin(t)), "cylinder")
    for _ in range(40):
        add((rng.uniform(0, 6), rng.uniform(0, 3), rng.uniform(0, 3.5)), unit([rng.gauss(0, 1) for _ in range(3)]), "noise")
    return pts, nrm, label


def test_scene_with_three_shapes() -> None:
    pts, nrm, label = scene(random.Random(41))
    shapes = detect_shapes(pts, nrm, eps=0.02, alpha_degrees=15, beta=0.45, min_support=100, seed=7)
    assert sorted(s[0] for s, _ in shapes) == ["cylinder", "plane", "sphere"]
    for (kind, par), idx in shapes:
        own = sum(1 for i in idx if label[i] == kind)
        assert own >= 0.95 * label.count(kind) and len(idx) - own <= 5
        if kind == "plane":
            assert abs(abs(par[0][2]) - 1) < 1e-3 and abs(par[1]) < 0.01
        elif kind == "sphere":
            assert math.dist(par[0], (1.5, 1.5, 2.5)) < 0.02 and abs(par[1] - 0.8) < 0.02
        else:
            c, a, r = par
            assert abs(abs(a[1]) - 1) < 1e-2 and abs(r - 0.6) < 0.02
            assert math.hypot(c[0] - 5, c[2] - 1) < 0.03


def test_connectivity_splits_coplanar_patches() -> None:
    rng = random.Random(42)
    big = [(rng.uniform(0, 2), rng.uniform(0, 2), 0.0) for _ in range(120)]
    small = [(rng.uniform(5, 6.5), rng.uniform(0, 1.5), 0.0) for _ in range(80)]
    pts = big + small
    nrm = [(0.0, 0.0, 1.0)] * len(pts)
    shapes = detect_shapes(pts, nrm, eps=0.01, alpha_degrees=10, beta=0.5, min_support=50, seed=3)
    assert [len(idx) for _, idx in shapes] == [120, 80]
    assert shapes[0][1] == list(range(120))


def test_pure_noise_gives_nothing() -> None:
    rng = random.Random(43)
    pts = [tuple(rng.uniform(0, 1) for _ in range(3)) for _ in range(120)]
    nrm = [unit([rng.gauss(0, 1) for _ in range(3)]) for _ in range(120)]
    assert detect_shapes(pts, nrm, eps=0.005, alpha_degrees=10, beta=0.2, min_support=30, seed=1) == []


def test_lazy_score_becomes_exact() -> None:
    pts, nrm, _ = scene(random.Random(44))
    shape = ("plane", ((0.0, 0.0, 1.0), 0.0))
    remaining = set(range(len(pts)))
    subsets = [list(range(len(pts)))[i::5] for i in range(5)]
    cand = Candidate(shape, 1)
    exact = sum(1 for i in remaining if compatible(shape, pts[i], nrm[i], 0.02, COS10))
    for _ in range(5):
        cand.refine(subsets, remaining, pts, nrm, 0.02, COS10)
        assert cand.lo <= exact <= cand.hi
    assert cand.est == cand.lo == cand.hi == exact


def test_hit_probability() -> None:
    assert hit_probability(50, 100, 1) == pytest.approx(0.125)
    assert hit_probability(50, 100, 2) == pytest.approx(1 - 0.875 ** 2)
    assert hit_probability(0, 100, 10) == 0.0
    assert hit_probability(100, 100, 1) == 1.0


def test_octree_cells_nest() -> None:
    rng = random.Random(45)
    pts = [tuple(rng.uniform(-1, 3) for _ in range(3)) for _ in range(200)]
    tree = Octree(pts, 4)
    for i, p in enumerate(pts):
        for level in range(5):
            assert i in tree.cell(p, level)
            if level:
                assert set(tree.cell(p, level)) <= set(tree.cell(p, level - 1))
    assert len(tree.cell(pts[0], 0)) == 200


def test_largest_component() -> None:
    pts = [(0, 0, 0), (0.5, 0, 0), (1.0, 0, 0), (5, 0, 0), (5.4, 0, 0), (9, 9, 9)]
    assert largest_component(pts, range(6), 0.6) == [0, 1, 2]
    assert largest_component(pts, [3, 4, 5], 0.6) == [3, 4]


def test_edges() -> None:
    with pytest.raises(ValueError):
        detect_shapes([(0, 0, 0)] * 3, [(0, 0, 1)] * 3, 0.1, 10, 0.5, 2)
    assert detect_shapes([], [], 0.1, 10, 0.5, 3) == []
