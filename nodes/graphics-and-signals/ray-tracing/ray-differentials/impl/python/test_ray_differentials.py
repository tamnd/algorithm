# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-differentials/. The authors are listed in prov/TZFVTD.jsonl.

import math
import random

from ray_differentials import camera_ray, dot, mip_level, norm, reflect, refract, scale, sub, trace

CAM = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1 / 256, 0.0, 0.0), (0.0, 1 / 256, 0.0))  # 90 degrees, 512 px
H = 1e-4


def close(a, b, tol):
    return norm(sub(a, b)) <= tol * max(1.0, norm(a), norm(b))


def finite_difference(x, y, surfaces):
    """Central differences of the traced hit point and direction: the reference."""
    out = []
    for ex, ey in ((H, 0.0), (0.0, H)):
        p1, d1, _, _ = trace(CAM, x + ex, y + ey, surfaces)
        p0, d0, _, _ = trace(CAM, x - ex, y - ey, surfaces)
        out.append((scale(1 / (2 * H), sub(p1, p0)), scale(1 / (2 * H), sub(d1, d0))))
    return out


def check(x, y, surfaces, tol=1e-5):
    _, _, dps, dds = trace(CAM, x, y, surfaces)
    for (fp, fd), dp, dd in zip(finite_difference(x, y, surfaces), dps, dds):
        assert close(dp, fp, tol), (dp, fp)
        assert close(dd, fd, tol), (dd, fd)


def test_camera_direction_derivative_matches_finite_difference():
    rng = random.Random(61)
    for _ in range(100):
        x, y = rng.uniform(-256, 256), rng.uniform(-256, 256)
        (_, d), diffs = camera_ray(CAM, x, y)
        (_, d1), _ = camera_ray(CAM, x + H, y)
        (_, d0), _ = camera_ray(CAM, x - H, y)
        assert close(diffs[0][1], scale(1 / (2 * H), sub(d1, d0)), 1e-6)
        assert abs(dot(diffs[0][1], d)) < 1e-12  # a unit vector's derivative is perpendicular


def test_head_on_plane_has_constant_footprint():
    plane = [("plane", (0.0, 0.0, 1.0), 10.0, "stop")]
    for x, y in ((0.0, 0.0), (100.0, -50.0), (-200.0, 230.0)):
        _, _, dps, _ = trace(CAM, x, y, plane)
        assert close(dps[0], (10 / 256, 0.0, 0.0), 1e-12)
        assert close(dps[1], (0.0, 10 / 256, 0.0), 1e-12)


def test_transfer_to_tilted_planes_matches_neighbor_rays():
    rng = random.Random(62)
    for _ in range(60):
        n = (rng.uniform(-1, 1), rng.uniform(-1, 1), -1.0)
        n = scale(1 / norm(n), n)
        surfaces = [("plane", n, -rng.uniform(5, 20), "stop")]
        x, y = rng.uniform(-100, 100), rng.uniform(-100, 100)
        if trace(CAM, x, y, surfaces)[0] is None:
            continue
        check(x, y, surfaces)


def test_reflection_from_sphere_then_plane_matches_neighbor_rays():
    surfaces = [("sphere", (0.0, 0.0, 6.0), 2.0, "reflect"), ("plane", (0.0, 1.0, 0.0), -3.0, "stop")]
    rng = random.Random(63)
    done = 0
    while done < 40:
        x, y = rng.uniform(-60, 60), rng.uniform(-90, -20)
        (o, d), _ = camera_ray(CAM, x, y)
        oc = sub(o, (0.0, 0.0, 6.0))
        if dot(oc, d) ** 2 - (dot(oc, oc) - 4) < 0.5:  # stay away from the silhouette
            continue
        p, d2, _, _ = trace(CAM, x, y, surfaces[:1] + [("plane", (0.0, 1.0, 0.0), -3.0, "stop")])
        if d2[1] >= -1e-3:  # the reflected ray must reach the floor
            continue
        check(x, y, surfaces)
        done += 1


def test_refraction_through_glass_sphere_matches_neighbor_rays():
    surfaces = [
        ("sphere", (0.0, 0.0, 8.0), 2.0, ("refract", 1 / 1.5)),
        ("sphere", (0.0, 0.0, 8.0), 2.0, ("refract", 1 / 1.5)),
        ("plane", (0.0, 0.0, -1.0), -20.0, "stop"),
    ]
    rng = random.Random(64)
    for _ in range(40):
        x, y = rng.uniform(-40, 40), rng.uniform(-40, 40)
        check(x, y, surfaces, tol=1e-4)


def test_refraction_and_reflection_keep_unit_length():
    rng = random.Random(65)
    for _ in range(200):
        d = tuple(rng.gauss(0, 1) for _ in range(3))
        d = scale(1 / norm(d), d)
        n = tuple(rng.gauss(0, 1) for _ in range(3))
        n = scale(1 / norm(n), n)
        if dot(d, n) > 0:
            n = scale(-1, n)
        r, _ = reflect(d, n, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        assert abs(norm(r) - 1) < 1e-12
        out = refract(d, n, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1 / 1.5)
        assert out is not None and abs(norm(out[0]) - 1) < 1e-12
    # Total internal reflection from glass to air beyond the critical angle.
    d = (math.sin(0.8), 0.0, -math.cos(0.8))
    assert refract(d, (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1.5) is None


def test_mip_level_of_ground_plane_grows_with_distance():
    ground = [("plane", (0.0, 1.0, 0.0), -1.0, "stop")]
    levels = []
    for y in (-200.0, -40.0, -8.0, -2.0):
        p, _, dps, _ = trace(CAM, 0.0, y, ground)
        uv = [(dp[0], dp[2]) for dp in dps]  # texture coordinates (u, v) = (x, z)
        levels.append(mip_level(uv[0], uv[1], 64))
    assert levels == sorted(levels)
    assert levels[0] == 0.0 and levels[-1] > 7
