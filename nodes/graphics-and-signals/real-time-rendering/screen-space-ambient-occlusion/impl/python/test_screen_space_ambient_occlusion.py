# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/screen-space-ambient-occlusion/. The authors are listed in prov/EGC7ET.jsonl.

"""SSAO on height fields with known answers."""

import math
import random

from screen_space_ambient_occlusion import (
    box_blur,
    half_ball_beyond,
    hemisphere_kernel,
    lookup,
    normal_from_depth,
    sphere_kernel,
    ssao,
    ssao_pixel,
    to_normal_frame,
)


def plane(w, h, d0, gx, gy):
    return [[d0 + gx * (i + 0.5) + gy * (j + 0.5) for i in range(w)] for j in range(h)]


def test_bilinear_lookup_is_exact_on_a_plane() -> None:
    D = plane(12, 10, 20.0, 0.25, -0.5)
    rng = random.Random(61)
    for _ in range(200):
        x, y = rng.uniform(0.5, 11.5), rng.uniform(0.5, 9.5)
        assert abs(lookup(D, x, y) - (20.0 + 0.25 * x - 0.5 * y)) < 1e-9


def test_sphere_kernel_gives_one_half_on_any_plane() -> None:
    rng = random.Random(62)
    kernel = sphere_kernel(rng, 16, 3.0)
    for gx, gy in [(0.0, 0.0), (0.3, 0.0), (-0.4, 0.7), (1.5, -0.2)]:
        D = plane(24, 24, 50.0, gx, gy)
        for i, j in [(10, 10), (12, 8), (8, 14)]:
            assert ssao_pixel(D, i, j, kernel, oriented=False) == 0.5


def test_hemisphere_kernel_gives_one_on_any_plane() -> None:
    rng = random.Random(63)
    kernel = hemisphere_kernel(rng, 32, 3.0)
    for gx, gy in [(0.0, 0.0), (0.3, 0.0), (-0.4, 0.7), (1.5, -0.2)]:
        D = plane(24, 24, 50.0, gx, gy)
        n = normal_from_depth(D, 11, 11)
        s = math.hypot(gx, gy, 1.0)
        assert all(abs(a - b) < 1e-12 for a, b in zip(n, (gx / s, gy / s, 1 / s)))
        for i, j in [(10, 10), (12, 8), (8, 14)]:
            assert ssao_pixel(D, i, j, kernel, oriented=True) == 1.0


def test_rotation_keeps_the_kernel_in_the_hemisphere() -> None:
    rng = random.Random(64)
    for _ in range(100):
        v = (rng.gauss(0, 1), rng.gauss(0, 1), abs(rng.gauss(0, 1)) + 0.1)
        L = math.sqrt(sum(c * c for c in v))
        n = tuple(c / L for c in v)
        for k in hemisphere_kernel(rng, 5, 1.0):
            o = to_normal_frame(k, n)
            assert abs(sum(c * c for c in o) - sum(c * c for c in k)) < 1e-12
            assert abs(sum(a * b for a, b in zip(o, n)) - k[2]) < 1e-12


def test_step_matches_the_volume_fraction() -> None:
    # Floor at depth 40 for x < 20, a block nearer by 30 for x >= 20.
    w, h, R = 40, 20, 6.0
    D = [[40.0 if i < 20 else 10.0 for i in range(w)] for _ in range(h)]
    rng = random.Random(65)
    kernel = hemisphere_kernel(rng, 6000, R)
    # Pixel 19 is left out: its central difference straddles the edge and
    # tilts the normal, which is a known artifact of normals from depth.
    for i in (18, 17, 15, 14):
        delta = 20 - (i + 0.5)
        A = ssao_pixel(D, i, 10, kernel, oriented=True, mode="nearest")
        assert abs((1 - A) - half_ball_beyond(delta, R)) < 0.025
    assert half_ball_beyond(0.0, R) == 0.5


def test_range_check_fades_far_occluders() -> None:
    # A plate 30 units in front of a frontal floor covers the right half.
    w, h, R = 30, 10, 4.0
    D = [[60.0 if i < 15 else 30.0 for i in range(w)] for _ in range(h)]
    rng = random.Random(66)
    kernel = hemisphere_kernel(rng, 400, R)
    plain = ssao_pixel(D, 13, 5, kernel, oriented=True, mode="nearest")
    ranged = ssao_pixel(D, 13, 5, kernel, oriented=True, mode="nearest", range_radius=R)
    assert abs((1 - plain) - half_ball_beyond(1.5, R)) < 0.05
    assert ranged > 0.95


def test_blur_keeps_constants_and_averages() -> None:
    A = [[0.25] * 7 for _ in range(5)]
    assert box_blur(A, 2) == A
    B = [[1.0 if (i + j) % 2 else 0.0 for i in range(9)] for j in range(9)]
    out = box_blur(B, 1)
    assert abs(out[4][4] - 4 / 9) < 1e-12


def test_whole_image_on_a_plane() -> None:
    D = plane(16, 12, 30.0, 0.2, 0.1)
    rng = random.Random(67)
    A = ssao(D, hemisphere_kernel(rng, 16, 2.0), oriented=True, blur=1)
    assert all(abs(a - 1.0) < 1e-12 for row in A for a in row)
