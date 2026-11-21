# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feldkamp-davis-kress/. The authors are listed in prov/7MNYCN.jsonl.
"""The Feldkamp-Davis-Kress (FDK) algorithm for a circular cone-beam scan.

Conventions:
- omega(b) = (cos b, sin b, 0), omega_perp(b) = (-sin b, cos b, 0), e3 = (0, 0, 1).
- The source at the angle beta is S(beta) = D omega_perp(beta), on a circle of
  radius D in the plane z = 0 (the mid-plane).
- The detector is a virtual flat detector through the axis, normal to
  omega_perp(beta). The detector point (t, z) is t omega(beta) + z e3. The data
  g[k][r][j] is the line integral of f along the ray from S(beta_k) through the
  detector point (t_j, z_r), with beta_k = 2 pi k / a,
  t_j = (j - (d - 1) / 2) tau and z_r = (r - (m - 1) / 2) zeta.
- The output slices are n x n images on [-1, 1]^2 at given heights x3. Pixel
  (i, j) has its center at x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n.
"""

import math


def ram_lak(m, tau):
    """h(m tau) of the ramp filter |sigma| band-limited to 1 / (2 tau)."""
    if m == 0:
        return 1.0 / (4.0 * tau * tau)
    if m % 2 == 0:
        return 0.0
    return -1.0 / (m * m * math.pi * math.pi * tau * tau)


def cone_ray(beta, t, z, dist):
    """The source point and the unit direction of the ray to the detector point (t, z)."""
    c, s = math.cos(beta), math.sin(beta)
    src = (-dist * s, dist * c, 0.0)
    det = (t * c, t * s, z)
    v = (det[0] - src[0], det[1] - src[1], det[2] - src[2])
    norm = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    return src, (v[0] / norm, v[1] / norm, v[2] / norm)


def detector_coordinates(x, y, z, beta, dist):
    """(U, t', z') of the point (x, y, z): U = (D - x . omega_perp) / D, t' = x . omega / U, z' = z / U."""
    c, s = math.cos(beta), math.sin(beta)
    u = (dist - (-x * s + y * c)) / dist
    return u, (x * c + y * s) / u, z / u


def filter_row(p, kern, tau):
    """q_j = tau * sum_l kern[j - l] p_l, the aperiodic convolution by a direct sum."""
    d = len(p)
    return [tau * sum(kern[j - l + d - 1] * p[l] for l in range(d)) for j in range(d)]


def bilinear(q, u, v):
    """Interpolate q[r][j] at the fractional row index u and column index v, 0 outside."""
    r0, j0 = math.floor(u), math.floor(v)
    wu, wv = u - r0, v - j0
    val = 0.0
    for dr, fr in ((0, 1.0 - wu), (1, wu)):
        r = r0 + dr
        if fr == 0.0 or r < 0 or r >= len(q):
            continue
        row = q[r]
        for dj, fj in ((0, 1.0 - wv), (1, wv)):
            j = j0 + dj
            if fj != 0.0 and 0 <= j < len(row):
                val += fr * fj * row[j]
    return val


def fdk_filter(data, dist, tau, zeta):
    """Cosine weight and row-wise ramp filter (h / 2) of each projection."""
    a, m, d = len(data), len(data[0]), len(data[0][0])  # @line L1
    kern = [0.5 * ram_lak(i, tau) for i in range(-(d - 1), d)]  # @line L2
    ts = [(j - (d - 1) / 2.0) * tau for j in range(d)]
    zs = [(r - (m - 1) / 2.0) * zeta for r in range(m)]
    out = []
    for k in range(a):  # @line L3
        proj = []
        for r in range(m):
            w = [dist / math.sqrt(dist * dist + t * t + zs[r] * zs[r]) for t in ts]
            p = [wj * v for wj, v in zip(w, data[k][r])]  # @line L4
            proj.append(filter_row(p, kern, tau))  # @line L5
        out.append(proj)
    return out


def fdk(data, dist, tau, zeta, n, heights):
    """FDK reconstruction of the slices x3 = h for h in heights, each an n x n image."""
    a, m, d = len(data), len(data[0]), len(data[0][0])
    q = fdk_filter(data, dist, tau, zeta)
    xs = [-1.0 + (2 * j + 1) / n for j in range(n)]
    ys = [1.0 - (2 * i + 1) / n for i in range(n)]
    cz, ct = (m - 1) / 2.0, (d - 1) / 2.0
    vol = [[[0.0] * n for _ in range(n)] for _ in heights]
    for k in range(a):
        beta = 2.0 * math.pi * k / a
        for sl, x3 in enumerate(heights):
            for i, y in enumerate(ys):  # @line L6
                row = vol[sl][i]
                for j, x in enumerate(xs):
                    u, tp, zp = detector_coordinates(x, y, x3, beta, dist)  # @line L7
                    row[j] += bilinear(q[k], zp / zeta + cz, tp / tau + ct) / (u * u)  # @line L8
    w = 2.0 * math.pi / a
    return [[[w * v for v in row] for row in img] for img in vol]  # @line L9
