# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-fourier-reconstruction/. The authors are listed in prov/1BAE5C.jsonl.
"""Direct Fourier reconstruction for parallel-beam data.

Conventions:
- The sinogram is a list of a projections, one per angle theta_k = k pi / a,
  each a list of d detector values. Bin j has its center at
  s_j = (j - (d - 1) / 2) tau, with the detector spacing tau.
- The Fourier transform uses ordinary frequency:
  F f(xi) = integral f(x) exp(-2 pi i x . xi) dx. By the Fourier slice
  theorem, the 1D transform of the projection at angle theta is
  F f(sigma (cos theta, sin theta)).
- The output is an n x n image on [-1, 1]^2, n even. Pixel (i, j) has its
  center at x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n, so y goes up.
"""

import cmath
import math

from imgkit import dft, idft2


def _pow2_at_least(m):
    length = 1
    while length < m:
        length *= 2
    return length


def polar_spectra(sino, tau, over=4):
    """The 1D transforms of the projections on the radial grid sigma_l = l / (L tau).

    Returns (spectra, L). spectra[k][l] approximates F f(sigma_l omega(theta_k)),
    with l < L / 2 for frequency l and l >= L / 2 for frequency l - L.
    """
    a, d = len(sino), len(sino[0])
    length = _pow2_at_least(over * d)
    c0 = (d - 1) / 2.0
    spectra = []
    for k in range(a):  # @line L2
        pf = dft(list(sino[k]) + [0.0] * (length - d))
        row = []
        for l in range(length):
            sigma = (l if l < length // 2 else l - length) / (length * tau)
            row.append(tau * pf[l] * cmath.exp(2j * math.pi * c0 * tau * sigma))  # @line L3
        spectra.append(row)
    return spectra, length


def _radial(row, length, r):
    """Linear interpolation of a spectrum row at the signed fractional index r, 0 off the grid."""
    r0 = math.floor(r)
    w = r - r0
    val = 0j
    for idx, wt in ((r0, 1.0 - w), (r0 + 1, w)):
        if wt != 0.0 and -length // 2 <= idx < length // 2:
            val += wt * row[idx % length]
    return val


def polar_value(spectra, length, tau, xi_x, xi_y, interp="linear"):
    """The spectrum at the Cartesian frequency (xi_x, xi_y), read from the polar grid."""
    a = len(spectra)
    rho = math.hypot(xi_x, xi_y)
    if rho > 1.0 / (2.0 * tau):
        return 0j
    phi = math.atan2(xi_y, xi_x)
    theta, sigma = (phi, rho) if phi >= 0.0 else (phi + math.pi, -rho)  # @line L5
    if theta >= math.pi:
        theta, sigma = 0.0, -sigma
    t = theta * a / math.pi
    k0 = math.floor(t)
    wk = t - k0
    if interp == "nearest":
        k = int(round(t))
        sgn = 1.0
        if k == a:
            k, sgn = 0, -1.0
        r = round(sgn * sigma * length * tau)
        return spectra[k][r % length] if -length // 2 <= r < length // 2 else 0j
    val = 0j
    for k, wt in ((k0, 1.0 - wk), (k0 + 1, wk)):
        if wt == 0.0:
            continue
        sgn = 1.0
        if k == a:  # angle pi is angle 0 with the radius negated
            k, sgn = 0, -1.0
        val += wt * _radial(spectra[k], length, sgn * sigma * length * tau)  # @line L6
    return val


def grid_spectrum(spectra, length, tau, n, pad=2, interp="linear"):
    """The N x N array G (N = pad n) of the Cartesian spectrum, with the pixel-center phase and dxi^2.

    G[v mod N][u mod N] = F f(u dxi, v dxi) exp(pi i (u + v) / N) dxi^2 for
    u, v = -N/2 .. N/2 - 1, with dxi = 1 / (N h) and the pixel size h = 2 / n.
    """
    big = pad * n
    dxi = n / (2.0 * big)
    g = [[0j] * big for _ in range(big)]
    for v in range(-big // 2, big // 2):  # @line L4
        for u in range(-big // 2, big // 2):
            val = polar_value(spectra, length, tau, u * dxi, v * dxi, interp)
            g[v % big][u % big] = val * cmath.exp(1j * math.pi * (u + v) / big) * dxi * dxi  # @line L7
    return g


def spectrum_to_image(g, n):
    """f at the pixel centers from G: f = N^2 IDFT2(G), read at m_x = j - n/2, m_y = n/2 - 1 - i."""
    big = len(g)
    h = idft2(g)  # @line L8
    scale = big * big
    return [[scale * h[(n // 2 - 1 - i) % big][(j - n // 2) % big].real for j in range(n)] for i in range(n)]  # @line L9


def direct_fourier_reconstruction(sino, tau, n, pad=2, over=4, interp="linear"):
    """Reconstruct an n x n image (n even) from a parallel-beam sinogram on [0, pi)."""
    if n % 2:
        raise ValueError("n must be even")
    spectra, length = polar_spectra(sino, tau, over)  # @line L1
    g = grid_spectrum(spectra, length, tau, n, pad, interp)
    return spectrum_to_image(g, n)
