# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-ray-tracing/. The authors are listed in prov/Z5NHPG.jsonl.

"""Tests against closed forms and an independent brute force tracer.

The reference tracer below does not sample. It intersects spheres by the geometric method, builds
its own frames, and replaces each random choice by a deterministic midpoint quadrature over the
same integral. Statistical tests use seeded random.Random and accept the estimate when it lies
within 4 standard errors of the reference (plus the stated quadrature error); for a correct
estimator, which is unbiased and close to normal at these sample sizes, each check fails with a
probability below 1e-4.
"""

import math
import random
import statistics

from distributed_ray_tracing import (
    Camera,
    DiskLight,
    Material,
    Plane,
    PointLight,
    Scene,
    Sphere,
    jittered_pairs,
    jittered_times,
    normalize,
    render_pixel,
    sample_lobe,
    trace,
)

# --------------------------------------------------------------------------- reference geometry


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _hit_sphere(c, r, o, d, eps):
    oc = (c[0] - o[0], c[1] - o[1], c[2] - o[2])
    tc = _dot(oc, d)
    d2 = _dot(oc, oc) - tc * tc
    if d2 > r * r:
        return None
    th = math.sqrt(max(0.0, r * r - d2))
    for t in (tc - th, tc + th):
        if t > eps:
            return t
    return None


def _hit(obj, o, d, time, eps):
    if isinstance(obj, Sphere):
        c = tuple(obj.center[i] + time * obj.velocity[i] for i in range(3))
        return _hit_sphere(c, obj.radius, o, d, eps)
    den = _dot(obj.n, d)
    if abs(den) < 1e-300:
        return None
    t = _dot(obj.n, tuple(obj.point[i] - o[i] for i in range(3))) / den
    return t if t > eps else None


def _blocked(objects, p, q, time, eps=1e-7):
    v = tuple(q[i] - p[i] for i in range(3))
    dist = math.sqrt(_dot(v, v))
    u = tuple(x / dist for x in v)
    return any((t := _hit(obj, p, u, time, eps * dist)) is not None and t < dist * (1 - eps) for obj in objects)


def _closest(objects, o, d, time, eps=1e-7):
    best = None
    for obj in objects:
        t = _hit(obj, o, d, time, eps)
        if t is not None and (best is None or t < best[0]):
            best = (t, obj)
    return best


def _whitted_reference(scene, o, d, depth, eps=1e-7):
    """Sharp recursive Whitted tracer with Whitted's formulas R = V' + 2N and P = kf (N + V') - N."""
    h = _closest(scene.objects, o, d, 0.0, eps)
    if h is None:
        return scene.background
    t, obj = h
    m = obj.material
    p = tuple(o[i] + t * d[i] for i in range(3))
    n = obj.normal(p, 0.0)
    kn = m.eta
    if _dot(n, d) > 0.0:
        n, kn = tuple(-x for x in n), 1.0 / m.eta
    value = m.ka
    for light in scene.point_lights:
        lv = tuple(light.position[i] - p[i] for i in range(3))
        cos_l = _dot(n, lv) / math.sqrt(_dot(lv, lv))
        if m.kd > 0.0 and cos_l > 0.0 and not _blocked(scene.objects, p, light.position, 0.0):
            value += m.kd * light.intensity * cos_l
    if depth == 0:
        return value
    s = 1.0 / abs(_dot(d, n))
    vp = tuple(s * x for x in d)
    if m.ks > 0.0:
        value += m.ks * _whitted_reference(scene, p, normalize(tuple(vp[i] + 2 * n[i] for i in range(3))), depth - 1)
    if m.kt > 0.0:
        tan = tuple(vp[i] + n[i] for i in range(3))
        qq = kn * kn * _dot(vp, vp) - _dot(tan, tan)
        if qq > 0.0:
            kf = 1.0 / math.sqrt(qq)
            pd = normalize(tuple(kf * tan[i] - n[i] for i in range(3)))
            value += m.kt * _whitted_reference(scene, p, pd, depth - 1)
    return value


def _check(samples, reference, slack=0.0):
    mean = statistics.fmean(samples)
    se = statistics.stdev(samples) / math.sqrt(len(samples))
    assert abs(mean - reference) <= 4.0 * se + slack, (mean, reference, se)


# --------------------------------------------------------------------------- tests


def test_sharp_limit_is_whitted_ray_tracing():
    floor = Plane((0.0, -1.0, 0.0), (0.0, 1.0, 0.0), Material(ka=0.05, kd=0.6, ks=0.2))
    mirror = Sphere((-1.0, 0.0, -5.0), 1.0, Material(ka=0.02, kd=0.1, ks=0.8))
    glass = Sphere((1.0, -0.2, -4.0), 0.8, Material(kd=0.05, ks=0.1, kt=0.85, eta=1.5))
    scene = Scene([floor, mirror, glass], point_lights=[PointLight((5.0, 6.0, 0.0), 0.7),
                                                         PointLight((-4.0, 3.0, -2.0), 0.4)], background=0.3)
    cam = Camera(16, 12, math.tan(math.radians(30.0)))
    rng = random.Random(1980)
    for _ in range(300):
        o, d = cam.ray(16 * rng.random(), 12 * rng.random(), (rng.random(), rng.random()))
        got = trace(scene, o, d, rng.random(), 4, rng)
        assert abs(got - _whitted_reference(scene, o, d, 4)) <= 1e-9


def test_disk_light_closed_form():
    # A disk light of radius R and radiance L at the height h above a diffuse point, facing it:
    # the irradiance is pi L R^2 / (h^2 + R^2), so the value is kd L R^2 / (h^2 + R^2).
    kd, lrad, big_r, h = 0.8, 2.0, 1.0, 2.0
    scene = Scene([Plane((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), Material(kd=kd))],
                  disk_lights=[DiskLight((0.0, h, 0.0), (0.0, -1.0, 0.0), big_r, lrad)])
    rng = random.Random(1984)
    samples = [trace(scene, (0.0, 0.5, 0.0), (0.0, -1.0, 0.0), 0.0, 0, rng) for _ in range(20000)]
    _check(samples, kd * lrad * big_r ** 2 / (h * h + big_r ** 2))


def _disk_quadrature(objects, light, p, n, m=240):
    """Midpoint rule in polar coordinates over the disk of L cos cos' / r^2 times visibility / pi."""
    a = normalize((1.0, 0.0, 0.0) if abs(light.normal[1]) > 0.5 else (0.0, 1.0, 0.0))
    ln = normalize(light.normal)
    a = normalize(tuple(a[i] - _dot(a, ln) * ln[i] for i in range(3)))
    b = (ln[1] * a[2] - ln[2] * a[1], ln[2] * a[0] - ln[0] * a[2], ln[0] * a[1] - ln[1] * a[0])
    total = 0.0
    for ir in range(m):
        r = light.radius * (ir + 0.5) / m
        for ip in range(m):
            phi = 2.0 * math.pi * (ip + 0.5) / m
            q = tuple(light.center[i] + r * math.cos(phi) * a[i] + r * math.sin(phi) * b[i] for i in range(3))
            v = tuple(q[i] - p[i] for i in range(3))
            r2 = _dot(v, v)
            cp, cq = _dot(n, v) / math.sqrt(r2), -_dot(ln, v) / math.sqrt(r2)
            if cp > 0 and cq > 0 and not _blocked(objects, p, q, 0.0):
                total += light.radiance * cp * cq / r2 * r
    return total * (light.radius / m) * (2.0 * math.pi / m) / math.pi


def test_penumbra_against_quadrature():
    floor = Plane((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), Material(kd=1.0))
    blocker = Sphere((0.3, 1.0, 0.0), 0.3, Material())
    light = DiskLight((0.0, 2.0, 0.0), (0.0, -1.0, 0.0), 0.8, 1.0)
    scene = Scene([floor, blocker], disk_lights=[light])
    rng = random.Random(7)
    for px, pz in ((0.0, 0.0), (0.5, 0.2), (1.0, -0.3)):
        ref = _disk_quadrature([floor, blocker], light, (px, 0.0, pz), (0.0, 1.0, 0.0))
        samples = [trace(scene, (px, 0.5, pz), (0.0, -1.0, 0.0), 0.0, 0, rng) for _ in range(20000)]
        # Slack: the midpoint rule on a 240 x 240 grid is off by under 0.5 percent at the shadow edge.
        _check(samples, ref, slack=5e-3 * ref)


def _lobe_quadrature(axis, exponent, visible, m=300):
    """Integral of visible(omega) under the Phong lobe, by the midpoint rule in (cos^(e+1), phi)."""
    helper = (0.0, 0.0, 1.0) if abs(axis[2]) < 0.9 else (0.0, 1.0, 0.0)
    a = normalize(tuple(helper[i] - _dot(helper, axis) * axis[i] for i in range(3)))
    b = (axis[1] * a[2] - axis[2] * a[1], axis[2] * a[0] - axis[0] * a[2], axis[0] * a[1] - axis[1] * a[0])
    total = 0
    for i in range(m):
        c = ((i + 0.5) / m) ** (1.0 / (exponent + 1.0))
        s = math.sqrt(1.0 - c * c)
        for j in range(m):
            phi = 2.0 * math.pi * (j + 0.5) / m
            w = tuple(c * axis[k] + s * math.cos(phi) * a[k] + s * math.sin(phi) * b[k] for k in range(3))
            total += visible(w)
    return total / (m * m)


def test_gloss_against_quadrature():
    floor = Plane((0.0, -1.0, 0.0), (0.0, 1.0, 0.0), Material(ks=0.9, gloss=20.0))
    bright = Sphere((0.0, 0.5, -5.0), 1.0, Material(ka=1.0))
    scene = Scene([floor, bright])
    d = normalize((0.0, -1.0, -3.0))
    p = (0.0, -1.0, -3.0)
    mirror = (d[0], -d[1], d[2])

    def visible(w):
        return 1 if w[1] > 0.0 and _closest([bright], p, w, 0.0) is not None else 0

    ref = 0.9 * _lobe_quadrature(mirror, 20.0, visible)
    assert 0.1 < ref < 0.8
    rng = random.Random(1986)
    samples = [trace(scene, (0.0, 0.0, 0.0), d, 0.0, 1, rng) for _ in range(20000)]
    _check(samples, ref, slack=5e-3)


def test_depth_of_field_against_quadrature():
    # A bright sphere behind the plane in focus. The fraction of the lens through which the film
    # point at the center sees it, by the midpoint rule over the lens disk, is the pixel value.
    lens, focus = 0.3, 3.0
    bright = Sphere((0.35, 0.0, -6.0), 0.5, Material(ka=1.0))
    scene = Scene([bright])
    cam = Camera(1, 1, 1e-9, lens_radius=lens, focus_distance=focus)
    m, covered = 300, 0.0
    for ir in range(m):
        r = lens * (ir + 0.5) / m
        for ip in range(m):
            phi = 2.0 * math.pi * (ip + 0.5) / m
            o = (r * math.cos(phi), r * math.sin(phi), 0.0)
            d = normalize((-o[0], -o[1], -focus))
            if _closest([bright], o, d, 0.0) is not None:
                covered += r
    ref = covered * (lens / m) * (2.0 * math.pi / m) / (math.pi * lens * lens)
    assert 0.1 < ref < 0.9
    rng = random.Random(1981)
    pixels = [render_pixel(scene, cam, 0, 0, 4, 0, rng) for _ in range(500)]
    _check(pixels, ref, slack=3e-3)
    # Stratification of the lens: the 16 stratified samples of one pixel vary less than 16
    # independent ones would, whose standard deviation is sqrt(ref (1 - ref) / 16).
    assert statistics.stdev(pixels) < math.sqrt(ref * (1.0 - ref) / 16.0)


def test_motion_blur_time_fraction():
    # A sphere of radius 0.2 moves along x through the line of sight of a pinhole pixel. It covers
    # the pixel while |x0 + t| < 0.2, a known fraction of the shutter interval. With q * q jittered
    # times, every slice inside the interval counts exactly, and at most two slices are cut by its
    # ends, so the error is at most 2 / q^2 for every seed, not only with high probability.
    cam = Camera(1, 1, 1e-9)
    rng = random.Random(42)
    for x0, exact in ((-0.5, 0.4), (-0.1, 0.3), (0.5, 0.0)):
        scene = Scene([Sphere((x0, 0.0, -5.0), 0.2, Material(ka=1.0), velocity=(1.0, 0.0, 0.0))])
        for q in (2, 4, 8):
            for _ in range(20):
                assert abs(render_pixel(scene, cam, 0, 0, q, 0, rng) - exact) <= 2.0 / (q * q) + 1e-12


def test_samplers():
    rng = random.Random(3)
    pts = jittered_pairs(5, rng)
    assert sorted((int(5 * x), int(5 * y)) for x, y in pts) == [(i, j) for i in range(5) for j in range(5)]
    ts = jittered_times(16, rng)
    assert sorted(int(16 * t) for t in ts) == list(range(16))
    # The Phong lobe of exponent e has the mean cosine (e + 1) / (e + 2).
    axis = normalize((0.3, -0.2, 0.9))
    for e in (1.0, 20.0):
        cosines = []
        for _ in range(20000):
            w = sample_lobe(axis, e, (rng.random(), rng.random()))
            assert abs(_dot(w, w) - 1.0) < 1e-12
            cosines.append(_dot(w, axis))
        _check(cosines, (e + 1.0) / (e + 2.0))
