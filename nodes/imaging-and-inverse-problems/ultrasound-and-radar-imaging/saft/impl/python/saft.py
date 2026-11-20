# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saft/. The authors are listed in prov/4W5EDR.jsonl.
"""Synthetic aperture focusing technique (SAFT), time domain.

Units: millimetres, microseconds and megahertz; 1540 m/s is 1.54 mm/us.
One transducer sits in turn at the positions (x_k, 0), sends a pulse and
records the echo at the same position (monostatic, pulse-echo). Trace k is a
complex baseband (IQ) signal b_k sampled at t0 + q / fs; the analytic RF signal
is r_k(t) = b_k(t) exp(i 2 pi f0 t).

At each pixel p = (x, z), SAFT sums r_k at the two-way time 2 |p - (x_k, 0)| / c,
that is along the hyperbola that a point at p draws in the B-scan, and takes
the modulus. An optional half angle limits the sum to the positions that see
p inside the beam of the transducer: |x - x_k| <= z tan(half_angle).
"""

import cmath
import math

SOUND_SPEED = 1.54  # mm per microsecond


def scan_positions(k_count, step):
    """x positions of the scan, centered at x = 0."""
    return [(k - (k_count - 1) / 2) * step for k in range(k_count)]


def simulate_bscan(positions, scatterers, f0, sigma_t, fs, t0, ns, c=SOUND_SPEED):
    """Monostatic traces of point scatterers (x, z, a) with a Gaussian envelope.

    No spreading loss and no beam directivity: every position sees every point.
    """
    traces = []
    for xk in positions:
        tr = [0j] * ns
        for (sx, sz, amp) in scatterers:
            tau = 2 * math.hypot(sx - xk, sz) / c
            rot = amp * cmath.exp(-2j * math.pi * f0 * tau)
            lo = max(0, math.ceil((tau - 5 * sigma_t - t0) * fs))
            hi = min(ns - 1, math.floor((tau + 5 * sigma_t - t0) * fs))
            for q in range(lo, hi + 1):
                dt = t0 + q / fs - tau
                tr[q] += rot * math.exp(-dt * dt / (2 * sigma_t * sigma_t))
        traces.append(tr)
    return traces


def sample(trace, t, t0, fs, f0):
    """The analytic RF value r(t) of a baseband trace, by linear interpolation."""
    u = (t - t0) * fs  # @line L8
    q = math.floor(u)
    phi = u - q
    if q < 0 or q + 1 >= len(trace):  # @line L9
        return 0j
    return ((1 - phi) * trace[q] + phi * trace[q + 1]) * cmath.exp(2j * math.pi * f0 * t)  # @line L10


def saft_complex(traces, positions, xs, zs, t0, fs, f0, half_angle=None, c=SOUND_SPEED):
    """The complex SAFT image before the modulus; rows follow zs, columns follow xs."""
    tan_half = None if half_angle is None else math.tan(half_angle)
    image = []
    for pz in zs:  # @line L1
        row = []
        for px in xs:
            acc = 0j  # @line L2
            for xk, tr in zip(positions, traces):  # @line L3
                if tan_half is not None and abs(px - xk) > pz * tan_half:  # @line L4
                    continue
                t = 2 * math.hypot(px - xk, pz) / c  # @line L5
                acc += sample(tr, t, t0, fs, f0)  # @line L6
            row.append(acc)
        image.append(row)
    return image


def saft(traces, positions, xs, zs, t0, fs, f0, half_angle=None, c=SOUND_SPEED):
    """The SAFT image |sum_k r_k(2 d_k(p))| on the grid xs by zs."""
    return [[abs(v) for v in row]
            for row in saft_complex(traces, positions, xs, zs, t0, fs, f0, half_angle, c)]  # @line L7


def saft_adjoint(image, positions, xs, zs, t0, fs, f0, ns, half_angle=None, c=SOUND_SPEED):
    """The exact adjoint of saft_complex: a discrete monostatic pulse-echo model."""
    tan_half = None if half_angle is None else math.tan(half_angle)
    traces = [[0j] * ns for _ in positions]
    for iz, pz in enumerate(zs):
        for ix, px in enumerate(xs):
            v = image[iz][ix]
            for k, xk in enumerate(positions):
                if tan_half is not None and abs(px - xk) > pz * tan_half:
                    continue
                t = 2 * math.hypot(px - xk, pz) / c
                u = (t - t0) * fs
                q = math.floor(u)
                if q < 0 or q + 1 >= ns:
                    continue
                phi = u - q
                w = v * cmath.exp(-2j * math.pi * f0 * t)
                traces[k][q] += (1 - phi) * w
                traces[k][q + 1] += phi * w
    return traces


def envelope_bscan(traces, positions, xs, zs, t0, fs, f0, c=SOUND_SPEED):
    """The unfocused B-scan: the envelope of the trace nearest to each column, at t = 2 z / c."""
    out = []
    for pz in zs:
        row = []
        for px in xs:
            k = min(range(len(positions)), key=lambda q: abs(positions[q] - px))
            row.append(abs(sample(traces[k], 2 * pz / c, t0, fs, f0)))
        out.append(row)
    return out
