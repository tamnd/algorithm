# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-step-fourier-migration/. The authors are listed in prov/C572NA.jsonl.
"""Split-step Fourier migration of a zero-offset section for a velocity v(x, z).

Conventions (the imaging and inverse problems pages):
- data[k][j] is the zero-offset sample at the two-way time t = k * dt and the
  surface position x = j * dx. vel[i][j] is the velocity (m/s) between the
  depths i dz and (i + 1) dz at x = j dx. image[i][j] is the image at depth i dz.
- U(omega) = sum u(t) exp(-i omega t); the x transform uses exp(-i kx x).
- Exploding reflector model: the slowness used is s = 2 / v (the slowness of
  the half velocity v / 2). Downward continuation by dz multiplies by
  exp(+i kz dz), kz = sgn(omega) sqrt(omega^2 s0^2 - kx^2).
- One step: a phase shift with the reference slowness s0 (the mean of s over
  x in the layer) in the (omega, kx) domain, then the correction
  exp(i omega (s(x) - s0) dz) in the (omega, x) domain.
- Only the frequencies 0 < omega < the Nyquist frequency are continued. The
  data are real, so the image is (2 / nt) Re sum over these frequencies.

Cost per frequency and depth step: two FFTs of length nx and O(nx) phase
factors, so O(nz * nt * nx log nx) in total with radix-2 FFTs.
"""

import cmath
import math

from imgkit import dft, idft


def kx_values(nx, dx):
    """The angular wavenumbers of the DFT indices 0 .. nx - 1."""
    return [2.0 * math.pi * (j if 2 * j < nx else j - nx) / (nx * dx) for j in range(nx)]


def split_step_fourier_migration(data, dt, dx, dz, vel):
    """Migrate a zero-offset section with the split-step Fourier method.

    data: nt x nx real samples; vel: nz x nx velocities. Returns the nz x nx
    image. Precondition: dt, dx, dz > 0 and every velocity > 0.
    """
    nt, nx = len(data), len(data[0])
    nz = len(vel)
    kxs = kx_values(nx, dx)
    spectra = [dft([data[k][j] for k in range(nt)]) for j in range(nx)]  # @line L1
    image = [[0.0] * nx for _ in range(nz)]
    for k in range(1, (nt + 1) // 2):  # @line L2
        omega = 2.0 * math.pi * k / (nt * dt)
        p = [spectra[j][k] for j in range(nx)]
        for i in range(nz):  # @line L3
            for j in range(nx):
                image[i][j] += 2.0 * p[j].real / nt  # @line L4
            s = [2.0 / v for v in vel[i]]
            s0 = sum(s) / nx  # @line L5
            q = dft(p)  # @line L6
            for j in range(nx):
                arg = (omega * s0) ** 2 - kxs[j] ** 2
                q[j] = q[j] * cmath.exp(1j * math.sqrt(arg) * dz) if arg > 0.0 else 0j  # @line L7
            p = idft(q)  # @line L8
            for j in range(nx):
                p[j] *= cmath.exp(1j * omega * (s[j] - s0) * dz)  # @line L9
    return image  # @line L10


def phase_error(omega, s, s0, kx, dz):
    """The phase error of one split step for a plane wave in a medium of slowness s.

    The exact phase is dz sqrt(omega^2 s^2 - kx^2); the split step gives
    dz (sqrt(omega^2 s0^2 - kx^2) + omega (s - s0)). Both roots must be real.
    """
    exact = math.sqrt((omega * s) ** 2 - kx * kx)
    approx = math.sqrt((omega * s0) ** 2 - kx * kx) + omega * (s - s0)
    return dz * (approx - exact)
