# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambda-tomography/. The authors are listed in prov/8VWFH5.jsonl.
"""Lambda tomography: the local reconstruction Lambda f = (1 / (2 pi)) R^# (-d^2/ds^2) R f.

Conventions:
- omega(t) = (cos t, sin t). The sinogram P[k][j] samples the Radon transform
  R f(theta_k, s_j) with theta_k = k pi / a and s_j = (j - (d - 1) / 2) tau.
- R^# g(x) = integral_0^pi g(theta, x . omega(theta)) dtheta, approximated by
  (pi / a) sum_k.
- Lambda = (-Laplacian)^(1/2), with the Fourier multiplier 2 pi |xi| in
  ordinary frequency. Lambda^(-1) f = (1 / (2 pi)) R^# R f.
- The output is an n x n image on [-1, 1]^2, pixel (i, j) centered at
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n.
- A sample outside the detector counts as 0. Only the samples within one bin
  of x . omega(theta_k) enter the value at x (with mu = 0).
"""

import math


def lambda_filter(p, tau, mu=0.0):
    """q_j = -(p_(j+1) - 2 p_j + p_(j-1)) / tau^2 + mu p_j, with p = 0 outside the detector."""
    d = len(p)
    out = []
    for j in range(d):
        left = p[j - 1] if j > 0 else 0.0
        right = p[j + 1] if j + 1 < d else 0.0
        out.append(-(right - 2.0 * p[j] + left) / (tau * tau) + mu * p[j])
    return out


def lin_interp(q, u):
    """The linear interpolation of q at the fractional index u, and 0 outside [0, len(q) - 1]."""
    b = math.floor(u)
    w = u - b
    val = 0.0
    if 0 <= b < len(q):
        val += (1.0 - w) * q[b]
    if 0 <= b + 1 < len(q):
        val += w * q[b + 1]
    return val


def lambda_tomography(sino, tau, n, mu=0.0):
    """Lambda f + mu Lambda^(-1) f on an n x n grid from a parallel sinogram on [0, pi)."""
    a, d = len(sino), len(sino[0])  # @line L1
    qs = [lambda_filter(p, tau, mu) for p in sino]  # @line L2
    xs = [-1.0 + (2 * j + 1) / n for j in range(n)]
    ys = [1.0 - (2 * i + 1) / n for i in range(n)]
    c0 = (d - 1) / 2.0
    img = [[0.0] * n for _ in range(n)]
    for k, q in enumerate(qs):
        c, s = math.cos(k * math.pi / a), math.sin(k * math.pi / a)
        for i, y in enumerate(ys):  # @line L3
            row = img[i]
            for j, x in enumerate(xs):
                row[j] += lin_interp(q, (x * c + y * s) / tau + c0)  # @line L4
    w = 1.0 / (2.0 * a)  # (1 / (2 pi)) * (pi / a)
    return [[w * v for v in row] for row in img]  # @line L5


def lambda_at(sino, tau, x, y, mu=0.0):
    """The value of lambda_tomography at one point (x, y)."""
    a, d = len(sino), len(sino[0])
    c0 = (d - 1) / 2.0
    total = 0.0
    for k, p in enumerate(sino):
        q = lambda_filter(p, tau, mu)
        theta = k * math.pi / a
        total += lin_interp(q, (x * math.cos(theta) + y * math.sin(theta)) / tau + c0)
    return total / (2.0 * a)
