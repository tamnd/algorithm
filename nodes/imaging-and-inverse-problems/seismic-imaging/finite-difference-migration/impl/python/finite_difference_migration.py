# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-difference-migration/. The authors are listed in prov/BK5R80.jsonl.
"""Finite-difference (Claerbout) migration of a zero-offset section, 15 degree equation.

Conventions (the imaging and inverse problems pages):
- data[k][j] is the zero-offset sample at the two-way time t = k * dt and the
  surface position x = j * dx. vel[i][j] is the velocity (m/s) between the
  depths i dz and (i + 1) dz at x = j dx. image[i][j] is the image at depth i dz.
- U(omega) = sum u(t) exp(-i omega t). Exploding reflector model: the field
  travels with v' = v / 2. Downward continuation by dz multiplies a plane wave
  by exp(+i kz dz), kz = (omega / v') sqrt(1 - (v' kx / omega)^2).
- The 15 degree equation replaces the square root by 1 - (v' kx / omega)^2 / 2:
      dP/dz = i (omega / v') P + i (v' / (2 omega)) d2P/dx2.
  Each depth step applies the thin lens exp(i omega dz / v') and then one
  Crank-Nicolson step of the second term:
      (I - i (b / 2) T) P_new = (I + i (b / 2) T) P,  b = v' dz / (2 omega dx^2),
  with T = tridiag(1, -2, 1) and P = 0 outside the grid (Dirichlet ends).
- Only 0 < omega < the Nyquist frequency are continued; the image is
  (2 / nt) Re of the sum over these frequencies.

Cost: O(nt log nt) per trace for the time FFT, then O(nx) per frequency and
depth step (one tridiagonal solve), so O(nz * nt * nx) in total.
"""

import cmath
import math

from imgkit import dft


def thomas_solve(lower, diag, upper, rhs):
    """Solve a tridiagonal system with the Thomas algorithm (no pivoting).

    lower[j] multiplies x[j - 1] in row j (lower[0] is unused), upper[j]
    multiplies x[j + 1] (upper[-1] is unused). Works for complex entries. It is
    stable for strictly diagonally dominant matrices, which is the case here.
    """
    n = len(diag)
    c = [0j] * n
    d = [0j] * n
    c[0] = upper[0] / diag[0]
    d[0] = rhs[0] / diag[0]
    for j in range(1, n):
        m = diag[j] - lower[j] * c[j - 1]
        c[j] = upper[j] / m if j < n - 1 else 0j
        d[j] = (rhs[j] - lower[j] * d[j - 1]) / m
    x = [0j] * n
    x[n - 1] = d[n - 1]
    for j in range(n - 2, -1, -1):
        x[j] = d[j] - c[j] * x[j + 1]
    return x


def apply_t(p):
    """(T p)_j = p_{j-1} - 2 p_j + p_{j+1}, with p = 0 outside the grid."""
    n = len(p)
    return [(p[j - 1] if j > 0 else 0j) - 2.0 * p[j] + (p[j + 1] if j < n - 1 else 0j) for j in range(n)]


def diffraction_step(p, b):
    """One Crank-Nicolson step (I - i (b / 2) T) p_new = (I + i (b / 2) T) p.

    b is a list of the values b_j = v'_j dz / (2 omega dx^2), one per point.
    """
    n = len(p)
    tp = apply_t(p)
    rhs = [p[j] + 0.5j * b[j] * tp[j] for j in range(n)]
    off = [-0.5j * b[j] for j in range(n)]
    diag = [1.0 + 1j * b[j] for j in range(n)]
    return thomas_solve(off, diag, off, rhs)


def finite_difference_migration(data, dt, dx, dz, vel):
    """Migrate a zero-offset section with the 15 degree finite-difference method.

    data: nt x nx real samples; vel: nz x nx velocities. Returns the nz x nx
    image. Precondition: dt, dx, dz > 0 and every velocity > 0.
    """
    nt, nx = len(data), len(data[0])
    nz = len(vel)
    spectra = [dft([data[k][j] for k in range(nt)]) for j in range(nx)]  # @line L1
    image = [[0.0] * nx for _ in range(nz)]
    for k in range(1, (nt + 1) // 2):  # @line L2
        omega = 2.0 * math.pi * k / (nt * dt)
        p = [spectra[j][k] for j in range(nx)]
        for i in range(nz):  # @line L3
            for j in range(nx):
                image[i][j] += 2.0 * p[j].real / nt  # @line L4
            vhalf = [v / 2.0 for v in vel[i]]
            p = [p[j] * cmath.exp(1j * omega * dz / vhalf[j]) for j in range(nx)]  # @line L5
            b = [vh * dz / (2.0 * omega * dx * dx) for vh in vhalf]  # @line L6
            p = diffraction_step(p, b)  # @line L7
    return image  # @line L8


def kz_15_degree(omega, kx, vhalf):
    """The vertical wavenumber of the continuous 15 degree equation."""
    return omega / vhalf - vhalf * kx * kx / (2.0 * omega)


def kz_crank_nicolson(omega, kx, vhalf, dx, dz):
    """The phase per unit depth of one discrete step (thin lens plus Crank-Nicolson) for exp(i kx x).

    The eigenvalue of T for this wave is lam = -4 sin^2(kx dx / 2), and the
    Crank-Nicolson factor is exp(2 i atan(b lam / 2)).
    """
    b = vhalf * dz / (2.0 * omega * dx * dx)
    lam = -4.0 * math.sin(kx * dx / 2.0) ** 2
    return omega / vhalf + 2.0 * math.atan(b * lam / 2.0) / dz
