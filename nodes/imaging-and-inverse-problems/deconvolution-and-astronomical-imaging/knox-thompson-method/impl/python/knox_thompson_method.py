# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knox-thompson-method/. The authors are listed in prov/SH6M7B.jsonl.
"""Knox-Thompson phase recovery from simulated speckle frames.

Images are n x n and periodic. A frequency is a signed pair u = (u1, u2) with
-n/2 <= u1, u2 < n/2; a spectrum stores it at index [u1 mod n][u2 mod n]. The
object is a dict {(a, b): flux} of points at signed pixel offsets, so its
spectrum is O(u) = sum flux * exp(-2 pi i (u1 a + u2 b) / n).

A frame is made by one random phase screen over a disk pupil: the pupil field
P = mask * exp(i phi), the PSF |DFT(P)|^2, and the transfer function
T = DFT(PSF) / T(0). The frame spectrum is I = O * T. With a pupil of
diameter d < n / 2, T is zero beyond about d cells, so nothing wraps.
"""

import cmath
import math
import random

from imgkit import dft2, fftshift, idft2

E1, E2 = (1, 0), (0, 1)


def signed(k, n):
    """The signed frequency of index k."""
    return k if k < n - n // 2 else k - n


def object_spectrum(points, n):
    """O(u) for a dict {(a, b): flux} of point sources."""
    out = [[0j] * n for _ in range(n)]
    for k1 in range(n):
        for k2 in range(n):
            out[k1][k2] = sum(f * cmath.exp(-2j * math.pi * (k1 * a + k2 * b) / n) for (a, b), f in points.items())
    return out


def screen_amplitude(n, sigma):
    """Amplitudes |f|^(-11/6) of a Kolmogorov screen, scaled so that the expected rms phase is sigma."""
    amp = [[0.0] * n for _ in range(n)]
    for k1 in range(n):
        for k2 in range(n):
            f2 = signed(k1, n) ** 2 + signed(k2, n) ** 2
            amp[k1][k2] = 0.0 if f2 == 0 else f2 ** (-11.0 / 12.0)
    scale = sigma / math.sqrt(sum(a * a for row in amp for a in row))
    return [[a * scale for a in row] for row in amp]


def phase_screen(rng, amp):
    """A random phase screen: the real part of filtered complex white noise."""
    n = len(amp)
    spec = [[a * complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)) for a in row] for row in amp]
    field = idft2(spec)
    return [[(v * n * n).real for v in row] for row in field]


def pupil_mask(n, d):
    """1 on the cells of a disk of diameter d at the center of the grid, 0 elsewhere."""
    c, r2 = n / 2.0 - 0.5, (d / 2.0) ** 2
    return [[1.0 if (i - c) ** 2 + (j - c) ** 2 <= r2 else 0.0 for j in range(n)] for i in range(n)]


def transfer_function(screen, mask):
    """The transfer function of one short exposure, with T(0) = 1."""
    field = dft2([[m * cmath.exp(1j * p) for m, p in zip(rm, rp)] for rm, rp in zip(mask, screen)])
    psf = [[abs(v) ** 2 for v in row] for row in field]
    t = dft2(psf)
    t0 = t[0][0].real
    return [[v / t0 for v in row] for row in t]


def simulate_frames(obj, n, d, sigma, draws, seed, antithetic=True):
    """Frame spectra I = O T for draws random screens.

    With antithetic = True each screen phi is also used as -phi, whose transfer
    function is conj(T). The pair keeps the symmetry phi -> -phi of the screen
    statistics exactly in the sample.
    """
    rng = random.Random(seed)
    amp = screen_amplitude(n, sigma)
    mask = pupil_mask(n, d)
    frames = []
    for _ in range(draws):
        t = transfer_function(phase_screen(rng, amp), mask)
        frames.append([[o * v for o, v in zip(ro, rt)] for ro, rt in zip(obj, t)])
        if antithetic:
            frames.append([[o * v.conjugate() for o, v in zip(ro, rt)] for ro, rt in zip(obj, t)])
    return frames


def cross_spectra(frames):
    """C_e(u) = mean of I(u) conj(I(u + e)) for e = e1 and e = e2."""
    n = len(frames[0])
    out = []
    for e1, e2 in (E1, E2):
        c = [[0j] * n for _ in range(n)]
        for f in frames:  # @line L1
            for k1 in range(n):
                for k2 in range(n):
                    c[k1][k2] += f[k1][k2] * f[(k1 + e1) % n][(k2 + e2) % n].conjugate()
        out.append([[v / len(frames) for v in row] for row in c])
    return out


def disk_order(n, radius):
    """The signed frequencies with |u| <= radius, sorted by |u1| + |u2|."""
    h = n // 2
    pts = [(a, b) for a in range(-h, n - h) for b in range(-h, n - h) if a * a + b * b <= radius * radius]
    return sorted(pts, key=lambda u: (abs(u[0]) + abs(u[1]), u))


def knox_thompson_phase(cross, n, radius):
    """Object phases phi(u) for |u| <= radius from the cross spectra (C_e1, C_e2)."""
    order = disk_order(n, radius)
    phase = {(0, 0): 0.0}  # @line L2
    for u in order[1:]:  # @line L3
        z = 0j  # @line L4
        steps = abs(u[0]) + abs(u[1])
        for c, (e1, e2) in zip(cross, (E1, E2)):  # @line L5
            for sgn in (1, -1):
                p = (u[0] - sgn * e1, u[1] - sgn * e2)
                if p not in phase or abs(p[0]) + abs(p[1]) != steps - 1:
                    continue
                if sgn == 1:  # u = p + e: arg C_e(p) = phi(p) - phi(u)
                    z += cmath.exp(1j * phase[p]) * c[p[0] % n][p[1] % n].conjugate()  # @line L6
                else:  # u = p - e: arg C_e(u) = phi(u) - phi(p)
                    z += cmath.exp(1j * phase[p]) * c[u[0] % n][u[1] % n]
        phase[u] = cmath.phase(z) if z != 0 else 0.0  # @line L7
    return phase  # @line L8


def power_spectrum(frames):
    """The mean of |I(u)|^2 over the frames (speckle interferometry)."""
    n = len(frames[0])
    return [[sum(abs(f[k1][k2]) ** 2 for f in frames) / len(frames) for k2 in range(n)] for k1 in range(n)]


def modulus_from_reference(obj_power, ref_power, phase):
    """|O(u)| = sqrt(<|I|^2> / <|T|^2>) on the frequencies of phase, from a point source reference."""
    n = len(obj_power)
    out = {}
    for u in phase:
        k1, k2 = u[0] % n, u[1] % n
        out[u] = math.sqrt(max(obj_power[k1][k2], 0.0) / ref_power[k1][k2]) if ref_power[k1][k2] > 0 else 0.0
    return out


def reconstruct(modulus, phase, n):
    """The real image with spectrum modulus * exp(i phase) on the given frequencies, center at n // 2."""
    spec = [[0j] * n for _ in range(n)]
    for u, ph in phase.items():
        spec[u[0] % n][u[1] % n] = modulus[u] * cmath.exp(1j * ph)  # @line L9
    img = idft2(spec)
    return fftshift([[v.real for v in row] for row in img])


def phase_error(phase, obj, n):
    """The largest |phi(u) - arg O(u)| over the recovered frequencies, wrapped to [0, pi]."""
    worst = 0.0
    for u, ph in phase.items():
        d = cmath.phase(cmath.exp(1j * (ph - cmath.phase(obj[u[0] % n][u[1] % n]))))
        worst = max(worst, abs(d))
    return worst
