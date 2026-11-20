# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stolt-migration/. The authors are listed in prov/HTV0W8.jsonl.
"""Stolt (f-k) migration of a zero-offset section in constant velocity.

Conventions (the imaging and inverse problems pages):
- data[k][j] is the zero-offset sample at the two-way time t = k * dt and the
  surface position x = j * dx. image[i][j] is the image at depth z = i * dz.
- U(omega) = sum u(t) exp(-i omega t), and the x transform uses exp(-i kx x).
  Index k of a DFT of length n stands for k for k < n / 2 and k - n otherwise.
- Exploding reflector model: the data is a one-way field in the velocity
  v' = v / 2. Downward continuation multiplies by exp(+i kz z).
- Stolt mapping: the image transform at (kz, kx) is
      M(kz, kx) = (dt / dz) * v' |kz| / sqrt(kx^2 + kz^2) * D(omega, kx),
  with omega = sgn(kz) v' sqrt(kx^2 + kz^2), and D is read from the data
  transform by linear interpolation along omega. The factor dt / dz turns the
  sums of the DFT into the integrals of the continuous formula.

Cost: one 2D FFT of the data, O(nz * nx) interpolations, and one inverse 2D
FFT of the image: O(nt nx log(nt nx) + nz nx log(nz nx)) with radix-2 FFTs.
"""

import math

from imgkit import dft2, idft2


def signed_index(k, n):
    """The signed frequency index of DFT index k: k for k < n / 2, else k - n."""
    return k if 2 * k < n else k - n


def stolt_map(kz, kx, vhalf):
    """omega = sgn(kz) v' sqrt(kx^2 + kz^2) and the Jacobian v' |kz| / sqrt(kx^2 + kz^2)."""
    r = math.hypot(kx, kz)
    if r == 0.0:
        return 0.0, 0.0
    return math.copysign(vhalf * r, kz), vhalf * abs(kz) / r


def stolt_migration(data, dt, dx, dz, nz, vel, pad=4):
    """Migrate a zero-offset section in the constant velocity vel (m/s).

    data: nt x nx real samples. Returns the nz x nx real image. Precondition:
    dt, dx, dz, vel > 0. The time axis is padded with zeros to pad * nt
    samples, so that linear interpolation along omega is accurate. Frequencies
    outside the band of the data (|omega| near the Nyquist frequency) are set
    to zero.
    """
    nx = len(data[0])
    padded = [list(row) for row in data] + [[0.0] * nx for _ in range((pad - 1) * len(data))]  # @line L1
    nt = len(padded)
    vhalf = vel / 2.0
    d = dft2(padded)  # @line L2
    dw = 2.0 * math.pi / (nt * dt)
    dkx = 2.0 * math.pi / (nx * dx)
    dkz = 2.0 * math.pi / (nz * dz)
    m = [[0j] * nx for _ in range(nz)]
    for i in range(nz):  # @line L3
        kz = signed_index(i, nz) * dkz
        for j in range(nx):
            kx = signed_index(j, nx) * dkx
            omega, jac = stolt_map(kz, kx, vhalf)  # @line L4
            u = omega / dw
            k0 = math.floor(u)
            frac = u - k0
            if jac == 0.0 or not (-nt // 2 < k0 and k0 + 1 < (nt + 1) // 2):  # @line L5
                continue  # the zero wavenumber or outside the band: M stays 0
            val = (1.0 - frac) * d[k0 % nt][j] + frac * d[(k0 + 1) % nt][j]  # @line L6
            m[i][j] = (dt / dz) * jac * val  # @line L7
    img = idft2(m)  # @line L8
    return [[v.real for v in row] for row in img]  # @line L9


def ricker(t, f0):
    """The Ricker wavelet (1 - 2 a) exp(-a) with a = (pi f0 t)^2, peak frequency f0."""
    a = (math.pi * f0 * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def diffractor_section(nt, nx, dt, dx, x0, z0, vel, f0):
    """Zero-offset data of one point diffractor at (x0, z0) in constant velocity.

    The event is a Ricker wavelet along t(x) = (2 / vel) sqrt(z0^2 + (x - x0)^2).
    """
    out = [[0.0] * nx for _ in range(nt)]
    for j in range(nx):
        t0 = 2.0 * math.hypot(z0, j * dx - x0) / vel
        for k in range(nt):
            out[k][j] = ricker(k * dt - t0, f0)
    return out
