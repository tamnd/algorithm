# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-shift-migration/. The authors are listed in prov/PNBG5B.jsonl.
"""Phase-shift (Gazdag) migration of a zero-offset section for a velocity v(z).

Conventions (the imaging and inverse problems pages):
- data[k][j] is the zero-offset sample at the two-way time t = k * dt and the
  surface position x = j * dx. image[i][j] is the image at depth z = i * dz.
- The time transform is U(omega) = sum u(t) exp(-i omega t), the same sign as
  the DFT, and the x transform uses exp(-i kx x). Index k of a DFT of length n
  stands for the frequency k for k < n / 2 and k - n otherwise.
- Exploding reflector model: the zero-offset data is a one-way upgoing field
  in a medium with half the velocity, v / 2.
- With this sign, downward continuation by dz multiplies the transform by
  exp(+i kz dz) with kz = sgn(omega) sqrt(omega^2 / v'^2 - kx^2), v' = v / 2.
  Evanescent components (|kx| > |omega| / v') are set to zero.

Cost: two 2D FFTs of the data, then O(nz * nt * nx) for the phase shifts,
plus one FFT of length nx per depth step.
"""

import cmath
import math

from imgkit import dft2, idft


def signed_freq(k, n, d):
    """The angular frequency 2 pi f of DFT index k for n samples with spacing d."""
    f = k if 2 * k < n else k - n
    return 2.0 * math.pi * f / (n * d)


def vertical_wavenumber(omega, kx, vel):
    """kz = sgn(omega) sqrt(omega^2 / vel^2 - kx^2), or None for an evanescent pair."""
    q = (omega / vel) ** 2 - kx * kx
    if q < 0.0 or omega == 0.0:
        return None
    return math.copysign(math.sqrt(q), omega)


def phase_shift_migration(data, dt, dx, dz, vz):
    """Migrate a zero-offset section with the phase-shift method.

    data: nt x nx real samples. vz: a list of nz velocities (m/s); vz[i] is the
    velocity between the depths i dz and (i + 1) dz. Returns the nz x nx image,
    whose row i is the field at time 0 after continuation to depth i dz.
    Precondition: dt, dx, dz > 0 and every velocity > 0.
    """
    nt, nx = len(data), len(data[0])
    nz = len(vz)
    p = dft2(data)  # @line L1
    omegas = [signed_freq(k, nt, dt) for k in range(nt)]
    kxs = [signed_freq(j, nx, dx) for j in range(nx)]
    image = []
    for i in range(nz):  # @line L2
        row_k = [sum(p[k][j] for k in range(nt)) / nt for j in range(nx)]  # @line L3
        image.append([v.real for v in idft(row_k)])  # @line L4
        vhalf = vz[i] / 2.0  # @line L5
        for k in range(nt):  # @line L6
            for j in range(nx):
                kz = vertical_wavenumber(omegas[k], kxs[j], vhalf)  # @line L7
                if kz is None:
                    p[k][j] = 0j  # @line L8
                else:
                    p[k][j] *= cmath.exp(1j * kz * dz)  # @line L9
    return image  # @line L10


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
