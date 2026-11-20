# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/capon-beamformer/. The authors are listed in prov/EAKMFX.jsonl.
"""The Capon (minimum variance distortionless response, MVDR) beamformer.

Narrowband form: for a Hermitian positive definite covariance R and a steering
vector a, the weights w = R^-1 a / (a^H R^-1 a) minimize the output power
w^H R w subject to w^H a = 1, and the minimum is 1 / (a^H R^-1 a).

Ultrasound form (Synnevag, Austeng and Holm 2007): after the focusing delays of
one pixel, the steering vector is the all-ones vector. The covariance comes
from one or more delayed snapshots by spatial smoothing over subarrays of
length L, with diagonal loading delta * trace(R) / L; both are design choices.

Linear algebra comes from the shared helper imgla (solve, dot).
"""

import cmath
import math

from imgla import dot, solve


def steering_vector(m_count, spacing, u):
    """a_m(u) = exp(-i 2 pi spacing m u) of a uniform linear array, spacing = d / lambda."""
    return [cmath.exp(-2j * math.pi * spacing * m * u) for m in range(m_count)]


def capon_weights(r, a, loading=0.0):
    """w = (R + loading I)^-1 a / (a^H (R + loading I)^-1 a)."""
    n = len(a)
    rl = [[r[i][j] + (loading if i == j else 0.0) for j in range(n)] for i in range(n)]  # @line L1
    z = solve(rl, a)  # @line L2
    return [v / dot(a, z) for v in z]  # @line L3


def capon_power(r, a):
    """The Capon spectrum value 1 / (a^H R^-1 a), the least output power under w^H a = 1."""
    return 1.0 / dot(a, solve(r, a)).real


def output_power(r, w):
    """w^H R w, a real number for Hermitian R."""
    rw = [sum(r[i][j] * w[j] for j in range(len(w))) for i in range(len(w))]
    return dot(w, rw).real


def outer_sum(vectors):
    """The sample covariance (1/K) sum_k x_k x_k^H of K snapshots."""
    n = len(vectors[0])
    r = [[0j] * n for _ in range(n)]
    for x in vectors:
        for i in range(n):
            xi = x[i]
            for j in range(n):
                r[i][j] += xi * x[j].conjugate()
    k = len(vectors)
    return [[v / k for v in row] for row in r]


def capon_pixel(snapshots, sub_len, delta):
    """The Capon value of one pixel from delayed channel snapshots.

    snapshots: a list of 2K + 1 delayed channel vectors (length M) at the
    sample times around the pixel; the middle one is the pixel sample.
    sub_len: the subarray length L, 1 <= L <= M. delta: the loading factor.
    """
    m = len(snapshots[0])
    n_sub = m - sub_len + 1
    subs = [x[l:l + sub_len] for x in snapshots for l in range(n_sub)]  # @line L4
    r = outer_sum(subs)  # @line L5
    trace = sum(r[i][i].real for i in range(sub_len))
    ones = [1.0] * sub_len
    w = capon_weights(r, ones, delta * trace / sub_len)  # @line L6
    centre = snapshots[len(snapshots) // 2]
    g = [sum(centre[l + i] for l in range(n_sub)) / n_sub for i in range(sub_len)]  # @line L7
    return dot(w, g)  # @line L8


# ---------------------------------------------------------------- a small imaging test bench

SOUND_SPEED = 1.54  # mm per microsecond (1540 m/s)


def element_positions(m_count, pitch):
    """x positions of a linear array, centered at x = 0."""
    return [(j - (m_count - 1) / 2) * pitch for j in range(m_count)]


def simulate_iq(elements, scatterers, f0, sigma_t, fs, t0, ns, c=SOUND_SPEED):
    """Complex baseband traces for a plane wave at normal incidence and point scatterers (x, z, amp)."""
    data = []
    for xj in elements:
        tr = [0j] * ns
        for (sx, sz, amp) in scatterers:
            tau = sz / c + math.hypot(sx - xj, sz) / c
            rot = amp * cmath.exp(-2j * math.pi * f0 * tau)
            lo = max(0, math.ceil((tau - 5 * sigma_t - t0) * fs))
            hi = min(ns - 1, math.floor((tau + 5 * sigma_t - t0) * fs))
            for q in range(lo, hi + 1):
                dt = t0 + q / fs - tau
                tr[q] += rot * math.exp(-dt * dt / (2 * sigma_t * sigma_t))
        data.append(tr)
    return data


def delayed_snapshots(data, elements, px, pz, t0, fs, f0, half_window, c=SOUND_SPEED):
    """Delayed analytic channel vectors at the pixel time plus or minus q / fs, q <= half_window."""
    out = []
    for q in range(-half_window, half_window + 1):
        x = []
        for xj, tr in zip(elements, data):
            t = pz / c + math.hypot(px - xj, pz) / c + q / fs
            u = (t - t0) * fs
            k = math.floor(u)
            if k < 0 or k + 1 >= len(tr):
                x.append(0j)
                continue
            phi = u - k
            x.append(((1 - phi) * tr[k] + phi * tr[k + 1]) * cmath.exp(2j * math.pi * f0 * t))
        out.append(x)
    return out
