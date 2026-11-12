# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phong-shading/. The authors are listed in prov/64PX56.jsonl.

import math
from fractions import Fraction

Vec3 = tuple[float, float, float]
Point = tuple[int, int]


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _unit(a: Vec3) -> Vec3:
    length = math.sqrt(_dot(a, a))
    return (a[0] / length, a[1] / length, a[2] / length)


def reflection_model(
    n: Vec3, light: Vec3, view: Vec3, ka: float, kd: float, ks: float, shininess: float, blinn: bool = False
) -> float:
    """Intensity of a unit normal n under a unit light direction and a unit view direction.

    Phong reflection model: ka + kd max(0, n.l) + ks max(0, r.v)^shininess with r = 2(n.l)n - l.
    With blinn=True the specular term is ks max(0, n.h)^shininess with h the unit half vector of l and v.
    The specular term is zero when the light is behind the surface (n.l <= 0).
    """
    nl = _dot(n, light)
    value = ka + kd * max(0.0, nl)
    if nl <= 0:
        return value
    if blinn:
        h = _unit((light[0] + view[0], light[1] + view[1], light[2] + view[2]))
        spec = max(0.0, _dot(n, h))
    else:
        r = (2 * nl * n[0] - light[0], 2 * nl * n[1] - light[1], 2 * nl * n[2] - light[2])
        spec = max(0.0, _dot(r, view))
    return value + ks * spec**shininess


def phong_triangle(
    verts: tuple[Point, Point, Point],
    normals: tuple[Vec3, Vec3, Vec3],
    light: Vec3,
    view: Vec3,
    material: tuple[float, float, float, float],
    width: int,
    height: int,
    sub: int = 16,
    blinn: bool = False,
) -> list[tuple[int, int, float]]:
    """Phong shading of one triangle: interpolate the vertex normals, normalize, light each pixel.

    The vertices are integers in units of 1/sub pixel (sub even), y down, and pixel (i, j)
    has its center at (i*sub + sub/2, j*sub + sub/2). Rows are half-open [ymin, ymax) and
    spans half-open [xl, xr), which covers the centers of the top-left rule. The normals are
    unit vectors; material is (ka, kd, ks, shininess). Returns (i, j, I) in row-major order.

    Cost: O(h + c) for h rows and c covered pixels, with one evaluation of the reflection
    model and one square root per covered pixel; O(1) extra space.
    """
    ka, kd, ks, shininess = material
    v = verts
    area2 = (v[1][0] - v[0][0]) * (v[2][1] - v[0][1]) - (v[1][1] - v[0][1]) * (v[2][0] - v[0][0])
    out: list[tuple[int, int, float]] = []
    if area2 == 0:
        return out
    half = sub // 2
    edges = []
    for k in range(3):
        a, b = k, (k + 1) % 3
        if v[a][1] == v[b][1]:
            continue
        if v[a][1] > v[b][1]:
            a, b = b, a
        edges.append((v[a], v[b], normals[a], normals[b]))
    ymin = min(p[1] for p in v)
    ymax = max(p[1] for p in v)
    for j in range(max(0, -((half - ymin) // sub)), height):  # @line L1
        yc = j * sub + half
        if yc >= ymax:
            break
        ends = []
        for pa, pb, na, nb in edges:  # @line L2
            if pa[1] <= yc < pb[1]:
                t = Fraction(yc - pa[1], pb[1] - pa[1])
                tf = float(t)
                n = tuple(na[q] + tf * (nb[q] - na[q]) for q in range(3))
                ends.append((pa[0] + t * (pb[0] - pa[0]), n))  # @line L3
        (xl, nl), (xr, nr) = sorted(ends, key=lambda e: e[0])  # @line L4
        if xl == xr:  # @line L5
            continue
        span = float(xr - xl)
        dn = tuple((nr[q] - nl[q]) / span for q in range(3))  # @line L6
        i = max(0, math.ceil((xl - half) / sub))  # @line L7
        xc = i * sub + half
        off = float(xc - xl)
        nvec = [nl[q] + off * dn[q] for q in range(3)]  # @line L8
        while xc < xr and i < width:  # @line L9
            unit = _unit((nvec[0], nvec[1], nvec[2]))  # @line L10
            out.append((i, j, reflection_model(unit, light, view, ka, kd, ks, shininess, blinn)))  # @line L11
            for q in range(3):  # @line L12
                nvec[q] += sub * dn[q]
            i += 1
            xc += sub
    return out
