# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plane-sweep-stereo/. The authors are listed in prov/8EH0Z3.jsonl.

import math
import random

from cvgeom import camera_matrix, make_K, project, random_rotation, rot_x, rot_y
from cvla import inv, matvec, mul, transpose
from plane_sweep_stereo import (
    bilinear,
    box_sum,
    inverse_depth_planes,
    pixel_costs,
    plane_homography,
    plane_sweep,
)

W, H = 24, 20
K = make_K(40.0, 40.0, 11.5, 9.5)


def texture(seed):
    rng = random.Random(seed)
    waves = []
    for _ in range(5):
        period = rng.uniform(0.25, 0.7)
        ang = rng.uniform(0.0, math.pi)
        k = 2.0 * math.pi / period
        waves.append((k * math.cos(ang), k * math.sin(ang), rng.uniform(0.0, 6.3), rng.uniform(15.0, 25.0)))

    def g(a, b):
        return 128.0 + sum(amp * math.sin(kx * a + ky * b + ph) for kx, ky, ph, amp in waves)

    return g


def camera(center, R):
    """(K, R, t) of a camera with the given center (in the reference frame) and rotation."""
    t = [-x for x in matvec(R, center)]
    return (K, R, t)


def render(cam, surfaces):
    """Ray cast an image. surfaces: list of (n, d, inside(X), texture(X))."""
    Kk, R, t = cam
    Rt = transpose(R)
    C = [-x for x in matvec(Rt, t)]
    Kinv = inv(Kk)
    img = [[0.0] * W for _ in range(H)]
    for v in range(H):
        for u in range(W):
            ray = matvec(Rt, matvec(Kinv, [u, v, 1.0]))
            best, val = math.inf, 128.0
            for n, d, inside, tex in surfaces:
                den = sum(a * b for a, b in zip(n, ray))
                if abs(den) < 1e-12:
                    continue
                s = (d - sum(a * b for a, b in zip(n, C))) / den
                X = [c + s * r for c, r in zip(C, ray)]
                if 0.0 < s < best and inside(X):
                    best, val = s, tex(X)
            img[v][u] = val
    return img


def two_plane_scene():
    back = texture(1)
    front = texture(2)
    surfaces = [
        ((0.0, 0.0, 1.0), 4.0, lambda X: True, lambda X: back(X[0], X[1])),
        ((0.0, 0.0, 1.0), 2.5, lambda X: abs(X[0]) <= 0.3 and abs(X[1]) <= 0.25,
         lambda X: front(X[0], X[1])),
    ]
    I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    cams = [camera([0.0, 0.0, 0.0], I3),
            camera([0.4, 0.0, 0.0], I3),
            camera([-0.3, 0.25, 0.0], mul(rot_y(0.02), rot_x(-0.02)))]
    images = [render(c, surfaces) for c in cams]
    return images, cams


def test_example_spacing() -> None:
    zs = inverse_depth_planes(1.0, 10.0, 500.0, 0.1)
    assert len(zs) == 46
    assert abs(zs[0] - 1.0) < 1e-12 and abs(zs[-1] - 10.0) < 1e-9
    disp = [500.0 * 0.1 / z for z in zs]
    assert all(abs((a - b) - 1.0) < 1e-9 for a, b in zip(disp, disp[1:]))


def test_example_shift() -> None:
    # A camera moved by b = 0.2 along X with fx = 50: the fronto-parallel
    # plane at depth Z shifts pixels by 10 / Z to the left.
    K1 = make_K(50.0, 50.0, 10.0, 10.0)
    I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    for Z, shift in ((2.0, 5.0), (2.5, 4.0), (5.0, 2.0), (10.0, 1.0)):
        Hm = plane_homography(K1, K1, I3, [-0.2, 0.0, 0.0], (0.0, 0.0, 1.0), Z)
        x = matvec(Hm, [7.0, 3.0, 1.0])
        assert abs(x[0] / x[2] - (7.0 - shift)) < 1e-12
        assert abs(x[1] / x[2] - 3.0) < 1e-12


def test_homography_lemma() -> None:
    rng = random.Random(5)
    for _ in range(100):
        K0 = make_K(rng.uniform(300, 900), rng.uniform(300, 900), rng.uniform(0, 640), rng.uniform(0, 480))
        Kk = make_K(rng.uniform(300, 900), rng.uniform(300, 900), rng.uniform(0, 640), rng.uniform(0, 480), rng.uniform(-2, 2))
        R = random_rotation(rng)
        t = [rng.uniform(-1, 1) for _ in range(3)]
        n = [rng.gauss(0, 1) for _ in range(3)]
        s = math.sqrt(sum(x * x for x in n))
        n = [x / s for x in n]
        d = rng.uniform(0.5, 5.0)
        Hm = plane_homography(K0, Kk, R, t, n, d)
        u, v = rng.uniform(0, 640), rng.uniform(0, 480)
        ray = matvec(inv(K0), [u, v, 1.0])
        den = sum(a * b for a, b in zip(n, ray))
        if abs(den) < 1e-3:
            continue
        X = [d / den * r for r in ray]  # the reference ray meets the plane at X
        Xk = [a + b for a, b in zip(matvec(R, X), t)]
        if abs(Xk[2]) < 1e-3:
            continue
        want = project(camera_matrix(Kk, R, t), X)
        got = matvec(Hm, [u, v, 1.0])
        scale = max(1.0, abs(want[0]), abs(want[1]))
        assert abs(got[0] / got[2] - want[0]) < 1e-8 * scale
        assert abs(got[1] / got[2] - want[1]) < 1e-8 * scale


def costs_by_back_projection(images, cams, n, d, miss):
    """Reference: back-project each pixel to the plane and project it with P_k."""
    Kinv = inv(cams[0][0])
    Ps = [camera_matrix(*c) for c in cams]
    out = [[miss] * W for _ in range(H)]
    near_border = set()
    for v in range(H):
        for u in range(W):
            ray = matvec(Kinv, [u, v, 1.0])
            X = [d / sum(a * b for a, b in zip(n, ray)) * r for r in ray]
            total, count = 0.0, 0
            for k in range(1, len(images)):
                Xh = matvec(Ps[k], X + [1.0])
                if Xh[2] <= 0:
                    continue
                x, y = Xh[0] / Xh[2], Xh[1] / Xh[2]
                if min(abs(x), abs(x - (W - 1)), abs(y), abs(y - (H - 1))) < 1e-6:
                    near_border.add((u, v))  # rounding decides inside or outside
                s = bilinear(images[k], x, y)
                if s is not None:
                    total += abs(images[0][v][u] - s)
                    count += 1
            if count:
                out[v][u] = total / count
    return out, near_border


def test_costs_match_back_projection() -> None:
    images, cams = two_plane_scene()
    for n, d in (((0.0, 0.0, 1.0), 2.5), ((0.0, 0.0, 1.0), 4.0), ((0.1, -0.2, 0.97), 3.0)):
        a = pixel_costs(images, cams, n, d, 255.0)
        b, skip = costs_by_back_projection(images, cams, n, d, 255.0)
        assert len(skip) < W * H // 4
        assert all(abs(a[v][u] - b[v][u]) < 1e-6 for v in range(H) for u in range(W) if (u, v) not in skip)


def test_box_sum() -> None:
    rng = random.Random(3)
    e = [[rng.randrange(10) for _ in range(7)] for _ in range(5)]
    s = box_sum(e, 1)
    for v in range(5):
        for u in range(7):
            want = sum(e[j][i] for j in range(max(v - 1, 0), min(v + 2, 5))
                       for i in range(max(u - 1, 0), min(u + 2, 7)))
            assert s[v][u] == want


def test_two_planes() -> None:
    images, cams = two_plane_scene()
    ds = [2.0, 2.25, 2.5, 2.8, 3.2, 3.6, 4.0, 4.5, 5.0]
    _, depth = plane_sweep(images, cams, (0.0, 0.0, 1.0), ds, 1)
    # The front square covers u in 11.5 +- 4.8 and v in 9.5 +- 4.0 in the reference.
    good = total = 0
    for v in range(H):
        for u in range(W):
            du = max(abs(u - 11.5) - 4.8, 0.0)
            dv = max(abs(v - 9.5) - 4.0, 0.0)
            inside = du == 0.0 and dv == 0.0
            edge = min(abs(abs(u - 11.5) - 4.8), abs(abs(v - 9.5) - 4.0))
            if inside and edge < 2.0:
                continue
            if not inside and max(du, dv) < 4.0:
                continue  # near the edge, or occluded in another view
            if u < 2 or u > W - 3:
                continue  # leaves the other images
            total += 1
            good += abs(depth[v][u] - (2.5 if inside else 4.0)) < 1e-9
    assert total > 100
    assert good >= 0.95 * total


def test_slanted_plane_any_direction() -> None:
    # One slanted plane, swept with its own normal: every pixel finds its d.
    n = (0.2, -0.1, 1.0)
    s = math.sqrt(sum(x * x for x in n))
    n = tuple(x / s for x in n)
    tex = texture(4)
    surfaces = [(n, 3.0, lambda X: True, lambda X: tex(X[0], X[1]))]
    I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    cams = [camera([0.0, 0.0, 0.0], I3), camera([0.4, 0.05, 0.0], I3), camera([-0.35, -0.1, 0.05], rot_y(-0.03))]
    images = [render(c, surfaces) for c in cams]
    ds = [2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6]
    index, depth = plane_sweep(images, cams, n, ds, 1)
    Kinv = inv(K)
    inner = [(u, v) for v in range(2, H - 2) for u in range(3, W - 3)]
    hits = sum(1 for u, v in inner if index[v][u] == 3)
    assert hits >= 0.95 * len(inner)
    for u, v in inner:
        if index[v][u] == 3:
            ray = matvec(Kinv, [u, v, 1.0])
            X = [depth[v][u] * r for r in ray]
            assert abs(sum(a * b for a, b in zip(n, X)) - 3.0) < 1e-9
