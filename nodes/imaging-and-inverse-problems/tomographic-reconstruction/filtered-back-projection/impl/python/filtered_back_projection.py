# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filtered-back-projection/. The authors are listed in prov/M3HFA2.jsonl.
"""Filtered back-projection for parallel-beam data.

Conventions:
- The sinogram is a list of a projections, one per angle theta_k = k pi / a,
  each a list of d detector values. Bin j has its center at
  s_j = (j - (d - 1) / 2) tau, with the detector spacing tau.
- The projection at angle theta is the Radon transform
  R f(theta, s) = integral f(s omega + t omega_perp) dt with
  omega = (cos theta, sin theta).
- The output is an n x n image on [-1, 1]^2. Pixel (i, j) has its center at
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n, so y goes up.
"""

import math

from imgkit import dft, idft, pixel_centers


def ram_lak_kernel(d, tau):
    """Samples h(m tau), m = -(d - 1) .. d - 1, of the ramp filter band-limited to 1 / (2 tau).

    Entry m + d - 1 holds h(m tau): 1 / (4 tau^2) at m = 0, 0 at even m, and
    -1 / (m^2 pi^2 tau^2) at odd m.
    """
    out = []
    for m in range(-(d - 1), d):
        if m == 0:
            out.append(1.0 / (4.0 * tau * tau))
        elif m % 2 == 0:
            out.append(0.0)
        else:
            out.append(-1.0 / (m * m * math.pi * math.pi * tau * tau))
    return out


def shepp_logan_kernel(d, tau):
    """Samples h(m tau) = -2 / (pi^2 tau^2 (4 m^2 - 1)), m = -(d - 1) .. d - 1."""
    return [-2.0 / (math.pi * math.pi * tau * tau * (4 * m * m - 1)) for m in range(-(d - 1), d)]


def filter_projection_direct(p, h, tau):
    """q_j = tau sum_k h((j - k) tau) p_k, the aperiodic convolution by a direct sum."""
    d = len(p)
    return [tau * sum(h[j - k + d - 1] * p[k] for k in range(d)) for j in range(d)]


def kernel_spectrum(h, d, length):
    """The DFT of length `length` of the kernel, wrapped so that h(0) sits at index 0."""
    buf = [0.0] * length
    for m in range(-(d - 1), d):
        buf[m % length] = h[m + d - 1]
    return dft(buf)


def filter_projection(p, hf, tau):
    """The same q as filter_projection_direct, by FFT with zero padding to len(hf) >= 2 d - 1."""
    d, length = len(p), len(hf)
    pf = dft(list(p) + [0.0] * (length - d))
    q = idft([u * v for u, v in zip(pf, hf)])
    return [tau * q[j].real for j in range(d)]


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


def back_project(qs, tau, n):
    """(pi / a) sum_k q_k(x cos theta_k + y sin theta_k) at each pixel center, theta_k = k pi / a."""
    a, d = len(qs), len(qs[0])
    xs, ys = pixel_centers(n)
    c0 = (d - 1) / 2.0
    img = [[0.0] * n for _ in range(n)]
    for k, q in enumerate(qs):
        theta = k * math.pi / a
        c, s = math.cos(theta), math.sin(theta)
        for i, y in enumerate(ys):  # @line L7
            row = img[i]
            for j, x in enumerate(xs):
                row[j] += lin_interp(q, (x * c + y * s) / tau + c0)  # @line L8
    w = math.pi / a
    return [[w * v for v in row] for row in img]  # @line L9


def filtered_back_projection(sino, tau, n, kernel="ram-lak"):
    """Reconstruct an n x n image from a parallel-beam sinogram on [0, pi)."""
    a, d = len(sino), len(sino[0])  # @line L1
    if kernel == "ram-lak":  # @line L2
        h = ram_lak_kernel(d, tau)
    elif kernel == "shepp-logan":
        h = shepp_logan_kernel(d, tau)
    else:
        raise ValueError("unknown kernel")
    length = 1  # @line L3
    while length < 2 * d - 1:
        length *= 2
    hf = kernel_spectrum(h, d, length)  # @line L4
    qs = []
    for k in range(a):  # @line L5
        qs.append(filter_projection(sino[k], hf, tau))  # @line L6
    return back_project(qs, tau, n)
