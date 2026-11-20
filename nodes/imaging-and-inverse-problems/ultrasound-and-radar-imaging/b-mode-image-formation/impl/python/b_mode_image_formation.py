# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-mode-image-formation/. The authors are listed in prov/P3DHGZ.jsonl.
"""B-mode image formation from beamformed RF lines.

The input is a set of real RF lines after beamforming, one per beam direction,
each sampled at the times t0 + q / fs. The steps are:

1. envelope detection: the magnitude of the analytic signal, computed with a
   DFT that keeps the zero frequency, doubles the positive frequencies and
   removes the negative ones;
2. time gain compensation (optional): multiply by a gain that grows with depth;
3. log compression to a dynamic range DR (a display choice), mapped to the
   gray levels 0 to 255;
4. scan conversion of a sector scan to a Cartesian grid by bilinear
   interpolation in (depth, angle).

Units are millimetres, microseconds and megahertz. Depth is z = c t / 2 with
c = 1.54 mm/us (1540 m/s), a convention for soft tissue.
"""

import math

from imgkit import dft, idft

SOUND_SPEED = 1.54  # mm per microsecond


def analytic_signal(x):
    """The discrete analytic signal of a real line: real part x, imaginary part a discrete Hilbert transform."""
    n = len(x)
    xf = dft(x)  # @line L2
    h = [0.0] * n
    h[0] = 1.0
    if n % 2 == 0:
        h[n // 2] = 1.0
        for k in range(1, n // 2):
            h[k] = 2.0
    else:
        for k in range(1, (n + 1) // 2):
            h[k] = 2.0
    return idft([hk * v for hk, v in zip(h, xf)])  # @line L3


def envelope(x):
    """The envelope |x + i H x| of a real line."""
    return [abs(v) for v in analytic_signal(x)]  # @line L4


def sample_depths(n, t0, fs, c=SOUND_SPEED):
    """Depth of sample q: z_q = c (t0 + q / fs) / 2."""
    return [c * (t0 + q / fs) / 2 for q in range(n)]


def tgc(env, depths, gain_db_per_mm):
    """Time gain compensation: multiply by 10^(gain_db_per_mm z / 20)."""
    return [e * 10 ** (gain_db_per_mm * z / 20) for e, z in zip(env, depths)]  # @line L5


def log_compress(lines, dynamic_range_db):
    """Gray levels 0..255 from envelopes: 20 log10(e / max) clipped to [-DR, 0], mapped linearly."""
    peak = max(max(row) for row in lines)  # @line L6
    out = []
    for row in lines:
        g = []
        for e in row:
            d = 20 * math.log10(e / peak) if e > 0 else -math.inf  # @line L7
            d = max(-dynamic_range_db, d)  # @line L8
            g.append(math.floor(255 * (d + dynamic_range_db) / dynamic_range_db + 0.5))  # @line L9
        out.append(g)
    return out


def scan_convert(polar, angles, depths, xs, zs):
    """Bilinear interpolation of polar[k][q] (line k at angle angles[k], depth depths[q]) on the grid (x, z).

    The angles and depths must be increasing and evenly spaced. The apex is at
    the origin and angle 0 points along +z. Pixels outside the sector are 0.
    """
    da = angles[1] - angles[0]
    dr = depths[1] - depths[0]
    out = []
    for z in zs:
        row = []
        for x in xs:
            r = math.hypot(x, z)  # @line L10
            th = math.atan2(x, z)
            u = (th - angles[0]) / da
            v = (r - depths[0]) / dr
            k, q = math.floor(u), math.floor(v)
            if u < 0 or v < 0 or u > len(angles) - 1 or v > len(depths) - 1:  # @line L11
                row.append(0.0)
                continue
            k, q = min(k, len(angles) - 2), min(q, len(depths) - 2)
            a, b = u - k, v - q
            row.append((1 - a) * (1 - b) * polar[k][q] + a * (1 - b) * polar[k + 1][q]  # @line L12
                       + (1 - a) * b * polar[k][q + 1] + a * b * polar[k + 1][q + 1])
        out.append(row)
    return out


def b_mode(lines, dynamic_range_db, gain_db_per_mm=0.0, t0=0.0, fs=1.0, c=SOUND_SPEED):
    """Envelope, optional TGC and log compression of every line (the image before scan conversion)."""
    depths = sample_depths(len(lines[0]), t0, fs, c)
    env = []
    for line in lines:  # @line L1
        e = envelope(line)
        if gain_db_per_mm:
            e = tgc(e, depths, gain_db_per_mm)
        env.append(e)
    return log_compress(env, dynamic_range_db)


def simulate_sector_lines(angles, n, t0, fs, f0, sigma_t, scatterers, beam_width, atten_db_per_mm=0.0,
                          c=SOUND_SPEED):
    """RF lines of a sector scan with point scatterers given as (r, theta, amplitude).

    A crude beam model: line k sees a scatterer at angle theta with the weight
    exp(-((theta - angle_k) / beam_width)^2 / 2). The echo is a Gaussian pulse
    at the two-way time 2 r / c, times 10^(-atten_db_per_mm 2 r / 20).
    """
    lines = []
    for ang in angles:
        line = [0.0] * n
        for (r, th, amp) in scatterers:
            w = amp * math.exp(-0.5 * ((th - ang) / beam_width) ** 2) * 10 ** (-atten_db_per_mm * 2 * r / 20)
            tau = 2 * r / c
            for q in range(n):
                dt = t0 + q / fs - tau
                line[q] += w * math.exp(-dt * dt / (2 * sigma_t * sigma_t)) * math.cos(2 * math.pi * f0 * dt)
        lines.append(line)
    return lines
