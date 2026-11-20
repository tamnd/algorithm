# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kirchhoff-migration/. The authors are listed in prov/ZFVWK9.jsonl.
"""Kirchhoff (diffraction summation) migration of a 2D zero-offset section.

Conventions (the imaging and inverse problems pages):
- data[k][j] is the zero-offset sample at the two-way time t = k * dt and the
  surface position x_j = j * dx. image[i][j] is the image at depth z_i = i * dz
  and position x_j. The velocity vel is constant (m/s).
- U(omega) = sum u(t) exp(-i omega t). With this sign the time derivative has
  the symbol i omega. The filter of the 2D formula is the half derivative with
  the symbol (-i omega)^(1/2) = |omega|^(1/2) exp(-i pi sgn(omega) / 4)
  (principal branch), which keeps real traces real. With the opposite
  transform sign it reads (i omega)^(1/2).
- Exploding reflector model: v' = vel / 2 and the traveltime from the image
  point (x, z) to the trace at x_r is t = r / v' = 2 r / vel, with
  r = sqrt(z^2 + (x - x_r)^2).

The 2D zero-offset formula (Schneider 1978, Yilmaz 2001 chapter 4) is
    I(x, z) = dx * sum_r cos(theta) / sqrt(2 pi v' r) * h(x_r, 2 r / vel),
with cos(theta) = z / r and h the half derivative of the trace. It is a high
frequency (stationary phase) approximation of the exact downward continuation.

Cost: O(nt log nt) per trace for the half derivative (radix-2 FFT when nt is a
power of 2), then O(nz * nx * n_traces) for the sums.
"""

import math

from imgkit import dft, idft


def half_derivative(trace, dt):
    """The half-derivative filter of a trace: multiply its DFT by (-i omega)^(1/2)."""
    n = len(trace)
    spec = dft(trace)
    out = []
    for k in range(n):
        f = k if 2 * k < n else k - n
        omega = 2.0 * math.pi * f / (n * dt)
        out.append(spec[k] * (-1j * omega) ** 0.5 if omega != 0.0 else 0j)
    return [v.real for v in idft(out)]


def sample(trace, t, dt):
    """Linear interpolation of a trace at time t; zero outside the record."""
    u = t / dt
    k = math.floor(u)
    if k < 0 or k + 1 >= len(trace):
        return 0.0
    frac = u - k
    return (1.0 - frac) * trace[k] + frac * trace[k + 1]


def kirchhoff_weight(x, z, xr, vel):
    """cos(theta) / sqrt(2 pi v' r) and the traveltime 2 r / vel, for z > 0."""
    r = math.hypot(z, x - xr)
    vhalf = vel / 2.0
    return (z / r) / math.sqrt(2.0 * math.pi * vhalf * r), r / vhalf


def kirchhoff_migration(data, dt, dx, dz, nz, vel):
    """Migrate a zero-offset section in constant velocity by diffraction summation.

    data: nt x nx real samples. Returns the nz x nx image; row 0 (z = 0) is
    left zero, since the formula needs z > 0. Precondition: dt, dx, dz, vel > 0.
    """
    nt, nx = len(data), len(data[0])
    cols = [half_derivative([data[k][j] for k in range(nt)], dt) for j in range(nx)]  # @line L1
    filtered = [[cols[j][k] for j in range(nx)] for k in range(nt)]
    return diffraction_stack(filtered, dt, dx, dz, nz, vel)


def diffraction_stack(data, dt, dx, dz, nz, vel):
    """Lines L2 to L7: the weighted sum along the diffraction curve of each image point.

    It is a linear map from data to image; kirchhoff_modeling is its exact adjoint.
    """
    nt, nx = len(data), len(data[0])
    cols = [[data[k][j] for k in range(nt)] for j in range(nx)]
    image = [[0.0] * nx for _ in range(nz)]
    for i in range(1, nz):  # @line L2
        z = i * dz
        for j in range(nx):
            x = j * dx
            s = 0.0  # @line L3
            for r in range(nx):  # @line L4
                w, t = kirchhoff_weight(x, z, r * dx, vel)  # @line L5
                s += w * sample(cols[r], t, dt)  # @line L6
            image[i][j] = dx * s  # @line L7
    return image  # @line L8


def kirchhoff_modeling(image, dt, nt, dx, dz, vel):
    """The exact adjoint of kirchhoff_migration without its half derivative.

    It spreads each image value w * I(x, z) * dx onto the trace at x_r along the
    diffraction curve t = 2 r / vel, with the transpose of the linear
    interpolation. Returns nt x nx data (before any half-derivative filter).
    """
    nz, nx = len(image), len(image[0])
    out = [[0.0] * nx for _ in range(nt)]
    for i in range(1, nz):
        z = i * dz
        for j in range(nx):
            val = image[i][j]
            if val == 0.0:
                continue
            for r in range(nx):
                w, t = kirchhoff_weight(j * dx, z, r * dx, vel)
                u = t / dt
                k = math.floor(u)
                if k < 0 or k + 1 >= nt:
                    continue
                frac = u - k
                out[k][r] += dx * w * (1.0 - frac) * val
                out[k + 1][r] += dx * w * frac * val
    return out
