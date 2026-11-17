# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-feature-histograms/. The authors are listed in prov/4N5YX7.jsonl.

import math
import random

import pytest

from point_feature_histograms import bin_index, fpfh, pair_features, pfh, radius_neighbors, spfh


def unit(v):
    length = math.sqrt(sum(x * x for x in v))
    return tuple(x / length for x in v)


def rotation(rng):
    """A random rotation matrix from a random unit quaternion."""
    w, x, y, z = unit([rng.gauss(0, 1) for _ in range(4)])
    return (
        (1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)),
        (2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)),
        (2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)),
    )


def apply(R, v, t=(0.0, 0.0, 0.0)):
    return tuple(sum(R[r][c] * v[c] for c in range(3)) + t[r] for r in range(3))


def sphere_cloud(rng, n):
    pts, nrm = [], []
    for _ in range(n):
        u = unit([rng.gauss(0, 1) for _ in range(3)])
        pts.append(u)
        nrm.append(u)
    return pts, nrm


def test_example_pair() -> None:
    f = pair_features((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.6, 0.0, 0.8))
    alpha, phi, theta, dist = f
    assert abs(alpha) < 1e-12 and abs(phi + 0.6) < 1e-12 and dist == 1.0
    assert abs(theta - math.atan2(-0.6, 0.8)) < 1e-12
    assert abs(math.degrees(theta) + 36.8699) < 1e-3


def test_pair_order_does_not_matter() -> None:
    rng = random.Random(51)
    for _ in range(200):
        pa, pb = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(2)]
        na, nb = [unit([rng.gauss(0, 1) for _ in range(3)]) for _ in range(2)]
        f, g = pair_features(pa, na, pb, nb), pair_features(pb, nb, pa, na)
        assert all(abs(x - y) < 1e-9 for x, y in zip(f, g))


def test_pair_features_are_rigid_invariant() -> None:
    rng = random.Random(52)
    for _ in range(100):
        R = rotation(rng)
        t = tuple(rng.uniform(-5, 5) for _ in range(3))
        pa, pb = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(2)]
        na, nb = [unit([rng.gauss(0, 1) for _ in range(3)]) for _ in range(2)]
        f = pair_features(pa, na, pb, nb)
        g = pair_features(apply(R, pa, t), apply(R, na), apply(R, pb, t), apply(R, nb))
        assert all(abs(x - y) < 1e-9 for x, y in zip(f, g))


def test_degenerate_pairs() -> None:
    assert pair_features((0, 0, 0), (0, 0, 1), (0, 0, 0), (0, 0, 1)) is None
    # Both normals along the line between the points: no frame.
    assert pair_features((0, 0, 0), (0, 0, 1), (0, 0, 1), (0, 0, 1)) is None


def test_plane_puts_all_mass_in_the_middle_bins() -> None:
    rng = random.Random(53)
    pts = [(rng.uniform(0, 1), rng.uniform(0, 1), 0.0) for _ in range(60)]
    nrm = [(0.0, 0.0, 1.0)] * 60
    for h in fpfh(pts, nrm, 0.3):
        assert h[5] == pytest.approx(1) and h[16] == pytest.approx(1) and h[27] == pytest.approx(1)
    h = pfh(pts, nrm, 0, 0.3)
    assert h[(2 * 5 + 2) * 5 + 2] == pytest.approx(1)


def fpfh_oracle(points, normals, radius, bins=11):
    """FPFH straight from the formula, with no reuse of the SPFH."""
    n = len(points)

    def part_norm(h):
        out = []
        for p in range(3):
            s = sum(h[p * bins:(p + 1) * bins])
            out += [x / s if s else 0.0 for x in h[p * bins:(p + 1) * bins]]
        return out

    def simple(i):
        nb = [j for j in range(n) if j != i and math.dist(points[i], points[j]) <= radius]
        return spfh(points, normals, i, nb, bins), nb

    result = []
    for i in range(n):
        own, nb = simple(i)
        total = list(own)
        for j in nb:
            other, _ = simple(j)
            w = 1.0 / (len(nb) * math.dist(points[i], points[j]))
            total = [a + w * b for a, b in zip(total, other)]
        result.append(part_norm(total))
    return result


def test_fpfh_matches_oracle() -> None:
    rng = random.Random(54)
    pts, nrm = sphere_cloud(rng, 40)
    got, want = fpfh(pts, nrm, 0.6), fpfh_oracle(pts, nrm, 0.6)
    for g, w in zip(got, want):
        assert all(abs(a - b) < 1e-12 for a, b in zip(g, w))


def test_parts_sum_to_one_and_invariance() -> None:
    rng = random.Random(55)
    pts, nrm = sphere_cloud(rng, 50)
    pts = [tuple(p[c] * (1.0 + 0.3 * c) for c in range(3)) for p in pts]  # an ellipsoid
    R = rotation(rng)
    t = (3.0, -1.0, 2.0)
    a = fpfh(pts, nrm, 0.7)
    b = fpfh([apply(R, p, t) for p in pts], [apply(R, m) for m in nrm], 0.7)
    for i, (h, g) in enumerate(zip(a, b)):
        want = 1.0 if radius_neighbors(pts, i, 0.7) else 0.0
        for part in range(3):
            assert sum(h[part * 11:(part + 1) * 11]) == pytest.approx(want)
        assert all(abs(x - y) < 1e-9 for x, y in zip(h, g))


def test_sphere_differs_from_plane() -> None:
    rng = random.Random(56)
    pts, nrm = sphere_cloud(rng, 80)
    h = fpfh(pts, nrm, 0.5)[0]
    # On a sphere both normals and the line between the points lie in one
    # plane through the center, so alpha is 0; phi and theta leave the
    # middle bins that a plane fills.
    assert h[5] == pytest.approx(1)
    assert h[16] < 0.5 and h[27] < 0.5
    assert sum(pfh(pts, nrm, 0, 0.5)) == pytest.approx(1)


def test_bins_and_neighbors() -> None:
    assert bin_index(-1.0, -1.0, 1.0, 11) == 0
    assert bin_index(1.0, -1.0, 1.0, 11) == 10
    assert bin_index(0.0, -math.pi, math.pi, 11) == 5
    pts = [(0, 0, 0), (0.5, 0, 0), (2, 0, 0)]
    assert radius_neighbors(pts, 0, 0.5) == [1]
    assert fpfh([(0.0, 0.0, 0.0)], [(0.0, 0.0, 1.0)], 1.0) == [[0.0] * 33]
    with pytest.raises(ValueError):
        fpfh(pts, [(0, 0, 1)], 1.0)
