# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whitted-ray-tracing/. The authors are listed in prov/GC6JDN.jsonl.

import math

from whitted_ray_tracing import (
    Material,
    Plane,
    PointLight,
    Sphere,
    dot,
    normalize,
    pixel_ray,
    refract,
    render,
    trace,
)

# ---------------------------------------------------------------------------
# An independent brute force tracer. It recurses on the ray tree instead of using a stack,
# intersects spheres by the geometric method (closest approach of the center), and builds the
# reflected and refracted rays with Whitted's own formulas R = V' + 2N and P = kf (N + V') - N.
# ---------------------------------------------------------------------------


def _hit_sphere(c, r, o, d, eps):
    oc = (c[0] - o[0], c[1] - o[1], c[2] - o[2])
    tc = dot(oc, d)
    d2 = dot(oc, oc) - tc * tc
    if d2 > r * r:
        return None
    th = math.sqrt(max(0.0, r * r - d2))
    for t in (tc - th, tc + th):
        if t > eps:
            return t
    return None


def _hit_plane(p0, n, o, d, eps):
    den = dot(n, d)
    if abs(den) < 1e-300:
        return None
    t = ((p0[0] - o[0]) * n[0] + (p0[1] - o[1]) * n[1] + (p0[2] - o[2]) * n[2]) / den
    return t if t > eps else None


def _hits(scene, o, d, eps):
    out = []
    for obj in scene:
        if isinstance(obj, Sphere):
            t = _hit_sphere(obj.center, obj.radius, o, d, eps)
        else:
            t = _hit_plane(obj.point, obj.n, o, d, eps)
        if t is not None:
            out.append((t, obj))
    return out


def _whitted_reflect(v, n):
    s = 1.0 / abs(dot(v, n))
    vp = (v[0] * s, v[1] * s, v[2] * s)
    return normalize((vp[0] + 2 * n[0], vp[1] + 2 * n[1], vp[2] + 2 * n[2]))


def _whitted_refract(v, n, kn):
    """kn = n_transmitted / n_incident. None when kf is imaginary (total internal reflection)."""
    s = 1.0 / abs(dot(v, n))
    vp = (v[0] * s, v[1] * s, v[2] * s)
    tan = (vp[0] + n[0], vp[1] + n[1], vp[2] + n[2])
    q = kn * kn * dot(vp, vp) - dot(tan, tan)
    if q <= 0.0:
        return None
    kf = 1.0 / math.sqrt(q)
    return normalize((kf * tan[0] - n[0], kf * tan[1] - n[1], kf * tan[2] - n[2]))


def reference_trace(scene, lights, o, d, depth, background, eps=1e-7):
    hits = _hits(scene, o, d, eps)
    if not hits:
        return background
    t, obj = min(hits, key=lambda h: h[0])
    m = obj.material
    p = (o[0] + t * d[0], o[1] + t * d[1], o[2] + t * d[2])
    n = obj.normal(p)
    kn = 1.0 / m.eta if dot(n, d) > 0.0 else m.eta
    if dot(n, d) > 0.0:
        n = (-n[0], -n[1], -n[2])
    value = m.ka
    for light in lights:
        lv = (light.position[0] - p[0], light.position[1] - p[1], light.position[2] - p[2])
        dist = math.sqrt(dot(lv, lv))
        lu = (lv[0] / dist, lv[1] / dist, lv[2] / dist)
        cos_l = dot(n, lu)
        if m.kd > 0.0 and cos_l > 0.0:
            blocked = any(th < dist * (1.0 - eps) for th, _ in _hits(scene, p, lu, eps * dist))
            if not blocked:
                value += m.kd * light.intensity * cos_l
    if depth == 0:
        return value
    if m.ks > 0.0:
        value += m.ks * reference_trace(scene, lights, p, _whitted_reflect(d, n), depth - 1, background, eps)
    if m.kt > 0.0:
        pdir = _whitted_refract(d, n, kn)
        if pdir is not None:
            value += m.kt * reference_trace(scene, lights, p, pdir, depth - 1, background, eps)
    return value


def demo_scene():
    floor = Plane((0.0, -1.0, 0.0), (0.0, 1.0, 0.0), Material(ka=0.05, kd=0.6, ks=0.2))
    back = Plane((0.0, 0.0, -9.0), (0.0, 0.0, 1.0), Material(ka=0.1, kd=0.5))
    mirror = Sphere((-1.2, 0.0, -5.0), 1.0, Material(ka=0.02, kd=0.1, ks=0.8))
    glass = Sphere((1.1, -0.2, -4.0), 0.8, Material(ka=0.0, kd=0.05, ks=0.1, kt=0.85, eta=1.5))
    small = Sphere((0.3, -0.7, -6.0), 0.3, Material(ka=0.1, kd=0.7))
    lights = [PointLight((5.0, 6.0, 0.0), 0.7), PointLight((-4.0, 3.0, -2.0), 0.4)]
    return [floor, back, mirror, glass, small], lights


def test_image_matches_brute_force_tracer():
    objects, lights = demo_scene()
    w, h, tan_half = 24, 16, math.tan(math.radians(30.0))
    for depth in (0, 1, 3, 5):
        image = render(objects, lights, (0.0, 0.0, 0.0), w, h, tan_half, depth, background=0.3)
        for j in range(h):
            for i in range(w):
                o, d = pixel_ray((0.0, 0.0, 0.0), w, h, tan_half, i, j)
                ref = reference_trace(objects, lights, o, d, depth, 0.3)
                assert abs(image[j][i] - ref) <= 1e-9 * max(1.0, abs(ref)), (depth, i, j)


def test_diffuse_sphere_closed_form():
    # A sphere of radius 1 at distance 5, lit by a point light at the eye: the hit point of the
    # ray with direction d has the normal n, and the value is ka + kd E (n . -d).
    sphere = Sphere((0.0, 0.0, -5.0), 1.0, Material(ka=0.1, kd=0.8))
    light = PointLight((0.0, 0.0, 0.0), 1.0)
    for angle in (0.0, 0.05, 0.1, 0.15, 0.2):
        d = (math.sin(angle), 0.0, -math.cos(angle))
        # Closed form: distance to the hit is 5 cos a - sqrt(1 - 25 sin^2 a).
        t = 5.0 * math.cos(angle) - math.sqrt(1.0 - 25.0 * math.sin(angle) ** 2)
        p = (t * d[0], t * d[1], t * d[2])
        n = (p[0], p[1], p[2] + 5.0)
        expect = 0.1 + 0.8 * -dot(n, d)
        assert abs(trace([sphere], [light], (0.0, 0.0, 0.0), d, 3) - expect) < 1e-12


def test_parallel_mirrors_geometric_series():
    # Two facing mirrors with reflectance r and ambient a. The ray bounces between them, and the
    # tree cut at depth D gives a (1 - r^(D + 1)) / (1 - r).
    a, r = 0.1, 0.7
    mat = Material(ka=a, ks=r)
    objects = [Plane((0.0, 0.0, -1.0), (0.0, 0.0, 1.0), mat), Plane((0.0, 0.0, 1.0), (0.0, 0.0, -1.0), mat)]
    for depth in (0, 1, 2, 10, 60):
        got = trace(objects, [], (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), depth)
        assert abs(got - a * (1.0 - r ** (depth + 1)) / (1.0 - r)) < 1e-12


def test_glass_sphere_center_ray():
    # A ray through the center meets both surfaces at normal incidence, so it is not bent, and it
    # reaches the background with the weight kt^2; with ks = 0 nothing else contributes.
    kt = 0.9
    glass = Sphere((0.0, 0.0, -4.0), 1.0, Material(kt=kt, eta=1.5))
    got = trace([glass], [], (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), 5, background=1.0)
    assert abs(got - kt * kt) < 1e-12


def test_refraction_obeys_snell():
    n = (0.0, 0.0, 1.0)
    for deg in (0.0, 10.0, 30.0, 60.0, 85.0):
        th = math.radians(deg)
        d = (math.sin(th), 0.0, -math.cos(th))
        t = refract(d, n, 1.0 / 1.5)
        assert abs(dot(t, t) - 1.0) < 1e-12
        assert abs(1.0 * math.sin(th) - 1.5 * t[0]) < 1e-12
        assert abs(dot(t, normalize(_whitted_refract(d, n, 1.5))) - 1.0) < 1e-12


def test_total_internal_reflection():
    critical = math.asin(1.0 / 1.5)
    n = (0.0, 0.0, 1.0)
    for deg in (42.0, 50.0, 80.0):
        th = math.radians(deg)
        assert th > critical
        assert refract((math.sin(th), 0.0, -math.cos(th)), n, 1.5) is None
    assert refract((math.sin(critical - 1e-6), 0.0, -math.cos(critical - 1e-6)), n, 1.5) is not None
    # In a scene: a ray that starts inside a glass sphere and meets the surface beyond the critical
    # angle has no refracted child, so with ks = 0 it sees nothing of the bright background.
    glass = Sphere((0.0, 0.0, 0.0), 1.0, Material(kt=1.0, eta=1.5))
    o = (0.0, 0.9, 0.0)                      # the ray along +x hits at angle asin(0.9) = 64 degrees
    assert trace([glass], [], o, (1.0, 0.0, 0.0), 4, background=1.0) == 0.0
    o = (0.0, 0.5, 0.0)                      # asin(0.5) = 30 degrees is below the critical angle
    assert trace([glass], [], o, (1.0, 0.0, 0.0), 4, background=1.0) == 1.0


def test_shadow_ray_blocks_light():
    floor = Plane((0.0, -1.0, 0.0), (0.0, 1.0, 0.0), Material(kd=1.0))
    blocker = Sphere((0.0, 1.0, -5.0), 0.5, Material())
    light = PointLight((0.0, 3.0, -5.0), 1.0)
    d = normalize((0.0, -1.0, -5.0))         # hits the floor at (0, -1, -5), straight under the light
    assert trace([floor, blocker], [light], (0.0, 0.0, 0.0), d, 0) == 0.0
    assert abs(trace([floor], [light], (0.0, 0.0, 0.0), d, 0) - 1.0) < 1e-12
