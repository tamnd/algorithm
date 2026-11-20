# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-focusing-method/. The authors are listed in prov/91YVZD.jsonl.
"""Total focusing method (TFM) on full matrix capture data.

Units: millimetres, microseconds and megahertz, so the speed of sound in soft
tissue, 1540 m/s, is 1.54 mm/us. The array lies on the line z = 0, with
element i at (x_i, 0). Depth z is positive down.

The data D[i][j] is the complex baseband (IQ) trace for transmit element i and
receive element j, sampled at t_k = t0 + k / fs. The analytic RF signal is
r(t) = b(t) exp(i 2 pi f0 t), where b is the baseband signal.

TFM forms, at every pixel p, the coherent sum over all transmit and receive
pairs of r_ij at the two-way time (|p - e_i| + |p - e_j|) / c, and returns its
modulus. The complex sum is a linear map of the data; tfm_adjoint is its exact
adjoint (a discrete pulse-echo model with the same interpolation).
"""

import cmath
import math

SOUND_SPEED = 1.54  # mm per microsecond, the soft tissue convention of 1540 m/s


def element_positions(m_count, pitch):
    """x positions of a linear array of m_count elements, centered at x = 0."""
    return [(i - (m_count - 1) / 2) * pitch for i in range(m_count)]


def one_way_times(px, pz, elements, c=SOUND_SPEED):
    """Travel times from each element (x_i, 0) to the point (px, pz)."""
    return [math.hypot(px - xe, pz) / c for xe in elements]


def simulate_fmc(elements, scatterers, f0, sigma_t, fs, t0, ns, c=SOUND_SPEED):
    """Full matrix capture of point scatterers: D[i][j][k] in complex baseband.

    Each scatterer (x, z, a) adds a * g(t - tau) * exp(-i 2 pi f0 tau) to the
    trace (i, j), with g a Gaussian envelope of standard deviation sigma_t and
    tau the two-way time. Geometric spreading and directivity are left out.
    """
    m_count = len(elements)
    data = [[[0j] * ns for _ in range(m_count)] for _ in range(m_count)]
    for (sx, sz, amp) in scatterers:
        d = one_way_times(sx, sz, elements, c)
        for i in range(m_count):
            for j in range(m_count):
                tau = d[i] + d[j]
                rot = amp * cmath.exp(-2j * math.pi * f0 * tau)
                lo = max(0, math.ceil((tau - 5 * sigma_t - t0) * fs))
                hi = min(ns - 1, math.floor((tau + 5 * sigma_t - t0) * fs))
                trace = data[i][j]
                for k in range(lo, hi + 1):
                    dt = t0 + k / fs - tau
                    trace[k] += rot * math.exp(-dt * dt / (2 * sigma_t * sigma_t))
    return data


def sample(trace, t, t0, fs, f0):
    """The analytic RF value r(t) from a baseband trace, by linear interpolation."""
    u = (t - t0) * fs  # @line L9
    k = math.floor(u)
    phi = u - k
    if k < 0 or k + 1 >= len(trace):  # @line L10
        return 0j
    return ((1 - phi) * trace[k] + phi * trace[k + 1]) * cmath.exp(2j * math.pi * f0 * t)  # @line L11


def tfm_complex(data, elements, xs, zs, t0, fs, f0, c=SOUND_SPEED):
    """The complex TFM image before the modulus: rows follow zs, columns follow xs."""
    m_count = len(elements)
    image = []
    for pz in zs:  # @line L1
        row = []
        for px in xs:
            d = one_way_times(px, pz, elements, c)  # @line L2
            acc = 0j  # @line L3
            for i in range(m_count):  # @line L4
                for j in range(m_count):  # @line L5
                    acc += sample(data[i][j], d[i] + d[j], t0, fs, f0)  # @line L6
            row.append(acc)
        image.append(row)
    return image


def tfm(data, elements, xs, zs, t0, fs, f0, c=SOUND_SPEED):
    """The TFM image |sum_ij r_ij(d_i + d_j)| on the grid xs by zs."""
    image = [[abs(v) for v in row] for row in tfm_complex(data, elements, xs, zs, t0, fs, f0, c)]  # @line L7
    return image  # @line L8


def tfm_half(data, elements, xs, zs, t0, fs, f0, c=SOUND_SPEED):
    """TFM that uses reciprocity: only pairs i <= j, the pairs i < j counted twice.

    It equals tfm when D[i][j] = D[j][i], and does about half the work.
    """
    m_count = len(elements)
    image = []
    for pz in zs:
        row = []
        for px in xs:
            d = one_way_times(px, pz, elements, c)
            acc = 0j
            for i in range(m_count):
                acc += sample(data[i][i], 2 * d[i], t0, fs, f0)
                for j in range(i + 1, m_count):
                    acc += 2 * sample(data[i][j], d[i] + d[j], t0, fs, f0)
            row.append(abs(acc))
        image.append(row)
    return image


def tfm_adjoint(image, elements, xs, zs, t0, fs, f0, ns, c=SOUND_SPEED):
    """The exact adjoint of tfm_complex: spread each pixel value into the data.

    For each pixel and pair, the interpolation weights and the conjugate phase
    put the value back on the two samples that SAMPLE read.
    """
    m_count = len(elements)
    data = [[[0j] * ns for _ in range(m_count)] for _ in range(m_count)]
    for iz, pz in enumerate(zs):
        for ix, px in enumerate(xs):
            v = image[iz][ix]
            d = one_way_times(px, pz, elements, c)
            for i in range(m_count):
                for j in range(m_count):
                    t = d[i] + d[j]
                    u = (t - t0) * fs
                    k = math.floor(u)
                    if k < 0 or k + 1 >= ns:
                        continue
                    phi = u - k
                    w = v * cmath.exp(-2j * math.pi * f0 * t)
                    data[i][j][k] += (1 - phi) * w
                    data[i][j][k + 1] += phi * w
    return data
