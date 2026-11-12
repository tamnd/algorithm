# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gouraud-shading/. The authors are listed in prov/43E96Q.jsonl.

import math
from fractions import Fraction
from numbers import Rational

Vec3 = tuple[float, float, float]
Point = tuple[int, int]


def vertex_normals(positions: list[Vec3], faces: list[tuple[int, int, int]]) -> list[Vec3]:
    """Return a unit normal per vertex: the normalized sum of the normals of the faces around it.

    The face normal is the cross product of two edges, so larger faces weigh more.
    A vertex in no face, or with normals that cancel, gets (0, 0, 0).
    Cost: O(V + F) time for V vertices and F faces.
    """
    acc = [[0.0, 0.0, 0.0] for _ in positions]
    for a, b, c in faces:
        pa, pb, pc = positions[a], positions[b], positions[c]
        u = [pb[t] - pa[t] for t in range(3)]
        v = [pc[t] - pa[t] for t in range(3)]
        n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        for k in (a, b, c):
            for t in range(3):
                acc[k][t] += n[t]
    out: list[Vec3] = []
    for x, y, z in acc:
        length = math.sqrt(x * x + y * y + z * z)
        out.append((x / length, y / length, z / length) if length > 0 else (0.0, 0.0, 0.0))
    return out


def lambert_intensity(normal: Vec3, light: Vec3, ka: float, kd: float) -> float:
    """Ambient plus Lambert diffuse intensity ka + kd max(0, n . l) for unit vectors n and l."""
    d = normal[0] * light[0] + normal[1] * light[1] + normal[2] * light[2]
    return ka + kd * max(0.0, d)


def gouraud_triangle(
    verts: tuple[Point, Point, Point],
    intensities: tuple[Rational, Rational, Rational] | tuple[float, float, float],
    width: int,
    height: int,
    sub: int = 16,
) -> list[tuple[int, int, Rational | float]]:
    """Gouraud scanline interpolation of vertex intensities over one triangle.

    The vertices are integers in units of 1/sub pixel (sub even), y down, and pixel
    (i, j) has its center at (i*sub + sub/2, j*sub + sub/2). The rows are half-open
    [ymin, ymax) and each span is half-open [xl, xr), which covers the same centers
    as the top-left rule. Intensities are linear along each edge and along each span.
    With Fraction intensities the result is exact. Returns (i, j, I) in row-major order.

    Cost: O(h + c) for h rows of the bounding box and c covered pixels; O(1) extra space.
    """
    v = verts
    area2 = (v[1][0] - v[0][0]) * (v[2][1] - v[0][1]) - (v[1][1] - v[0][1]) * (v[2][0] - v[0][0])
    out: list[tuple[int, int, Rational | float]] = []
    if area2 == 0:
        return out
    half = sub // 2
    edges = []
    for k in range(3):
        a, b = k, (k + 1) % 3
        if v[a][1] == v[b][1]:
            continue  # a horizontal edge is never active on a half-open row range
        if v[a][1] > v[b][1]:
            a, b = b, a
        edges.append((v[a], v[b], intensities[a], intensities[b]))
    ymin = min(p[1] for p in v)
    ymax = max(p[1] for p in v)
    j0 = max(0, -((half - ymin) // sub))
    for j in range(j0, height):  # @line L1
        yc = j * sub + half
        if yc >= ymax:
            break
        ends = []
        for pa, pb, ia, ib in edges:  # @line L2
            if pa[1] <= yc < pb[1]:
                t = Fraction(yc - pa[1], pb[1] - pa[1])
                ends.append((pa[0] + t * (pb[0] - pa[0]), ia + t * (ib - ia)))  # @line L3
        (xl, il), (xr, ir) = sorted(ends, key=lambda e: e[0])  # @line L4
        if xl == xr:  # @line L5
            continue
        di = (ir - il) / (xr - xl)  # @line L6
        i = max(0, math.ceil((xl - half) / sub))  # @line L7
        xc = i * sub + half
        value = il + (xc - xl) * di  # @line L8
        step = sub * di
        while xc < xr and i < width:  # @line L9
            out.append((i, j, value))  # @line L10
            value += step  # @line L11
            i += 1
            xc += sub
    return out
