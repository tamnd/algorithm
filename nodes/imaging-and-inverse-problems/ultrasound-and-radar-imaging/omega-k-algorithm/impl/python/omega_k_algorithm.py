# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/omega-k-algorithm/. The authors are listed in prov/R4DMS8.jsonl.
"""Omega-k (wavenumber domain) algorithm for stripmap SAR with zero squint.

Geometry: the radar moves along a straight line at the speed V and sends one
pulse at each slow time eta_p = (p - n_az / 2) / PRF, at the position
x_p = V eta_p. A point target at the along-track position x and the closest
range R0 has the range history R(eta) = sqrt(R0^2 + (x_p - x)^2). The radar
sees it only inside the beam: |x_p - x| / R <= beam.

Signals: complex baseband. The pulse is a linear FM chirp
p(t) = exp(i pi Kr (t - T/2)^2) for 0 <= t < T. The echo of a target of
amplitude a is a p(t - 2R/c) exp(-i 4 pi f0 R / c). The Fourier sign is
exp(-i 2 pi f t), the sign of the DFT. Range sample j is the two-way delay
t_start + j / fs, that is the slant range r_start + j c / (2 fs).

In the two-dimensional frequency domain, with K = 4 pi (f0 + fr) / c and
kx = 2 pi f_eta / V, a target has the phase -R0 sqrt(K^2 - kx^2) - kx x
(stationary phase). The Stolt mapping makes this phase linear in the new
range frequency, so one 2D inverse DFT focuses every range at once.
Data layout: data[p][j], row p a pulse, column j a range bin.
"""

import cmath
import math

from imgkit import dft, fftshift, idft

C = 3.0e8


class Stripmap:
    """The parameters of a stripmap acquisition (SI units)."""

    def __init__(self, f0=300e6, bandwidth=100e6, pulse_len=0.2e-6, fs=120e6,
                 v=100.0, prf=80.0, n_range=64, n_az=128, r_start=380.0, beam=0.125):
        self.f0 = f0
        self.bandwidth = bandwidth
        self.pulse_len = pulse_len
        self.fs = fs
        self.v = v
        self.prf = prf
        self.n_range = n_range
        self.n_az = n_az
        self.r_start = r_start
        self.beam = beam
        self.kr = bandwidth / pulse_len
        self.dr = C / (2.0 * fs)

    def slant_range(self, j):
        return self.r_start + j * self.dr

    def x_pulse(self, p):
        return self.v * (p - self.n_az // 2) / self.prf

    def doppler(self, k):
        """The Doppler frequency of azimuth DFT bin k, wrapped to [-PRF/2, PRF/2)."""
        kk = k if k < self.n_az // 2 else k - self.n_az
        return kk * self.prf / self.n_az

    def range_freq(self, q):
        """The baseband range frequency of range DFT bin q, wrapped to [-fs/2, fs/2)."""
        qq = q if q < self.n_range // 2 else q - self.n_range
        return qq * self.fs / self.n_range

    def chirp(self, t):
        if 0.0 <= t < self.pulse_len:
            return cmath.exp(1j * math.pi * self.kr * (t - self.pulse_len / 2) ** 2)
        return 0j


def simulate_raw(g, targets):
    """Raw echo data of point targets (x, R0, amplitude), exact hyperbolic range."""
    t_start = 2.0 * g.r_start / C
    data = []
    for p in range(g.n_az):
        xp = g.x_pulse(p)
        row = [0j] * g.n_range
        for (x, r0, amp) in targets:
            r = math.hypot(r0, xp - x)
            if abs(xp - x) > g.beam * r:
                continue
            tau = 2.0 * r / C
            ph = amp * cmath.exp(-4j * math.pi * g.f0 * r / C)
            for j in range(g.n_range):
                row[j] += ph * g.chirp(t_start + j / g.fs - tau)
        data.append(row)
    return data


def sinc_interp(seq, u, taps=8):
    """Value of a sampled band-limited sequence at the fractional index u (Hann-windowed sinc)."""
    half = taps // 2
    i0 = math.floor(u)
    acc = 0j
    for m in range(i0 - half + 1, i0 + half + 1):
        if 0 <= m < len(seq):
            x = u - m
            w = 1.0 if x == 0 else math.sin(math.pi * x) / (math.pi * x)
            acc += seq[m] * w * (0.5 + 0.5 * math.cos(math.pi * x / half))
    return acc


def omega_k(g, data, r_ref=None, stolt=True):
    """Focus raw stripmap data. Returns the complex image img[p][j].

    With stolt=False the Stolt interpolation is skipped, so only the
    reference range r_ref is focused exactly (the bulk compression alone).
    """
    if r_ref is None:
        r_ref = g.slant_range(g.n_range / 2)
    n, m = g.n_range, g.n_az
    t_start = 2.0 * g.r_start / C
    ref = [g.chirp(j / g.fs) for j in range(n)]
    pconj = [v.conjugate() for v in dft(ref)]
    rows = []
    for p in range(m):
        spec = dft(data[p])  # @line L1
        rows.append([spec[q] * pconj[q] * cmath.exp(-2j * math.pi * g.range_freq(q) * t_start)
                     for q in range(n)])  # @line L2
    cols = [dft([rows[p][q] for p in range(m)]) for q in range(n)]  # @line L1
    f_max = 2.0 * g.v * g.beam * g.f0 / C
    half_band = g.bandwidth / 2.0
    out = [[0j] * n for _ in range(m)]
    for k in range(m):
        fa = g.doppler(k)
        if abs(fa) > f_max:
            continue
        kx = 2.0 * math.pi * fa / g.v
        d3 = (1.0 - (C * fa / (2.0 * g.v * g.f0)) ** 2) ** 1.5
        gain = g.prf * math.sqrt(C * r_ref / (2.0 * g.v ** 2 * g.f0 * d3))
        line = []
        for q in range(n):
            kk = 4.0 * math.pi * (g.f0 + g.range_freq(q)) / C
            ky = math.sqrt(max(kk * kk - kx * kx, 0.0))
            line.append(cols[q][k] * gain * cmath.exp(1j * r_ref * ky))  # @line L3
        shifted = fftshift(line)  # increasing frequency, zero at index n // 2
        for q in range(n):
            fr2 = g.range_freq(q)
            if abs(fr2) > half_band:
                continue
            if stolt:
                fr = math.sqrt((g.f0 + fr2) ** 2 + (C * fa / (2.0 * g.v)) ** 2) - g.f0  # @line L4
            else:
                fr = fr2
            val = sinc_interp(shifted, fr * n / g.fs + n // 2)  # @line L4
            delay = 2.0 * (r_ref - g.r_start) / C
            out[k][q] = val * cmath.exp(-2j * math.pi * fr2 * delay)  # @line L5
    rows2 = [idft(out[k]) for k in range(m)]  # @line L6
    cols2 = [idft([rows2[k][j] for k in range(m)]) for j in range(n)]  # @line L6
    img = [[0j] * n for _ in range(m)]
    for j in range(n):
        fix = cmath.exp(4j * math.pi * g.f0 * (g.slant_range(j) - r_ref) / C)  # @line L7
        for p in range(m):
            img[p][j] = cols2[j][p] * fix
    return img


def target_pixel(g, x, r0):
    """The (fractional) image position (p, j) where a target at (x, R0) focuses."""
    return x * g.prf / g.v + g.n_az // 2, (r0 - g.r_start) / g.dr
