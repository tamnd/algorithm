# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/angular-spectrum-method/. The authors are listed in prov/BPG5QE.jsonl.

"""Angular spectrum propagation of a sampled scalar field.

Conventions:
- The field u is an n1 x n2 image, u[i][j] at y = i d and x = j d, with the
  sample spacing d. The grid is periodic with the periods n1 d and n2 d.
- Time dependence exp(-i omega t), so the plane wave exp(2 pi i (fx x + fy y
  + fz z)) with fz > 0 travels toward +z.
- The DFT is unnormalized forward with exp(-2 pi i j k / n), and the inverse
  has 1 / n (imgkit). DFT index k stands for the frequency k / (n d) for
  k < n / 2 and (k - n) / (n d) otherwise.
- Transfer function H(fx, fy) = exp(2 pi i z sqrt(1 / lambda^2 - fx^2 - fy^2))
  where the root is real and positive, and 0 elsewhere (evanescent waves are
  dropped).

Cost: two 2D DFTs and O(n1 n2) other work, so O(n^2 log n) for an n x n
grid with n a power of two.
"""

import cmath
import math

from imgkit import dft2, idft2


def signed_index(k, n):
    """The signed frequency index of DFT index k: k if 2 k < n, else k - n."""
    return k if 2 * k < n else k - n


def frequencies(n, d):
    """The spatial frequencies (cycles per unit length) of the n DFT indices."""
    return [signed_index(k, n) / (n * d) for k in range(n)]


def band_limit(n, d, wavelength, z):
    """The band limit of Matsushima and Shimobaba for an axis of n samples.

    With the frequency spacing du = 1 / (n d), the sampled transfer function
    has a phase step of at most pi between neighbors for |f| below
    1 / (wavelength sqrt((2 du z)^2 + 1)).
    """
    du = 1.0 / (n * d)
    return 1.0 / (wavelength * math.sqrt((2.0 * du * z) ** 2 + 1.0))


def transfer_function(n1, n2, d, wavelength, z, limit=False):
    """H on the DFT grid, in DFT order, with evanescent entries set to 0."""
    fys, fxs = frequencies(n1, d), frequencies(n2, d)
    inv2 = 1.0 / (wavelength * wavelength)
    ly = band_limit(n1, d, wavelength, abs(z)) if limit else math.inf
    lx = band_limit(n2, d, wavelength, abs(z)) if limit else math.inf
    h = [[0j] * n2 for _ in range(n1)]
    for k, fy in enumerate(fys):
        for l, fx in enumerate(fxs):
            w = inv2 - fx * fx - fy * fy
            if w > 0.0 and abs(fx) <= lx and abs(fy) <= ly:
                h[k][l] = cmath.exp(2j * math.pi * z * math.sqrt(w))
    return h


def angular_spectrum(u, d, wavelength, z, limit=False):
    """The field at distance z from the sampled field u (periodic model)."""
    n1, n2 = len(u), len(u[0])
    spec = dft2(u)  # @line L1
    fys, fxs = frequencies(n1, d), frequencies(n2, d)
    inv2 = 1.0 / (wavelength * wavelength)
    ly = band_limit(n1, d, wavelength, abs(z)) if limit else math.inf
    lx = band_limit(n2, d, wavelength, abs(z)) if limit else math.inf
    out = [[0j] * n2 for _ in range(n1)]
    for k in range(n1):  # @line L2
        for l in range(n2):
            fy, fx = fys[k], fxs[l]  # @line L3
            w = inv2 - fx * fx - fy * fy  # @line L4
            if w > 0.0 and abs(fx) <= lx and abs(fy) <= ly:  # @line L5
                out[k][l] = spec[k][l] * cmath.exp(2j * math.pi * z * math.sqrt(w))
            else:
                out[k][l] = 0j  # @line L6
    return idft2(out)  # @line L7


def angular_spectrum_padded(u, d, wavelength, z, limit=False):
    """Propagate u embedded in a grid twice as large (zeros around it), then crop.

    The padding keeps light that leaves the window from wrapping around to
    the other side, so the result approximates the aperiodic field.
    """
    n1, n2 = len(u), len(u[0])
    big = [[0j] * (2 * n2) for _ in range(2 * n1)]
    for i in range(n1):
        for j in range(n2):
            big[i + n1 // 2][j + n2 // 2] = u[i][j]
    res = angular_spectrum(big, d, wavelength, z, limit)
    return [row[n2 // 2:n2 // 2 + n2] for row in res[n1 // 2:n1 // 2 + n1]]


def fresnel_transfer(n1, n2, d, wavelength, z):
    """The paraxial (Fresnel) transfer function exp(2 pi i z / lambda) exp(-i pi lambda z f^2)."""
    fys, fxs = frequencies(n1, d), frequencies(n2, d)
    c = cmath.exp(2j * math.pi * z / wavelength)
    return [[c * cmath.exp(-1j * math.pi * wavelength * z * (fx * fx + fy * fy)) for fx in fxs] for fy in fys]
