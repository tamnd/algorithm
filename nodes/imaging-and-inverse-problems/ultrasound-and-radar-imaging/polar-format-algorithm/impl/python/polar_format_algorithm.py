# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polar-format-algorithm/. The authors are listed in prov/8JG48Y.jsonl.
"""Polar format algorithm (PFA) for spotlight SAR.

Geometry: the scene is a plane with points p = (x, y) and its center at the
origin. Pulse m looks at the center from the angle theta_m, from the radar
position a_m = -Rc (sin theta_m, cos theta_m). The radar dechirps each echo
against the echo of the center, so fast-time sample n of pulse m holds

    d[m][n] = sum over targets of amp exp(-i u_n dR_m(p)),

with u_n = 4 pi (f0 + Kr t_n) / c and dR_m(p) = |a_m - p| - Rc, the range
relative to the center. The Fourier sign is exp(-i 2 pi f t), the sign of the
DFT, so the image is a sum with exp(+i ...). In the far field,
dR_m(p) is close to x sin theta_m + y cos theta_m, so d samples the 2D Fourier
transform of the scene on a polar raster: radius u_n, angle theta_m. PFA
resamples this raster onto a Cartesian grid (range then azimuth, the keystone
order) and takes one 2D inverse DFT.
"""

import cmath
import math

from imgkit import fftshift, idft2

C = 3.0e8


class Spotlight:
    """The parameters of a spotlight collection (SI units)."""

    def __init__(self, f0=10e9, bandwidth=1e9, n_fast=32, n_pulses=32, span=0.1, rc=1000.0):
        self.f0 = f0
        self.bandwidth = bandwidth
        self.n_fast = n_fast
        self.n_pulses = n_pulses
        self.span = span  # the total change of look angle, in radians
        self.rc = rc

    def u(self, n):
        """The radial spatial frequency of fast-time sample n (rad/m)."""
        f = self.f0 - self.bandwidth / 2 + self.bandwidth * n / (self.n_fast - 1)
        return 4.0 * math.pi * f / C

    def theta(self, m):
        return -self.span / 2 + self.span * m / (self.n_pulses - 1)


def simulate_dechirped(g, targets, plane_wave=False):
    """Dechirped data d[m][n] of point targets (x, y, amp): exact ranges, or the plane-wave model."""
    data = []
    for m in range(g.n_pulses):
        th = g.theta(m)
        s, c = math.sin(th), math.cos(th)
        ax, ay = -g.rc * s, -g.rc * c
        row = [0j] * g.n_fast
        for x, y, amp in targets:
            dr = x * s + y * c if plane_wave else math.hypot(x - ax, y - ay) - g.rc
            for n in range(g.n_fast):
                row[n] += amp * cmath.exp(-1j * g.u(n) * dr)
        data.append(row)
    return data


def sinc_interp(seq, t, taps=8):
    """Value of a sampled band-limited sequence at the fractional index t (Hann-windowed sinc)."""
    half = taps // 2
    i0 = math.floor(t)
    acc = 0j
    for k in range(i0 - half + 1, i0 + half + 1):
        if 0 <= k < len(seq):
            x = t - k
            w = 1.0 if x == 0 else math.sin(math.pi * x) / (math.pi * x)
            acc += seq[k] * w * (0.5 + 0.5 * math.cos(math.pi * x / half))
    return acc


def cartesian_grid(g):
    """The keystone grid inside the polar annulus: ky values (rows) and kx values (columns)."""
    half = g.span / 2
    ky_lo, ky_hi = g.u(0), g.u(g.n_fast - 1) * math.cos(half)
    kys = [ky_lo + (ky_hi - ky_lo) * n / (g.n_fast - 1) for n in range(g.n_fast)]
    kx_hi = ky_lo * math.tan(half)
    kxs = [-kx_hi + 2 * kx_hi * m / g.n_pulses for m in range(g.n_pulses)]
    return kys, kxs


def pixel_coords(g):
    """The image coordinates: ys for rows, xs for columns, both centered on the scene center."""
    kys, kxs = cartesian_grid(g)
    dky = kys[1] - kys[0]
    dkx = kxs[1] - kxs[0]
    ny, nx = len(kys), len(kxs)
    ys = [2 * math.pi * (i - ny // 2) / (ny * dky) for i in range(ny)]
    xs = [2 * math.pi * (j - nx // 2) / (nx * dkx) for j in range(nx)]
    return ys, xs


def pfa(g, data):
    """Focus dechirped spotlight data. Returns img[i][j] at (xs[j], ys[i]) of pixel_coords."""
    kys, kxs = cartesian_grid(g)
    u0 = g.u(0)
    du = g.u(1) - g.u(0)
    dth = g.span / (g.n_pulses - 1)
    # range interpolation: on pulse m, the sample with u cos(theta_m) = ky
    stage = []
    for m in range(g.n_pulses):
        c = math.cos(g.theta(m))
        stage.append([sinc_interp(data[m], (ky / c - u0) / du) for ky in kys])  # @line L1
    # azimuth interpolation: on row ky, the pulse with ky tan(theta) = kx
    grid = []
    for n, ky in enumerate(kys):
        col = [stage[m][n] for m in range(g.n_pulses)]
        grid.append([sinc_interp(col, (math.atan2(kx, ky) + g.span / 2) / dth) for kx in kxs])  # @line L2
    img = fftshift(idft2(grid))  # @line L3
    ys, xs = pixel_coords(g)
    ny, nx = len(kys), len(kxs)
    return [[img[i][j] * ny * nx * cmath.exp(1j * (kys[0] * ys[i] + kxs[0] * xs[j]))
             for j in range(nx)] for i in range(ny)]  # @line L4


def polar_sum(g, data, pixels):
    """Brute force: the direct polar Fourier sum at each pixel (x, y), O(N^2) per pixel."""
    out = []
    for x, y in pixels:
        acc = 0j
        for m in range(g.n_pulses):
            th = g.theta(m)
            proj = x * math.sin(th) + y * math.cos(th)
            for n in range(g.n_fast):
                acc += data[m][n] * cmath.exp(1j * g.u(n) * proj)
        out.append(acc)
    return out
