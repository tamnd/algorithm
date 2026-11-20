# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chirp-scaling-algorithm/. The authors are listed in prov/C270V5.jsonl.
"""Chirp scaling algorithm (CSA) for stripmap SAR with zero squint.

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

The algorithm uses only DFTs and multiplications by phase functions: no
interpolation. Data layout: data[p][j], row p a pulse, column j a range bin.
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


def migration_factor(g, f):
    """D(f) = sqrt(1 - (c f / (2 V f0))^2)."""
    return math.sqrt(1.0 - (C * f / (2.0 * g.v * g.f0)) ** 2)


def modified_fm_rate(g, f, r):
    """Km = Kr / (1 - Kr c r f^2 / (2 V^2 f0^3 D^3)), the range FM rate in the range-Doppler domain."""
    d = migration_factor(g, f)
    return g.kr / (1.0 - g.kr * C * r * f ** 2 / (2.0 * g.v ** 2 * g.f0 ** 3 * d ** 3))


def csa(g, data, r_ref=None, scaling=True):
    """Focus raw stripmap data. Returns the complex image img[p][j].

    With scaling=False the chirp scaling multiply is skipped, so only the
    bulk migration of r_ref is corrected (for the tests).
    """
    if r_ref is None:
        r_ref = g.slant_range(g.n_range / 2)
    t_start = 2.0 * g.r_start / C
    f_max = 2.0 * g.v * g.beam * g.f0 / C
    cols = [dft([data[p][j] for p in range(g.n_az)]) for j in range(g.n_range)]  # @line L1
    rd = [[cols[j][k] for j in range(g.n_range)] for k in range(g.n_az)]  # rd[k][j]
    gain_r = g.fs / math.sqrt(g.kr)
    for k in range(g.n_az):
        f = g.doppler(k)
        if abs(f) > f_max:
            rd[k] = [0j] * g.n_range
            continue
        d = migration_factor(g, f)
        km = modified_fm_rate(g, f, r_ref)
        a = 1.0 / d - 1.0  # @line L2
        tau_ref = 2.0 * r_ref / (C * d) + g.pulse_len / 2
        line = rd[k]
        if scaling:
            line = [v * cmath.exp(1j * math.pi * km * a * (t_start + j / g.fs - tau_ref) ** 2)
                    for j, v in enumerate(line)]  # @line L3
        spec = dft(line)  # @line L4
        shift = 2.0 * r_ref * a / C + g.pulse_len / 2
        for q in range(g.n_range):
            fr = g.range_freq(q)
            spec[q] *= gain_r * cmath.exp(1j * math.pi * d * fr ** 2 / km
                                          + 2j * math.pi * fr * shift)  # @line L5
        line = idft(spec)  # @line L6
        ka = 2.0 * g.v ** 2 * g.f0 * d ** 3 / (C * r_ref)
        for j in range(g.n_range):
            r0 = g.slant_range(j)
            resid = 4.0 * math.pi * km / C ** 2 * (1.0 - d) * (r0 - r_ref) ** 2 / d ** 2
            if not scaling:
                resid = 0.0
            line[j] *= (g.prf / math.sqrt(ka)) * cmath.exp(
                1j * (4.0 * math.pi * g.f0 * r0 * d / C - resid))  # @line L7
        rd[k] = line
    cols_img = [idft([rd[k][j] for k in range(g.n_az)]) for j in range(g.n_range)]  # @line L8
    return [[cols_img[j][p] for j in range(g.n_range)] for p in range(g.n_az)]


def target_pixel(g, x, r0):
    """The (fractional) image position (p, j) where a target at (x, R0) focuses."""
    return x * g.prf / g.v + g.n_az // 2, (r0 - g.r_start) / g.dr
