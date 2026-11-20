# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-factorized-backprojection/. The authors are listed in prov/NKKE4Y.jsonl.
"""Fast factorized backprojection (FFBP) for SAR on a straight track.

Geometry: the antenna moves along the x axis. Pulse p is sent from (xa[p], 0)
and the scene is in the half plane y > 0. Signals: complex baseband,
range-compressed. Sample j of a pulse is the two-way delay t0 + j / fs. A
point target of amplitude a gives a sinc(B (t - 2R/c)) exp(-i 4 pi f0 R / c).
The Fourier sign is exp(-i 2 pi f t), the sign of the DFT.

A subaperture with center (cx, 0) and length l stores a polar subimage
J(r, beta) on a grid of range r and direction cosine beta = (x - cx) / r.
The point with polar coordinates (r, beta) is (cx + r beta, r sqrt(1 - beta^2)).
J is the backprojection sum of the subaperture at that point times
exp(-i 4 pi f0 r / c), so J is smooth in beta: it needs a beta step of about
lambda / (4 l) only. Each stage merges pairs of subapertures, so the number of
beta samples doubles while the number of subimages halves.
"""

import cmath
import math

from imgkit import dft, idft

C = 3.0e8


def sinc(x):
    return 1.0 if x == 0 else math.sin(math.pi * x) / (math.pi * x)


def simulate_compressed(xa, targets, f0, bandwidth, fs, t0, n):
    """Range-compressed pulses data[p][j] of point targets (x, y, amplitude)."""
    data = []
    for ax in xa:
        row = [0j] * n
        for x, y, amp in targets:
            r = math.hypot(ax - x, y)
            ph = amp * cmath.exp(-4j * math.pi * f0 * r / C)
            for j in range(n):
                row[j] += ph * sinc(bandwidth * (t0 + j / fs - 2.0 * r / C))
        data.append(row)
    return data


def upsample(row, factor):
    """Band-limited interpolation by zero padding the DFT: factor times more samples."""
    n = len(row)
    spec = dft(row)
    half = n // 2
    padded = spec[:half] + [0j] * (n * factor - n) + spec[half:]
    return [v * factor for v in idft(padded)]


def direct_backprojection(data, xa, pixels, f0, fs, t0, factor=8):
    """Brute force: global backprojection, O(1) work per pulse and pixel."""
    step = C / (2.0 * fs * factor)
    out = [0j] * len(pixels)
    for row, ax in zip(data, xa):
        fine = upsample(row, factor)
        for i, (x, y) in enumerate(pixels):
            r = math.hypot(x - ax, y)
            out[i] += _lerp(fine, (r - C * t0 / 2.0) / step) * cmath.exp(4j * math.pi * f0 * r / C)
    return out


def _lerp(seq, u):
    k = math.floor(u)
    if k < 0 or k >= len(seq) - 1:
        return 0j
    w = u - k
    return (1.0 - w) * seq[k] + w * seq[k + 1]


class Polar:
    """A polar grid r_k = r_lo + k dr, beta_m = b_lo + m db, with values J[m][k]."""

    def __init__(self, cx, length, r_lo, dr, nr, b_lo, db, nb):
        self.cx, self.length = cx, length
        self.r_lo, self.dr, self.nr = r_lo, dr, nr
        self.b_lo, self.db, self.nb = b_lo, db, nb
        self.J = [[0j] * nr for _ in range(nb)]

    def point(self, m, k):
        r = self.r_lo + k * self.dr
        b = self.b_lo + m * self.db
        return self.cx + r * b, r * math.sqrt(1.0 - b * b), r

    def value(self, r, b):
        """Bilinear interpolation of J at (r, beta); zero outside the grid."""
        u = (r - self.r_lo) / self.dr
        k = math.floor(u)
        if k < 0 or k >= self.nr - 1:
            return 0j
        w = u - k
        if self.nb == 1:
            row = self.J[0]
            return (1.0 - w) * row[k] + w * row[k + 1]
        v = (b - self.b_lo) / self.db
        m = math.floor(v)
        if m < 0 or m >= self.nb - 1:
            return 0j
        z = v - m
        a0, a1 = self.J[m], self.J[m + 1]
        return ((1.0 - z) * ((1.0 - w) * a0[k] + w * a0[k + 1])
                + z * ((1.0 - w) * a1[k] + w * a1[k + 1]))


def _box(pixels):
    xs = [x for x, _ in pixels]
    ys = [y for _, y in pixels]
    return min(xs), max(xs), min(ys), max(ys)


def _grid_for(cx, length, box, dr, lam, oversample, margin=2):
    """The polar grid of a subaperture that covers the scene box (with a margin of samples)."""
    x0, x1, y0, y1 = box
    corners = [(x, y) for x in (x0, x1) for y in (y0, y1)]
    rs = [math.hypot(x - cx, y) for x, y in corners]
    bs = [(x - cx) / r for (x, y), r in zip(corners, rs)]
    near = y0 if x0 <= cx <= x1 else min(rs)  # the closest point may be on an edge
    r_lo = near - margin * dr
    nr = int(math.ceil((max(rs) + margin * dr - r_lo) / dr)) + 1
    db = lam / (oversample * length)
    b_lo = min(bs) - margin * db
    nb = int(math.ceil((max(bs) + margin * db - b_lo) / db)) + 1
    return r_lo, nr, b_lo, db, nb


def ffbp_cost(xa, box, n_pixels, f0, fs, factor=8, oversample=16.0, n_final=4):
    """The number of interpolations ffbp does, from the grid sizes alone (no data needed)."""
    lam = C / f0
    dr = C / (2.0 * fs * factor)
    spacing = xa[1] - xa[0]
    centers = list(xa)
    ops = sum(_grid_for(cx, spacing, box, dr, lam, oversample)[1] for cx in centers)
    length = spacing
    while len(centers) > n_final:
        centers = [0.5 * (a + b) for a, b in zip(centers[0::2], centers[1::2])]
        length *= 2
        for cx in centers:
            _, nr, _, _, nb = _grid_for(cx, length, box, dr, lam, oversample)
            ops += 2 * nr * nb
    return ops + len(centers) * n_pixels


def ffbp(data, xa, pixels, f0, fs, t0, factor=8, oversample=16.0, n_final=4, count=None):
    """Factorized backprojection. len(xa) must be n_final times a power of 2 and xa evenly spaced.

    Returns the image values at the pixels. If count is a list, the number of
    interpolations done is appended to it.
    """
    lam = C / f0
    dr = C / (2.0 * fs * factor)
    spacing = xa[1] - xa[0]
    box = _box(pixels)
    ops = 0
    subs = []
    for row, ax in zip(data, xa):  # stage 0: one pulse per subaperture, J does not depend on beta
        fine = upsample(row, factor)  # @line L1
        r_lo, nr = _grid_for(ax, spacing, box, dr, lam, oversample)[:2]
        s = Polar(ax, spacing, r_lo, dr, nr, 0.0, 1.0, 1)
        r0 = C * t0 / 2.0
        s.J[0] = [_lerp(fine, (r_lo + k * dr - r0) / dr) for k in range(nr)]  # @line L2
        ops += nr
        subs.append(s)
    while len(subs) > n_final:  # @line L3
        merged = []
        for a, b in zip(subs[0::2], subs[1::2]):
            cx = 0.5 * (a.cx + b.cx)
            length = a.length + b.length
            r_lo, nr, b_lo, db, nb = _grid_for(cx, length, box, dr, lam, oversample)  # @line L4
            s = Polar(cx, length, r_lo, dr, nr, b_lo, db, nb)
            for m in range(nb):
                row = s.J[m]
                for k in range(nr):
                    px, py, r = s.point(m, k)
                    acc = 0j
                    for child in (a, b):
                        rc = math.hypot(px - child.cx, py)  # @line L5
                        val = child.value(rc, (px - child.cx) / rc)  # @line L6
                        acc += val * cmath.exp(4j * math.pi * f0 * (rc - r) / C)  # @line L7
                    row[k] = acc
            ops += 2 * nr * nb
            merged.append(s)
        subs = merged  # @line L8
    out = [0j] * len(pixels)
    for s in subs:  # @line L9
        for i, (x, y) in enumerate(pixels):
            r = math.hypot(x - s.cx, y)
            out[i] += s.value(r, (x - s.cx) / r) * cmath.exp(4j * math.pi * f0 * r / C)
        ops += len(pixels)
    if count is not None:
        count.append(ops)
    return out


def image_grid(xs, ys):
    """The pixel list of a grid: row-major, y outer."""
    return [(x, y) for y in ys for x in xs]
