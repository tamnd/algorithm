# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-multiply-and-sum/. The authors are listed in prov/SF6EBZ.jsonl.
"""Delay-multiply-and-sum (DMAS) beamforming (Matrone et al. 2015).

The input of the combiner is the vector s_1, ..., s_M of real RF channel
samples after the focusing delays of one pixel. DMAS returns

    y = sum over pairs i < j of sign(s_i s_j) sqrt(|s_i s_j|).

With the signed square roots r_i = sign(s_i) sqrt(|s_i|), each term is r_i r_j,
so y = ((sum r_i)^2 - sum r_i^2) / 2, which costs O(M) in place of O(M^2).

The image part uses a plane wave at normal incidence and a linear array on
z = 0, in millimetres, microseconds and megahertz (1540 m/s is 1.54 mm/us).
"""

import math

SOUND_SPEED = 1.54  # mm per microsecond


def signed_sqrt(v):
    """sign(v) sqrt(|v|), with the value 0 at 0."""
    return math.copysign(math.sqrt(abs(v)), v) if v != 0 else 0.0


def dmas(samples):
    """DMAS of one delayed channel vector in O(M), by the square of the sum."""
    r = [signed_sqrt(s) for s in samples]  # @line L1
    total = sum(r)  # @line L2
    energy = sum(abs(s) for s in samples)  # @line L3
    return (total * total - energy) / 2  # @line L4


def dmas_pairs(samples):
    """DMAS by the defining double sum over the pairs i < j, in O(M^2)."""
    m = len(samples)
    y = 0.0
    for i in range(m):
        for j in range(i + 1, m):
            p = samples[i] * samples[j]
            y += math.copysign(math.sqrt(abs(p)), p) if p != 0 else 0.0
    return y


def das(samples):
    """Delay-and-sum of the same delayed samples, for comparison."""
    return sum(samples)


def element_positions(m_count, pitch):
    """x positions of a linear array, centered at x = 0."""
    return [(j - (m_count - 1) / 2) * pitch for j in range(m_count)]


def simulate_rf(elements, scatterers, f0, sigma_t, fs, t0, ns, c=SOUND_SPEED):
    """Real RF traces for a plane wave at normal incidence and point scatterers (x, z, amp).

    The pulse is g(t) cos(2 pi f0 t) with a Gaussian envelope g of standard
    deviation sigma_t, delayed by z / c + |p - e_j| / c.
    """
    data = []
    for xj in elements:
        tr = [0.0] * ns
        for (sx, sz, amp) in scatterers:
            tau = sz / c + math.hypot(sx - xj, sz) / c
            lo = max(0, math.ceil((tau - 5 * sigma_t - t0) * fs))
            hi = min(ns - 1, math.floor((tau + 5 * sigma_t - t0) * fs))
            for q in range(lo, hi + 1):
                dt = t0 + q / fs - tau
                tr[q] += amp * math.exp(-dt * dt / (2 * sigma_t * sigma_t)) * math.cos(2 * math.pi * f0 * dt)
        data.append(tr)
    return data


def delayed_samples(data, elements, px, pz, t0, fs, c=SOUND_SPEED):
    """The RF sample of each channel at the two-way time of the pixel, by linear interpolation."""
    out = []
    for xj, tr in zip(elements, data):
        t = pz / c + math.hypot(px - xj, pz) / c
        u = (t - t0) * fs
        q = math.floor(u)
        if q < 0 or q + 1 >= len(tr):
            out.append(0.0)
            continue
        phi = u - q
        out.append((1 - phi) * tr[q] + phi * tr[q + 1])
    return out


def beamform(data, elements, xs, zs, t0, fs, combiner, c=SOUND_SPEED):
    """The RF image combiner(delayed samples) on the grid; rows follow zs."""
    return [[combiner(delayed_samples(data, elements, px, pz, t0, fs, c)) for px in xs] for pz in zs]
