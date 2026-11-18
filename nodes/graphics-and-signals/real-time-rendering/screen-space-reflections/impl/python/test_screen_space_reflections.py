# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/screen-space-reflections/. The authors are listed in prov/4JP2C2.jsonl.

"""Screen-space reflections in a small analytic room."""

import math
import random

from screen_space_reflections import Camera, reflect, reflection, trace

CAM = Camera(64, 48, 0.5, 0.1)
TAU = 0.3


def scene_hit(w):
    """Depth and label of the view ray through the depth-1 point w."""
    best = None
    if w[1] < 0:  # floor y = -1, up to the back wall
        d = -1.0 / w[1]
        if d <= 12.0:
            best = (d, "floor")
    if 12.0 * w[1] <= 3.0:  # back wall at depth 12, top at y = 3
        if best is None or 12.0 < best[0]:
            best = (12.0, "wall")
    if -1.5 <= 6.0 * w[0] <= 0.0 and -1.0 <= 6.0 * w[1] <= 0.5:  # box face at depth 6
        if best is None or 6.0 < best[0]:
            best = (6.0, "box")
    return best


def render():
    D, C = [], []
    for j in range(CAM.height):
        drow, crow = [], []
        for i in range(CAM.width):
            hit = scene_hit(CAM.pixel_ray(i + 0.5, j + 0.5))
            drow.append(None if hit is None else hit[0])
            crow.append("sky" if hit is None else (hit[1], i, j))
        D.append(drow)
        C.append(crow)
    return D, C


D, COLOR = render()


def normalize(v):
    L = math.sqrt(sum(c * c for c in v))
    return tuple(c / L for c in v)


def march_reference(origin, dirn, max_dist, thickness, h=0.004):
    """A fine march of the 3D ray, testing the point depth at each pixel."""
    length = max_dist
    if origin[2] + dirn[2] * length > -CAM.near:
        length = (-CAM.near - origin[2]) / dirn[2]
    sx0, sy0, _ = CAM.project(origin)
    start = (int(math.floor(sx0)), int(math.floor(sy0)))
    t = h
    while t <= length:
        p = tuple(o + t * r for o, r in zip(origin, dirn))
        sx, sy, k = CAM.project(p)
        i, j = int(math.floor(sx)), int(math.floor(sy))
        if not (0 <= i < CAM.width and 0 <= j < CAM.height):
            return None
        s = D[j][i]
        if (i, j) != start and s is not None and s <= 1.0 / k <= s + thickness:
            return i, j
        t += h
    return None


def floor_pixels():
    return [(i, j) for j in range(CAM.height) for i in range(CAM.width) if COLOR[j][i] != "sky" and COLOR[j][i][0] == "floor"]


def test_inverse_depth_and_q_are_linear_in_screen_space() -> None:
    rng = random.Random(91)
    for _ in range(200):
        a = (rng.uniform(-3, 3), rng.uniform(-3, 3), -rng.uniform(1, 20))
        b = (rng.uniform(-3, 3), rng.uniform(-3, 3), -rng.uniform(1, 20))
        x0, y0, k0 = CAM.project(a)
        x1, y1, k1 = CAM.project(b)
        if abs(x1 - x0) < 1e-3:
            continue
        for _ in range(5):
            t = rng.random()
            p = tuple(u + t * (v - u) for u, v in zip(a, b))
            sx, sy, k = CAM.project(p)
            lam = (sx - x0) / (x1 - x0)
            k_lin = k0 + lam * (k1 - k0)
            assert abs(k_lin - k) < 1e-12 * max(1.0, k)
            q = tuple(u * k0 + lam * (v * k1 - u * k0) for u, v in zip(a, b))
            assert all(abs(qc / k_lin - pc) < 1e-9 for qc, pc in zip(q, p))
            assert abs(y0 + lam * (y1 - y0) - sy) < 1e-9


def test_first_hit_agrees_with_a_fine_march() -> None:
    rng = random.Random(92)
    pixels = rng.sample(floor_pixels(), 40)
    hits = 0
    for i, j in pixels:
        d = D[j][i]
        view = CAM.pixel_ray(i + 0.5, j + 0.5)
        origin = tuple(c * d for c in view)
        r = reflect(normalize(view), (0.0, 1.0, 0.0))
        got = trace(D, CAM, origin, r, 40.0, TAU)
        ref = march_reference(origin, r, 40.0, TAU)
        assert (got is None) == (ref is None)
        if got is not None:
            hits += 1
            assert abs(got[0] - ref[0]) <= 1 and abs(got[1] - ref[1]) <= 1
            assert D[got[1]][got[0]] <= -got[2][2] + 1e-9 <= D[got[1]][got[0]] + TAU + 0.5
    assert hits >= 20


def test_hit_point_lies_on_the_ray() -> None:
    i, j = 20, 5
    d = D[j][i]
    view = CAM.pixel_ray(i + 0.5, j + 0.5)
    origin = tuple(c * d for c in view)
    r = reflect(normalize(view), (0.0, 1.0, 0.0))
    hit = trace(D, CAM, origin, r, 40.0, TAU)
    assert hit is not None
    p = hit[2]
    t = sum((pc - oc) * rc for pc, oc, rc in zip(p, origin, r))
    closest = tuple(oc + t * rc for oc, rc in zip(origin, r))
    assert all(abs(a - b) < 1e-9 for a, b in zip(p, closest))


def test_self_hit_on_a_flat_surface_and_the_offset() -> None:
    # A ray that starts exactly on the wall overlaps the wall at the next pixel.
    on_wall = (2.0, 0.0, -12.0)
    assert trace(D, CAM, on_wall, normalize((1.0, 0.2, 0.6)), 40.0, TAU) is not None
    # Moved off the surface, the same ray leaves the screen: a miss.
    origin = (2.0, 0.0, -11.9)
    assert trace(D, CAM, origin, normalize((1.0, 0.2, 0.6)), 40.0, TAU) is None
    # Straight toward the camera: clipped at the near plane, and it leaves
    # the screen before it gets there.
    assert trace(D, CAM, origin, (0.0, 0.0, 1.0), 40.0, TAU) is None


def test_thickness_decides_hits_behind_the_box() -> None:
    # A ray at depth 9 that passes behind the box face at depth 6.
    origin, side = (-4.0, -0.25, -9.0), (1.0, 0.0, 0.0)
    assert trace(D, CAM, origin, side, 8.0, 0.5) is None
    thick = trace(D, CAM, origin, side, 8.0, float("inf"))
    assert thick is not None and COLOR[thick[1]][thick[0]][0] == "box"
    assert abs(-thick[2][2] - 9.0) < 1e-9  # reported 3 units behind the face
    # A ray from the hidden wall toward the camera crosses the face.
    origin, toward_camera = (-0.6, -0.25, -12.0), (0.0, 0.0, 1.0)
    thick = trace(D, CAM, origin, toward_camera, 40.0, float("inf"))
    thin = trace(D, CAM, origin, toward_camera, 40.0, 0.5)
    assert thick is not None and -thick[2][2] > 8.0  # the first pixel behind the face
    assert thin is not None and 6.0 <= -thin[2][2] <= 6.7  # near the true crossing


def test_reflection_uses_the_hit_or_the_environment() -> None:
    env = lambda r: ("environment", r[1] > 0)
    outs = [reflection(D, COLOR, CAM, i, j, (0.0, 1.0, 0.0), env, 40.0, TAU) for i, j in floor_pixels()]
    assert any(o[0] == "wall" for o in outs)
    assert any(o[0] == "box" for o in outs)
    assert any(o[0] == "environment" for o in outs)
    assert all(o[0] in ("wall", "box", "environment") for o in outs)
