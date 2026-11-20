# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-doppler-algorithm/. The authors are listed in prov/76HEMZ.jsonl.
"""Range-Doppler algorithm (RDA) for stripmap SAR with zero squint.

Geometry: the radar moves along a straight line at the speed V and sends one
pulse at each slow time eta_p = (p - n_az / 2) / PRF, at the position
x_p = V eta_p. A point target at the along-track position x and the closest
range R0 has the range history R(eta) = sqrt(R0^2 + (x_p - x)^2). The radar
sees it only inside the beam: |x_p - x| / R <= beam (the sine of the half
beam angle).

Signals: complex baseband. The pulse is a linear FM chirp
p(t) = exp(i pi Kr (t - T/2)^2) for 0 <= t < T. The echo of a target of
amplitude a is a p(t - 2R/c) exp(-i 4 pi f0 R / c). The Fourier sign is
exp(-i 2 pi f t), the sign of the DFT. Range sample j of a pulse is the
two-way delay t_start + j / fs, that is the slant range r_start + j c / (2 fs).

Data layout: data[p][j], row p is a pulse (slow time), column j a range bin.
"""

import cmath
import math

from imgkit import dft, idft

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
        """The slant range of range bin j (it may be fractional)."""
        return self.r_start + j * self.dr

    def x_pulse(self, p):
        """The along-track position of pulse p."""
        return self.v * (p - self.n_az // 2) / self.prf

    def doppler(self, k):
        """The Doppler frequency of DFT bin k: k PRF / n_az, wrapped to [-PRF/2, PRF/2)."""
        kk = k if k < self.n_az // 2 else k - self.n_az
        return kk * self.prf / self.n_az

    def chirp(self, t):
        """The baseband pulse p(t)."""
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


def range_compress(g, data):
    """Matched filter in range: multiply each pulse spectrum by conj(P) (circular)."""
    ref = [g.chirp(j / g.fs) for j in range(g.n_range)]
    h = [v.conjugate() for v in dft(ref)]
    return [idft([a * b for a, b in zip(dft(row), h)]) for row in data]


def sinc_interp(row, u, taps=8):
    """Value of a sampled band-limited signal at the fractional index u (Hann-windowed sinc)."""
    half = taps // 2
    i0 = math.floor(u)
    acc = 0j
    for m in range(i0 - half + 1, i0 + half + 1):
        if 0 <= m < len(row):
            x = u - m
            w = 1.0 if x == 0 else math.sin(math.pi * x) / (math.pi * x)
            acc += row[m] * w * (0.5 + 0.5 * math.cos(math.pi * x / half))
    return acc


def migration_factor(g, f):
    """D(f) = sqrt(1 - (c f / (2 V f0))^2), the cosine of the squint angle of Doppler f."""
    return math.sqrt(1.0 - (C * f / (2.0 * g.v * g.f0)) ** 2)


def rda(g, data, rcmc=True):
    """Focus raw stripmap data. Returns the complex image img[p][j]."""
    rc = range_compress(g, data)  # @line L1
    cols = [dft([rc[p][j] for p in range(g.n_az)]) for j in range(g.n_range)]  # @line L2
    f_max = 2.0 * g.v * g.beam * g.f0 / C  # the Doppler band of the beam
    out = [[0j] * g.n_az for _ in range(g.n_range)]
    for k in range(g.n_az):
        f = g.doppler(k)  # @line L3
        if abs(f) > f_max:
            continue
        d = migration_factor(g, f)  # @line L4
        line = [cols[j][k] for j in range(g.n_range)]
        for j in range(g.n_range):
            r0 = g.slant_range(j)
            u = (r0 / d - g.r_start) / g.dr if rcmc else j  # @line L5
            val = sinc_interp(line, u)  # @line L6
            ka = 2.0 * g.v ** 2 * g.f0 * d ** 3 / (C * r0)  # azimuth FM rate at f
            h = (g.prf / math.sqrt(ka)) * cmath.exp(4j * math.pi * g.f0 * r0 * d / C)  # @line L7
            out[j][k] = val * h  # @line L8
    cols_img = [idft(col) for col in out]  # @line L9
    return [[cols_img[j][p] for j in range(g.n_range)] for p in range(g.n_az)]


def target_pixel(g, x, r0):
    """The (fractional) image position (p, j) where a target at (x, R0) focuses."""
    return x * g.prf / g.v + g.n_az // 2, (r0 - g.r_start) / g.dr
