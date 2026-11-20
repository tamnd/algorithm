# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transport-of-intensity-equation/. The authors are listed in prov/5EFCMW.jsonl.

"""Phase from a defocus series with the transport of intensity equation (TIE).

Conventions:
- Images are n1 x n2 lists of rows on a periodic grid with spacing d,
  pixel (i, j) at y = i d and x = j d. The DFT is unnormalized forward with
  exp(-2 pi i j k / n) (imgkit); index k stands for k if 2 k < n, else k - n.
- Time dependence exp(-i omega t), so the paraxial field is
  U = sqrt(I) exp(i phi) exp(i k z) and the TIE reads
  div(I grad phi) = -k dI/dz with k = 2 pi / wavelength.
- The phase is found up to an additive constant; the result has mean 0.

Method (Teague 1983): write I grad phi = grad psi. Then lap psi = -k dI/dz,
and lap phi = div(grad psi / I). Both Poisson equations are solved with the
FFT. The intensity derivative comes from a central difference of two images
at -dz and +dz.

Cost: a fixed number of 2D DFTs, O(n^2 log n) for n x n images with n a
power of two.
"""

import math

from imgkit import dft2, idft2


def _freqs(n, d):
    return [(k if 2 * k < n else k - n) / (n * d) for k in range(n)]


def inverse_laplacian(rhs, d):
    """The mean-zero periodic solution u of lap u = rhs - mean(rhs).

    In Fourier space, U(f) = -RHS(f) / (4 pi^2 |f|^2), and U(0) = 0.
    """
    n1, n2 = len(rhs), len(rhs[0])
    fy, fx = _freqs(n1, d), _freqs(n2, d)
    spec = dft2(rhs)
    for k in range(n1):
        for l in range(n2):
            q = 4.0 * math.pi * math.pi * (fx[l] ** 2 + fy[k] ** 2)
            spec[k][l] = 0j if k == 0 and l == 0 else -spec[k][l] / q
    return [[v.real for v in row] for row in idft2(spec)]


def gradient(u, d):
    """The spectral gradient (du/dx, du/dy) of a periodic real image."""
    n1, n2 = len(u), len(u[0])
    fy, fx = _freqs(n1, d), _freqs(n2, d)
    spec = dft2(u)
    gx = [[2j * math.pi * fx[l] * spec[k][l] for l in range(n2)] for k in range(n1)]
    gy = [[2j * math.pi * fy[k] * spec[k][l] for l in range(n2)] for k in range(n1)]
    if n2 % 2 == 0:  # the Nyquist column has no sign; drop it so the result is real
        for k in range(n1):
            gx[k][n2 // 2] = 0j
    if n1 % 2 == 0:
        gy[n1 // 2] = [0j] * n2
    return [[v.real for v in row] for row in idft2(gx)], [[v.real for v in row] for row in idft2(gy)]


def divergence(gx, gy, d):
    """The spectral divergence d gx/dx + d gy/dy."""
    ax, _ = gradient(gx, d)
    _, by = gradient(gy, d)
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(ax, by)]


def tie_phase(i_minus, i_focus, i_plus, dz, d, wavelength):
    """The phase in the focal plane from the intensities at -dz, 0 and +dz.

    i_focus must be positive everywhere.
    """
    k = 2.0 * math.pi / wavelength
    didz = [[(p - m) / (2.0 * dz) for p, m in zip(rp, rm)] for rp, rm in zip(i_plus, i_minus)]  # @line L1
    psi = inverse_laplacian([[-k * v for v in row] for row in didz], d)  # @line L2
    gx, gy = gradient(psi, d)  # @line L3
    gx = [[a / i for a, i in zip(ra, ri)] for ra, ri in zip(gx, i_focus)]  # @line L4
    gy = [[a / i for a, i in zip(ra, ri)] for ra, ri in zip(gy, i_focus)]
    return inverse_laplacian(divergence(gx, gy, d), d)  # @line L5


def tie_phase_uniform(i_minus, i_plus, intensity, dz, d, wavelength):
    """The special case of a uniform intensity I0: lap phi = -(k / I0) dI/dz."""
    k = 2.0 * math.pi / wavelength
    rhs = [[-k / intensity * (p - m) / (2.0 * dz) for p, m in zip(rp, rm)] for rp, rm in zip(i_plus, i_minus)]
    return inverse_laplacian(rhs, d)
