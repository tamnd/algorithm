# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plane-wave-compounding/. The authors are listed in prov/HTFN8H.jsonl.
"""Coherent plane-wave compounding (Montaldo et al. 2009).

Units: millimetres, microseconds and megahertz; 1540 m/s is 1.54 mm/us.
The array lies on z = 0 with element j at (x_j, 0), centered at x = 0. For the
steering angle alpha, the plane wave travels in the direction
(sin alpha, cos alpha), and the time origin is the moment its wavefront passes
the point (0, 0). The wave then reaches (x, z) at (z cos alpha + x sin alpha) / c.

data[a][j] is the complex baseband (IQ) trace of receive element j for angle a,
sampled at t0 + q / fs; the analytic RF signal is b(t) exp(i 2 pi f0 t).
For each angle the beamformer sums the receive elements at the transmit time
plus the receive time; compounding adds the complex images of all angles
before the modulus.
"""

import cmath
import math

SOUND_SPEED = 1.54  # mm per microsecond


def element_positions(m_count, pitch):
    """x positions of a linear array of m_count elements, centered at x = 0."""
    return [(j - (m_count - 1) / 2) * pitch for j in range(m_count)]


def transmit_time(px, pz, alpha, c=SOUND_SPEED):
    """The time at which the plane wave of angle alpha reaches (px, pz)."""
    return (pz * math.cos(alpha) + px * math.sin(alpha)) / c


def simulate_plane_waves(elements, angles, scatterers, f0, sigma_t, fs, t0, ns, c=SOUND_SPEED):
    """data[a][j]: echoes of point scatterers (x, z, amp) for each plane wave."""
    data = []
    for alpha in angles:
        per_angle = []
        for xj in elements:
            tr = [0j] * ns
            for (sx, sz, amp) in scatterers:
                tau = transmit_time(sx, sz, alpha, c) + math.hypot(sx - xj, sz) / c
                rot = amp * cmath.exp(-2j * math.pi * f0 * tau)
                lo = max(0, math.ceil((tau - 5 * sigma_t - t0) * fs))
                hi = min(ns - 1, math.floor((tau + 5 * sigma_t - t0) * fs))
                for q in range(lo, hi + 1):
                    dt = t0 + q / fs - tau
                    tr[q] += rot * math.exp(-dt * dt / (2 * sigma_t * sigma_t))
            per_angle.append(tr)
        data.append(per_angle)
    return data


def sample(trace, t, t0, fs, f0):
    """The analytic RF value of a baseband trace at time t, by linear interpolation."""
    u = (t - t0) * fs
    q = math.floor(u)
    phi = u - q
    if q < 0 or q + 1 >= len(trace):
        return 0j
    return ((1 - phi) * trace[q] + phi * trace[q + 1]) * cmath.exp(2j * math.pi * f0 * t)


def _in_aperture(px, pz, xj, fnum):
    return fnum is None or abs(px - xj) <= pz / (2 * fnum)


def compound_complex(data, elements, angles, xs, zs, t0, fs, f0, fnum=None, c=SOUND_SPEED):
    """The complex compounded image; rows follow zs, columns follow xs."""
    image = []
    for pz in zs:  # @line L1
        row = []
        for px in xs:
            rx = [math.hypot(px - xj, pz) / c for xj in elements]  # @line L2
            acc = 0j  # @line L3
            for a, alpha in enumerate(angles):  # @line L4
                tx = transmit_time(px, pz, alpha, c)  # @line L5
                for j, xj in enumerate(elements):  # @line L6
                    if _in_aperture(px, pz, xj, fnum):  # @line L7
                        acc += sample(data[a][j], tx + rx[j], t0, fs, f0)  # @line L8
            row.append(acc)
        image.append(row)
    return image


def compound(data, elements, angles, xs, zs, t0, fs, f0, fnum=None, c=SOUND_SPEED):
    """The compounded image: the modulus of the coherent sum over angles and elements."""
    return [[abs(v) for v in row]
            for row in compound_complex(data, elements, angles, xs, zs, t0, fs, f0, fnum, c)]  # @line L9


def compound_adjoint(image, elements, angles, xs, zs, t0, fs, f0, ns, fnum=None, c=SOUND_SPEED):
    """The exact adjoint of compound_complex: a discrete plane-wave pulse-echo model."""
    data = [[[0j] * ns for _ in elements] for _ in angles]
    for iz, pz in enumerate(zs):
        for ix, px in enumerate(xs):
            v = image[iz][ix]
            for a, alpha in enumerate(angles):
                tx = transmit_time(px, pz, alpha, c)
                for j, xj in enumerate(elements):
                    if not _in_aperture(px, pz, xj, fnum):
                        continue
                    t = tx + math.hypot(px - xj, pz) / c
                    u = (t - t0) * fs
                    q = math.floor(u)
                    if q < 0 or q + 1 >= ns:
                        continue
                    phi = u - q
                    w = v * cmath.exp(-2j * math.pi * f0 * t)
                    data[a][j][q] += (1 - phi) * w
                    data[a][j][q + 1] += phi * w
    return data
