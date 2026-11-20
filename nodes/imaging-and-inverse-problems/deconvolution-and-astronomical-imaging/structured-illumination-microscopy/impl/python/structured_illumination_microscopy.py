# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-illumination-microscopy/. The authors are listed in prov/BKPK9D.jsonl.
"""Linear structured illumination microscopy (SIM) reconstruction in 2D.

Model, periodic on n1 x n2 pixels: the sample x is lit by the stripes

    P(r, c) = 1 + m cos(2 pi (u r / n1 + v c / n2) + phi)

with an integer frequency k0 = (u, v), a modulation depth m and a phase phi.
The camera records the periodic convolution of P x with the PSF whose DFT is
the OTF H (real and symmetric, so the PSF is real). With the DFT of imgkit,
X(k) = sum x exp(-2 pi i k . r / n), one frame is

    D(k) = H(k) [X(k) + (m/2) e^{i phi} X(k - k0) + (m/2) e^{-i phi} X(k + k0)].

Three phases give three linear equations for the three bands H X(k),
H X(k - k0) and H X(k + k0) at each k. All frequency indices are taken
modulo the image size, so k0 plus the OTF cutoff must stay below n / 2.
"""

import cmath
import math

from imgkit import dft2, idft2, new_image


def signed(k, n):
    """The signed frequency of DFT index k: k for k < n / 2, k - n otherwise."""
    return k if k < n - k else k - n


def otf_incoherent(n1, n2, kc):
    """The OTF of an aberration-free circular pupil with the cutoff kc (DFT index units).

    H(k) = (2 / pi) (acos rho - rho sqrt(1 - rho^2)) for rho = |k| / kc < 1, else 0.
    """
    h = new_image(n1, n2)
    for a in range(n1):
        for b in range(n2):
            rho = math.hypot(signed(a, n1), signed(b, n2)) / kc
            if rho < 1:
                h[a][b] = (2 / math.pi) * (math.acos(rho) - rho * math.sqrt(1 - rho * rho))
    return h


def psf_of_otf(h):
    """The real PSF, centered at index (0, 0), whose DFT is the real symmetric OTF h."""
    return [[z.real for z in row] for row in idft2(h)]


def pattern(n1, n2, k0, phi, m):
    """The illumination 1 + m cos(2 pi (u r / n1 + v c / n2) + phi)."""
    u, v = k0
    return [[1 + m * math.cos(2 * math.pi * (u * r / n1 + v * c / n2) + phi)
             for c in range(n2)] for r in range(n1)]


def blur(img, h):
    """Periodic convolution of img with the PSF of the OTF h, by the DFT."""
    f = dft2(img)
    g = [[h[a][b] * f[a][b] for b in range(len(f[0]))] for a in range(len(f))]
    return [[z.real for z in row] for row in idft2(g)]


def sim_frames(x, h, k0, phases, m):
    """The raw frames of one stripe direction: blur(P_j x) for each phase phi_j."""
    n1, n2 = len(x), len(x[0])
    frames = []
    for phi in phases:
        p = pattern(n1, n2, k0, phi, m)
        lit = [[p[r][c] * x[r][c] for c in range(n2)] for r in range(n1)]
        frames.append(blur(lit, h))
    return frames


def mixing_matrix(phases, m):
    """Row j is (1, (m/2) e^{i phi_j}, (m/2) e^{-i phi_j})."""
    return [[1, (m / 2) * cmath.exp(1j * phi), (m / 2) * cmath.exp(-1j * phi)]
            for phi in phases]


def _cofactor(a, i, j):
    r = [t for t in range(3) if t != i]
    c = [t for t in range(3) if t != j]
    minor = a[r[0]][c[0]] * a[r[1]][c[1]] - a[r[0]][c[1]] * a[r[1]][c[0]]
    return minor if (i + j) % 2 == 0 else -minor


def inv3(a, tol=1e-12):
    """The inverse of a 3 x 3 complex matrix by the adjugate.

    Raises ValueError when |det| <= tol * max|a_ij|^3 (equal phases, or m = 0).
    """
    det = sum(a[0][j] * _cofactor(a, 0, j) for j in range(3))
    scale = max(abs(z) for row in a for z in row)
    if abs(det) <= tol * scale ** 3:
        raise ValueError("the phases do not separate the three bands")
    return [[_cofactor(a, j, i) / det for j in range(3)] for i in range(3)]


def separate_bands(frames, phases, m):
    """The DFTs of the bands (H X(k), H X(k - k0), H X(k + k0)) from three frames."""
    if len(frames) != 3 or len(phases) != 3:
        raise ValueError("linear SIM needs three phases per direction")
    minv = inv3(mixing_matrix(phases, m))
    f = [dft2(d) for d in frames]
    n1, n2 = len(f[0]), len(f[0][0])
    bands = []
    for b in range(3):
        s = [[sum(minv[b][j] * f[j][r][c] for j in range(3)) for c in range(n2)]
             for r in range(n1)]
        bands.append(s)
    return bands


def shifted(img, k0, sign):
    """T(k) = img(k + sign k0), with the indices modulo the image size."""
    n1, n2 = len(img), len(img[0])
    u, v = k0
    return [[img[(r + sign * u) % n1][(c + sign * v) % n2] for c in range(n2)]
            for r in range(n1)]


def sim_reconstruct(frames_by_dir, k0s, phases, m, h, w=0.0):
    """Linear SIM reconstruction with a generalized Wiener filter.

    frames_by_dir[d] holds the three frames of direction d, lit with the
    frequency k0s[d] and the given phases. Returns the real image whose DFT is
    sum_b conj(H_b) T_b / (sum_b |H_b|^2 + w), set to 0 where the
    denominator is 0. With w = 0 and noise-free frames this is x with every
    frequency outside the extended support removed.
    """
    n1, n2 = len(h), len(h[0])
    num = [[0j] * n2 for _ in range(n1)]  # @line L1
    den = [[float(w)] * n2 for _ in range(n1)]  # @line L1
    for frames, k0 in zip(frames_by_dir, k0s):  # @line L2
        s0, sp, sm = separate_bands(frames, phases, m)  # @line L3
        tp, hp = shifted(sp, k0, 1), shifted(h, k0, 1)  # @line L4
        tm, hm = shifted(sm, k0, -1), shifted(h, k0, -1)  # @line L4
        for r in range(n1):  # @line L5
            for c in range(n2):  # @line L5
                for t, hb in ((s0, h), (tp, hp), (tm, hm)):  # @line L5
                    num[r][c] += hb[r][c] * t[r][c]  # @line L5
                    den[r][c] += hb[r][c] * hb[r][c]  # @line L5
    est = [[num[r][c] / den[r][c] if den[r][c] > 0 else 0j for c in range(n2)]  # @line L6
           for r in range(n1)]  # @line L6
    return [[z.real for z in row] for row in idft2(est)]  # @line L7


def extended_support(h, k0s):
    """The mask of the frequencies k with H(k) != 0, H(k + k0) != 0 or H(k - k0) != 0."""
    n1, n2 = len(h), len(h[0])
    mask = [[h[r][c] != 0 for c in range(n2)] for r in range(n1)]
    for k0 in k0s:
        for sign in (1, -1):
            hs = shifted(h, k0, sign)
            for r in range(n1):
                for c in range(n2):
                    mask[r][c] = mask[r][c] or hs[r][c] != 0
    return mask


def widefield(frames):
    """The mean of the frames; for three equally spaced phases it is blur(x)."""
    k = len(frames)
    n1, n2 = len(frames[0]), len(frames[0][0])
    return [[sum(f[r][c] for f in frames) / k for c in range(n2)] for r in range(n1)]


def wiener_deconvolve(img, h, w):
    """The Wiener estimate conj(H) D / (|H|^2 + w), set to 0 where the denominator is 0."""
    f = dft2(img)
    n1, n2 = len(f), len(f[0])
    g = new_image(n1, n2)
    for r in range(n1):
        for c in range(n2):
            d = h[r][c] * h[r][c] + w
            g[r][c] = h[r][c] * f[r][c] / d if d > 0 else 0j
    return [[z.real for z in row] for row in idft2(g)]
