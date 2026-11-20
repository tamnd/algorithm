# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sar-backprojection/. The authors are listed in prov/KA63T0.jsonl.
"""Time-domain backprojection for SAR, for any flight path.

Geometry: the scene is a plane with points (x, y). Pulse p is sent from the
antenna position pos[p] = (x, y, z), so a point at (x, y) has the range
R_p = |pos[p] - (x, y, 0)|. Nothing assumes a straight path or a constant
speed.

Signals: complex baseband, range-compressed. Sample j of pulse p is the
two-way delay t0 + j / fs. A point target of amplitude a gives
a sinc(B (t - 2 R_p / c)) exp(-i 4 pi f0 R_p / c), the ideal compressed
pulse of bandwidth B. The Fourier sign is exp(-i 2 pi f t), the sign of the
DFT. Backprojection undoes the carrier phase with exp(+i 4 pi f0 R / c).
"""

import cmath
import math

from imgkit import dft, idft

C = 3.0e8


def sinc(x):
    return 1.0 if x == 0 else math.sin(math.pi * x) / (math.pi * x)


def simulate_compressed(pos, targets, f0, bandwidth, fs, t0, n):
    """Range-compressed pulses data[p][j] of point targets (x, y, amplitude)."""
    data = []
    for px, py, pz in pos:
        row = [0j] * n
        for x, y, amp in targets:
            r = math.sqrt((px - x) ** 2 + (py - y) ** 2 + pz ** 2)
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


def backproject(data, pos, pixels, f0, fs, t0, factor=8):
    """The complex image value at each pixel (x, y): sum over pulses of d_p(R_p) exp(+i 4 pi f0 R_p / c)."""
    out = [0j] * len(pixels)
    step = C / (2.0 * fs * factor)  # range spacing of the upsampled samples
    r0 = C * t0 / 2.0
    for row, (px, py, pz) in zip(data, pos):
        fine = upsample(row, factor)  # @line L1
        last = len(fine) - 1
        for i, (x, y) in enumerate(pixels):
            r = math.sqrt((px - x) ** 2 + (py - y) ** 2 + pz ** 2)  # @line L2
            u = (r - r0) / step  # @line L3
            k = math.floor(u)
            if k < 0 or k >= last:
                continue
            w = u - k
            val = (1.0 - w) * fine[k] + w * fine[k + 1]  # @line L4
            out[i] += val * cmath.exp(4j * math.pi * f0 * r / C)  # @line L5
    return out  # @line L6


def backproject_exact(data, pos, pixels, f0, bandwidth, fs, t0):
    """Brute force: the same sum with the exact sinc interpolation over all samples.

    The data rows were sampled from sinc(B t) pulses, so the sum over all
    samples of d_j sinc(fs (t - t_j)) recovers the pulse at any delay t when
    fs >= B. This costs O(n) per pixel and pulse instead of O(1).
    """
    out = [0j] * len(pixels)
    for row, (px, py, pz) in zip(data, pos):
        for i, (x, y) in enumerate(pixels):
            r = math.sqrt((px - x) ** 2 + (py - y) ** 2 + pz ** 2)
            t = 2.0 * r / C
            val = sum(d * sinc(fs * (t - t0 - j / fs)) for j, d in enumerate(row) if d != 0)
            out[i] += val * cmath.exp(4j * math.pi * f0 * r / C)
    return out


def image_grid(xs, ys):
    """The pixel list of a grid: row-major, y outer."""
    return [(x, y) for y in ys for x in xs]
