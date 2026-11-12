# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primary-ray-generation/. The authors are listed in prov/NCFKVH.jsonl.

import math
import random
from fractions import Fraction

from primary_ray_generation import Camera, concentric_disk, generate_image_rays, look_at

F = Fraction
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def project(cam, p):
    """Reference: the pixel coordinates (x, y) of the point p, by the
    perspective division of its camera coordinates. Exact in Fraction."""
    rel = [p[k] - cam.eye[k] for k in range(3)]
    cx = sum(rel[k] * cam.u[k] for k in range(3))
    cy = sum(rel[k] * cam.v[k] for k in range(3))
    cz = -sum(rel[k] * cam.w[k] for k in range(3))           # depth in front of the eye
    sx, sy = cx / cz / cam.tan_half_fov, cy / cz / cam.tan_half_fov
    return ((sx * cam.height + cam.width) / 2, (cam.height - sy * cam.height) / 2), cz


def rational_camera(rng, lens_radius=0, focus_distance=1):
    eye = tuple(F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(3))
    # an axis permutation with signs is an exact orthonormal basis
    perm = rng.sample(range(3), 3)
    sg = [rng.choice((-1, 1)) for _ in range(2)]
    u = tuple(sg[0] * x for x in AXES[perm[0]])
    v = tuple(sg[1] * x for x in AXES[perm[1]])
    w = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return Camera(eye, u, v, w, rng.randint(1, 9), rng.randint(1, 9), F(rng.randint(1, 8), 4),
                  lens_radius, focus_distance)


def test_center_pixel_looks_along_minus_w():
    cam = Camera((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), 3, 3, F(1))
    o, d = cam.primary_ray(1, 1)
    assert o == (0, 0, 0) and d == (0, 0, -1)
    # the top left pixel center of a 3 by 3 image with a 90 degree field of view
    o, d = cam.primary_ray(0, 0)
    assert d == (F(-2, 3), F(2, 3), -1)


def test_pinhole_rays_pass_through_the_pixel_sample():
    rng = random.Random(1968)
    for _ in range(300):
        cam = rational_camera(rng)
        i, j = rng.randrange(cam.width), rng.randrange(cam.height)
        sx, sy = F(rng.randint(0, 15), 16), F(rng.randint(0, 15), 16)
        o, d = cam.primary_ray(i, j, sx, sy)
        assert o == cam.eye
        for _ in range(3):
            t = F(rng.randint(1, 50), rng.randint(1, 7))
            p = tuple(o[k] + t * d[k] for k in range(3))
            (x, y), depth = project(cam, p)
            assert (x, y) == (i + sx, j + sy) and depth == t


def test_thin_lens_rays_meet_on_the_focus_plane():
    rng = random.Random(1981)
    for _ in range(300):
        zf = F(rng.randint(1, 40), rng.randint(1, 4))
        cam = rational_camera(rng, lens_radius=F(rng.randint(1, 8), 8), focus_distance=zf)
        i, j = rng.randrange(cam.width), rng.randrange(cam.height)
        pin = Camera(cam.eye, cam.u, cam.v, cam.w, cam.width, cam.height, cam.tan_half_fov)
        _, dp = pin.primary_ray(i, j)
        focus = tuple(cam.eye[k] + zf * dp[k] for k in range(3))
        for _ in range(4):
            lens = (F(rng.randint(-5, 5), 8), F(rng.randint(-5, 5), 8))
            o, d = cam.primary_ray(i, j, lens_point=lens)
            # the ray starts on the lens, in the plane of the eye ...
            assert sum((o[k] - cam.eye[k]) * cam.w[k] for k in range(3)) == 0
            # ... and reaches the focus point at t = 1
            assert tuple(o[k] + d[k] for k in range(3)) == focus
            assert project(cam, focus)[0] == (i + F(1, 2), j + F(1, 2))


def test_zero_radius_is_the_pinhole():
    rng = random.Random(3)
    cam = rational_camera(rng, lens_radius=0, focus_distance=F(7))
    pin = rational_camera(random.Random(3))
    for i in range(cam.width):
        for j in range(cam.height):
            assert cam.primary_ray(i, j, lens_point=(F(1, 2), F(1, 3))) == pin.primary_ray(i, j)


def test_blur_grows_with_the_distance_from_the_focus_plane():
    # rays through opposite lens edges spread by 2 R |z - zf| / zf at depth z
    R, zf = F(1, 4), F(10)
    cam = Camera((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), 5, 5, F(1), R, zf)
    for z in (F(2), F(5), F(10), F(20), F(40)):
        pts = []
        for lens in ((1, 0), (-1, 0)):
            o, d = cam.primary_ray(2, 2, lens_point=lens)
            t = z / zf                     # d has the component -zf along w
            pts.append(o[0] + t * d[0])
        assert abs(pts[0] - pts[1]) == 2 * R * abs(z - zf) / zf


def test_concentric_disk_radius_and_area():
    n = 64
    inside = 0
    for a in range(n):
        for b in range(n):
            x1, x2 = (a + 0.5) / n, (b + 0.5) / n
            px, py = concentric_disk(x1, x2)
            rad = math.hypot(px, py)
            assert abs(rad - max(abs(2 * x1 - 1), abs(2 * x2 - 1))) < 1e-12
            inside += rad < 0.5
    # the square of half side 1/2 maps onto the disk of radius 1/2: a quarter of the area
    assert inside == n * n // 4


def test_look_at_and_a_full_frame():
    u, v, w = look_at((0.0, 0.0, 5.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
    for a, b in ((u, (1.0, 0.0, 0.0)), (v, (0.0, 1.0, 0.0)), (w, (0.0, 0.0, 1.0))):
        assert all(abs(x - y) < 1e-15 for x, y in zip(a, b))
    cam = Camera((0.0, 0.0, 5.0), u, v, w, 8, 6, math.tan(math.radians(30)), 0.1, 5.0)
    rays = generate_image_rays(cam, 2, random.Random(9))
    assert len(rays) == 8 * 6 * 2
    for (i, j), (o, d) in rays:
        # every ray ends on the focus plane z = 0 at t = 1 and inside its pixel
        p = tuple(o[k] + d[k] for k in range(3))
        assert abs(p[2]) < 1e-12
        px = (p[0] / 5.0 / cam.tan_half_fov * cam.height + cam.width) / 2
        py = (cam.height - p[1] / 5.0 / cam.tan_half_fov * cam.height) / 2
        assert i - 1e-9 <= px <= i + 1 + 1e-9 and j - 1e-9 <= py <= j + 1 + 1e-9
